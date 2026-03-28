from fastapi.testclient import TestClient

from backend.api.app import app


client = TestClient(app)


def test_meta_endpoints_return_registry_data():
    paths = [
        "/api/meta/sources",
        "/api/meta/docs",
        "/api/meta/presets",
        "/api/meta/program-groups",
        "/api/meta/comparison-groups",
        "/api/meta/indicators",
        "/api/eligibility/profiles",
    ]

    for path in paths:
        response = client.get(path)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
