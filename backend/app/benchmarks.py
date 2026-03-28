from __future__ import annotations

from statistics import median


def calc_ttu_vs_history(current_value: float, prior_value: float) -> dict[str, float]:
    delta = current_value - prior_value
    pct_change = 0.0 if prior_value == 0 else (delta / prior_value) * 100
    return {
        "current_value": current_value,
        "prior_value": prior_value,
        "delta": delta,
        "percent_change": pct_change,
    }


def calc_peer_median(peer_values: list[float]) -> float | None:
    if not peer_values:
        return None
    return float(median(peer_values))


def calc_delta_to_peer_median(ttu_value: float, peer_values: list[float]) -> float | None:
    peer_median = calc_peer_median(peer_values)
    if peer_median is None:
        return None
    return ttu_value - peer_median


def calc_rank_percentile_placeholder(ttu_value: float, peer_values: list[float]) -> dict[str, float | int | None]:
    if not peer_values:
        return {
            "rank": None,
            "percentile": None,
            "group_size": 0,
            "available": False,
        }

    all_values = sorted(peer_values + [ttu_value], reverse=True)
    rank = all_values.index(ttu_value) + 1
    percentile = ((len(all_values) - rank) / (len(all_values) - 1)) * 100 if len(all_values) > 1 else 100.0
    return {
        "rank": rank,
        "percentile": round(percentile, 2),
        "group_size": len(all_values),
        "available": True,
    }
