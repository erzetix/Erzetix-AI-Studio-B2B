"""
Модели данных рабочего места команды.

Учётные данные сотрудников, учётные данные доступа к аккаунтам компаний
и требования брендов компаний относятся к защищаемым сведениям и не входят
в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """Роль сотрудника команды."""

    ACCOUNT_MANAGER = "account_manager"
    CONTENT_SPECIALIST = "content_specialist"


class ApprovalMode(str, Enum):
    """Режим утверждения материалов."""

    MANUAL = "manual"
    HYBRID = "hybrid"
    AUTONOMOUS = "autonomous"


class MaterialState(str, Enum):
    """Состояние материала в контуре утверждения."""

    IN_PRODUCTION = "in_production"
    AWAITING_APPROVAL = "awaiting_approval"
    AWAITING_CLIENT_SIGNOFF = "awaiting_client_signoff"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"


class DecisionSource(str, Enum):
    """Сторона, принявшая решение по материалу."""

    TEAM = "team"
    CLIENT = "client"


class ClientAccount(BaseModel):
    """Компания, аккаунт которой ведёт команда."""

    client_id: str
    display_name: str
    character_ids: list[str] = Field(default_factory=list)
    approval_mode: ApprovalMode
    brand_rules_ref: str
    account_credentials_ref: str
    account_manager: str
    # Периодичность отчёта для компании устанавливается договором
    # с компанией.
    report_period_days: int | None = Field(default=None, ge=1)


class MaterialView(BaseModel):
    """Представление материала в контуре утверждения."""

    material_id: str
    campaign_id: str
    draft_id: str
    format: str
    state: MaterialState
    preview_ref: str
    caption: str | None = None
    guardian_verdict: str | None = None
    failed_checks: list[str] = Field(default_factory=list)
    client_signoff_required: bool = False
    created_at: datetime


class CampaignView(BaseModel):
    """Представление кампании в рабочем месте команды."""

    campaign_id: str
    client_id: str
    character_id: str
    title: str
    state: str
    approval_mode: ApprovalMode
    materials_total: int = Field(ge=0, default=0)
    materials_awaiting_approval: int = Field(ge=0, default=0)
    created_at: datetime
    updated_at: datetime
    state_observed_at: datetime | None = None


class ApprovalDecision(BaseModel):
    """Решение об утверждении или отклонении материала."""

    material_id: str
    approved: bool
    source: DecisionSource = DecisionSource.TEAM
    decided_by: str
    decided_at: datetime
    rejection_reason: str | None = None
    # Канал, по которому получено решение компании (созвон, переписка).
    # Заполняется при source = client.
    client_channel: str | None = None


class PublicationMetrics(BaseModel):
    """Показатели эффективности публикации, вводимые специалистом."""

    material_id: str
    platform: str
    published_at: datetime
    views: int = Field(ge=0)
    reactions: int = Field(ge=0)
    comments: int = Field(ge=0)
    shares: int = Field(ge=0)
    reported_by: str


class ClientReport(BaseModel):
    """Периодический отчёт о ведении аккаунта, направляемый компании."""

    report_id: str
    client_id: str
    period_start: datetime
    period_end: datetime
    campaign_ids: list[str] = Field(default_factory=list)
    materials_published: int = Field(ge=0, default=0)
    metrics: list[PublicationMetrics] = Field(default_factory=list)
    prepared_by: str
    created_at: datetime
