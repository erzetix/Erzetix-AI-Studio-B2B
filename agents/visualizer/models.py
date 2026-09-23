"""
Модели данных агента-визуализатора (Visualizer).

Параметры визуальной идентичности персонажа (Facial DNA, Body DNA,
Style DNA, Prompt DNA), шаблоны технических промптов и правила
обеспечения консистентности относятся к коммерческой тайне
и не входят в состав данного модуля.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class AssetType(str, Enum):
    """Тип генерируемого материала."""

    IMAGE = "image"
    VIDEO = "video"
    SPEECH = "speech"


class Provider(str, Enum):
    """Внешний генеративный сервис."""

    HIGGSFIELD_SOUL_2 = "higgsfield_soul_2"
    NANO_BANANA_2 = "nano_banana_2"
    NANO_BANANA_PRO = "nano_banana_pro"
    SEEDREAM_5 = "seedream_5"
    KLING_3 = "kling_3"
    SEEDANCE_2 = "seedance_2"
    VEO_3_1 = "veo_3_1"
    ELEVENLABS = "elevenlabs"
    YANDEX_SPEECHKIT = "yandex_speechkit"


class GenerationFailureReason(str, Enum):
    """Причина отказа генерации материала."""

    ALL_PROVIDERS_UNAVAILABLE = "all_providers_unavailable"
    CONSISTENCY_THRESHOLD_NOT_MET = "consistency_threshold_not_met"
    PROVIDER_REJECTED_PROMPT = "provider_rejected_prompt"
    TIMEOUT = "timeout"


class GenerationTask(BaseModel):
    """Задание на генерацию, направляемое в API-оркестратор."""

    task_id: str
    draft_id: str
    scene_index: int | None = None
    asset_type: AssetType
    provider: Provider
    fallback_provider: Provider | None = None
    prompt_ref: str


class MediaAsset(BaseModel):
    """Сгенерированный медиаматериал."""

    asset_id: str
    draft_id: str
    scene_index: int | None = None
    asset_type: AssetType
    provider: Provider
    prompt_ref: str | None = None
    storage_ref: str
    consistency_score: float | None = Field(default=None, ge=0.0, le=1.0)
    duration_sec: float | None = Field(default=None, gt=0)
    generation_attempts: int = Field(ge=1, default=1)


class FailedAsset(BaseModel):
    """Материал, генерация которого не была выполнена."""

    draft_id: str
    scene_index: int | None = None
    asset_type: AssetType
    failure_reason: GenerationFailureReason
    attempts_made: int = Field(ge=1)


class AssetBundle(BaseModel):
    """Набор медиаматериалов кампании, передаваемый агенту-хранителю бренда."""

    campaign_id: str
    character_id: str
    created_at: datetime
    revision: int = Field(ge=1, default=1)
    assets: list[MediaAsset] = Field(default_factory=list)
    failed_assets: list[FailedAsset] = Field(default_factory=list)
