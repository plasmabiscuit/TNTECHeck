"""Source adapter contracts and implementations for TNTECheck."""

from .base import SourceAdapter
from .models import (
    AdapterCapabilities,
    AdapterHealth,
    AdapterQuery,
    AdapterResult,
    SourceRecord,
)
from .registry import get_default_adapters

__all__ = [
    "AdapterCapabilities",
    "AdapterHealth",
    "AdapterQuery",
    "AdapterResult",
    "SourceAdapter",
    "SourceRecord",
    "get_default_adapters",
]
