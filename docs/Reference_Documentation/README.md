# TNTECheck Data Source Documentation Index

This index is the **entry point** for all source-specific implementation and debugging work.

## Required workflow for development/debugging

For any feature or bug that touches a data source adapter, registry entry, indicator mapping, or report logic:

1. Open this index first.
2. Open the source folder's `README.md` (or equivalent lead document) before writing code.
3. Confirm field names, constraints, and caveats from source docs.
4. Record provenance in code comments, tests, and/or report metadata where practical.

> If source docs and implementation disagree, update the docs corpus and implementation together.

## Source coverage matrix

| Source | Adapter / Registry ID(s) | Current doc status | Primary local docs | Notable gaps to add next |
|---|---|---|---|---|
| Urban Institute Education Data API | `urban_ed_api`, `urban` adapter | **Strong** | `UrbanInstitute/Urban_Education_API_README.md`; `UrbanInstitute/Urban_Colleges_API_Overview.md`; `UrbanInstitute/Urban_Colleges_Endpoint_Inventory.md`; `UrbanInstitute/Urban_Summary_Endpoints.md`; `UrbanInstitute/Urban_Client_Packages_and_Usage.md`; `UrbanInstitute/Urban_TNTECHeck_Implementation_Guide.md` | Parameter cookbook for top TNTECheck queries; error/timeout behavior notes |
| NCES / IPEDS | `nces_ipeds`, `ipeds_manual_import` adapter | **Moderate** | `IPEDS/README.md`; `IPEDS/Data_Dictionary.json`; `IPEDS/HumanGlossary.json`; `IPEDS/IPEDS202425Tablesdoc.xlsx` | Adapter-facing manual-import mapping guide; yearly refresh SOP |
| College Scorecard | `college_scorecard` adapter | **Strong** | `CollegeScorecard/README.md`; `CollegeScorecard/CollegeScorecard_Institution_Core.md`; `CollegeScorecard/CollegeScorecard_Institution_Outcomes.md`; `CollegeScorecard/CollegeScorecard_FieldOfStudy.md`; `CollegeScorecard/CollegeScorecard_Cohort_Coverage.md` | Crosswalk from Scorecard fields to indicator registry IDs |
| NIH RePORTER | `nih_reporter` adapter | **Strong** | `NIHRePORTER/RePORTER_Project_API_README.md`; `NIHRePORTER/RePORTER_Project_API_Query_Map.md`; `NIHRePORTER/RePORTER_Project_API_Field_Catalog.md`; `NIHRePORTER/RePORTER_Project_API_Admin_IC_Codes.md`; `NIHRePORTER/RePORTER_Project_API_Spending_Categories_FY2024.md` | TTU organization-matching strategy note; pagination/rate-limit handling note |
| NSF Award Search | `nsf_award_search` adapter | **Moderate** | `NSFAwardSearch/README.md`; `NSFAwardSearch/NSF_Award_Search_Official_Sources.md`; `NSFAwardSearch/NSF_Award_Search_API_Query_and_Field_Notes.md`; `NSFAwardSearch/NSF_Award_Search_Query_Templates.md`; `NSFAwardSearch/NSF_Open_GitHub_Repos_Implementation_Notes.md` | Add adapter-facing response normalization test matrix and refresh SOP |
| USDA/NIFA Data Gateway | `nifa_data_gateway` adapter | **Moderate** | `NIFADataGateway/README.md`; `NIFADataGateway/NIFA_Endpoint_Filter_Inventory.md`; `NIFADataGateway/NIFA_Field_Mapping_Notes.md`; `NIFADataGateway/NIFA_Status_FY_Handling.md` | Add adapter implementation notes and refresh SOP; add Advanced Search Data Element/Values Key artifact once obtained |
| Grants.gov (opportunity/eligibility support) | eligibility/reporting support | **Strong** | `grantsdotgov/README.md`; `grantsdotgov/GrantsGov_API_README.md`; `grantsdotgov/GrantsGov_REST_Opportunity_APIs.md`; `grantsdotgov/GrantsGov_S2S_Opportunity_and_Package_Services.md`; `grantsdotgov/GrantsGov_Opportunity_Schemas.md`; `grantsdotgov/GrantsGov_Common_Types.md`; `grantsdotgov/GrantsGov_Eligibility_Extraction_Notes.md` | Mapping guide from opportunity fields to editable eligibility profile schema |

## Current corpus organization standard

- One folder per source under `docs/Reference_Documentation/<SourceName>/`
- Each source folder should contain:
  - a `README.md` landing page
  - field catalogs and query maps
  - implementation notes (adapter-specific decisions)
  - known limitations/risk notes
- JSON/XLSX raw references are allowed, but should be accompanied by a Markdown guide explaining how to use them.

## Documentation debt backlog

See `docs/Reference_Documentation/DOCUMENTATION_GAPS.md` for prioritized additions.


## Shared/non-source-specific docs

- `docs/meta-endpoints.md` — backend metadata endpoint behavior used by frontend metadata loading and adapters.
