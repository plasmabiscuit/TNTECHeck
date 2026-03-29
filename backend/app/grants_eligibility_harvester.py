from __future__ import annotations

import argparse
import html
import io
import json
import re
import time
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

_ELIGIBILITY_TERMS_RAW = (
    "eligibility",
    "eligible",
    "eligible applicants",
    "who may apply",
    "applicant eligibility",
)
# Precompiled word-boundary patterns so "ineligible" / "noneligible" are not matched.
_ELIGIBILITY_PATTERNS = tuple(
    re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
    for term in _ELIGIBILITY_TERMS_RAW
)
HEADING_PATTERN = re.compile(r"^(?:[A-Z][A-Z\s/&,-]{4,}|\d+(?:\.\d+)*\s+[A-Z].{0,120})$")

_SEARCH_PAGE_SIZE = 100  # rows per search2 request — Grants.gov supports up to 1000

# ---------------------------------------------------------------------------
# Grants.gov search2 applicant-type eligibility codes
# (two-digit zero-padded strings matching the grants.gov API vocabulary)
# ---------------------------------------------------------------------------
ELIGIBILITY_CODE_STATE_GOVTS = "00"               # State governments
ELIGIBILITY_CODE_PUBLIC_IHE = "06"                # Public / State-controlled Institutions of Higher Education
ELIGIBILITY_CODE_NONPROFITS_501C3 = "09"          # Nonprofits with 501(c)(3) IRS status (non-IHE)
ELIGIBILITY_CODE_PRIVATE_IHE = "10"               # Private Institutions of Higher Education
ELIGIBILITY_CODE_UNRESTRICTED = "99"              # Unrestricted (open to any entity type)

# Default codes used by the harvest script:
# • Higher Education (public/state-controlled only)
# • State governments
# • Unrestricted opportunities
DEFAULT_HARVEST_ELIGIBILITY_CODES: tuple[str, ...] = (
    ELIGIBILITY_CODE_STATE_GOVTS,
    ELIGIBILITY_CODE_PUBLIC_IHE,
    ELIGIBILITY_CODE_UNRESTRICTED,
)

# Default inter-request delay (seconds) applied between per-opportunity calls
# inside the harvest loop to respect grants.gov rate limits.
DEFAULT_REQUEST_DELAY = 0.5


def _encode_search2_multi(value: str | list[str] | tuple[str, ...]) -> str:
    """Encode a search2 multi-value field as a pipe-delimited string."""
    if isinstance(value, str):
        return value
    return "|".join(v for v in value if v)


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
            "User-Agent": "TNTECheck-EligibilityHarvester/0.1 (+https://github.com/plasmabiscuit/TNTECheck)",
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


def _page_opportunities(
    extra_payload: dict[str, Any],
    today: date,
    _page_size: int,
) -> list[dict[str, Any]]:
    """Fetch all pages of a single search2 query and return filtered hits."""
    hits_out: list[dict[str, Any]] = []
    start = 0

    while True:
        payload: dict[str, Any] = {
            "rows": _page_size,
            "startRecordNum": start,
            "oppStatuses": _encode_search2_multi(["posted"]),
            **extra_payload,
        }
        data = _post_json(SEARCH2_URL, payload).get("data", {})
        hits = data.get("oppHits", [])
        hit_count = int(data.get("hitCount") or 0)

        for hit in hits:
            if hit.get("oppStatus") != "posted":
                continue
            close_date = _to_iso_date(hit.get("closeDate"))
            if close_date and close_date < today:
                continue
            hits_out.append(
                {
                    "id": hit.get("id"),
                    "number": hit.get("number"),
                    "title": hit.get("title"),
                    "agency": hit.get("agencyCode") or hit.get("agency"),
                    "close_date": hit.get("closeDate"),
                }
            )

        start += len(hits)
        if not hits or start >= hit_count:
            break

    return hits_out


def discover_current_research_opportunities(
    *,
    eligibility_codes: tuple[str, ...] | list[str] | None = None,
    _page_size: int = _SEARCH_PAGE_SIZE,
) -> list[dict[str, Any]]:
    """Page through currently-posted open opportunities via search2.

    When *eligibility_codes* is provided, **one search is issued per code** and
    the results are merged (OR semantics: an opportunity is included if it
    matches *any* of the listed applicant-type codes).  Passing all codes in a
    single request would apply AND semantics on the grants.gov side, returning
    only the rare opportunities that explicitly list every code.

    Grants.gov uses zero-padded two-digit strings (e.g. ``"06"`` for public
    IHEs, ``"99"`` for unrestricted).  See
    :data:`DEFAULT_HARVEST_ELIGIBILITY_CODES` for the recommended set.

    ``fetchOpportunity`` is intentionally skipped here to avoid an O(N)
    per-hit REST call during bulk discovery; the harvest loop performs that
    call lazily only when the funding-description-link fallback is needed.
    """
    today = date.today()

    if not eligibility_codes:
        return _page_opportunities({}, today, _page_size)

    # Issue one search per code and union results — guarantees OR semantics.
    seen_ids: set[int | str] = set()
    all_hits: list[dict[str, Any]] = []
    for code in eligibility_codes:
        for hit in _page_opportunities({"eligibilities": _encode_search2_multi([code])}, today, _page_size):
            key = hit["id"] if hit["id"] is not None else hit["number"]
            if key in seen_ids:
                continue
            seen_ids.add(key)
            all_hits.append(hit)

    return all_hits


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
            "User-Agent": "TNTECheck-EligibilityHarvester/0.1 (+https://github.com/plasmabiscuit/TNTECheck)",
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
        headers={"User-Agent": "Mozilla/5.0 (compatible; TNTECheck/0.1; +https://github.com/plasmabiscuit/TNTECheck)"},
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        content_type = response.headers.get("Content-Type", "").lower()
        payload = response.read()

    if "pdf" in content_type or instructions_url.lower().endswith(".pdf"):
        return _pdf_to_text(payload)

    decoded = payload.decode("utf-8", errors="ignore")
    if "html" in content_type or re.search(r"<html[\s>]", decoded, re.IGNORECASE):
        return _strip_html(decoded)

    return decoded


def _strip_html(value: str) -> str:
    without_scripts = re.sub(r"<script.*?>.*?</script>", " ", value, flags=re.IGNORECASE | re.DOTALL)
    without_styles = re.sub(r"<style.*?>.*?</style>", " ", without_scripts, flags=re.IGNORECASE | re.DOTALL)
    normalized_breaks = re.sub(
        r"</?(?:p|div|h1|h2|h3|h4|h5|h6|li|br|tr|section|article|table)[^>]*>",
        "\n",
        without_styles,
        flags=re.IGNORECASE,
    )
    html_stripped = re.sub(r"<[^>]+>", " ", normalized_breaks)
    unescaped = html.unescape(html_stripped)
    lines = [re.sub(r"\s+", " ", line).strip() for line in unescaped.splitlines()]
    return "\n".join(line for line in lines if line)


def extract_eligibility_sections(instruction_text: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in instruction_text.splitlines()]
    nonempty = [line for line in lines if line]
    sections: list[dict[str, str]] = []

    for idx, line in enumerate(nonempty):
        if not any(pat.search(line) for pat in _ELIGIBILITY_PATTERNS):
            continue

        heading = line
        if idx > 0 and HEADING_PATTERN.match(nonempty[idx - 1]):
            heading = nonempty[idx - 1]

        block = [line]
        for tail in nonempty[idx + 1 :]:
            if HEADING_PATTERN.match(tail) and not any(pat.search(tail) for pat in _ELIGIBILITY_PATTERNS):
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


def harvest_current_research_eligibility(
    max_opportunities: int | None = None,
    eligibility_codes: tuple[str, ...] | list[str] | None = None,
    request_delay: float = DEFAULT_REQUEST_DELAY,
) -> dict[str, Any]:
    """Harvest eligibility information for currently-posted opportunities.

    Parameters
    ----------
    max_opportunities:
        If provided, only the first *max_opportunities* discovered results are
        processed.  Useful for smoke-testing or dry-run invocations.
    eligibility_codes:
        Applicant-type filter forwarded to :func:`discover_current_research_opportunities`.
        Pass :data:`DEFAULT_HARVEST_ELIGIBILITY_CODES` (or any subset) to
        restrict the harvest to opportunities relevant to higher-education,
        state-government, and unrestricted applicants.
        ``None`` (default) collects all currently-posted opportunities.
    request_delay:
        Seconds to sleep between successive per-opportunity HTTP calls (SOAP
        metadata fetch + instruction download) so the harvester respects
        grants.gov rate limits.  Defaults to :data:`DEFAULT_REQUEST_DELAY`.
    """
    opportunities = discover_current_research_opportunities(eligibility_codes=eligibility_codes)
    if max_opportunities is not None:
        opportunities = opportunities[:max_opportunities]

    harvested: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for idx, opportunity in enumerate(opportunities):
        number = opportunity.get("number")
        if not number:
            continue
        # Rate-limit: pause before each opportunity (skip delay before the first).
        if idx > 0 and request_delay > 0:
            time.sleep(request_delay)
        try:
            package = fetch_opportunity_package_metadata(number)
            if not package.instructions_url:
                failures.append({"opportunity_number": number, "reason": "missing_instructions_url"})
                continue

            instruction_text = download_instruction_text(package.instructions_url)
            extracted = extract_eligibility_sections(instruction_text)
            text_source = "instructions_url"

            if not extracted:
                # Lazy-fetch the REST detail only when the instructions yielded nothing,
                # to get fundingDescLinkUrl without adding a per-hit call to discovery.
                try:
                    detail = _post_json(
                        FETCH_OPPORTUNITY_URL, {"opportunityId": opportunity["id"]}
                    ).get("data", {})
                    funding_link = (detail.get("synopsis") or {}).get("fundingDescLinkUrl")
                except (urllib.error.HTTPError, urllib.error.URLError, ValueError):
                    funding_link = None
                if funding_link:
                    link_text = download_instruction_text(funding_link)
                    extracted = extract_eligibility_sections(link_text)
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

    selection_criteria: dict[str, Any] = {
        "opp_status": "posted",
        "current_open_or_no_close_date": True,
    }
    if eligibility_codes is not None:
        selection_criteria["eligibility_codes"] = list(eligibility_codes)

    return {
        "generated_at_utc": datetime.now(tz=UTC).isoformat(),
        "source": "grants.gov",
        "selection_criteria": selection_criteria,
        "records": harvested,
        "failures": failures,
    }


def write_harvest_output(payload: dict[str, Any], destination: Path | None = None) -> Path:
    """Persist *payload* to *destination* as JSON.

    The run-specific ``generated_at_utc`` key is stripped from the written file
    to keep committed-artifact diffs stable across re-runs.  The key remains
    present in the in-memory *payload* dict returned by
    :func:`harvest_current_research_eligibility`.
    """
    output = destination or BASE_DATA_DIR / "grants_gov_instruction_eligibility_extracts.json"
    # Omit the run-specific timestamp from the committed artifact to keep diffs clean.
    persisted = {k: v for k, v in payload.items() if k != "generated_at_utc"}
    output.write_text(json.dumps(persisted, indent=2), encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Harvest grants.gov eligibility data for currently-posted opportunities.",
    )
    parser.add_argument(
        "--max-opportunities",
        type=int,
        default=None,
        metavar="N",
        help="Process at most N opportunities (useful for smoke-testing).",
    )
    args = parser.parse_args()

    payload = harvest_current_research_eligibility(
        max_opportunities=args.max_opportunities,
        eligibility_codes=DEFAULT_HARVEST_ELIGIBILITY_CODES,
        request_delay=DEFAULT_REQUEST_DELAY,
    )
    output = write_harvest_output(payload)
    print(f"Wrote {len(payload['records'])} records to {output}")
    if payload["failures"]:
        print(f"Encountered {len(payload['failures'])} failure(s) during harvesting:")
        for f in payload["failures"]:
            print(f"  {f['opportunity_number']}: {f['reason']}")


if __name__ == "__main__":
    main()
