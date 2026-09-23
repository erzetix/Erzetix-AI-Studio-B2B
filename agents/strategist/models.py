"""
Модели данных агента-стратега (Strategist).

Механики повышения виральности, весовые коэффициенты приоритизации
концептов и шаблоны сценариев персонажа относятся к коммерческой тайне
и не входят в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ContentFormat(str, Enum):
    """Формат единицы контента."""

    SHORT_VIDEO = "short_video"
    IMAGE_POST = "image_post"
    CAROUSEL = "carousel"
    TEXT_POST = "text_post"
    STORY = "story"


class TargetPlatform(str, Enum):
    """Целевая платформа размещения."""

    TELEGRAM = "telegram"
    VK = "vk"
    YOUTUBE = "youtube"


class ABRecommendation(BaseModel):
    """Рекомендация системы A/B-тестирования по результатам предшествующих кампаний."""

    recommendation_id: str
    applies_to_format: ContentFormat
    adjustment: str
    confidence: float = Field(ge=0.0, le=1.0)


class ContentConcept(BaseModel):
    """Единица контент-плана, передаваемая агенту-креатору."""

    concept_id: str
    title: str
    format: ContentFormat
    target_platform: TargetPlatform
    priority: int = Field(ge=1)
    source_trend_id: str | None = None
    key_message: str
    virality_mechanics: list[str] = Field(default_factory=list)


class ContentPlan(BaseModel):
    """Итоговый контент-план кампании."""

    campaign_id: str
    character_id: str
    created_at: datetime
    concepts: list[ContentConcept] = Field(default_factory=list)
    fallback_used: bool = False
