"""
Конфигурация агента "Ядро персонажа" (Character Core).

Системный промпт и логика валидации идентичности являются коммерческой
тайной и не публикуются в открытом репозитории. Ниже приведён контракт
агента: конфигурация, точки входа и точки расширения.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from agents.metrics_analyst.models import MetricsAnalysis

from .models import (
    Brief,
    CampaignContext,
    CharacterProfile,
    CharacterRegistration,
    IdentityValidationResult,
)


@dataclass
class CharacterCoreConfig:
    """Конфигурация агента для оркестратора."""

    name: str = "character-core"
    model: str = "claude-sonnet-5"
    tools: list[str] = field(
        default_factory=lambda: [
            "character_profile_store",  # доступ к защищённому хранилищу профилей
            "identity_lock_validator",  # проверка консистентности идентичности
        ]
    )
    system_prompt_ref: str = "confidential://prompts/character-core"


class CharacterCoreAgent:
    """
    Ведёт профили персонажей: регистрация, проверка идентичности,
    активация, обновление поведенческого состояния. Принимает бриф,
    обогащает его данными идентичности персонажа и возвращает контекст
    кампании, который оркестратор передаёт последующим подсистемам.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: CharacterCoreConfig | None = None) -> None:
        self.config = config or CharacterCoreConfig()

    def register_profile(self, registration: CharacterRegistration) -> CharacterProfile:
        """Регистрирует персонажа компании; профиль создаётся в состоянии draft."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def validate_identity(self, character_id: str) -> IdentityValidationResult:
        """Проверяет консистентность параметров идентичности персонажа."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def activate_profile(self, character_id: str) -> CharacterProfile:
        """Переводит профиль в состояние active после успешной проверки идентичности."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def handle_brief(self, brief: Brief) -> CampaignContext:
        """Принимает бриф и возвращает обогащённый контекст кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def update_from_metrics(self, analysis: MetricsAnalysis) -> CharacterProfile:
        """Обновляет поведенческое состояние персонажа по результатам анализа метрик."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
