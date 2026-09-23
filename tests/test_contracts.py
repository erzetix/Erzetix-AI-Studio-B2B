"""
Проверка контрактов: соответствие JSON-примеров документации моделям
данных, импорт подсистем, правила переходов между состояниями.
"""

from __future__ import annotations

import importlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

from ab_testing.models import Experiment, ExperimentResult
from agents.brand_guardian.models import (
    CheckCategory,
    MaterialVerdict,
    NoteAuthor,
    ReviewReport,
    RevisionNote,
    TargetAgent,
    Verdict,
)
from agents.character_core.models import Brief, CampaignContext
from agents.creator.models import DraftBundle
from agents.metrics_analyst.models import MetricsAnalysis
from agents.strategist.models import ContentPlan
from agents.trend_analyst.models import TrendReport
from agents.visualizer.models import AssetBundle
from orchestrator.models import CampaignRun, CampaignState, MaterialRun, MaterialState
from orchestrator.pipeline import (
    CAMPAIGN_TRANSITIONS,
    MATERIAL_TRANSITIONS,
    TERMINAL_MATERIAL_STATES,
    OrchestratorConfig,
    can_transition_material,
    is_campaign_completed,
    state_after_review,
)
from workspace.models import ApprovalDecision, ClientReport, MaterialView

ROOT = Path(__file__).resolve().parent.parent
NOW = datetime(2026, 9, 1, tzinfo=timezone.utc)


def json_examples(relative_path: str) -> list[dict]:
    text = (ROOT / relative_path).read_text(encoding="utf-8")
    return [json.loads(block) for block in re.findall(r"```json\n(.*?)```", text, re.S)]


# --- Документация ---------------------------------------------------------


@pytest.mark.parametrize(
    "path",
    sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("*.md") if ".git" not in p.parts),
)
def test_json_examples_are_valid_json(path: str) -> None:
    json_examples(path)


# Полные JSON-примеры документации и модели, которым они соответствуют.
# Сокращённые фрагменты входных контрактов в перечень не входят.
FULL_EXAMPLES: list[tuple[str, int, type[BaseModel]]] = [
    ("agents/character_core/README.md", 0, Brief),
    ("agents/trend_analyst/README.md", 1, TrendReport),
    ("agents/strategist/README.md", 1, ContentPlan),
    ("agents/creator/README.md", 1, DraftBundle),
    ("agents/visualizer/README.md", 1, AssetBundle),
    ("agents/brand_guardian/README.md", 1, ReviewReport),
    ("agents/metrics_analyst/README.md", 1, MetricsAnalysis),
    ("ab_testing/README.md", 0, Experiment),
    ("ab_testing/README.md", 1, ExperimentResult),
    ("workspace/README.md", 0, MaterialView),
    ("workspace/README.md", 1, ApprovalDecision),
]


@pytest.mark.parametrize(("path", "index", "model"), FULL_EXAMPLES)
def test_full_examples_match_models(path: str, index: int, model: type[BaseModel]) -> None:
    model.model_validate(json_examples(path)[index])


def test_campaign_context_example_matches_model() -> None:
    brief, context = json_examples("agents/character_core/README.md")[0:2]
    context["brief"] = brief
    CampaignContext.model_validate(context)


# --- Подсистемы ------------------------------------------------------------

MODULES = [
    "agents.character_core.agent",
    "agents.trend_analyst.agent",
    "agents.strategist.agent",
    "agents.creator.agent",
    "agents.visualizer.agent",
    "agents.brand_guardian.agent",
    "agents.metrics_analyst.agent",
    "ab_testing.experiments",
    "orchestrator.pipeline",
    "workspace.api",
]


@pytest.mark.parametrize("module", MODULES)
def test_modules_import_and_configs_instantiate(module: str) -> None:
    imported = importlib.import_module(module)
    for name in dir(imported):
        if name.endswith("Config"):
            getattr(imported, name)()


# --- Переходы состояний ------------------------------------------------------


def test_transition_tables_cover_all_states() -> None:
    assert set(CAMPAIGN_TRANSITIONS) == set(CampaignState)
    assert set(MATERIAL_TRANSITIONS) == set(MaterialState)
    for targets in MATERIAL_TRANSITIONS.values():
        assert set(targets) <= set(MaterialState)


def test_publishing_only_from_approved() -> None:
    sources = {s for s, targets in MATERIAL_TRANSITIONS.items() if MaterialState.PUBLISHING in targets}
    assert sources == {MaterialState.APPROVED}


def test_approval_only_by_human_decision() -> None:
    sources = {s for s, targets in MATERIAL_TRANSITIONS.items() if MaterialState.APPROVED in targets}
    assert sources == {MaterialState.AWAITING_APPROVAL}


def test_terminal_material_states() -> None:
    assert TERMINAL_MATERIAL_STATES == {
        MaterialState.PUBLISHED,
        MaterialState.BLOCKED,
        MaterialState.REJECTED,
        MaterialState.FAILED,
    }


def material(state: MaterialState = MaterialState.REVIEWING, cycles: int = 0) -> MaterialRun:
    return MaterialRun(
        material_id="mat_001",
        campaign_id="camp_001",
        concept_id="cpt_001",
        draft_id="drf_001",
        state=state,
        revision_cycles=cycles,
        updated_at=NOW,
    )


def note(target: TargetAgent) -> RevisionNote:
    return RevisionNote(
        note_id="nte_001",
        draft_id="drf_001",
        target_agent=target,
        category=CheckCategory.BRIEF_CONSTRAINTS,
        issue="Замечание",
        required_action="Действие",
    )


LIMIT = OrchestratorConfig().max_revision_cycles


def test_approved_verdict_goes_to_human() -> None:
    verdict = MaterialVerdict(draft_id="drf_001", verdict=Verdict.APPROVED)
    assert state_after_review(material(), verdict, LIMIT) == MaterialState.AWAITING_APPROVAL


@pytest.mark.parametrize(
    ("target", "expected"),
    [(TargetAgent.CREATOR, MaterialState.DRAFTING), (TargetAgent.VISUALIZER, MaterialState.GENERATING)],
)
def test_revision_returns_material_to_target(target: TargetAgent, expected: MaterialState) -> None:
    verdict = MaterialVerdict(
        draft_id="drf_001", verdict=Verdict.REVISION_REQUIRED, revision_notes=[note(target)]
    )
    assert state_after_review(material(), verdict, LIMIT) == expected


def test_revision_limit_escalates() -> None:
    verdict = MaterialVerdict(
        draft_id="drf_001",
        verdict=Verdict.REVISION_REQUIRED,
        revision_notes=[note(TargetAgent.CREATOR)],
    )
    assert state_after_review(material(cycles=LIMIT), verdict, LIMIT) == MaterialState.ESCALATED


def test_every_review_outcome_is_allowed_transition() -> None:
    for verdict_value in Verdict:
        notes = [note(TargetAgent.CREATOR)] if verdict_value == Verdict.REVISION_REQUIRED else []
        verdict = MaterialVerdict(draft_id="drf_001", verdict=verdict_value, revision_notes=notes)
        target = state_after_review(material(), verdict, LIMIT)
        assert can_transition_material(MaterialState.REVIEWING, target)


def test_campaign_completed_when_all_materials_terminal() -> None:
    run = CampaignRun(
        campaign_id="camp_001",
        character_id="nick_v1",
        client_id="erzetix_media",
        state=CampaignState.PRODUCING,
        materials=[material(MaterialState.PUBLISHED), material(MaterialState.AWAITING_APPROVAL)],
        created_at=NOW,
        updated_at=NOW,
    )
    assert not is_campaign_completed(run)
    run.materials[1].state = MaterialState.REJECTED
    assert is_campaign_completed(run)


# --- Правила моделей -------------------------------------------------------


def test_guardian_note_requires_category() -> None:
    with pytest.raises(ValidationError):
        RevisionNote(
            note_id="nte_001",
            draft_id="drf_001",
            target_agent=TargetAgent.CREATOR,
            issue="Замечание",
            required_action="Действие",
        )
    RevisionNote(
        note_id="nte_002",
        draft_id="drf_001",
        target_agent=TargetAgent.CREATOR,
        author=NoteAuthor.SPECIALIST,
        issue="Замечание",
        required_action="Действие",
    )


def test_return_requires_notes() -> None:
    with pytest.raises(ValidationError):
        ApprovalDecision(material_id="mat_001", approved=False, decided_by="s", decided_at=NOW)
    with pytest.raises(ValidationError):
        ApprovalDecision(
            material_id="mat_001",
            approved=True,
            decided_by="s",
            decided_at=NOW,
            revision_notes=[note(TargetAgent.CREATOR)],
        )


def test_report_period_order() -> None:
    with pytest.raises(ValidationError):
        ClientReport(
            report_id="rep_001",
            client_id="client_001",
            period_start=NOW,
            period_end=NOW,
            generated_at=NOW,
        )
