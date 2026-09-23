"""
Модели данных агента-креатора (Creator).

Голосовые характеристики персонажа, речевые шаблоны и системный промпт
агента относятся к коммерческой тайне и не входят в состав данного модуля.

Структура замечания к доработке (`RevisionNote`) определена в модуле
агента-хранителя бренда, формирующего замечания, и импортируется
подсистемой при обработке доработок.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class DraftStatus(str, Enum):
    """Статус обработки концепта."""

    READY = "ready"
    BLOCKED = "blocked"
    REVISION_REQUIRED = "revision_required"


class Scene(BaseModel):
    """Отдельная сцена сценария."""

    scene_index: int = Field(ge=1)
    duration_sec: float = Field(gt=0)
    spoken_line: str | None = None
    visual_description: str
    on_screen_text: str | None = None


class Draft(BaseModel):
    """Текстовые материалы, сформированные по одному концепту."""

    draft_id: str
    concept_id: str
    format: str
    status: DraftStatus = DraftStatus.READY
    scenes: list[Scene] = Field(default_factory=list)
    caption: str | None = None
    hashtags: list[str] = Field(default_factory=list)
    blocked_by_constraint: str | None = None


class DraftBundle(BaseModel):
    """Набор материалов кампании, передаваемый агенту-визуализатору."""

    campaign_id: str
    character_id: str
    created_at: datetime
    revision: int = Field(ge=1, default=1)
    drafts: list[Draft] = Field(default_factory=list)
