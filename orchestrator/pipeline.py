"""
Схема производственного конвейера и правила переходов между состояниями
кампании и материалов.

Реализация маршрутизации, обращения к внешним генеративным сервисам
и ведения журнала выполнения находится в закрытой ветке разработки
и не входит в состав публичного репозитория.
"""

from __future__ import annotations

from dataclasses import dataclass

from agents.brand_guardian.models import MaterialVerdict, RevisionNote, TargetAgent, Verdict
from agents.character_core.models import Brief
from agents.visualizer.models import GenerationTask, MediaAsset

from .models import CampaignRun, CampaignState, MaterialRun, MaterialState


@dataclass(frozen=True)
class PipelineStage:
    """Этап производственного конвейера."""

    state: CampaignState | MaterialState
    subsystem: str


# Этапы уровня кампании: выполняются один раз для всей кампании.
CAMPAIGN_STAGES: tuple[PipelineStage, ...] = (
    PipelineStage(CampaignState.ENRICHING, "character-core"),
    PipelineStage(CampaignState.ANALYZING, "trend-analyst"),
    PipelineStage(CampaignState.PLANNING, "strategist"),
)

# Этапы уровня материала: выполняются для каждого материала отдельно.
MATERIAL_STAGES: tuple[PipelineStage, ...] = (
    PipelineStage(MaterialState.DRAFTING, "creator"),
    PipelineStage(MaterialState.GENERATING, "visualizer"),
    PipelineStage(MaterialState.REVIEWING, "brand-guardian"),
)

# Допустимые переходы между состояниями кампании. Переход, отсутствующий
# в таблице, считается недопустимым и не выполняется.
CAMPAIGN_TRANSITIONS: dict[CampaignState, tuple[CampaignState, ...]] = {
    CampaignState.RECEIVED: (CampaignState.ENRICHING, CampaignState.FAILED),
    CampaignState.ENRICHING: (CampaignState.ANALYZING, CampaignState.FAILED),
    CampaignState.ANALYZING: (CampaignState.PLANNING, CampaignState.FAILED),
    CampaignState.PLANNING: (CampaignState.PRODUCING, CampaignState.FAILED),
    CampaignState.PRODUCING: (CampaignState.COMPLETED, CampaignState.FAILED),
    CampaignState.COMPLETED: (),
    CampaignState.FAILED: (),
}

# Допустимые переходы между состояниями материала.
MATERIAL_TRANSITIONS: dict[MaterialState, tuple[MaterialState, ...]] = {
    MaterialState.DRAFTING: (
        MaterialState.GENERATING,
        MaterialState.BLOCKED,  # концепт невозможно раскрыть без нарушения брифа
        MaterialState.FAILED,
    ),
    MaterialState.GENERATING: (MaterialState.REVIEWING, MaterialState.FAILED),
    MaterialState.REVIEWING: (
        MaterialState.DRAFTING,  # доработка текстовой составляющей
        MaterialState.GENERATING,  # доработка визуальной составляющей
        MaterialState.AWAITING_APPROVAL,
        MaterialState.ESCALATED,
        MaterialState.REJECTED,
        MaterialState.FAILED,
    ),
    MaterialState.AWAITING_APPROVAL: (
        MaterialState.APPROVED,
        MaterialState.AWAITING_CLIENT_SIGNOFF,
        MaterialState.DRAFTING,  # возвращено специалистом: текст
        MaterialState.GENERATING,  # возвращено специалистом: визуальный ряд
    ),
    MaterialState.ESCALATED: (MaterialState.AWAITING_APPROVAL,),
    MaterialState.AWAITING_CLIENT_SIGNOFF: (
        MaterialState.APPROVED,
        MaterialState.DRAFTING,  # отклонено компанией: текст
        MaterialState.GENERATING,  # отклонено компанией: визуальный ряд
    ),
    MaterialState.APPROVED: (MaterialState.PUBLISHING,),
    MaterialState.PUBLISHING: (MaterialState.PUBLISHED, MaterialState.FAILED),
    MaterialState.PUBLISHED: (),
    MaterialState.BLOCKED: (),
    MaterialState.REJECTED: (),
    MaterialState.FAILED: (),
}

# Состояния, в которых обработка материала завершена.
TERMINAL_MATERIAL_STATES: frozenset[MaterialState] = frozenset(
    state for state, targets in MATERIAL_TRANSITIONS.items() if not targets
)


@dataclass
class OrchestratorConfig:
    """Конфигурация оркестратора."""

    name: str = "orchestrator"
    campaign_stages: tuple[PipelineStage, ...] = CAMPAIGN_STAGES
    material_stages: tuple[PipelineStage, ...] = MATERIAL_STAGES
    provider_credentials_ref: str = "vault://provider-credentials"

    # Число повторных вызовов подсистемы при недоступности и параметры
    # экспоненциальной задержки определяются по результатам эксплуатации
    # на Этапе 2.
    max_subsystem_retries: int | None = None
    retry_backoff_base_sec: float | None = None

    # Предельное число циклов автоматической доработки одного материала.
    # Начальное значение, подлежит уточнению по результатам эксплуатации
    # на Этапе 2.
    max_revision_cycles: int = 3


def can_transition_campaign(current: CampaignState, target: CampaignState) -> bool:
    """Проверяет допустимость перехода между состояниями кампании."""
    return target in CAMPAIGN_TRANSITIONS.get(current, ())


def can_transition_material(current: MaterialState, target: MaterialState) -> bool:
    """Проверяет допустимость перехода между состояниями материала."""
    return target in MATERIAL_TRANSITIONS.get(current, ())


def is_campaign_completed(run: CampaignRun) -> bool:
    """Кампания завершена, когда обработка всех её материалов завершена."""
    return bool(run.materials) and all(
        m.state in TERMINAL_MATERIAL_STATES for m in run.materials
    )


def revision_target(notes: list[RevisionNote]) -> MaterialState:
    """Состояние, в которое материал возвращается на доработку.

    При наличии замечаний к текстовой составляющей материал возвращается
    агенту-креатору: изменение текста влечёт повторную генерацию визуального
    ряда. В остальных случаях материал возвращается агенту-визуализатору.
    """
    if any(n.target_agent == TargetAgent.CREATOR for n in notes):
        return MaterialState.DRAFTING
    return MaterialState.GENERATING


def state_after_review(
    material: MaterialRun,
    verdict: MaterialVerdict,
    max_revision_cycles: int,
) -> MaterialState:
    """Определяет состояние материала по заключению агента-хранителя бренда.

    Материал, получивший заключение approved, передаётся на утверждение
    специалисту команды. Передача материала в публикацию без утверждения
    человеком не предусмотрена.
    """
    if verdict.verdict == Verdict.REJECTED:
        return MaterialState.REJECTED
    if verdict.verdict == Verdict.ESCALATED:
        return MaterialState.ESCALATED
    if verdict.verdict == Verdict.REVISION_REQUIRED:
        if material.revision_cycles >= max_revision_cycles:
            return MaterialState.ESCALATED
        return revision_target(verdict.revision_notes)

    return MaterialState.AWAITING_APPROVAL


class PipelineOrchestrator:
    """
    Управляет последовательностью вызовов подсистем и внешних
    генеративных сервисов, ведёт учёт состояния кампании и материалов
    и журнал выполнения этапов.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: OrchestratorConfig | None = None) -> None:
        self.config = config or OrchestratorConfig()

    def start(self, brief: Brief, client_id: str) -> CampaignRun:
        """Принимает бриф и инициирует обработку кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def advance(self, run: CampaignRun) -> CampaignRun:
        """Выполняет очередные этапы кампании и её материалов."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def dispatch_generation(self, tasks: list[GenerationTask]) -> list[MediaAsset]:
        """Направляет задания на генерацию внешним сервисам с учётом резервных провайдеров."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
