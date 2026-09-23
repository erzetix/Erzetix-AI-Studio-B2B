"""
Модели данных агента-аналитика трендов (Trend Analyst).

Критерии отбора и весовые коэффициенты ранжирования трендов настраиваются
под каждого персонажа, относятся к коммерческой тайне и не входят в состав
данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TrendSource(str, Enum):
    """Тип внешнего источника, из которого получен сигнал о тренде."""

    TELEGRAM = "telegram"
    VK = "vk"
    YOUTUBE = "youtube"
    THEMATIC_CHANNEL = "thematic_channel"


class RejectionReason(str, Enum):
    """Причина отклонения тренда при фильтрации."""

    OFF_TOPIC = "off_topic"
    TONE_MISMATCH = "tone_mismatch"
    CONSTRAINT_VIOLATION = "constraint_violation"
    REPUTATIONAL_RISK = "reputational_risk"
    EXPIRED = "expired"


class TrendSignal(BaseModel):
    """Необработанный сигнал о тренде, полученный из внешнего источника."""

    trend_id: str
    title: str
    source: TrendSource
    observed_at: datetime
    raw_context: str | None = None


class AcceptedTrend(BaseModel):
    """Тренд, прошедший фильтрацию и допущенный к построению контент-плана."""

    trend_id: str
    title: str
    source: TrendSource
    relevance_score: float = Field(ge=0.0, le=1.0)
    rationale: str


class RejectedTrend(BaseModel):
    """Тренд, отклонённый при фильтрации, с указанием причины."""

    trend_id: str
    title: str
    rejection_reason: RejectionReason


class TrendReport(BaseModel):
    """Итоговый отчёт, передаваемый агенту-стратегу."""

    campaign_id: str
    character_id: str
    collected_at: datetime
    accepted: list[AcceptedTrend] = Field(default_factory=list)
    rejected: list[RejectedTrend] = Field(default_factory=list)
    degraded_sources: list[TrendSource] = Field(default_factory=list)
