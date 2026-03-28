# NSF Award Search API — Query and Field Notes

Source basis: official API page at `https://resources.research.gov/common/webapi/awardapisearch-v1.htm` (verified 2026-03-28).

## Request URL patterns

- Search: `GET https://api.nsf.gov/services/v1/awards.{format}?parameters`
- Single award: `GET https://api.nsf.gov/services/v1/awards/{id}.{format}`
- Project outcomes: `GET https://api.nsf.gov/services/v1/awards/{id}/projectoutcomes.{format}`

Supported output formats shown in docs/examples: XML, JSON, JSONP.

## Core request parameters used by TNTECheck

| Parameter | Purpose | Notes |
|---|---|---|
| `keyword` | free-text search | Supports boolean operators and wildcard patterns per Award Search help/docs. |
| `rpp` | results per page | Combine with `offset` for deterministic pagination. |
| `offset` | start record position | Typical first page starts at `0`. |
| `id` | NSF award identifier | Required for single-award and project outcomes calls. |
| `awardeeName` | institution/entity name search | Useful for TTU history queries; phrase quoting helps reduce false positives. |
| `awardeeStateCode` | state filter | Two-letter state code (e.g., `TN`). |
| `dateStart` / `dateEnd` | award date range | Docs specify `mm/dd/yyyy` format. |
| `startDateStart` / `startDateEnd` | award start date range | Docs specify `mm/dd/yyyy` format. |
| `expDateStart` / `expDateEnd` | award expiration date range | Docs specify `mm/dd/yyyy` format. |
| `piLastName` | PI filtering | Use for investigator-specific slicing where needed. |
| `pdPIName` | PD/PI name | Useful when reconciling PI fields in output. |
| `sortBy` | sort key | Docs include sort options and default behavior. |
| `printFields` | output field subset | API docs currently note this is no longer functional; do not rely on it. |

## Pagination/sorting implementation guidance

- Always pass explicit `rpp` and `offset`; use metadata in responses (`totalCount`, `offset`, `rpp`) to continue paging.
- Do not assume API default sorting for stable ETL. Pass `sortBy` where reproducibility is required.
- Because `printFields` is marked non-functional, downstream field trimming should happen in adapter normalization.

## Response normalization starters

Common API response fields visible in official examples and live samples include:

- identity and award fields: `id`, `awardTitle`, `awardAgencyCode`
- institution/location: `awardeeName`, `awardeeCity`, `awardeeStateCode`, `awardeeZipCode`
- personnel: `pdPIName`, `coPDPI`
- financial/timing: `fundsObligatedAmt`, `date`, `startDate`, `expDate`
- taxonomy/context: `fundProgramName`, `fundAgencyCode`, `cfdaNumber`

Adapter note: preserve raw field names in provenance payloads and map to TNTECheck-normalized names in a separate transform step.

## Boolean and text query behavior

Per official Boolean help page:

- Operators: `AND`, `OR`, `NOT`
- Operators are documented as case-sensitive and must be uppercase.
- Quoted phrases and wildcard patterns are documented in Award Search/API notes.

## Caveats to track

1. API docs still show `http://` examples; use `https://` in implementation.
2. `printFields` behavior is explicitly flagged as non-functional in current docs.
3. Date strings are documented as `mm/dd/yyyy`; validate and normalize adapter-side to avoid silent mismatches.
