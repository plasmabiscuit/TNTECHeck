from __future__ import annotations

from dataclasses import dataclass

from ..base import SourceAdapter
from ..models import AdapterCapabilities, AdapterHealth, AdapterQuery, AdapterResult
from ..normalization import (
    normalize_funding,
    normalize_institution_identity,
    normalize_program_cip,
    normalize_time,
)


@dataclass
class StubSourceAdapter(SourceAdapter):
    """Shared behavior for non-networked adapter stubs."""

    source_name: str
    capabilities: AdapterCapabilities

    institution_identity_normalizer = staticmethod(normalize_institution_identity)
    time_normalizer = staticmethod(normalize_time)
    program_cip_normalizer = staticmethod(normalize_program_cip)
    funding_normalizer = staticmethod(normalize_funding)

    def healthcheck(self) -> AdapterHealth:
        return AdapterHealth(
            ok=True,
            source=self.source_name,
            message="adapter stub ready",
            details={
                "mode": "stub",
                "network_calls": "disabled",
                "supports_smoke_query": self.capabilities.supports_smoke_query,
            },
        )

    def fetch(self, query: AdapterQuery) -> AdapterResult:
        return AdapterResult(
            source=self.source_name,
            records=[],
            warnings=[
                (
                    f"{self.source_name} adapter is currently a stub; "
                    "remote calls are intentionally not implemented in v1."
                )
            ],
            provenance={
                "query": {
                    "metric": query.metric,
                    "institution_id": query.institution_id,
                    "start_year": query.start_year,
                    "end_year": query.end_year,
                    "filters": query.filters,
                },
                "stub": True,
            },
        )
