from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class RegistryBase(BaseModel):
    id: str = Field(min_length=1)

    class Config:
        extra = "forbid"
class SourceRegistryEntry(RegistryBase):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    adapter: str = Field(min_length=1)
    base_url: str = Field(min_length=1)
    supports_summary_endpoints: bool
    supports_live_queries: bool
    status: Literal["active", "degraded", "offline"]


class SourceDocRegistryEntry(RegistryBase):
    source: str = Field(min_length=1)
    label: str = Field(min_length=1)
    url: str = Field(min_length=1)
    category: Literal["api", "data_dictionary", "download", "help", "terms"]


class PresetRegistryEntry(RegistryBase):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    funder_tags: list[str] = Field(default_factory=list)
    required_sources: list[str] = Field(default_factory=list)
    indicators: list[str] = Field(default_factory=list)
    supports_comparison: bool = False
    supports_program_groups: bool = False
    supports_eligibility_profile: bool = False


class ProgramGroupMapping(BaseModel):
    cip_code: str = Field(min_length=2)
    label: str = Field(min_length=1)


class ProgramGroupRegistryEntry(RegistryBase):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    mappings: list[ProgramGroupMapping] = Field(..., min_length=1)


class ComparisonGroupRegistryEntry(RegistryBase):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    unitids: list[int] = Field(min_length=1)


class EligibilityCriterion(BaseModel):
    id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    comparator: Literal[">", ">=", "<", "<=", "==", "!="]
    threshold: float
    indicator_id: str = Field(min_length=1)
    notes: str | None = None


class EligibilityProfileRegistryEntry(RegistryBase):
    name: str = Field(min_length=1)
    funder: str = Field(min_length=1)
    program: str = Field(min_length=1)
    version_label: str = Field(min_length=1)
    effective_date: date
    criteria: list[EligibilityCriterion] = Field(default_factory=list)
    manual_override_allowed: bool = True
    provenance_notes: str | None = None


class IndicatorRegistryEntry(RegistryBase):
    name: str = Field(min_length=1)
    label: str = Field(min_length=1)
    description: str = Field(min_length=1)
    domain: str = Field(min_length=1)
    source: str = Field(min_length=1)
    source_topic: str = Field(min_length=1)
    source_variable: str = Field(min_length=1)
    allowed_years: list[int] = Field(min_length=1)
    allowed_filters: list[str] = Field(min_length=1)
    aggregation_modes: list[str] = Field(min_length=1)
    format: str = Field(min_length=1)
    unit: str = Field(min_length=1)
    default_chart: str = Field(min_length=1)
    notes: str | None = None
    provenance: str = Field(min_length=1)
    is_public_source: bool = True
    supports_comparison: bool = True
    supports_disaggregation: bool = False


class RegistryBundle(BaseModel):
    institution_unitid: int = 221847
    institution_name: str = "Tennessee Technological University"
    sources: list[SourceRegistryEntry]
    source_docs: list[SourceDocRegistryEntry]
    presets: list[PresetRegistryEntry]
    program_groups: list[ProgramGroupRegistryEntry]
    comparison_groups: list[ComparisonGroupRegistryEntry]
    eligibility_profiles: list[EligibilityProfileRegistryEntry]
    indicators: list[IndicatorRegistryEntry]
