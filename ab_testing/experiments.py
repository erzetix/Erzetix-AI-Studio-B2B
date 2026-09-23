"""
Конфигурация и контракт операций системы A/B-тестирования.

Реализация сопоставления вариантов и оценки достоверности результатов
находится в закрытой ветке разработки и не входит в состав публичного
репозитория.
"""

from __future__ import annotations

from dataclasses import dataclass

from agents.metrics_analyst.models import MetricsAnalysis
from agents.strategist.models import ABRecommendation

from .models import Experiment, ExperimentResult


@dataclass
class ABTestingConfig:
    """Конфигурация системы A/B-тестирования."""

    name: str = "ab-testing"

    # Минимальное число публикаций каждого варианта и пороговое значение
    # достоверности результата определяются по результатам калибровки
    # на реальных данных на Этапе 2.
    min_publications_per_variant: int | None = None
    min_confidence: float | None = None


class ABTestingService:
    """
    Ведёт эксперименты, сопоставляет варианты контента по результатам
    анализа метрик и формирует рекомендации для агента-стратега.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: ABTestingConfig | None = None) -> None:
        self.config = config or ABTestingConfig()

    def register(self, experiment: Experiment) -> Experiment:
        """Формирует эксперимент в состоянии planned."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def active_experiments(self, character_id: str) -> list[Experiment]:
        """Возвращает эксперименты персонажа, варианты которых включаются в контент-план."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def evaluate(
        self,
        experiment: Experiment,
        analyses: list[MetricsAnalysis],
    ) -> ExperimentResult:
        """Сопоставляет варианты эксперимента по результатам анализа метрик."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def recommend(self, results: list[ExperimentResult]) -> list[ABRecommendation]:
        """Формирует рекомендации для агента-стратега по достоверным результатам."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
