from ..models import AdapterCapabilities
from ._stub_base import StubSourceAdapter


class CollegeScorecardAdapter(StubSourceAdapter):
    def __init__(self) -> None:
        super().__init__(
            source_name="college_scorecard",
            capabilities=AdapterCapabilities(
                supports_institution_profile=True,
                supports_completions=False,
                supports_awards=False,
                supports_summary_endpoints=False,
            ),
        )
