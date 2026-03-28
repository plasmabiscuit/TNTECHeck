# NIFA Data Gateway Award/Project Field Mapping Notes

## Purpose

This document maps key Data Gateway fields into TNTECheck-friendly normalized concepts for the `nifa_data_gateway` adapter.

## Provenance

- Recent Awards public module metadata from `portal.nifa.usda.gov/lmd4/recent_awards` and its `get_data.js` payload.
- Projects public module metadata from `portal.nifa.usda.gov/lmd4/projects` page script.
- NIFA Data Gateway / LMD official descriptions from NIFA Data Gateway and LMD user-guide PDFs.
- Retrieval date for this draft mapping: March 28, 2026 (UTC).

## Mapping draft: Recent Awards

| Source field (as observed) | Suggested normalized field | Type | Notes |
|---|---|---|---|
| `Award Date` | `award_date` | date | Parse `MM/DD/YYYY`; preserve raw text for provenance. |
| `Grant Number` | `award_id` | string | Candidate primary award identifier in award listing context. |
| `Proposal Number` | `proposal_id` | string\|null | Can be `N/A` in observed samples. |
| `Grant Title` | `title` | string\|null | May be missing/`N/A` in some rows. |
| `State Name` | `state_name` | string | Uppercase state names observed. |
| `Grantee Name` | `recipient_name` | string | Institution/organization display name. |
| `Award Dollars` | `award_amount_usd` | decimal | Strip currency symbols/commas before numeric parse. |
| `Program Name` | `program_name` | string | Supports grant-program grouping. |
| `Program Area Name` | `program_area_name` | string | Secondary program categorization dimension. |
| `Public Flag` | `is_public_record` | boolean | Observed values represented as string booleans (`true`/`false`). |

## Mapping draft: Projects listing

| Source field (as observed in module config) | Suggested normalized field | Type | Notes |
|---|---|---|---|
| `Accession Number` | `project_accession_id` | string | Useful for linking to technical report flows. |
| `Type` | `project_type` | string | Keep raw source values; do not pre-collapse categories. |
| `Grantee Name` | `recipient_name` | string | Can align with award listing entity matching. |
| `Title` | `project_title` | string | Project display title. |
| `Keywords` | `keywords_raw` | string | Adapter may split to array downstream. |
| `Program Code` | `program_code` | string | Preserve as text (possible leading zeros). |
| `Program Code Name` | `program_code_name` | string | Human-readable label for program code. |
| `Program Area Code` | `program_area_code` | string | Preserve as text. |
| `Program Area Name` | `program_area_name` | string | Human-readable area label. |
| `Multistate Project Number` | `multistate_project_number` | string\|null | Not present on all records. |

## Normalization guidance

1. Preserve raw source row payload alongside normalized fields when possible.
2. Do not hardcode NIFA-program-specific business rules in field transforms.
3. Keep fiscal-year fields explicit (`appropriation_fiscal_year`, `award_fiscal_year`, `submission_fiscal_year`) when sourced from Awards/Budget cubes.
4. For missing text (`N/A`, blank), normalize to `null` but retain raw-value provenance.

## Cross-source comparison caveat

NIFA award/project classifications (program areas, KA/SOI/FOS dimensions, and funding categories) are source-specific taxonomies; do not force 1:1 joins with NSF/NIH program taxonomies at ingestion time.
