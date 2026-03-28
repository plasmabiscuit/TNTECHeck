from ..models import AdapterCapabilities
from ._stub_base import StubSourceAdapter


class IPEDSManualImportAdapter(StubSourceAdapter):
    def __init__(self) -> None:
        super().__init__(
            source_name="ipeds_manual_import",
            capabilities=AdapterCapabilities(
                supports_institution_profile=True,
                supports_completions=True,
                supports_awards=False,
                supports_manual_import=True,
                supports_smoke_query=False,
            ),
        )
