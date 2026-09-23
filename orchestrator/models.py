"""
Модели данных API-оркестратора контент-пайплайна.

Учётные данные доступа к внешним генеративным сервисам относятся
к защищаемым сведениям и не входят в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class CampaignState(str, Enum):
    """Состояние кампании в производственном конвейере."""

    RECEIVED = "received"
    ENRICHING = "enriching"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    PRODUCING = "producing"
    COMPLETED = "completed"
    FAILED = "failed"


class MaterialState(str, Enum):
    """Состояние отдельного материала кампании."""

    DRAFTING = "drafting"
    GENERATING = "generating"
    REVIEWING = "reviewing"
    AWAITING_APPROVAL = "awaiting_approval"
    ESCALATED = "escalated"
    APPROVED = "approved"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    FAILED = "failed"


class StageOutcome(str, Enum):
    """Результат выполнения этапа конвейера."""

    SUCCESS = "success"
    RETRY = "retry"
    FALLBACK_USED = "fallback_used"
    FAILURE = "failure"


class StageRecord(BaseModel):
    """Запись журнала выполнения этапа конвейера.

    Этап уровня кампании фиксируется в поле campaign_state, этап
    отдельного материала — в полях material_id и material_state.
    """

    record_id: str
    campaign_id: str
    campaign_state: CampaignState | None = None
    material_id: str | None = None
    material_state: MaterialState | None = None
    subsystem: str
    outcome: StageOutcome
    started_at: datetime
    finished_at: datetime | None = None
    attempt: int = Field(ge=1, default=1)
    provider_used: str | None = None
    fallback_provider_used: str | None = None
    error_code: str | None = None

    @model_validator(mode="after")
    def _stage_is_set(self) -> StageRecord:
        if self.campaign_state is None and self.material_state is None:
            raise ValueError("Не указан этап: campaign_state или material_state")
        if self.material_state is not None and self.material_id is None:
            raise ValueError("Для этапа материала требуется material_id")
        return self


class MaterialRun(BaseModel):
    """Состояние обработки отдельного материала кампании."""

    material_id: str
    campaign_id: str
    concept_id: str
    draft_id: str
    state: MaterialState = MaterialState.DRAFTING
    # Число выполненных циклов автоматической доработки по замечаниям
    # агента-хранителя бренда. Возвраты материала специалистом в счётчик
    # не входят.
    revision_cycles: int = Field(ge=0, default=0)
    # Ссылка на готовый медиафайл, собранный оркестратором из результатов
    # генерации.
    final_media_ref: str | None = None
    updated_at: datetime
    failure_reason: str | None = None


class CampaignRun(BaseModel):
    """Текущее состояние обработки кампании."""

    campaign_id: str
    character_id: str
    client_id: str
    state: CampaignState = CampaignState.RECEIVED
    materials: list[MaterialRun] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    journal: list[StageRecord] = Field(default_factory=list)
    failure_reason: str | None = None
