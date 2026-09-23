"""
Модели данных ядра персонажа (Character Core).

Реализация параметров идентичности персонажа (Character DNA, Facial DNA,
Body DNA, Style DNA, Prompt DNA) вынесена в защищённое хранилище и не
входит в состав данного модуля в соответствии с требованиями защиты
коммерческой тайны (см. Положение о коммерческой тайне).
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class BehavioralState(BaseModel):
    """Текущее поведенческое состояние персонажа, обновляемое по метрикам кампаний."""

    tone: str
    recent_topics: list[str] = Field(default_factory=list)
    engagement_trend: str


class CharacterProfile(BaseModel):
    """Единый источник данных об идентичности персонажа (single source of truth)."""

    character_id: str
    # Компания, под бренд которой создан персонаж.
    client_id: str
    display_name: str
    # Ссылки на защищённое хранилище, а не сами параметры идентичности.
    identity_ref: str
    voice_profile_ref: str
    behavioral_state: BehavioralState
    profile_version: str
    updated_at: datetime


class Brief(BaseModel):
    """Входной бриф, формируемый командой в рабочем месте команды."""

    campaign_id: str
    character_id: str
    goal: str
    constraints: list[str] = Field(default_factory=list)
    deadline: datetime | None = None
    requested_by: str


class CampaignContext(BaseModel):
    """Контекст кампании, передаваемый оркестратором каждой последующей подсистеме без изменений."""

    profile: CharacterProfile
    brief: Brief
