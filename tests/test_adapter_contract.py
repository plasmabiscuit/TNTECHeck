from __future__ import annotations

from tntecheck.adapters import (
    AdapterCapabilities,
    AdapterHealth,
    AdapterQuery,
    AdapterResult,
    SourceAdapter,
    get_default_adapters,
)
from tntecheck.adapters.models import TTU_NAME, TTU_UNITID


REQUIRED_SOURCES = {
    "urban",
    "college_scorecard",
    "nih_reporter",
    "nsf_award_search",
    "nifa_data_gateway",
    "ipeds_manual_import",
}


def test_required_adapter_set_is_present() -> None:
    adapters = get_default_adapters()
    assert {a.source_name for a in adapters} == REQUIRED_SOURCES


def test_all_adapters_implement_contract() -> None:
    for adapter in get_default_adapters():
        assert isinstance(adapter, SourceAdapter)
        assert isinstance(adapter.capabilities, AdapterCapabilities)

        health = adapter.healthcheck()
        assert isinstance(health, AdapterHealth)
        assert health.source == adapter.source_name

        query = AdapterQuery(metric="institution_overview")
        result = adapter.fetch(query)
        assert isinstance(result, AdapterResult)
        assert result.source == adapter.source_name


def test_ttu_defaults_are_preserved_in_query_model() -> None:
    query = AdapterQuery(metric="anything")
    assert query.institution_id == TTU_UNITID


def test_normalization_hooks_exist_and_are_callable() -> None:
    sample = {"fiscal_year": 2024, "cip": "26.0101", "amount": 10}

    for adapter in get_default_adapters():
        assert callable(adapter.institution_identity_normalizer)
        assert callable(adapter.time_normalizer)
        assert callable(adapter.program_cip_normalizer)
        assert callable(adapter.funding_normalizer)

        normalized = adapter.institution_identity_normalizer(sample)
        normalized = adapter.time_normalizer(normalized)
        normalized = adapter.program_cip_normalizer(normalized)
        normalized = adapter.funding_normalizer(normalized)

        assert normalized["institution_id"] == TTU_UNITID
        assert normalized["institution_name"] == TTU_NAME
        assert normalized["year"] == 2024
        assert normalized["cip_code"] == "26.0101"
        assert normalized["value"] == 10
