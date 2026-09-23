"""
Конфигурация агента "Аналитик трендов" (Trend Analyst).

Системный промпт и критерии оценки применимости трендов являются
коммерческой тайной и не публикуются в открытом репозитории. Ниже приведён
контракт агента: конфигурация, точки входа и точки расширения.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import TrendReport, TrendSignal, TrendSource


@dataclass
class TrendAnalystConfig:
    """Конфигурация агента для оркестратора."""

    name: str = "trend-analyst"
    model: str = "claude-haiku-4-5"
    tools: list[str] = field(
        default_factory=lambda: [
            "source_collector",  # сбор сигналов из подключённых источников
            "relevance_scorer",  # оценка применимости тренда к персонажу
        ]
    )
    system_prompt_ref: str = "confidential://prompts/trend-analyst"
    scoring_profile_ref: str = "vault://scoring-profiles/trend-analyst"

    enabled_sources: list[TrendSource] = field(
        default_factory=lambda: [
            TrendSource.TELEGRAM,
            TrendSource.VK,
            TrendSource.YOUTUBE,
            TrendSource.THEMATIC_CHANNEL,
        ]
    )

    # Пороговое значение оценки применимости тренда. Определяется по
    # результатам калибровки на реальных данных на Этапе 2.
    min_relevance_score: float | None = None


class TrendAnalystAgent:
    """
    Собирает сигналы о трендах из внешних источников, оценивает их
    применимость к персонажу и передаёт отфильтрованный отчёт
    агенту-стратегу.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: TrendAnalystConfig | None = None) -> None:
        self.config = config or TrendAnalystConfig()

    def collect_signals(self, character_id: str) -> list[TrendSignal]:
        """Собирает необработанные сигналы о трендах из подключённых источников."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def analyze(self, context: "CampaignContext") -> TrendReport:  # noqa: F821
        """Формирует отчёт по трендам на основании контекста кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
