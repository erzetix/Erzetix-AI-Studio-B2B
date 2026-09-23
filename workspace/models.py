"""
Модели данных рабочего места команды.

Учётные данные сотрудников, учётные данные доступа к аккаунтам компаний
и требования брендов компаний относятся к защищаемым сведениям и не входят
в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator

from agents.brand_guardian.models import CheckCategory, RevisionNote, Verdict
from agents.metrics_analyst.models import AnalysisFinding, PublicationMetrics
from agents.strategist.models import ContentFormat
from orchestrator.models import CampaignState, MaterialState


class DecisionSource(str, Enum):
    """Сторона, принявшая решение по материалу."""

    TEAM = "team"
    CLIENT = "client"


class ClientAccount(BaseModel):
    """Компания, аккаунт которой ведёт команда.

    Персонажи компании определяются по полю client_id профиля персонажа.
    """

    client_id: str
    display_name: str
    brand_rules_ref: str
    account_credentials_ref: str
    # Специалисты команды, закреплённые за компанией.
    assigned_specialists: list[str] = Field(min_length=1)
    # Периодичность отчёта для компании устанавливается договором
    # с компанией.
    report_period_days: int | None = Field(default=None, ge=1)


class MaterialView(BaseModel):
    """Представление материала в контуре утверждения."""

    material_id: str
    campaign_id: str
    concept_id: str
    draft_id: str
    format: ContentFormat
    state: MaterialState
    preview_ref: str
    caption: str | None = None
    guardian_verdict: Verdict | None = None
    failed_checks: list[CheckCategory] = Field(default_factory=list)
    client_signoff_required: bool = False
    created_at: datetime


class CampaignView(BaseModel):
    """Представление кампании в рабочем месте команды."""

    campaign_id: str
    client_id: str
    character_id: str
    title: str
    state: CampaignState
    materials_total: int = Field(ge=0, default=0)
    materials_awaiting_approval: int = Field(ge=0, default=0)
    created_at: datetime
    updated_at: datetime
    state_observed_at: datetime | None = None


class ApprovalDecision(BaseModel):
    """Решение об утверждении материала или возврате его на доработку.

    При возврате на доработку указываются замечания, адресованные
    агенту-креатору или агенту-визуализатору.
    """

    material_id: str
    approved: bool
    source: DecisionSource = DecisionSource.TEAM
    decided_by: str
    decided_at: datetime
    revision_notes: list[RevisionNote] = Field(default_factory=list)
    # Канал, по которому получено решение компании (созвон, переписка).
    client_channel: str | None = None

    @model_validator(mode="after")
    def _consistent(self) -> ApprovalDecision:
        if not self.approved and not self.revision_notes:
            raise ValueError("При возврате на доработку требуются revision_notes")
        if self.approved and self.revision_notes:
            raise ValueError("Утверждённый материал не содержит замечаний к доработке")
        if self.source == DecisionSource.CLIENT and not self.client_channel:
            raise ValueError("Для решения компании требуется client_channel")
        return self


class ClientReport(BaseModel):
    """Периодический отчёт о ведении аккаунта, направляемый компании."""

    report_id: str
    client_id: str
    period_start: datetime
    period_end: datetime
    campaign_ids: list[str] = Field(default_factory=list)
    materials_published: int = Field(ge=0, default=0)
    metrics: list[PublicationMetrics] = Field(default_factory=list)
    findings: list[AnalysisFinding] = Field(default_factory=list)
    prepared_by: str
    created_at: datetime

    @model_validator(mode="after")
    def _period_order(self) -> ClientReport:
        if self.period_end <= self.period_start:
            raise ValueError("period_end должен быть позже period_start")
        return self
