"""
Конфигурация агента "Стратег" (Strategist).

Системный промпт, механики повышения виральности и правила приоритизации
концептов являются коммерческой тайной и не публикуются в открытом
репозитории. Ниже приведён контракт агента: конфигурация, точки входа
и точки расширения.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import ABRecommendation, ContentPlan


@dataclass
class StrategistConfig:
    """Конфигурация агента для оркестратора."""

    name: str = "strategist"
    model: str = "claude-sonnet-5"
    tools: list[str] = field(
        default_factory=lambda: [
            "scenario_template_store",  # доступ к шаблонам сценариев персонажа
            "virality_playbook",  # механики повышения виральности
            "concept_prioritizer",  # приоритизация концептов контент-плана
        ]
    )
    system_prompt_ref: str = "confidential://prompts/strategist"
    playbook_ref: str = "vault://playbooks/virality"
    scenario_templates_ref: str = "vault://scenario-templates"

    # Контент-план формируется на недельный производственный цикл.
    planning_period_days: int = 7

    # Целевой показатель проекта — не менее 70 концептов в неделю —
    # относится к производству комплекса в целом, а не к отдельному плану.
    # Предельное число концептов в плане определяется по результатам
    # эксплуатации на Этапе 2 на основании фактической пропускной
    # способности контура утверждения.
    max_concepts_per_plan: int | None = None


class StrategistAgent:
    """
    Формирует контент-план кампании на основании контекста персонажа,
    отчёта по трендам и рекомендаций системы A/B-тестирования.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: StrategistConfig | None = None) -> None:
        self.config = config or StrategistConfig()

    def build_plan(
        self,
        context: "CampaignContext",  # noqa: F821
        trend_report: "TrendReport",  # noqa: F821
        ab_recommendations: list[ABRecommendation] | None = None,
    ) -> ContentPlan:
        """Формирует контент-план на основании входных данных кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def build_fallback_plan(self, context: "CampaignContext") -> ContentPlan:  # noqa: F821
        """Формирует контент-план на базовых сценариях при отсутствии применимых трендов."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
