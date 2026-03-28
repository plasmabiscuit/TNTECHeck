from __future__ import annotations

import pytest

from app.benchmarks import (
    build_benchmark_snapshot,
    compute_peer_median,
    compute_rank_percentile_placeholder,
    compute_ttu_delta_to_peer_median,
    compute_ttu_vs_history,
)
from app.models import ComparisonGroupDefinition


def test_manual_comparison_group_definition_validates() -> None:
    definition = ComparisonGroupDefinition(type="manual", institution_unitids=[1, 2, 3])
    assert definition.type == "manual"
    assert definition.institution_unitids == [1, 2, 3]


def test_rule_based_comparison_group_definition_validates() -> None:
    definition = ComparisonGroupDefinition(
        type="rule_based",
        rule={"rule_type": "carnegie", "params": {"basic_classification": "M1"}},
    )
    assert definition.type == "rule_based"
    assert definition.rule.rule_type == "carnegie"


def test_manual_comparison_group_rejects_empty_unitids() -> None:
    with pytest.raises(ValueError):
        ComparisonGroupDefinition(type="manual", institution_unitids=[])


def test_rule_based_comparison_group_rejects_manual_unitids() -> None:
    with pytest.raises(ValueError):
        ComparisonGroupDefinition(
            type="rule_based",
            institution_unitids=[220978],
            rule={"rule_type": "carnegie", "params": {}},
        )


def test_benchmark_calculations() -> None:
    assert compute_ttu_vs_history(current_value=120.0, historical_values=[100.0, 110.0])["delta"] == 10.0
    assert compute_peer_median([90.0, 110.0, 130.0]) == 110.0
    assert compute_ttu_delta_to_peer_median(120.0, [90.0, 110.0, 130.0])["delta_to_peer_median"] == 10.0

    rank_payload = compute_rank_percentile_placeholder(120.0, [90.0, 110.0, 130.0])
    assert rank_payload["status"] == "placeholder"
    assert rank_payload["rank"] == 2


def test_benchmark_snapshot_has_required_sections() -> None:
    snapshot = build_benchmark_snapshot(current_value=120.0, historical_values=[100.0], peer_values=[90.0, 130.0])
    assert set(snapshot) == {
        "ttu_vs_own_history",
        "ttu_vs_peer_median",
        "ttu_delta_to_peer_median",
        "ttu_rank_percentile",
    }
