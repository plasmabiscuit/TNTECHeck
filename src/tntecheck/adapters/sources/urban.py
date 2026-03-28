from ..models import AdapterCapabilities
from ._stub_base import StubSourceAdapter


class UrbanAdapter(StubSourceAdapter):
    def __init__(self) -> None:
        super().__init__(
            source_name="urban",
            capabilities=AdapterCapabilities(
                supports_institution_profile=True,
                supports_completions=True,
                supports_awards=False,
                supports_summary_endpoints=True,
            ),
        )
