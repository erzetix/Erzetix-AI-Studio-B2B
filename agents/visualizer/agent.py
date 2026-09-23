"""
Конфигурация агента "Визуализатор" (Visualizer).

Системный промпт, шаблоны технических промптов и правила обеспечения
визуальной консистентности персонажа являются коммерческой тайной
и не публикуются в открытом репозитории. Ниже приведён контракт агента:
конфигурация, точки входа и точки расширения.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import AssetBundle, AssetType, GenerationTask, Provider


@dataclass
class VisualizerConfig:
    """Конфигурация агента для оркестратора."""

    name: str = "visualizer"
    model: str = "claude-sonnet-5"
    tools: list[str] = field(
        default_factory=lambda: [
            "identity_store",  # доступ к параметрам визуальной идентичности
            "prompt_composer",  # формирование технических промптов
            "consistency_scorer",  # оценка соответствия эталонной внешности
        ]
    )
    system_prompt_ref: str = "confidential://prompts/visualizer"
    identity_ref: str = "vault://character-dna"

    provider_routing: dict[AssetType, Provider] = field(
        default_factory=lambda: {
            AssetType.IMAGE: Provider.HIGGSFIELD_SOUL_2,
            AssetType.VIDEO: Provider.KLING_3,
            AssetType.SPEECH: Provider.ELEVENLABS,
        }
    )
    fallback_routing: dict[AssetType, Provider] = field(
        default_factory=lambda: {
            AssetType.IMAGE: Provider.NANO_BANANA_PRO,
            AssetType.VIDEO: Provider.SEEDANCE_2,
            AssetType.SPEECH: Provider.YANDEX_SPEECHKIT,
        }
    )

    # Пороговое значение оценки консистентности определяется по
    # результатам калибровки на реальных данных на Этапе 2.
    min_consistency_score: float | None = None

    # Предельное число попыток генерации. Начальное значение, подлежит
    # уточнению по фактической статистике генерации на Этапе 2.
    max_generation_attempts: int = 5


class VisualizerAgent:
    """
    Формирует технические промпты для генеративных сервисов, выбирает
    провайдера под задачу и обеспечивает визуальную консистентность
    персонажа между материалами.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: VisualizerConfig | None = None) -> None:
        self.config = config or VisualizerConfig()

    def compose_tasks(
        self,
        context: "CampaignContext",  # noqa: F821
        draft_bundle: "DraftBundle",  # noqa: F821
    ) -> list[GenerationTask]:
        """Формирует задания на генерацию по материалам агента-креатора."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def generate(
        self,
        context: "CampaignContext",  # noqa: F821
        draft_bundle: "DraftBundle",  # noqa: F821
    ) -> AssetBundle:
        """Выполняет генерацию медиаматериалов через API-оркестратор."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def revise(
        self,
        bundle: AssetBundle,
        notes: list["RevisionNote"],  # noqa: F821
    ) -> AssetBundle:
        """Выполняет повторную генерацию по замечаниям агента-хранителя бренда."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
