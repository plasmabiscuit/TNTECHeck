from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable

from .models import AdapterCapabilities, AdapterHealth, AdapterQuery, AdapterResult

Normalizer = Callable[[dict[str, Any]], dict[str, Any]]


class SourceAdapter(ABC):
    """Shared source adapter contract for all public data integrations."""

    source_name: str
    capabilities: AdapterCapabilities
    institution_identity_normalizer: Normalizer
    time_normalizer: Normalizer
    program_cip_normalizer: Normalizer
    funding_normalizer: Normalizer

    @abstractmethod
    def healthcheck(self) -> AdapterHealth:
        """Return adapter-local health state (without heavy remote calls in v1)."""

    @abstractmethod
    def fetch(self, query: AdapterQuery) -> AdapterResult:
        """Execute a source query and return normalized records."""
