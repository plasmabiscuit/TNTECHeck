from __future__ import annotations

import io
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from app.registry import BASE_DATA_DIR

SEARCH2_URL = "https://api.grants.gov/v1/api/search2"
FETCH_OPPORTUNITY_URL = "https://api.grants.gov/v1/api/fetchOpportunity"
SOAP_OPPORTUNITY_URL = "https://ws07.grants.gov/grantsws-applicant/services/v2/ApplicantWebServicesSoapPort"

_GRANTS_COMMON_NS = "http://apply.grants.gov/system/GrantsCommonElements-V1.0"
_APPLICANT_COMMON_NS = "http://apply.grants.gov/system/ApplicantCommonElements-V1.0"
_SERVICE_NS = "http://apply.grants.gov/services/ApplicantWebServices-V2.0"

ELIGIBILITY_TERMS = (
    "eligibility",
    "eligible",
    "eligible applicants",
    "who may apply",
    "applicant eligibility",
)
HEADING_PATTERN = re.compile(r"^(?:[A-Z][A-Z\s/&,-]{4,}|\d+(?:\.\d+)*\s+[A-Z].{0,120})$")


@dataclass
class OpportunityPackageMetadata:
    opportunity_number: str
    funding_opportunity_title: str
    package_id: str | None
    offering_agency: str | None
    instructions_url: str | None


def _post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "TNTECheck-EligibilityHarvester/0.1 (+https://github.com/)",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _to_iso_date(value: str | None) -> date | None:
    if not value:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    return None


def discover_current_research_opportunities(max_hits: int = 25) -> list[dict[str, Any]]:
    payload = {"rows": max_hits}
    response = _post_json(SEARCH2_URL, payload)
    hits = response.get("data", {}).get("oppHits", [])
    today = date.today()
    filtered: list[dict[str, Any]] = []

    for hit in hits:
        if hit.get("oppStatus") != "posted":
            continue

        close_date = _to_iso_date(hit.get("closeDate"))
        if close_date and close_date < today:
            continue

        detail = _post_json(FETCH_OPPORTUNITY_URL, {"opportunityId": hit.get("id")}).get("data", {})
        synopsis_desc = (detail.get("synopsis") or {}).get("synopsisDesc") or ""
        haystack = f"{hit.get('title', '')}\n{synopsis_desc}"
        if not re.search(r"\bresearch\b", haystack, flags=re.IGNORECASE):
            continue

        filtered.append(
            {
                "id": hit.get("id"),
                "number": detail.get("opportunityNumber") or hit.get("number"),
                "title": detail.get("opportunityTitle") or hit.get("title"),
                "agency": hit.get("agency") or detail.get("owningAgencyCode"),
                "close_date": hit.get("closeDate"),
                "synopsis_desc": synopsis_desc,
                "funding_desc_link_url": (detail.get("synopsis") or {}).get("fundingDescLinkUrl"),
            }
        )

    return filtered


def _build_get_opportunity_list_envelope(opportunity_number: str) -> bytes:
    xml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:tns=\"{_SERVICE_NS}\" xmlns:app=\"{_APPLICANT_COMMON_NS}\" xmlns:gr=\"{_GRANTS_COMMON_NS}\">
  <soapenv:Header/>
  <soapenv:Body>
    <tns:GetOpportunityListRequest>
      <app:OpportunityFilter>
        <gr:FundingOpportunityNumber>{opportunity_number}</gr:FundingOpportunityNumber>
      </app:OpportunityFilter>
    </tns:GetOpportunityListRequest>
  </soapenv:Body>
</soapenv:Envelope>"""
    return xml.encode("utf-8")


def _extract_soap_xml(payload: str) -> str:
    # Match any SOAP Envelope regardless of namespace prefix, e.g. <soap:Envelope>,
    # <soapenv:Envelope>, <SOAP-ENV:Envelope>, etc.
    match = re.search(
        r"<(?P<prefix>[^:\s>]+):Envelope\b.*?</(?P=prefix):Envelope>",
        payload,
        flags=re.DOTALL,
    )
    if not match:
        return payload
    return match.group(0)


def parse_opportunity_package_metadata(soap_payload: str) -> OpportunityPackageMetadata:
    xml = _extract_soap_xml(soap_payload)
    root = ET.fromstring(xml)

    details = root.find(f".//{{{_APPLICANT_COMMON_NS}}}OpportunityDetails")
    if details is None:
        raise ValueError("SOAP payload does not contain OpportunityDetails.")

    number = details.findtext(f"{{{_GRANTS_COMMON_NS}}}FundingOpportunityNumber", "")
    title = details.findtext(f"{{{_GRANTS_COMMON_NS}}}FundingOpportunityTitle", "")
    package_id = details.findtext(f"{{{_GRANTS_COMMON_NS}}}PackageID")
    offering_agency = details.findtext(f"{{{_GRANTS_COMMON_NS}}}OfferingAgency")
    instructions_url = details.findtext(f"{{{_GRANTS_COMMON_NS}}}InstructionsURL")

    return OpportunityPackageMetadata(
        opportunity_number=number,
        funding_opportunity_title=title,
        package_id=package_id,
        offering_agency=offering_agency,
        instructions_url=instructions_url,
    )


def fetch_opportunity_package_metadata(opportunity_number: str) -> OpportunityPackageMetadata:
    request = urllib.request.Request(
        SOAP_OPPORTUNITY_URL,
        data=_build_get_opportunity_list_envelope(opportunity_number),
        headers={
            "Content-Type": "text/xml; charset=utf-8",
            "User-Agent": "TNTECheck-EligibilityHarvester/0.1 (+https://github.com/)",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read().decode("utf-8", errors="ignore")
    return parse_opportunity_package_metadata(payload)


def _pdf_to_text(pdf_bytes: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(pdf_bytes))
    chunks = [(page.extract_text() or "") for page in reader.pages]
    return "\n".join(chunks)


def download_instruction_text(instructions_url: str) -> str:
    request = urllib.request.Request(
        instructions_url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; TNTECheck/0.1; +https://github.com/)"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        content_type = response.headers.get("Content-Type", "").lower()
        payload = response.read()

    if "pdf" in content_type or instructions_url.lower().endswith(".pdf"):
        return _pdf_to_text(payload)

    return payload.decode("utf-8", errors="ignore")


def _strip_html(value: str) -> str:
    without_scripts = re.sub(r"<script.*?>.*?</script>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    without_styles = re.sub(r"<style.*?>.*?</style>", " ", without_scripts, flags=re.IGNORECASE | re.DOTALL)
    normalized_breaks = re.sub(
        r"</?(?:p|div|h1|h2|h3|h4|h5|h6|li|br|tr|section|article|table)[^>]*>",
        "\n",
        without_styles,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"<[^>]+>", " ", normalized_breaks)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def extract_eligibility_sections(instruction_text: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in instruction_text.splitlines()]
    nonempty = [line for line in lines if line]
    sections: list[dict[str, str]] = []

    for idx, line in enumerate(nonempty):
        normalized = line.lower()
        if not any(term in normalized for term in ELIGIBILITY_TERMS):
            continue

        heading = line
        if idx > 0 and HEADING_PATTERN.match(nonempty[idx - 1]):
            heading = nonempty[idx - 1]

        block = [line]
        for tail in nonempty[idx + 1 :]:
            if HEADING_PATTERN.match(tail) and not any(term in tail.lower() for term in ELIGIBILITY_TERMS):
                break
            block.append(tail)
            if len(" ".join(block)) > 2400:
                break

        section_text = "\n".join(block).strip()
        if len(section_text) < 80:
            continue

        sections.append({"heading": heading, "text": section_text})

    deduped: list[dict[str, str]] = []
    seen = set()
    for section in sections:
        fingerprint = re.sub(r"\s+", " ", section["text"].lower())
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        deduped.append(section)

    return deduped


def harvest_current_research_eligibility(max_opportunities: int = 10) -> dict[str, Any]:
    opportunities = discover_current_research_opportunities(max_hits=25)[:max_opportunities]

    harvested: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for opportunity in opportunities:
        number = opportunity.get("number")
        if not number:
            continue
        try:
            package = fetch_opportunity_package_metadata(number)
            if not package.instructions_url:
                failures.append({"opportunity_number": number, "reason": "missing_instructions_url"})
                continue

            instruction_text = download_instruction_text(package.instructions_url)
            extracted = extract_eligibility_sections(instruction_text)
            text_source = "instructions_url"

            if not extracted and opportunity.get("funding_desc_link_url"):
                link_text = download_instruction_text(opportunity["funding_desc_link_url"])
                extracted = extract_eligibility_sections(_strip_html(link_text))
                if extracted:
                    text_source = "funding_description_link"

            harvested.append(
                {
                    "opportunity_number": package.opportunity_number,
                    "opportunity_title": package.funding_opportunity_title or opportunity.get("title"),
                    "funder": package.offering_agency or opportunity.get("agency"),
                    "package_id": package.package_id,
                    "instructions_url": package.instructions_url,
                    "eligibility_sections": extracted,
                    "eligibility_section_count": len(extracted),
                    "text_source": text_source,
                }
            )
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError, ET.ParseError, RuntimeError) as exc:
            failures.append({"opportunity_number": number, "reason": str(exc)[:240]})

    return {
        "generated_at_utc": datetime.now(tz=UTC).isoformat(),
        "source": "grants.gov",
        "selection_criteria": {
            "opp_status": "posted",
            "current_open_or_no_close_date": True,
            "research_keyword_in_title_or_synopsis": True,
        },
        "records": harvested,
        "failures": failures,
    }


def write_harvest_output(payload: dict[str, Any], destination: Path | None = None) -> Path:
    output = destination or BASE_DATA_DIR / "grants_gov_instruction_eligibility_extracts.json"
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output


def main() -> None:
    payload = harvest_current_research_eligibility()
    output = write_harvest_output(payload)
    print(f"Wrote {len(payload['records'])} records to {output}")
    if payload["failures"]:
        print(f"Encountered {len(payload['failures'])} failures during harvesting")


if __name__ == "__main__":
    main()
