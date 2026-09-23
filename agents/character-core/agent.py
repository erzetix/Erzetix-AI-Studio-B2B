"""
Конфигурация агента "Ядро персонажа" (Character Core).

Системный промпт и логика валидации идентичности являются коммерческой
тайной и не публикуются в открытом репозитории. Ниже приведён контракт
агента: конфигурация, точки входа и точки расширения.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import Brief, CampaignContext


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
    Принимает бриф, обогащает его данными идентичности персонажа
    и возвращает контекст кампании, который оркестратор передаёт
    последующим подсистемам.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: CharacterCoreConfig | None = None) -> None:
        self.config = config or CharacterCoreConfig()

    def handle_brief(self, brief: Brief) -> CampaignContext:
        """Принимает бриф и возвращает обогащённый контекст кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def update_from_metrics(self, character_id: str, metrics: dict) -> None:
        """Обновляет поведенческое состояние персонажа по результатам кампаний."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
