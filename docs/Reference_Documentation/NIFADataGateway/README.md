# USDA NIFA Data Gateway Reference Pack

This folder is the source pack for the `nifa_data_gateway` adapter and related indicator/report work.

## Scope

This pack documents **official NIFA-managed Data Gateway surfaces** that are relevant to TNTECheck award and project reporting:

- NIFA Data Gateway landing page and module descriptions.
- NIFA Data Gateway Resource Page and official user highlight PDFs.
- NIFA Enterprise Search / LMD public pages and public data endpoints discovered from NIFA portal page source.

## Required pre-dev checks (adapter/report work)

Before implementing or debugging source-backed behavior:

1. Confirm module semantics on the official Data Gateway page (`recent_awards`, Congressional, KA/SOI/FOS, trends).
2. Validate filters and field names from this folder's inventory docs.
3. Record provenance (source URL + retrieval date) in adapter notes/tests where source assumptions are used.
4. Treat eligibility/compliance outcomes as downstream logic; this source pack documents data retrieval only.

## Files in this pack

- `README.md` — landing page and usage protocol.
- `NIFA_Endpoint_Filter_Inventory.md` — endpoint inventory, filter model, and query patterns.
- `NIFA_Field_Mapping_Notes.md` — award/project field mapping notes for TNTECheck normalization.
- `NIFA_Status_FY_Handling.md` — fiscal-year and status handling behavior from official docs + observed payloads.

## Official documentation used (retrieved March 28, 2026 UTC)

1. NIFA Data Gateway page: https://www.nifa.usda.gov/data/data-gateway
2. NIFA Data Gateway Resource Page: https://www.nifa.usda.gov/data/data-gateway/data-gateway-resource-page
3. Data Gateway Fact Sheet (PDF): https://www.nifa.usda.gov/sites/default/files/resource/Data%20Gateway%20Fact%20Sheet.pdf
4. Data Gateway Advanced Search Highlights (PDF): https://www.nifa.usda.gov/sites/default/files/resource/Advanced%20Search%20Highlights.pdf
5. Basic Navigation in LMD User Guide (PDF): https://portal.nifa.usda.gov/web/documents/Basic_Navigation_in_LMD_User_Guide_Start_Here.pdf
6. Public NIFA portal pages used for endpoint inspection:
   - https://portal.nifa.usda.gov/lmd4/recent_awards
   - https://portal.nifa.usda.gov/lmd4/projects

## Known open item

The Advanced Search Highlights PDF references an **"Advanced Search Data Element and Values Key"** on the resource page. That artifact was not discoverable through current public indexing/crawl responses and should be added here once directly obtained.
