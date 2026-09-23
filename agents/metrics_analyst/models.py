"""
Модели данных агента-аналитика метрик (Metrics Analyst).

Методы интерпретации показателей эффективности и правила формирования
выводов относятся к коммерческой тайне и не входят в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from agents.character_core.models import BehavioralState
from agents.strategist.models import ABVariantRef, ContentFormat, TargetPlatform


class MetricField(str, Enum):
    """Показатель эффективности публикации."""

    VIEWS = "views"
    REACTIONS = "reactions"
    COMMENTS = "comments"
    SHARES = "shares"


class PublicationMetrics(BaseModel):
    """Показатели эффективности публикации, вводимые специалистом команды."""

    material_id: str
    campaign_id: str
    concept_id: str
    platform: TargetPlatform
    published_at: datetime
    views: int = Field(ge=0)
    reactions: int = Field(ge=0)
    comments: int = Field(ge=0)
    shares: int = Field(ge=0)
    reported_by: str


class ConceptResult(BaseModel):
    """Сводные показатели публикаций по концепту контент-плана."""

    concept_id: str
    format: ContentFormat
    platform: TargetPlatform
    material_ids: list[str] = Field(default_factory=list)
    views: int = Field(ge=0)
    reactions: int = Field(ge=0)
    comments: int = Field(ge=0)
    shares: int = Field(ge=0)
    ab_variant: ABVariantRef | None = None


class AnalysisFinding(BaseModel):
    """Вывод по результатам анализа с указанием подтверждающих концептов."""

    finding_id: str
    statement: str
    supporting_concept_ids: list[str] = Field(default_factory=list)


class MetricsAnalysis(BaseModel):
    """Результат анализа показателей эффективности публикаций кампании."""

    analysis_id: str
    campaign_id: str
    character_id: str
    analyzed_at: datetime
    concept_results: list[ConceptResult] = Field(default_factory=list)
    findings: list[AnalysisFinding] = Field(default_factory=list)
    # Предлагаемое поведенческое состояние персонажа. Обновление профиля
    # выполняется ядром персонажа.
    proposed_behavioral_state: BehavioralState | None = None
    # Показатели, исключённые из анализа: концепт отсутствует в контент-плане.
    excluded_material_ids: list[str] = Field(default_factory=list)
