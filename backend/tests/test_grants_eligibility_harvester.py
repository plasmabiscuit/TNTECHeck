from __future__ import annotations

from datetime import date, timedelta

from app.grants_eligibility_harvester import (
    _strip_html,
    discover_current_research_opportunities,
    download_instruction_text,
    extract_eligibility_sections,
    parse_opportunity_package_metadata,
)


def test_extract_eligibility_sections_from_instruction_text() -> None:
    text = """
I. FUNDING OPPORTUNITY DESCRIPTION
This notice supports translational research projects.

III. ELIGIBILITY INFORMATION
Eligible Applicants
Higher education institutions, including public and private nonprofit institutions, are eligible.
Foreign organizations are not eligible to apply.

IV. APPLICATION AND SUBMISSION INFORMATION
Submit all required forms before the stated due date.
"""

    sections = extract_eligibility_sections(text)

    assert sections
    assert any("eligible applicants" in section["text"].lower() for section in sections)
    assert any("foreign organizations are not eligible" in section["text"].lower() for section in sections)


def test_extract_eligibility_sections_does_not_match_ineligible_only() -> None:
    """Lines that only contain 'ineligible' (not standalone 'eligible') must not trigger a match."""
    text = """
I. OVERVIEW
This program does not support ineligible organizations.
Organizations that are ineligible include those with pending debarment actions or suspension notices.
No other restrictions apply to all applicants at this time and the process remains open.
"""
    sections = extract_eligibility_sections(text)
    assert not sections


def test_parse_opportunity_package_metadata_from_soap_payload() -> None:
    soap_payload = """
--uuid:abc123
Content-Type: application/xop+xml; charset=UTF-8; type="text/xml"

<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ns2:GetOpportunityListResponse xmlns:ns2="http://apply.grants.gov/services/ApplicantWebServices-V2.0" xmlns:ns5="http://apply.grants.gov/system/ApplicantCommonElements-V1.0" xmlns="http://apply.grants.gov/system/GrantsCommonElements-V1.0">
      <ns5:OpportunityDetails>
        <FundingOpportunityNumber>PAR-25-274</FundingOpportunityNumber>
        <FundingOpportunityTitle>Example Research Opportunity</FundingOpportunityTitle>
        <PackageID>PKG00288883</PackageID>
        <OfferingAgency>National Institutes of Health</OfferingAgency>
        <InstructionsURL>https://apply07.grants.gov/apply/opportunities/instructions/PKG00288883-instructions.pdf</InstructionsURL>
      </ns5:OpportunityDetails>
    </ns2:GetOpportunityListResponse>
  </soap:Body>
</soap:Envelope>
--uuid:abc123--
"""

    metadata = parse_opportunity_package_metadata(soap_payload)

    assert metadata.opportunity_number == "PAR-25-274"
    assert metadata.package_id == "PKG00288883"
    assert metadata.offering_agency == "National Institutes of Health"
    assert metadata.instructions_url.endswith("PKG00288883-instructions.pdf")


def test_parse_opportunity_package_metadata_alternate_soap_prefix() -> None:
    """SOAP envelope with a non-standard prefix (soapenv) must still be parsed."""
    soap_payload = """
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
  <soapenv:Body>
    <ns2:GetOpportunityListResponse xmlns:ns2="http://apply.grants.gov/services/ApplicantWebServices-V2.0" xmlns:ns5="http://apply.grants.gov/system/ApplicantCommonElements-V1.0" xmlns="http://apply.grants.gov/system/GrantsCommonElements-V1.0">
      <ns5:OpportunityDetails>
        <FundingOpportunityNumber>FOA-99-001</FundingOpportunityNumber>
        <FundingOpportunityTitle>Alt Prefix Test</FundingOpportunityTitle>
        <PackageID>PKG99001</PackageID>
        <OfferingAgency>NSF</OfferingAgency>
        <InstructionsURL>https://example.gov/instructions.pdf</InstructionsURL>
      </ns5:OpportunityDetails>
    </ns2:GetOpportunityListResponse>
  </soapenv:Body>
</soapenv:Envelope>
"""
    metadata = parse_opportunity_package_metadata(soap_payload)
    assert metadata.opportunity_number == "FOA-99-001"
    assert metadata.package_id == "PKG99001"


def test_strip_html_unescapes_entities() -> None:
    """_strip_html must HTML-unescape entities like &amp;, &nbsp;, &quot;."""
    html_input = "<p>Rock &amp; Roll &nbsp; &quot;the best&quot;</p>"
    result = _strip_html(html_input)
    assert "&amp;" not in result
    assert "&nbsp;" not in result
    assert "&quot;" not in result
    assert "Rock & Roll" in result
    assert '"the best"' in result


def test_download_instruction_text_detects_and_strips_html_by_content_type(monkeypatch) -> None:
    """download_instruction_text must strip HTML when Content-Type is text/html."""
    import io
    import urllib.request

    html_body = b"<html><body><p>Eligible applicants include universities &amp; colleges.</p></body></html>"

    class FakeResponse:
        headers = {"Content-Type": "text/html; charset=utf-8"}

        def read(self):
            return html_body

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **kw: FakeResponse())
    text = download_instruction_text("https://example.gov/page.html")
    assert "<" not in text
    assert "universities & colleges" in text


def test_discover_current_research_opportunities_paginates_and_filters(monkeypatch) -> None:
    """discover_current_research_opportunities must page through all results and filter correctly."""
    import app.grants_eligibility_harvester as mod

    tomorrow = (date.today() + timedelta(days=1)).strftime("%m/%d/%Y")
    yesterday = (date.today() - timedelta(days=1)).strftime("%m/%d/%Y")

    # Three total hits across two pages (page size forced to 2 by _page_size kwarg).
    all_hits = [
        # Page 1
        {"id": 1, "number": "A-1", "title": "Grant A", "oppStatus": "posted", "closeDate": tomorrow, "agencyCode": "NIH"},
        {"id": 2, "number": "A-2", "title": "Grant B", "oppStatus": "forecasted", "closeDate": tomorrow},
        # Page 2
        {"id": 3, "number": "A-3", "title": "Grant C", "oppStatus": "posted", "closeDate": yesterday},
        {"id": 4, "number": "A-4", "title": "Grant D", "oppStatus": "posted", "closeDate": None},
    ]
    calls: list[dict] = []

    def fake_post_json(url, payload):
        calls.append({"url": url, "payload": payload})
        if "search2" in url:
            start = payload.get("startRecordNum", 0)
            rows = payload.get("rows", 100)
            page = all_hits[start : start + rows]
            return {"data": {"hitCount": len(all_hits), "oppHits": page}}
        return {"data": {}}

    monkeypatch.setattr(mod, "_post_json", fake_post_json)

    results = discover_current_research_opportunities(_page_size=2)

    # A-1: valid posted + open → included
    # A-2: forecasted → excluded
    # A-3: posted but expired close date → excluded
    # A-4: posted, no close date → included
    assert len(results) == 2
    numbers = {r["number"] for r in results}
    assert numbers == {"A-1", "A-4"}

    # Two pages of search2 calls must have been made
    search_calls = [c for c in calls if "search2" in c["url"]]
    assert len(search_calls) == 2
    assert search_calls[0]["payload"]["startRecordNum"] == 0
    assert search_calls[1]["payload"]["startRecordNum"] == 2

    # oppStatuses filter must be sent on every page
    for sc in search_calls:
        assert sc["payload"].get("oppStatuses") == ["posted"]


def test_search_page_size_default() -> None:
    """_SEARCH_PAGE_SIZE must be the expected default so bulk harvests are efficient."""
    import app.grants_eligibility_harvester as mod

    assert mod._SEARCH_PAGE_SIZE == 100


def test_discover_current_research_opportunities_sends_eligibility_codes(monkeypatch) -> None:
    """Each eligibility code must trigger its own search2 request (OR semantics)."""
    import app.grants_eligibility_harvester as mod

    calls: list[dict] = []

    def fake_post_json(url, payload):
        calls.append({"url": url, "payload": payload})
        return {"data": {"hitCount": 0, "oppHits": []}}

    monkeypatch.setattr(mod, "_post_json", fake_post_json)

    codes = [mod.ELIGIBILITY_CODE_PUBLIC_IHE, mod.ELIGIBILITY_CODE_UNRESTRICTED]
    mod.discover_current_research_opportunities(eligibility_codes=codes)

    search_calls = [c for c in calls if "search2" in c["url"]]
    # One request per code — each carrying a single-element eligibilities list.
    assert len(search_calls) == len(codes)
    sent_codes = [c["payload"]["eligibilities"] for c in search_calls]
    assert [mod.ELIGIBILITY_CODE_PUBLIC_IHE] in sent_codes
    assert [mod.ELIGIBILITY_CODE_UNRESTRICTED] in sent_codes


def test_discover_current_research_opportunities_deduplicates_across_codes(monkeypatch) -> None:
    """An opportunity returned by two per-code searches must appear only once."""
    import app.grants_eligibility_harvester as mod
    from datetime import timedelta

    tomorrow = (date.today() + timedelta(days=1)).strftime("%m/%d/%Y")

    shared_hit = {"id": 1, "number": "X-1", "title": "G1", "oppStatus": "posted", "closeDate": tomorrow, "agencyCode": "NIH"}
    unique_hit = {"id": 2, "number": "X-2", "title": "G2", "oppStatus": "posted", "closeDate": None, "agencyCode": "NSF"}

    call_count = 0

    def fake_post_json(url, payload):
        nonlocal call_count
        call_count += 1
        code = (payload.get("eligibilities") or [None])[0]
        if code == mod.ELIGIBILITY_CODE_PUBLIC_IHE:
            return {"data": {"hitCount": 2, "oppHits": [shared_hit, unique_hit]}}
        # Second code also returns the shared hit
        return {"data": {"hitCount": 1, "oppHits": [shared_hit]}}

    monkeypatch.setattr(mod, "_post_json", fake_post_json)

    results = mod.discover_current_research_opportunities(
        eligibility_codes=[mod.ELIGIBILITY_CODE_PUBLIC_IHE, mod.ELIGIBILITY_CODE_STATE_GOVTS]
    )

    numbers = [r["number"] for r in results]
    assert numbers.count("X-1") == 1, "Shared hit must appear exactly once"
    assert "X-2" in numbers


def test_discover_current_research_opportunities_no_eligibility_filter_by_default(monkeypatch) -> None:
    """With no eligibility_codes, the 'eligibilities' key must NOT appear in the payload."""
    import app.grants_eligibility_harvester as mod

    calls: list[dict] = []

    def fake_post_json(url, payload):
        calls.append({"url": url, "payload": payload})
        return {"data": {"hitCount": 0, "oppHits": []}}

    monkeypatch.setattr(mod, "_post_json", fake_post_json)

    mod.discover_current_research_opportunities()

    assert calls
    assert "eligibilities" not in calls[0]["payload"]


def test_harvest_respects_request_delay(monkeypatch) -> None:
    """harvest_current_research_eligibility must sleep between per-opportunity calls."""
    import app.grants_eligibility_harvester as mod

    sleep_calls: list[float] = []
    monkeypatch.setattr(mod.time, "sleep", lambda s: sleep_calls.append(s))

    def fake_post_json(url, payload):
        if "search2" in url:
            return {
                "data": {
                    "hitCount": 2,
                    "oppHits": [
                        {"id": 1, "number": "X-1", "title": "G1", "oppStatus": "posted", "closeDate": None},
                        {"id": 2, "number": "X-2", "title": "G2", "oppStatus": "posted", "closeDate": None},
                    ],
                }
            }
        return {"data": {}}

    def fake_fetch_metadata(number):
        return mod.OpportunityPackageMetadata(
            opportunity_number=number,
            funding_opportunity_title="Test",
            package_id=None,
            offering_agency=None,
            instructions_url=None,
        )

    monkeypatch.setattr(mod, "_post_json", fake_post_json)
    monkeypatch.setattr(mod, "fetch_opportunity_package_metadata", fake_fetch_metadata)

    mod.harvest_current_research_eligibility(request_delay=0.25)

    # Two opportunities → one inter-opportunity sleep (before the second)
    assert len(sleep_calls) == 1
    assert sleep_calls[0] == 0.25


def test_harvest_no_delay_for_single_opportunity(monkeypatch) -> None:
    """With a single opportunity, no sleep call should be made."""
    import app.grants_eligibility_harvester as mod

    sleep_calls: list[float] = []
    monkeypatch.setattr(mod.time, "sleep", lambda s: sleep_calls.append(s))

    def fake_post_json(url, payload):
        if "search2" in url:
            return {
                "data": {
                    "hitCount": 1,
                    "oppHits": [
                        {"id": 1, "number": "X-1", "title": "G1", "oppStatus": "posted", "closeDate": None},
                    ],
                }
            }
        return {"data": {}}

    def fake_fetch_metadata(number):
        return mod.OpportunityPackageMetadata(
            opportunity_number=number,
            funding_opportunity_title="Test",
            package_id=None,
            offering_agency=None,
            instructions_url=None,
        )

    monkeypatch.setattr(mod, "_post_json", fake_post_json)
    monkeypatch.setattr(mod, "fetch_opportunity_package_metadata", fake_fetch_metadata)

    mod.harvest_current_research_eligibility(request_delay=1.0)

    assert sleep_calls == []


def test_harvest_selection_criteria_includes_eligibility_codes(monkeypatch) -> None:
    """When eligibility_codes are supplied they must appear in selection_criteria output."""
    import app.grants_eligibility_harvester as mod

    monkeypatch.setattr(mod, "_post_json", lambda url, payload: {"data": {"hitCount": 0, "oppHits": []}})

    codes = [mod.ELIGIBILITY_CODE_STATE_GOVTS, mod.ELIGIBILITY_CODE_PUBLIC_IHE]
    result = mod.harvest_current_research_eligibility(eligibility_codes=codes, request_delay=0)

    assert result["selection_criteria"]["eligibility_codes"] == codes


def test_harvest_selection_criteria_omits_eligibility_codes_when_none(monkeypatch) -> None:
    """When eligibility_codes is None, selection_criteria must NOT include the key."""
    import app.grants_eligibility_harvester as mod

    monkeypatch.setattr(mod, "_post_json", lambda url, payload: {"data": {"hitCount": 0, "oppHits": []}})

    result = mod.harvest_current_research_eligibility(request_delay=0)

    assert "eligibility_codes" not in result["selection_criteria"]


def test_default_harvest_eligibility_codes_contains_expected_codes() -> None:
    """DEFAULT_HARVEST_ELIGIBILITY_CODES must contain state govts, public IHE, and unrestricted."""
    import app.grants_eligibility_harvester as mod

    codes = set(mod.DEFAULT_HARVEST_ELIGIBILITY_CODES)
    assert mod.ELIGIBILITY_CODE_STATE_GOVTS in codes       # state governments
    assert mod.ELIGIBILITY_CODE_PUBLIC_IHE in codes        # public / state-controlled IHE
    assert mod.ELIGIBILITY_CODE_UNRESTRICTED in codes      # unrestricted
    # private IHE and non-IHE 501(c)(3) are intentionally excluded from defaults
    assert mod.ELIGIBILITY_CODE_PRIVATE_IHE not in codes
    assert mod.ELIGIBILITY_CODE_NONPROFITS_501C3 not in codes

