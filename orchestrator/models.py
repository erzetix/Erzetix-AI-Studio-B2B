"""
Модели данных API-оркестратора контент-пайплайна.

Учётные данные доступа к внешним генеративным сервисам относятся
к защищаемым сведениям и не входят в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class CampaignState(str, Enum):
    """Состояние кампании в производственном конвейере."""

    RECEIVED = "received"
    ENRICHING = "enriching"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    DRAFTING = "drafting"
    GENERATING = "generating"
    REVIEWING = "reviewing"
    AWAITING_APPROVAL = "awaiting_approval"
    ESCALATED = "escalated"
    APPROVED = "approved"
    PUBLISHING = "publishing"
    FAILED = "failed"


class StageOutcome(str, Enum):
    """Результат выполнения этапа конвейера."""

    SUCCESS = "success"
    RETRY = "retry"
    FALLBACK_USED = "fallback_used"
    FAILURE = "failure"


class StageRecord(BaseModel):
    """Запись журнала выполнения этапа конвейера."""

    record_id: str
    campaign_id: str
    stage: CampaignState
    subsystem: str
    outcome: StageOutcome
    started_at: datetime
    finished_at: datetime | None = None
    attempt: int = Field(ge=1, default=1)
    provider_used: str | None = None
    fallback_provider_used: str | None = None
    error_code: str | None = None


class CampaignRun(BaseModel):
    """Текущее состояние обработки кампании."""

    campaign_id: str
    character_id: str
    state: CampaignState = CampaignState.RECEIVED
    revision_cycles: int = Field(ge=0, default=0)
    created_at: datetime
    updated_at: datetime
    journal: list[StageRecord] = Field(default_factory=list)
    failure_reason: str | None = None
