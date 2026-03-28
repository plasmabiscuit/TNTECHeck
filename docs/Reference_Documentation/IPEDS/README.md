# IPEDS Reference Pack for TNTECheck

This folder contains IPEDS reference artifacts used for semantic grounding and manual/fallback workflows.

## Files

- `Data_Dictionary.json` — structured dictionary export with table metadata and field-level definitions.
- `HumanGlossary.json` — glossary-style reference for human-readable terms and concepts.
- `IPEDS202425Tablesdoc.xlsx` — table documentation workbook for the 2024-25 cycle.

## Intended TNTECheck usage

- Validate meanings for normalized indicators when adapter output is ambiguous.
- Support fallback/manual-import workflows for data not available through API-first sources.
- Confirm table/field semantics before changing indicator definitions, comparisons, or report narratives.

## Required usage rule

Before implementing/debugging any IPEDS-backed feature:

1. Check the relevant table and field in `Data_Dictionary.json`.
2. Verify plain-language interpretation in `HumanGlossary.json`.
3. Use the workbook when table-level context is required.

## Gaps to fill

- Add a Markdown crosswalk of TNTECheck indicator IDs to IPEDS table/field references.
- Add manual-import mapping documentation for `ipeds_manual_import` adapter payloads.
- Add yearly refresh checklist (where to fetch updated files and how to validate changes).
