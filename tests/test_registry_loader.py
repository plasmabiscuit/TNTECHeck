from __future__ import annotations

import json

import pytest

from backend.registry.loader import RegistryValidationError, load_registries


def test_load_registries_successfully_loads_seed_data():
    bundle = load_registries("registries")

    assert bundle.institution_unitid == 221847
    assert any(source.id == "urban-ed-api" for source in bundle.sources)
    assert any(profile.id == "capacity-template-v1" for profile in bundle.eligibility_profiles)


def test_load_registries_fails_on_malformed_json(tmp_path):
    source = tmp_path / "sources.json"
    source.write_text("[", encoding="utf-8")

    for filename in [
        "source_docs.json",
        "presets.json",
        "program_groups.json",
        "comparison_groups.json",
        "eligibility_profiles.json",
        "indicators.json",
    ]:
        (tmp_path / filename).write_text("[]", encoding="utf-8")

    with pytest.raises(RegistryValidationError, match="Invalid JSON"):
        load_registries(tmp_path)


def test_load_registries_fails_on_missing_required_field(tmp_path):
    (tmp_path / "sources.json").write_text(
        json.dumps(
            [
                {
                    "id": "urban-ed-api",
                    "name": "Urban",
                    "description": "desc",
                    "adapter": "urban",
                    "supports_summary_endpoints": True,
                    "supports_live_queries": True,
                    "status": "active",
                }
            ]
        ),
        encoding="utf-8",
    )

    for filename in [
        "source_docs.json",
        "presets.json",
        "program_groups.json",
        "comparison_groups.json",
        "eligibility_profiles.json",
        "indicators.json",
    ]:
        (tmp_path / filename).write_text("[]", encoding="utf-8")

    with pytest.raises(RegistryValidationError, match="failed validation"):
        load_registries(tmp_path)


def test_load_registries_fails_on_duplicate_ids(tmp_path):
    (tmp_path / "sources.json").write_text(
        json.dumps(
            [
                {
                    "id": "urban-ed-api",
                    "name": "Urban",
                    "description": "desc",
                    "adapter": "urban",
                    "base_url": "https://educationdata.urban.org",
                    "supports_summary_endpoints": True,
                    "supports_live_queries": True,
                    "status": "active",
                },
                {
                    "id": "urban-ed-api",
                    "name": "Urban Duplicate",
                    "description": "desc",
                    "adapter": "urban",
                    "base_url": "https://educationdata.urban.org",
                    "supports_summary_endpoints": True,
                    "supports_live_queries": True,
                    "status": "active",
                },
            ]
        ),
        encoding="utf-8",
    )

    for filename in [
        "source_docs.json",
        "presets.json",
        "program_groups.json",
        "comparison_groups.json",
        "eligibility_profiles.json",
        "indicators.json",
    ]:
        (tmp_path / filename).write_text("[]", encoding="utf-8")

    with pytest.raises(RegistryValidationError, match="duplicate id"):
        load_registries(tmp_path)
