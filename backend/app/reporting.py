from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

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
    selected_comparison = _resolve_filter(request.filters, "comparison_group_id") or "tn_public_peers"

    kpis = [
        KpiResult(
            id="headcount_total",
            label="TTU Total Enrollment",
            value=10291,
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
    ]

    table = TableSection(
        id="institutional_overview_table",
        label="Institutional Overview by Group",
        columns=[
            TableColumn(key="group", label="Institution Group", kind="dimension"),
            TableColumn(key="headcount_total", label="Total Enrollment", kind="metric", unit="students"),
            TableColumn(key="pell_share", label="Pell Grant Share", kind="metric", unit="percent"),
        ],
        rows=[
            TableRow(cells={"group": "TTU", "headcount_total": 10291, "pell_share": 45.6}),
            TableRow(cells={"group": "Tennessee Public Peers", "headcount_total": 12388, "pell_share": 41.2}),
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
            "record_count": len(table.rows),
            "source": "urban_ed_api",
        },
        warnings=[
            "Values are seeded for end-to-end report execution scaffolding; live source adapter calls are not enabled yet."
        ],
    )
