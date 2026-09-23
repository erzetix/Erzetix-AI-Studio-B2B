"""
Схема производственного конвейера и правила переходов между состояниями
кампании.

Реализация маршрутизации, обращения к внешним генеративным сервисам
и ведения журнала выполнения находится в закрытой ветке разработки
и не входит в состав публичного репозитория.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import CampaignRun, CampaignState


@dataclass(frozen=True)
class PipelineStage:
    """Этап производственного конвейера."""

    state: CampaignState
    subsystem: str
    next_state: CampaignState


# Последовательность этапов основного потока обработки.
PIPELINE_STAGES: tuple[PipelineStage, ...] = (
    PipelineStage(CampaignState.ENRICHING, "character-core", CampaignState.ANALYZING),
    PipelineStage(CampaignState.ANALYZING, "trend-analyst", CampaignState.PLANNING),
    PipelineStage(CampaignState.PLANNING, "strategist", CampaignState.DRAFTING),
    PipelineStage(CampaignState.DRAFTING, "creator", CampaignState.GENERATING),
    PipelineStage(CampaignState.GENERATING, "visualizer", CampaignState.REVIEWING),
    PipelineStage(CampaignState.REVIEWING, "brand-guardian", CampaignState.AWAITING_APPROVAL),
)

# Допустимые переходы между состояниями кампании. Переход, отсутствующий
# в таблице, считается недопустимым и не выполняется.
ALLOWED_TRANSITIONS: dict[CampaignState, tuple[CampaignState, ...]] = {
    CampaignState.RECEIVED: (CampaignState.ENRICHING, CampaignState.FAILED),
    CampaignState.ENRICHING: (CampaignState.ANALYZING, CampaignState.FAILED),
    CampaignState.ANALYZING: (CampaignState.PLANNING, CampaignState.FAILED),
    CampaignState.PLANNING: (CampaignState.DRAFTING, CampaignState.FAILED),
    CampaignState.DRAFTING: (CampaignState.GENERATING, CampaignState.FAILED),
    CampaignState.GENERATING: (CampaignState.REVIEWING, CampaignState.FAILED),
    CampaignState.REVIEWING: (
        CampaignState.DRAFTING,  # доработка текстовых материалов
        CampaignState.GENERATING,  # доработка визуальных материалов
        CampaignState.AWAITING_APPROVAL,
        CampaignState.ESCALATED,
        CampaignState.FAILED,
    ),
    CampaignState.AWAITING_APPROVAL: (
        CampaignState.APPROVED,
        CampaignState.DRAFTING,  # отклонено человеком
        CampaignState.FAILED,
    ),
    CampaignState.ESCALATED: (CampaignState.AWAITING_APPROVAL, CampaignState.FAILED),
    CampaignState.APPROVED: (CampaignState.PUBLISHING,),
    CampaignState.PUBLISHING: (),
    CampaignState.FAILED: (),
}


@dataclass
class OrchestratorConfig:
    """Конфигурация оркестратора."""

    name: str = "orchestrator"
    stages: tuple[PipelineStage, ...] = PIPELINE_STAGES
    provider_credentials_ref: str = "vault://provider-credentials"

    # Число повторных вызовов подсистемы при недоступности и параметры
    # экспоненциальной задержки определяются по результатам эксплуатации
    # на Этапе 2.
    max_subsystem_retries: int | None = None
    retry_backoff_base_sec: float | None = None

    # Предельное число циклов доработки. Начальное значение, подлежит
    # уточнению по результатам эксплуатации на Этапе 2.
    max_revision_cycles: int = 3


class PipelineOrchestrator:
    """
    Управляет последовательностью вызовов подсистем и внешних
    генеративных сервисов, ведёт учёт состояния кампании и журнал
    выполнения этапов.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: OrchestratorConfig | None = None) -> None:
        self.config = config or OrchestratorConfig()

    def start(self, brief: "Brief") -> CampaignRun:  # noqa: F821
        """Принимает бриф и инициирует обработку кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def advance(self, run: CampaignRun) -> CampaignRun:
        """Выполняет текущий этап конвейера и переводит кампанию в следующее состояние."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def dispatch_generation(self, tasks: list["GenerationTask"]) -> list["MediaAsset"]:  # noqa: F821
        """Направляет задания на генерацию внешним сервисам с учётом резервных провайдеров."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def can_transition(self, current: CampaignState, target: CampaignState) -> bool:
        """Проверяет допустимость перехода между состояниями кампании."""
        return target in ALLOWED_TRANSITIONS.get(current, ())
