"""
Модели данных системы A/B-тестирования.

Методы сопоставления вариантов и оценки достоверности результатов
относятся к коммерческой тайне и не входят в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from agents.metrics_analyst.models import MetricField
from agents.strategist.models import ContentFormat


class ExperimentStatus(str, Enum):
    """Состояние эксперимента."""

    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ExperimentVariant(BaseModel):
    """Вариант контента, участвующий в эксперименте."""

    variant_id: str
    description: str


class Experiment(BaseModel):
    """Эксперимент: сопоставление вариантов контента по показателю, согласованному с компанией."""

    experiment_id: str
    character_id: str
    hypothesis: str
    applies_to_format: ContentFormat
    target_metric: MetricField
    variants: list[ExperimentVariant] = Field(min_length=2)
    status: ExperimentStatus = ExperimentStatus.PLANNED
    created_at: datetime


class VariantResult(BaseModel):
    """Сводные результаты варианта по целевому показателю эксперимента."""

    variant_id: str
    concept_ids: list[str] = Field(default_factory=list)
    publications: int = Field(ge=0)
    metric_total: int = Field(ge=0)


class ExperimentResult(BaseModel):
    """Результат сопоставления вариантов эксперимента."""

    experiment_id: str
    evaluated_at: datetime
    variant_results: list[VariantResult] = Field(default_factory=list)
    conclusive: bool
    winning_variant_id: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
