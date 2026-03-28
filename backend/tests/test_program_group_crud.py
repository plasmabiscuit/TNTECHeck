from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def write_program_groups(tmp_path, payload):
    path = tmp_path / "program_groups.json"
    path.write_text(json.dumps(payload))


def test_program_group_crud_with_preview(monkeypatch, tmp_path) -> None:
    seed = [
        {
            "id": "seed_group",
            "label": "Seed Group",
            "scope": "strict",
            "description": "Seed",
            "cip_codes": ["26.0101"],
            "award_levels": ["bachelor"],
            "notes": "seed",
            "version": 1,
        }
    ]
    write_program_groups(tmp_path, seed)
    monkeypatch.setattr("app.main.BASE_DATA_DIR", tmp_path)

    listed = client.get("/api/program-groups")
    assert listed.status_code == 200
    assert listed.json()["meta"]["count"] == 1

    preview = client.post(
        "/api/program-groups/preview",
        json={
            "id": "custom_stem",
            "label": "Custom STEM",
            "scope": "custom",
            "description": "custom definition",
            "cip_codes": ["14.0801", "26.0101"],
            "award_levels": ["bachelor", "master"],
            "notes": "draft",
        },
    )
    assert preview.status_code == 200
    assert preview.json()["total_combinations"] == 4

    created = client.post(
        "/api/program-groups",
        json={
            "id": "custom_stem",
            "label": "Custom STEM",
            "scope": "custom",
            "description": "custom definition",
            "cip_codes": ["14.0801", "26.0101"],
            "award_levels": ["bachelor", "master"],
            "notes": "draft",
        },
    )
    assert created.status_code == 200
    assert created.json()["id"] == "custom_stem"

    updated = client.put(
        "/api/program-groups/custom_stem",
        json={
            "id": "custom_stem_renamed",
            "label": "Custom STEM Updated",
            "scope": "broad",
            "description": "updated",
            "cip_codes": ["14.0801"],
            "award_levels": ["doctorate"],
            "notes": "updated",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["id"] == "custom_stem_renamed"
    assert updated.json()["version"] == 2

    deleted = client.delete("/api/program-groups/custom_stem_renamed")
    assert deleted.status_code == 204


def test_program_group_validation_errors(monkeypatch, tmp_path) -> None:
    write_program_groups(
        tmp_path,
        [
            {
                "id": "existing_group",
                "label": "Existing",
                "scope": "strict",
                "description": None,
                "cip_codes": ["26.0101"],
                "award_levels": ["bachelor"],
                "notes": None,
                "version": 1,
            }
        ],
    )
    monkeypatch.setattr("app.main.BASE_DATA_DIR", tmp_path)

    duplicate = client.post(
        "/api/program-groups",
        json={
            "id": "existing_group",
            "label": "Duplicate",
            "scope": "custom",
            "description": None,
            "cip_codes": ["26.0101"],
            "award_levels": ["bachelor"],
            "notes": None,
        },
    )
    assert duplicate.status_code == 409
    assert duplicate.json()["error"]["code"] == "DUPLICATE_PROGRAM_GROUP_ID"

    malformed_cip = client.post(
        "/api/program-groups",
        json={
            "id": "invalid_cip_group",
            "label": "Invalid CIP",
            "scope": "custom",
            "description": None,
            "cip_codes": ["bad-cip"],
            "award_levels": ["bachelor"],
            "notes": None,
        },
    )
    assert malformed_cip.status_code == 422
    assert malformed_cip.json()["error"]["code"] == "INVALID_PROGRAM_GROUP_CIP"

    empty_definition = client.post(
        "/api/program-groups",
        json={
            "id": "empty_group",
            "label": "Empty Group",
            "scope": "custom",
            "description": None,
            "cip_codes": [],
            "award_levels": [],
            "notes": None,
        },
    )
    assert empty_definition.status_code == 422
    assert empty_definition.json()["error"]["code"] in {
        "EMPTY_PROGRAM_GROUP_CIPS",
        "EMPTY_PROGRAM_GROUP_AWARD_LEVELS",
    }
