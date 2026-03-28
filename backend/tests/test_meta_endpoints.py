from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.registry import RegistryError, load_registry

client = TestClient(app)


@pytest.mark.parametrize(
    "path,expected_key",
    [
        ("/api/meta/sources", "capabilities"),
        ("/api/meta/indicators", "category"),
        ("/api/meta/program-groups", "cip_codes"),
        ("/api/meta/comparison-groups", "definition"),
        ("/api/meta/presets", "sections"),
        ("/api/meta/docs", "url"),
        ("/api/meta/eligibility-profiles", "criteria"),
    ],
)
def test_metadata_endpoints_success(path: str, expected_key: str) -> None:
    response = client.get(path)

    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"data", "meta"}
    assert payload["meta"]["version"] == "v1"
    assert payload["meta"]["count"] == len(payload["data"])
    assert payload["data"], "Seed registry should not be empty"
    assert expected_key in payload["data"][0]


def test_missing_registry_returns_explicit_error(tmp_path) -> None:
    with pytest.raises(RegistryError) as exc:
        load_registry("sources", model_type=dict, data_dir=tmp_path)  # type: ignore[arg-type]

    assert exc.value.code == "REGISTRY_NOT_FOUND"
    assert exc.value.details["registry"] == "sources"
    assert str(tmp_path / "sources.json") in exc.value.details["path"]


def test_endpoint_missing_registry_shape(monkeypatch) -> None:
    from app import main

    def _missing(*_, **__):
        raise RegistryError(
            code="REGISTRY_NOT_FOUND",
            message="Registry 'sources' is missing.",
            details={"registry": "sources", "path": "/tmp/sources.json"},
        )

    monkeypatch.setattr(main, "_load", _missing)

    response = client.get("/api/meta/sources")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "REGISTRY_NOT_FOUND",
            "message": "Registry 'sources' is missing.",
            "details": {"registry": "sources", "path": "/tmp/sources.json"},
        }
    }
