"""
Модели данных ядра персонажа (Character Core).

Реализация параметров идентичности персонажа (Character DNA, Facial DNA,
Body DNA, Style DNA, Prompt DNA) вынесена в защищённое хранилище и не
входит в состав данного модуля в соответствии с требованиями защиты
коммерческой тайны (см. Положение о коммерческой тайне).
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class CharacterOwnership(str, Enum):
    """Принадлежность прав на персонажа."""

    STUDIO = "studio"
    CLIENT = "client"
    SHARED = "shared"


class CharacterStatus(str, Enum):
    """Состояние профиля персонажа."""

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class EngagementTrend(str, Enum):
    """Динамика вовлечённости аудитории персонажа."""

    GROWING = "growing"
    STABLE = "stable"
    DECLINING = "declining"


class BehavioralState(BaseModel):
    """Текущее поведенческое состояние персонажа, обновляемое по метрикам кампаний."""

    tone: str
    recent_topics: list[str] = Field(default_factory=list)
    engagement_trend: EngagementTrend


class CharacterProfile(BaseModel):
    """Единый источник данных об идентичности персонажа (single source of truth)."""

    character_id: str
    # Компания, под бренд которой создан персонаж.
    client_id: str
    # Принадлежность прав на персонажа определяется договором с компанией.
    # Условия договора относятся к защищаемым сведениям и передаются ссылкой.
    ownership: CharacterOwnership
    rights_agreement_ref: str | None = None
    display_name: str
    # Ссылки на защищённое хранилище, а не сами параметры идентичности.
    identity_ref: str
    voice_profile_ref: str
    behavioral_state: BehavioralState
    status: CharacterStatus = CharacterStatus.DRAFT
    profile_version: str
    updated_at: datetime


class CharacterRegistration(BaseModel):
    """Данные для регистрации нового персонажа компании.

    Параметры идентичности и голосовой профиль размещаются в защищённом
    хранилище до регистрации; в запросе передаются ссылки на них.
    """

    character_id: str
    client_id: str
    ownership: CharacterOwnership
    rights_agreement_ref: str | None = None
    display_name: str
    identity_ref: str
    voice_profile_ref: str
    initial_behavioral_state: BehavioralState
    requested_by: str


class IdentityValidationResult(BaseModel):
    """Результат проверки консистентности параметров идентичности персонажа."""

    character_id: str
    profile_version: str
    passed: bool
    issues: list[str] = Field(default_factory=list)
    validated_at: datetime


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
