from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def isolated_registry_dir(tmp_path, monkeypatch):
    from app import main

    data_dir = tmp_path / "data"
    data_dir.mkdir()

    for name in ["comparison_groups", "program_groups", "presets", "indicators", "sources", "docs", "eligibility_profiles"]:
        src = main.BASE_DATA_DIR / f"{name}.json"
        data_dir.joinpath(f"{name}.json").write_text(src.read_text())

    monkeypatch.setattr(main, "BASE_DATA_DIR", data_dir)
    yield data_dir


def test_create_manual_comparison_group_requires_unitids(isolated_registry_dir) -> None:
    response = client.post(
        "/api/comparison-groups",
        json={
            "id": "empty_manual",
            "label": "Empty Manual",
            "definition_type": "manual_list",
            "institution_unitids": [],
            "rules": [],
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "EMPTY_COMPARISON_GROUP_UNITIDS"


def test_create_rule_based_comparison_group_requires_rules(isolated_registry_dir) -> None:
    response = client.post(
        "/api/comparison-groups",
        json={
            "id": "rule_without_rules",
            "label": "Rule Missing",
            "definition_type": "rule_based_placeholder",
            "institution_unitids": [],
            "rules": [],
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "EMPTY_COMPARISON_GROUP_RULES"


def test_create_and_update_rule_based_comparison_group(isolated_registry_dir) -> None:
    create_response = client.post(
        "/api/comparison-groups",
        json={
            "id": "rule_group",
            "label": "Rule Group",
            "definition_type": "rule_based_placeholder",
            "institution_unitids": [],
            "rules": [{"field": "state", "operator": "eq", "value": "TN"}],
            "notes": "seed",
        },
    )

    assert create_response.status_code == 200
    created = create_response.json()
    assert created["version"] == 1

    update_response = client.put(
        "/api/comparison-groups/rule_group",
        json={
            "id": "rule_group",
            "label": "Rule Group Updated",
            "definition_type": "rule_based_placeholder",
            "institution_unitids": [],
            "rules": [
                {"field": "state", "operator": "eq", "value": "TN"},
                {"field": "sector", "operator": "eq", "value": "public_4_year"},
            ],
            "notes": "updated",
        },
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["version"] == 2
    assert len(updated["rules"]) == 2

    # persisted registry check
    payload = json.loads((isolated_registry_dir / "comparison_groups.json").read_text())
    matched = next(item for item in payload if item["id"] == "rule_group")
    assert matched["version"] == 2
