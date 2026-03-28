from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl, model_validator


class MetaEnvelope(BaseModel):
    version: Literal["v1"] = "v1"
    count: int = Field(ge=0)


class ErrorBody(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorBody


class SourceMeta(BaseModel):
    id: str
    name: str
    kind: Literal["public_api", "download", "manual_import"]
    capabilities: list[str]
    default_enabled: bool = True
    docs_url: HttpUrl | None = None


class IndicatorMeta(BaseModel):
    id: str
    label: str
    category: str
    unit: str
    default_aggregation: str
    source_ids: list[str]
    description: str | None = None


class ProgramGroupMeta(BaseModel):
    id: str
    label: str
    description: str | None = None
    cip_codes: list[str]


class ComparisonGroupRule(BaseModel):
    rule_type: str
    params: dict[str, Any] = Field(default_factory=dict)


class ComparisonGroupDefinition(BaseModel):
    type: Literal["manual", "rule_based"]
    institution_unitids: list[int] = Field(default_factory=list)
    rule: ComparisonGroupRule | None = None

    @model_validator(mode="after")
    def validate_shape(self) -> "ComparisonGroupDefinition":
        if self.type == "manual":
            if not self.institution_unitids:
                raise ValueError("manual comparison groups must include at least one institution_unitid")
            if self.rule is not None:
                raise ValueError("manual comparison groups cannot define rule placeholders")

        if self.type == "rule_based":
            if self.institution_unitids:
                raise ValueError("rule-based comparison groups cannot include fixed institution_unitids")
            if self.rule is None:
                raise ValueError("rule-based comparison groups must define a rule placeholder")

        return self


class ComparisonGroupMeta(BaseModel):
    id: str
    label: str
    description: str | None = None
    definition: ComparisonGroupDefinition


class PresetSection(BaseModel):
    indicator_ids: list[str]
    program_group_ids: list[str] = Field(default_factory=list)
    comparison_group_id: str | None = None


class PresetMeta(BaseModel):
    id: str
    label: str
    sponsor_context: list[str]
    description: str
    sections: list[PresetSection]


class DocsMeta(BaseModel):
    id: str
    label: str
    url: HttpUrl
    source_id: str | None = None
    tags: list[str] = Field(default_factory=list)


class EligibilityCriterion(BaseModel):
    id: str
    label: str
    indicator_id: str
    operator: Literal[">", ">=", "<", "<=", "==", "!=", "between"]
    threshold: float | list[float] | str
    editable: bool = True


class EligibilityProfileMeta(BaseModel):
    id: str
    label: str
    description: str
    criteria: list[EligibilityCriterion]
    provenance_notes: str | None = None


class DataResponse(BaseModel):
    data: list[Any]
    meta: MetaEnvelope


class QueryFilter(BaseModel):
    field: str
    operator: Literal["eq", "neq", "in", "not_in", "gte", "lte", "between", "contains"]
    value: str | int | float | list[str] | list[int] | list[float]


class ReportFilters(BaseModel):
    items: list[QueryFilter] = Field(default_factory=list)


class ReportRunRequest(BaseModel):
    preset_id: str
    filters: ReportFilters = Field(default_factory=ReportFilters)


class KpiResult(BaseModel):
    id: str
    label: str
    value: float | int | str
    unit: str | None = None
    trend: Literal["up", "down", "flat"] | None = None
    context_note: str | None = None


class TableColumn(BaseModel):
    key: str
    label: str
    kind: Literal["dimension", "metric"] = "metric"
    unit: str | None = None


class TableRow(BaseModel):
    cells: dict[str, Any]


class TableSection(BaseModel):
    id: str
    label: str
    columns: list[TableColumn]
    rows: list[TableRow]


class ChartPoint(BaseModel):
    x: str | int | float
    y: int | float


class ChartResult(BaseModel):
    id: str
    label: str
    chart_type: Literal["bar", "line", "none"] = "none"
    x_key: str | None = None
    y_key: str | None = None
    points: list[ChartPoint] = Field(default_factory=list)
    note: str | None = None


class SourceNote(BaseModel):
    source_id: str
    source_name: str
    note: str
    used_summary_endpoint: bool = False
    partial_failure: bool = False


class ReportRunResult(BaseModel):
    run_id: str
    preset_id: str
    preset_label: str
    status: Literal["completed", "partial", "failed"]
    generated_at_utc: datetime
    institution_id: str
    filters: ReportFilters
    kpis: list[KpiResult] = Field(default_factory=list)
    tables: list[TableSection] = Field(default_factory=list)
    charts: list[ChartResult] = Field(default_factory=list)
    source_notes: list[SourceNote] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
