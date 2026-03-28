from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

TTU_UNITID = "221847"
TTU_NAME = "Tennessee Technological University"


@dataclass(frozen=True)
class AdapterCapabilities:
    """Declares what an adapter can currently support."""

    supports_institution_profile: bool
    supports_completions: bool
    supports_awards: bool
    supports_manual_import: bool = False
    supports_summary_endpoints: bool = False
    supports_smoke_query: bool = True


@dataclass(frozen=True)
class AdapterHealth:
    """Healthcheck status for a source adapter."""

    ok: bool
    source: str
    checked_at_utc: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    message: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AdapterQuery:
    """Normalized request payload passed from service-layer to adapters."""

    metric: str
    institution_id: str = TTU_UNITID
    start_year: int | None = None
    end_year: int | None = None
    filters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SourceRecord:
    """A normalized record emitted by a source adapter."""

    source: str
    indicator: str
    value: Any
    institution_id: str = TTU_UNITID
    institution_name: str = TTU_NAME
    year: int | None = None
    cip_code: str | None = None
    sponsor: str | None = None
    unit: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AdapterResult:
    """Uniform result envelope for adapter queries."""

    source: str
    records: list[SourceRecord] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    provenance: dict[str, Any] = field(default_factory=dict)
