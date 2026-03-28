# Grants.gov Reference Pack Index

This folder documents Grants.gov opportunity and eligibility-support surfaces used by TNTECheck.

## Files and purpose

- `GrantsGov_API_README.md` — scope and platform-level orientation.
- `GrantsGov_REST_Opportunity_APIs.md` — REST opportunity search/detail endpoints.
- `GrantsGov_S2S_Opportunity_and_Package_Services.md` — SOAP S2S package/opportunity services.
- `GrantsGov_Opportunity_Schemas.md` — opportunity-focused schema elements and structures.
- `GrantsGov_Common_Types.md` — type/value constraints relevant to request/response validation.
- `GrantsGov_Eligibility_Extraction_Notes.md` — limits of API-only eligibility extraction and document-based caveats.

## Required usage rule

Before implementing/debugging opportunity ingestion or eligibility logic:

1. Check endpoint behavior docs first.
2. Validate schema/type constraints.
3. Reconfirm extraction limitations from eligibility notes (API screening vs legal eligibility truth).

## Gaps to fill

- Add TNTECheck eligibility-profile mapping guide (Grants.gov fields -> editable criteria schema).
- Add sample parsing outputs for common opportunity notices used by TTU workflows.
