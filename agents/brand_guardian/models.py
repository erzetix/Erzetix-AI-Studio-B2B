"""
Модели данных агента-хранителя бренда (Brand Guardian).

Правила допустимого контента, требования брендов клиентов и эталонные
параметры визуальной идентичности персонажа относятся к коммерческой
тайне и не входят в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator


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


class NoteAuthor(str, Enum):
    """Сторона, сформировавшая замечание к доработке."""

    BRAND_GUARDIAN = "brand_guardian"
    SPECIALIST = "specialist"


class RevisionNote(BaseModel):
    """Замечание, направляемое подсистеме-исполнителю на доработку.

    Формируется агентом-хранителем бренда по результатам проверки либо
    специалистом при возврате материала на доработку. Категория проверки
    указывается для замечаний агента-хранителя бренда.
    """

    note_id: str
    draft_id: str
    target_agent: TargetAgent
    author: NoteAuthor = NoteAuthor.BRAND_GUARDIAN
    category: CheckCategory | None = None
    scene_index: int | None = None
    issue: str
    required_action: str

    @model_validator(mode="after")
    def _guardian_note_has_category(self) -> RevisionNote:
        if self.author == NoteAuthor.BRAND_GUARDIAN and self.category is None:
            raise ValueError("Для замечания агента-хранителя бренда требуется category")
        return self


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
