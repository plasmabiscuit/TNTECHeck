from ..models import AdapterCapabilities
from ._stub_base import StubSourceAdapter


class NSFAwardSearchAdapter(StubSourceAdapter):
    def __init__(self) -> None:
        super().__init__(
            source_name="nsf_award_search",
            capabilities=AdapterCapabilities(
                supports_institution_profile=False,
                supports_completions=False,
                supports_awards=True,
            ),
        )
