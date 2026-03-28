from __future__ import annotations

from app.benchmarks import (
    calc_delta_to_peer_median,
    calc_peer_median,
    calc_rank_percentile_placeholder,
    calc_ttu_vs_history,
)


def test_calc_ttu_vs_history() -> None:
    result = calc_ttu_vs_history(120.0, 100.0)

    assert result["delta"] == 20.0
    assert result["percent_change"] == 20.0


def test_calc_peer_median_and_delta() -> None:
    peers = [10.0, 20.0, 40.0]
    assert calc_peer_median(peers) == 20.0
    assert calc_delta_to_peer_median(25.0, peers) == 5.0


def test_rank_percentile_placeholder_with_data() -> None:
    result = calc_rank_percentile_placeholder(40.0, [10.0, 20.0, 30.0])

    assert result["available"] is True
    assert result["rank"] == 1
    assert result["group_size"] == 4


def test_rank_percentile_placeholder_without_data() -> None:
    result = calc_rank_percentile_placeholder(40.0, [])

    assert result == {
        "rank": None,
        "percentile": None,
        "group_size": 0,
        "available": False,
    }
