from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


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


class ComparisonGroupMeta(BaseModel):
    id: str
    label: str
    description: str | None = None
    institution_unitids: list[int]


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
