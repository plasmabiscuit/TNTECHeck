from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.benchmarks import build_benchmark_snapshot
from app.models import (
    ChartPoint,
    ChartResult,
    ComparisonGroupMeta,
    KpiResult,
    ReportFilters,
    ReportRunRequest,
    ReportRunResult,
    SourceNote,
    TableColumn,
    TableRow,
    TableSection,
)
from app.registry import load_registry


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
    selected_comparison = _resolve_filter(request.filters, "comparison_group_id") or "tn_public_peers"
    comparison_registry = {item.id: item for item in load_registry("comparison_groups", ComparisonGroupMeta)}
    selected_group = comparison_registry.get(selected_comparison)

    ttu_headcount = 10291
    peer_headcounts = [11842, 12388, 12901]
    ttu_history = [10042, 10177]
    benchmark_snapshot = build_benchmark_snapshot(
        current_value=ttu_headcount,
        historical_values=ttu_history,
        peer_values=peer_headcounts,
    )

    kpis = [
        KpiResult(
            id="headcount_total",
            label="TTU Total Enrollment",
            value=ttu_headcount,
            unit="students",
            trend="up",
            context_note="Latest institutional profile snapshot from Urban summary endpoint pathway.",
        ),
        KpiResult(
            id="pell_share",
            label="TTU Pell Grant Share",
            value=45.6,
            unit="percent",
            trend="flat",
            context_note="Share of undergraduates receiving Pell grants in latest snapshot year.",
        ),
        KpiResult(
            id="headcount_vs_history_delta",
            label="TTU Enrollment Δ vs Prior Year",
            value=benchmark_snapshot["ttu_vs_own_history"]["delta"] or "n/a",
            unit="students",
            context_note="Benchmark utility: TTU current value compared with own historical baseline.",
        ),
        KpiResult(
            id="headcount_vs_peer_median_delta",
            label="TTU Enrollment Δ vs Peer Median",
            value=benchmark_snapshot["ttu_delta_to_peer_median"]["delta_to_peer_median"] or "n/a",
            unit="students",
            context_note="Benchmark utility: TTU delta to selected peer median.",
        ),
    ]

    peer_label = selected_group.label if selected_group else "Comparison Group"
    comparison_mode = selected_group.definition.type if selected_group else "unknown"

    table = TableSection(
        id="institutional_overview_table",
        label="Institutional Overview by Group",
        columns=[
            TableColumn(key="group", label="Institution Group", kind="dimension"),
            TableColumn(key="headcount_total", label="Total Enrollment", kind="metric", unit="students"),
            TableColumn(key="pell_share", label="Pell Grant Share", kind="metric", unit="percent"),
        ],
        rows=[
            TableRow(cells={"group": "TTU", "headcount_total": ttu_headcount, "pell_share": 45.6}),
            TableRow(
                cells={
                    "group": f"{peer_label} Median",
                    "headcount_total": benchmark_snapshot["ttu_vs_peer_median"]["peer_median"],
                    "pell_share": 41.2,
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
            ChartPoint(x="TTU", y=ttu_headcount),
            ChartPoint(x=f"{peer_label} Median", y=benchmark_snapshot["ttu_vs_peer_median"]["peer_median"] or 0),
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
            "record_count": len(table.rows),
            "source": "urban_ed_api",
            "comparison_group": {
                "id": selected_comparison,
                "mode": comparison_mode,
                "resolved_unitid_count": len(selected_group.definition.institution_unitids) if selected_group else 0,
            },
            "benchmarks": benchmark_snapshot,
        },
        warnings=[
            "Values are seeded for end-to-end report execution scaffolding; live source adapter calls are not enabled yet."
        ],
    )
