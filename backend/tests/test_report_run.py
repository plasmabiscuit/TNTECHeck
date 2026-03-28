from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_run_institutional_profile_report_success() -> None:
    response = client.post(
        "/api/report/run",
        json={
            "preset_id": "institutional_profile_core",
            "filters": {"items": [{"field": "comparison_group_id", "operator": "eq", "value": "tn_public_peers"}]},
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "completed"
    assert payload["preset_id"] == "institutional_profile_core"
    assert payload["kpis"], "Expected KPI payload for first real report run"
    assert payload["tables"], "Expected table payload for first real report run"
    assert payload["source_notes"], "Expected source notes for provenance visibility"
    assert "mode" in payload["provenance"]


def test_run_report_rejects_unknown_preset() -> None:
    response = client.post("/api/report/run", json={"preset_id": "unknown_preset", "filters": {"items": []}})

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "PRESET_NOT_FOUND"


def test_run_report_rejects_invalid_comparison_filter() -> None:
    response = client.post(
        "/api/report/run",
        json={
            "preset_id": "institutional_profile_core",
            "filters": {"items": [{"field": "comparison_group_id", "operator": "eq", "value": "bad_group"}]},
        },
    )

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "INVALID_FILTER"
    assert body["error"]["details"]["field"] == "comparison_group_id"
