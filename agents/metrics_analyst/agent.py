"""
Конфигурация агента "Аналитик метрик" (Metrics Analyst).

Системный промпт и методы интерпретации показателей эффективности
являются коммерческой тайной и не публикуются в открытом репозитории.
Ниже приведён контракт агента: конфигурация, точки входа и точки
расширения.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from agents.character_core.models import CampaignContext
from agents.strategist.models import ContentPlan

from .models import MetricsAnalysis, PublicationMetrics


@dataclass
class MetricsAnalystConfig:
    """Конфигурация агента для оркестратора."""

    name: str = "metrics-analyst"
    model: str = "claude-haiku-4-5"
    tools: list[str] = field(
        default_factory=lambda: [
            "metrics_store",  # доступ к показателям эффективности публикаций
            "performance_aggregator",  # сведение показателей по концептам
        ]
    )
    system_prompt_ref: str = "confidential://prompts/metrics-analyst"


class MetricsAnalystAgent:
    """
    Обрабатывает показатели эффективности публикаций кампании, формирует
    сводные результаты по концептам, выводы для отчёта компании
    и предложение по обновлению поведенческого состояния персонажа.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: MetricsAnalystConfig | None = None) -> None:
        self.config = config or MetricsAnalystConfig()

    def analyze(
        self,
        context: CampaignContext,
        content_plan: ContentPlan,
        metrics: list[PublicationMetrics],
    ) -> MetricsAnalysis:
        """Формирует результат анализа показателей эффективности кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
