"""
Конфигурация агента "Хранитель бренда" (Brand Guardian).

Системный промпт, правила допустимого контента и требования брендов
клиентов являются коммерческой тайной и не публикуются в открытом
репозитории. Ниже приведён контракт агента: конфигурация, точки входа
и точки расширения.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import CheckCategory, ReviewReport


@dataclass
class BrandGuardianConfig:
    """Конфигурация агента для оркестратора."""

    name: str = "brand-guardian"
    model: str = "claude-sonnet-5"
    escalation_model: str = "claude-opus-4-8"
    tools: list[str] = field(
        default_factory=lambda: [
            "identity_store",  # доступ к эталонным параметрам идентичности
            "brand_rules_store",  # доступ к требованиям брендов клиентов
            "content_policy_checker",  # проверка по правилам допустимого контента
            "consistency_scorer",  # оценка соответствия эталонной внешности
        ]
    )
    system_prompt_ref: str = "confidential://prompts/brand-guardian"
    brand_rules_ref: str = "vault://brand-rules"
    identity_ref: str = "vault://character-dna"

    enabled_checks: list[CheckCategory] = field(
        default_factory=lambda: [
            CheckCategory.VISUAL_CONSISTENCY,
            CheckCategory.BRAND_COMPLIANCE,
            CheckCategory.CONTENT_POLICY,
            CheckCategory.BRIEF_CONSTRAINTS,
            CheckCategory.REPUTATIONAL_RISK,
        ]
    )

    # Условия эскалации на модель более высокого уровня возможностей
    # определяются по результатам эксплуатации на Этапе 2.
    escalation_rules_ref: str = "confidential://escalation-rules/brand-guardian"


class BrandGuardianAgent:
    """
    Выполняет автоматическую проверку материалов на соответствие
    визуальной консистентности персонажа, требованиям бренда клиента
    и внутренним правилам допустимого контента.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: BrandGuardianConfig | None = None) -> None:
        self.config = config or BrandGuardianConfig()

    def review(
        self,
        context: "CampaignContext",  # noqa: F821
        draft_bundle: "DraftBundle",  # noqa: F821
        asset_bundle: "AssetBundle",  # noqa: F821
    ) -> ReviewReport:
        """Выполняет проверку материалов и формирует заключения."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def escalate_to_senior_model(
        self,
        draft_id: str,
        category: CheckCategory,
    ) -> "MaterialVerdict":  # noqa: F821
        """Направляет материал на оценку модели более высокого уровня возможностей."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
