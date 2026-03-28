from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.benchmarks import (
    calc_delta_to_peer_median,
    calc_peer_median,
    calc_rank_percentile_placeholder,
    calc_ttu_vs_history,
)
from app.models import (
    ChartPoint,
    ChartResult,
    KpiResult,
    ReportFilters,
    ReportRunRequest,
    ReportRunResult,
    SourceNote,
    TableColumn,
    TableRow,
    TableSection,
)


def _resolve_filter(filters: ReportFilters, key: str) -> str | int | None:
    for item in filters.items:
        if item.field == key and item.operator == "eq":
            return item.value if isinstance(item.value, (str, int)) else None
    return None


def run_preset_report(request: ReportRunRequest) -> ReportRunResult:
    """Execute a report run for supported preset ids."""

    if request.preset_id == "institutional_profile_core":
        return _run_institutional_profile(request)

    raise NotImplementedError(f"Preset '{request.preset_id}' is not implemented yet.")


def _run_institutional_profile(request: ReportRunRequest) -> ReportRunResult:
    selected_comparison = request.comparison_group_id or _resolve_filter(request.filters, "comparison_group_id") or "tn_public_peers"
    benchmark_seed = {
        "tn_public_peers": {"headcount": [11890, 12388, 12990], "pell_share": [40.3, 41.2, 43.1]},
        "appalachian_masters": {"headcount": [8144, 9020, 9760], "pell_share": [43.9, 46.5, 48.2]},
    }.get(selected_comparison, {"headcount": [12388], "pell_share": [41.2]})

    headcount_history = calc_ttu_vs_history(10291, 9978)
    headcount_peer_median = calc_peer_median(benchmark_seed["headcount"]) or 0.0
    headcount_delta_to_peer = calc_delta_to_peer_median(10291, benchmark_seed["headcount"]) or 0.0
    headcount_rank = calc_rank_percentile_placeholder(10291, benchmark_seed["headcount"])

    pell_history = calc_ttu_vs_history(45.6, 45.2)
    pell_peer_median = calc_peer_median(benchmark_seed["pell_share"]) or 0.0
    pell_delta_to_peer = calc_delta_to_peer_median(45.6, benchmark_seed["pell_share"]) or 0.0
    pell_rank = calc_rank_percentile_placeholder(45.6, benchmark_seed["pell_share"])

    kpis = [
        KpiResult(
            id="headcount_total",
            label="TTU Total Enrollment",
            value=10291,
            unit="students",
            trend="up",
            context_note=(
                f"TTU history delta {headcount_history['delta']:.0f}; peer median {headcount_peer_median:.0f}; "
                f"delta-to-median {headcount_delta_to_peer:.0f}; rank placeholder "
                f"{headcount_rank['rank']}/{headcount_rank['group_size']}."
            ),
        ),
        KpiResult(
            id="pell_share",
            label="TTU Pell Grant Share",
            value=45.6,
            unit="percent",
            trend="flat",
            context_note=(
                f"TTU history delta {pell_history['delta']:.1f}pp; peer median {pell_peer_median:.1f}%; "
                f"delta-to-median {pell_delta_to_peer:.1f}pp; percentile placeholder {pell_rank['percentile']}."
            ),
        ),
    ]

    table = TableSection(
        id="institutional_overview_table",
        label="Institutional Overview by Group",
        columns=[
            TableColumn(key="group", label="Institution Group", kind="dimension"),
            TableColumn(key="headcount_total", label="Total Enrollment", kind="metric", unit="students"),
            TableColumn(key="pell_share", label="Pell Grant Share", kind="metric", unit="percent"),
            TableColumn(key="headcount_delta_peer_median", label="Enrollment Δ vs Peer Median", kind="metric", unit="students"),
            TableColumn(key="pell_delta_peer_median", label="Pell Share Δ vs Peer Median", kind="metric", unit="percent"),
        ],
        rows=[
            TableRow(
                cells={
                    "group": "TTU",
                    "headcount_total": 10291,
                    "pell_share": 45.6,
                    "headcount_delta_peer_median": round(headcount_delta_to_peer, 2),
                    "pell_delta_peer_median": round(pell_delta_to_peer, 2),
                }
            ),
            TableRow(
                cells={
                    "group": "Peer Median",
                    "headcount_total": round(headcount_peer_median, 2),
                    "pell_share": round(pell_peer_median, 2),
                    "headcount_delta_peer_median": 0,
                    "pell_delta_peer_median": 0,
                }
            ),
        ],
    )

    chart = ChartResult(
        id="headcount_comparison",
        label="Enrollment Snapshot",
        chart_type="bar",
        x_key="group",
        y_key="headcount_total",
        points=[
            ChartPoint(x="TTU", y=10291),
            ChartPoint(x="Tennessee Public Peers", y=12388),
        ],
        note="Lightweight preview rendering; charting library integration is pending.",
    )

    return ReportRunResult(
        run_id=f"run_{uuid4().hex[:12]}",
        preset_id=request.preset_id,
        preset_label="Institutional Profile (Core)",
        status="completed",
        generated_at_utc=datetime.now(timezone.utc),
        institution_id="221847",
        filters=request.filters,
        kpis=kpis,
        tables=[table],
        charts=[chart],
        source_notes=[
            SourceNote(
                source_id="urban_ed_api",
                source_name="Urban Education Data API",
                note="Stubbed summary pathway currently returns seeded benchmark values for v1 execution flow.",
                used_summary_endpoint=True,
                partial_failure=False,
            )
        ],
        provenance={
            "mode": "stub_summary",
            "query": {
                "comparison_group_id": selected_comparison,
                "institution_id": "221847",
                "output": "report",
            },
            "benchmark": {
                "headcount": {
                    "history": headcount_history,
                    "peer_median": headcount_peer_median,
                    "delta_to_peer_median": headcount_delta_to_peer,
                    "rank_percentile_placeholder": headcount_rank,
                },
                "pell_share": {
                    "history": pell_history,
                    "peer_median": pell_peer_median,
                    "delta_to_peer_median": pell_delta_to_peer,
                    "rank_percentile_placeholder": pell_rank,
                },
            },
            "record_count": len(table.rows),
            "source": "urban_ed_api",
        },
        warnings=[
            "Values are seeded for end-to-end report execution scaffolding; live source adapter calls are not enabled yet."
        ],
    )
