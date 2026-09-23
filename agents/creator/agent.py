"""
Конфигурация агента "Креатор" (Creator).

Системный промпт, речевые шаблоны и правила воспроизведения стиля
персонажа являются коммерческой тайной и не публикуются в открытом
репозитории. Ниже приведён контракт агента: конфигурация, точки входа
и точки расширения.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from agents.brand_guardian.models import RevisionNote
from agents.character_core.models import CampaignContext
from agents.strategist.models import ContentPlan

from .models import DraftBundle


@dataclass
class CreatorConfig:
    """Конфигурация агента для оркестратора."""

    name: str = "creator"
    model: str = "claude-sonnet-5"
    tools: list[str] = field(
        default_factory=lambda: [
            "voice_profile_store",  # доступ к голосовому профилю персонажа
            "speech_length_estimator",  # оценка длительности реплики при синтезе речи
            "constraint_checker",  # проверка соответствия ограничениям брифа
        ]
    )
    system_prompt_ref: str = "confidential://prompts/creator"
    voice_profile_ref: str = "vault://voice-profile"

    # Число циклов доработки ограничивается API-оркестратором,
    # ведущим учёт состояния кампании. Подсистема собственного счётчика
    # циклов не ведёт.

    # Предельное число сцен определяется форматом и длительностью
    # материала, фиксированное значение не устанавливается.


class CreatorAgent:
    """
    Формирует тексты, сценарии и диалоги в голосе и стиле персонажа
    на основании контент-плана, а также выполняет доработку материалов
    по замечаниям агента-хранителя бренда.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: CreatorConfig | None = None) -> None:
        self.config = config or CreatorConfig()

    def create_drafts(
        self,
        context: CampaignContext,
        content_plan: ContentPlan,
    ) -> DraftBundle:
        """Формирует текстовые материалы по концептам контент-плана."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def revise(
        self,
        bundle: DraftBundle,
        notes: list[RevisionNote],
    ) -> DraftBundle:
        """Выполняет доработку материалов по замечаниям агента-хранителя бренда."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
