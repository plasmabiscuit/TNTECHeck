from __future__ import annotations

from .base import SourceAdapter
from .sources import (
    CollegeScorecardAdapter,
    IPEDSManualImportAdapter,
    NIFADataGatewayAdapter,
    NIHReporterAdapter,
    NSFAwardSearchAdapter,
    UrbanAdapter,
)


def get_default_adapters() -> list[SourceAdapter]:
    """Return required v1 source adapters in deterministic order."""

    return [
        UrbanAdapter(),
        CollegeScorecardAdapter(),
        NIHReporterAdapter(),
        NSFAwardSearchAdapter(),
        NIFADataGatewayAdapter(),
        IPEDSManualImportAdapter(),
    ]
