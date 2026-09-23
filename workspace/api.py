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
)


@dataclass
class WorkspaceConfig:
    """Конфигурация рабочего места команды."""

    name: str = "workspace"
    default_approval_mode: ApprovalMode = ApprovalMode.MANUAL


class WorkspaceAPI:
    """
    Перечень операций рабочего места команды.

    Все операции выполняются специалистом команды и доступны ему
    в отношении компаний, за которыми он закреплён. Операция
    в отношении компании, за которой специалист не закреплён,
    отклоняется с кодом FORBIDDEN.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: WorkspaceConfig | None = None) -> None:
        self.config = config or WorkspaceConfig()

    # --- Компании -------------------------------------------------------

    def list_clients(self, specialist_id: str) -> list[ClientAccount]:
        """GET /clients — получение списка компаний, за которыми закреплён специалист."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_client(self, client_id: str, specialist_id: str) -> ClientAccount:
        """GET /clients/{client_id} — получение параметров компании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Кампании -------------------------------------------------------

    def create_campaign(self, brief: "Brief", specialist_id: str) -> CampaignView:  # noqa: F821
        """POST /campaigns — создание кампании на основании брифа."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def list_campaigns(self, specialist_id: str, client_id: str | None = None) -> list[CampaignView]:
        """GET /campaigns — получение списка кампаний."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_campaign(self, campaign_id: str, specialist_id: str) -> CampaignView:
        """GET /campaigns/{campaign_id} — получение состояния кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Материалы ------------------------------------------------------

    def list_materials(self, campaign_id: str, specialist_id: str) -> list[MaterialView]:
        """GET /campaigns/{campaign_id}/materials — получение материалов кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def approve_material(self, material_id: str, specialist_id: str) -> ApprovalDecision:
        """POST /materials/{material_id}/approve — утверждение материала командой."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def reject_material(
        self,
        material_id: str,
        reason: str,
        specialist_id: str,
    ) -> ApprovalDecision:
        """POST /materials/{material_id}/reject — отклонение материала командой."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def request_client_signoff(self, material_id: str, specialist_id: str) -> MaterialView:
        """POST /materials/{material_id}/client-signoff — назначение согласования с компанией."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def record_client_decision(
        self,
        decision: ApprovalDecision,
        specialist_id: str,
    ) -> ApprovalDecision:
        """POST /materials/{material_id}/client-decision — фиксация решения компании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Показатели и отчётность ----------------------------------------

    def submit_metrics(self, metrics: PublicationMetrics, specialist_id: str) -> None:
        """POST /campaigns/{campaign_id}/metrics — ввод показателей публикации."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_metrics(self, campaign_id: str, specialist_id: str) -> list[PublicationMetrics]:
        """GET /campaigns/{campaign_id}/metrics — получение показателей кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def build_report(
        self,
        client_id: str,
        period_start: datetime,
        period_end: datetime,
        specialist_id: str,
    ) -> ClientReport:
        """POST /clients/{client_id}/reports — формирование периодического отчёта для компании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Профиль персонажа ----------------------------------------------

    def get_character_profile(self, character_id: str, specialist_id: str) -> dict:
        """GET /characters/{character_id} — получение профиля персонажа."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Разграничение доступа ------------------------------------------

    def has_access(self, specialist_id: str, client: ClientAccount) -> bool:
        """Проверяет закрепление специалиста за компанией."""
        return specialist_id in client.assigned_specialists
