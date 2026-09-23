"""
Модели данных агента-хранителя бренда (Brand Guardian).

Правила допустимого контента, требования брендов клиентов и эталонные
параметры визуальной идентичности персонажа относятся к коммерческой
тайне и не входят в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class CheckCategory(str, Enum):
    """Категория выполняемой проверки."""

    VISUAL_CONSISTENCY = "visual_consistency"
    BRAND_COMPLIANCE = "brand_compliance"
    CONTENT_POLICY = "content_policy"
    BRIEF_CONSTRAINTS = "brief_constraints"
    REPUTATIONAL_RISK = "reputational_risk"


class Verdict(str, Enum):
    """Заключение по материалу."""

    APPROVED = "approved"
    REVISION_REQUIRED = "revision_required"
    REJECTED = "rejected"
    ESCALATED = "escalated"


class TargetAgent(str, Enum):
    """Подсистема, которой направляется замечание."""

    CREATOR = "creator"
    VISUALIZER = "visualizer"


class RevisionNote(BaseModel):
    """Замечание, направляемое подсистеме-исполнителю на доработку."""

    note_id: str
    draft_id: str
    target_agent: TargetAgent
    category: CheckCategory
    scene_index: int | None = None
    issue: str
    required_action: str


class MaterialVerdict(BaseModel):
    """Заключение по отдельному материалу."""

    draft_id: str
    verdict: Verdict
    checks_passed: list[CheckCategory] = Field(default_factory=list)
    failed_checks: list[CheckCategory] = Field(default_factory=list)
    skipped_checks: list[CheckCategory] = Field(default_factory=list)
    revision_notes: list[RevisionNote] = Field(default_factory=list)
    escalated_to_senior_model: bool = False


class ReviewReport(BaseModel):
    """Отчёт о проверке материалов кампании."""

    campaign_id: str
    character_id: str
    reviewed_at: datetime
    revision: int = Field(ge=1, default=1)
    verdicts: list[MaterialVerdict] = Field(default_factory=list)
    escalated_to_human: list[str] = Field(default_factory=list)
