from __future__ import annotations

from statistics import median
from typing import Any


def compute_ttu_vs_history(current_value: float, historical_values: list[float]) -> dict[str, Any]:
    if not historical_values:
        return {
            "current": current_value,
            "history_baseline": None,
            "delta": None,
            "pct_change": None,
            "note": "No historical baseline values available.",
        }

    baseline = historical_values[-1]
    delta = current_value - baseline
    pct_change = None if baseline == 0 else (delta / baseline) * 100
    return {
        "current": current_value,
        "history_baseline": baseline,
        "delta": round(delta, 2),
        "pct_change": None if pct_change is None else round(pct_change, 2),
    }


def compute_peer_median(peer_values: list[float]) -> float | None:
    if not peer_values:
        return None
    return float(median(peer_values))


def compute_ttu_delta_to_peer_median(current_value: float, peer_values: list[float]) -> dict[str, Any]:
    peer_median = compute_peer_median(peer_values)
    if peer_median is None:
        return {
            "current": current_value,
            "peer_median": None,
            "delta_to_peer_median": None,
            "note": "No peer values available.",
        }

    return {
        "current": current_value,
        "peer_median": peer_median,
        "delta_to_peer_median": round(current_value - peer_median, 2),
    }


def compute_rank_percentile_placeholder(current_value: float, peer_values: list[float]) -> dict[str, Any]:
    population = [*peer_values, current_value]
    if len(population) < 2:
        return {
            "rank": None,
            "percentile": None,
            "status": "insufficient_data",
            "note": "Rank/percentile placeholders require at least one peer value.",
        }

    # Descending rank: higher values are better by default until indicator-specific direction metadata is introduced.
    rank = 1 + sum(1 for value in population if value > current_value)
    percentile = sum(1 for value in population if value <= current_value) / len(population) * 100
    return {
        "rank": rank,
        "percentile": round(percentile, 2),
        "status": "placeholder",
        "note": "Placeholder ranking uses naive descending ordering and can be refined per-indicator later.",
    }


def build_benchmark_snapshot(current_value: float, historical_values: list[float], peer_values: list[float]) -> dict[str, Any]:
    return {
        "ttu_vs_own_history": compute_ttu_vs_history(current_value=current_value, historical_values=historical_values),
        "ttu_vs_peer_median": {
            "current": current_value,
            "peer_median": compute_peer_median(peer_values),
        },
        "ttu_delta_to_peer_median": compute_ttu_delta_to_peer_median(current_value=current_value, peer_values=peer_values),
        "ttu_rank_percentile": compute_rank_percentile_placeholder(current_value=current_value, peer_values=peer_values),
    }
