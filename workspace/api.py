"""
Точки входа рабочего места команды.

Реализация операций, подключение к оркестратору и проверка учётных
данных сотрудников находятся в закрытой ветке разработки и не входят
в состав публичного репозитория.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from agents.brand_guardian.models import RevisionNote
from agents.character_core.models import Brief, CharacterProfile
from agents.metrics_analyst.models import PublicationMetrics

from .models import (
    ApprovalDecision,
    CampaignView,
    ClientAccount,
    ClientReport,
    MaterialView,
)


@dataclass
class WorkspaceConfig:
    """Конфигурация рабочего места команды."""

    name: str = "workspace"


class WorkspaceAPI:
    """
    Перечень операций рабочего места команды.

    Операции выполняются специалистом команды. Распределение компаний
    и материалов между специалистами определяется отдельным
    организационным документом и в данном модуле не устанавливается.

    Реализация методов ниже находится в закрытой ветке разработки
    и не входит в состав публичного репозитория.
    """

    def __init__(self, config: WorkspaceConfig | None = None) -> None:
        self.config = config or WorkspaceConfig()

    # --- Компании -------------------------------------------------------

    def create_client(self, client: ClientAccount, specialist_id: str) -> ClientAccount:
        """POST /clients — подключение компании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def list_clients(self, specialist_id: str) -> list[ClientAccount]:
        """GET /clients — получение списка компаний."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_client(self, client_id: str, specialist_id: str) -> ClientAccount:
        """GET /clients/{client_id} — получение параметров компании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Персонажи ------------------------------------------------------

    def list_characters(self, client_id: str, specialist_id: str) -> list[CharacterProfile]:
        """GET /clients/{client_id}/characters — получение персонажей компании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_character_profile(self, character_id: str, specialist_id: str) -> CharacterProfile:
        """GET /characters/{character_id} — получение профиля персонажа."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    # --- Кампании -------------------------------------------------------

    def create_campaign(self, brief: Brief, specialist_id: str) -> CampaignView:
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
        """POST /materials/{material_id}/approve — утверждение материала специалистом."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def return_material(
        self,
        material_id: str,
        notes: list[RevisionNote],
        specialist_id: str,
    ) -> ApprovalDecision:
        """POST /materials/{material_id}/return — возврат материала на доработку."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def submit_metrics(self, metrics: PublicationMetrics, specialist_id: str) -> None:
        """POST /campaigns/{campaign_id}/metrics — ввод показателей публикации."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_metrics(self, campaign_id: str, specialist_id: str) -> list[PublicationMetrics]:
        """GET /campaigns/{campaign_id}/metrics — получение показателей кампании."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")

    def get_report(
        self,
        client_id: str,
        period_start: datetime,
        period_end: datetime,
        specialist_id: str,
    ) -> ClientReport:
        """GET /clients/{client_id}/report — автоматически сформированный отчёт об эффективности за период."""
        raise NotImplementedError("Логика реализована в закрытой ветке разработки")
