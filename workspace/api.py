"""
Точки входа рабочего места команды.

Реализация операций, подключение к оркестратору и проверка учётных
данных сотрудников находятся в закрытой ветке разработки и не входят
в состав публичного репозитория.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .models import (
    ApprovalDecision,
    ApprovalMode,
    CampaignView,
    ClientAccount,
    ClientReport,
    MaterialView,
    PublicationMetrics,
    UserRole,
)

# Операции, доступные каждой роли сотрудника. Операция, отсутствующая
# в перечне роли, отклоняется с кодом FORBIDDEN.
ROLE_PERMISSIONS: dict[UserRole, tuple[str, ...]] = {
    UserRole.ACCOUNT_MANAGER: (
        "list_clients",
        "get_client",
        "create_campaign",
        "list_campaigns",
        "get_campaign",
        "list_materials",
        "approve_material",
        "reject_material",
        "request_client_signoff",
        "record_client_decision",
        "get_metrics",
        "build_report",
        "get_character_profile",
    ),
    UserRole.CONTENT_SPECIALIST: (
        "list_clients",
        "get_client",
        "list_campaigns",
        "get_campaign",
        "list_materials",
        "approve_material",
        "reject_material",
        "submit_metrics",
        "get_metrics",
        "get_character_profile",
    ),
}


@dataclass
class WorkspaceConfig:
    """Конфигурация рабочего места команды."""

    name: str = "workspace"
    default_approval_mode: ApprovalMode = ApprovalMode.MANUAL


class WorkspaceAPI:
    """
    Перечень операций рабочего места команды.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: WorkspaceConfig | None = None) -> None:
        self.config = config or WorkspaceConfig()

    # --- Компании -------------------------------------------------------

    def list_clients(self, role: UserRole) -> list[ClientAccount]:
        """GET /clients — получение списка компаний, аккаунты которых ведёт команда."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_client(self, client_id: str, role: UserRole) -> ClientAccount:
        """GET /clients/{client_id} — получение параметров компании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Кампании -------------------------------------------------------

    def create_campaign(self, brief: "Brief", role: UserRole) -> CampaignView:  # noqa: F821
        """POST /campaigns — создание кампании на основании брифа."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def list_campaigns(self, role: UserRole, client_id: str | None = None) -> list[CampaignView]:
        """GET /campaigns — получение списка кампаний."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_campaign(self, campaign_id: str, role: UserRole) -> CampaignView:
        """GET /campaigns/{campaign_id} — получение состояния кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Материалы ------------------------------------------------------

    def list_materials(self, campaign_id: str, role: UserRole) -> list[MaterialView]:
        """GET /campaigns/{campaign_id}/materials — получение материалов кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def approve_material(self, material_id: str, role: UserRole) -> ApprovalDecision:
        """POST /materials/{material_id}/approve — утверждение материала командой."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def reject_material(
        self,
        material_id: str,
        reason: str,
        role: UserRole,
    ) -> ApprovalDecision:
        """POST /materials/{material_id}/reject — отклонение материала командой."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def request_client_signoff(self, material_id: str, role: UserRole) -> MaterialView:
        """POST /materials/{material_id}/client-signoff — назначение согласования с компанией."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def record_client_decision(
        self,
        decision: ApprovalDecision,
        role: UserRole,
    ) -> ApprovalDecision:
        """POST /materials/{material_id}/client-decision — фиксация решения компании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Показатели и отчётность ----------------------------------------

    def submit_metrics(self, metrics: PublicationMetrics, role: UserRole) -> None:
        """POST /campaigns/{campaign_id}/metrics — ввод показателей публикации."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_metrics(self, campaign_id: str, role: UserRole) -> list[PublicationMetrics]:
        """GET /campaigns/{campaign_id}/metrics — получение показателей кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def build_report(
        self,
        client_id: str,
        period_start: datetime,
        period_end: datetime,
        role: UserRole,
    ) -> ClientReport:
        """POST /clients/{client_id}/reports — формирование периодического отчёта для компании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Профиль персонажа ----------------------------------------------

    def get_character_profile(self, character_id: str, role: UserRole) -> dict:
        """GET /characters/{character_id} — получение профиля персонажа."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Разграничение доступа ------------------------------------------

    def is_permitted(self, role: UserRole, operation: str) -> bool:
        """Проверяет доступность операции для роли сотрудника."""
        return operation in ROLE_PERMISSIONS.get(role, ())
