from __future__ import annotations

from app.grants_eligibility_harvester import extract_eligibility_sections, parse_opportunity_package_metadata


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
