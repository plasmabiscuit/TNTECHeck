from __future__ import annotations

from app.grants_eligibility_harvester import (
    _strip_html,
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
