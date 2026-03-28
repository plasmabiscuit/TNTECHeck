from ..models import AdapterCapabilities
from ._stub_base import StubSourceAdapter


class NIHReporterAdapter(StubSourceAdapter):
    def __init__(self) -> None:
        super().__init__(
            source_name="nih_reporter",
            capabilities=AdapterCapabilities(
                supports_institution_profile=False,
                supports_completions=False,
                supports_awards=True,
            ),
        )
