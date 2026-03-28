# Grants.gov API Markdown Pack
This pack is focused on **opportunity discovery**, **package retrieval**, **instruction/package metadata**, and the schema/type material needed to extract or infer eligibility requirements.

## Scope
This is **not** a full Grants.gov platform dump. It is intentionally focused on:
- Applicant S2S SOAP **V2.0**
- REST opportunity search/detail endpoints that help with eligibility screening
- Common schema/data elements relevant to opportunity/package requests
- Type definitions and validation constraints needed for implementation

## Source pages used
- Grants.gov Applicant S2S `Versions & WSDLs`
- Grants.gov Applicant S2S `Web Services`
- `Get Opportunity List`
- `Get Application Info`
- `Get Application Zip`
- `Grants Common Elements`
- `Applicant Common Elements`
- `Grants Common Types`
- Grants.gov Applicant API `search2`
- Grants.gov Applicant API `fetchOpportunity`
- Grants.gov `Applicant Eligibility`

## Files in this pack
- `GrantsGov_S2S_Opportunity_and_Package_Services.md`
- `GrantsGov_REST_Opportunity_APIs.md`
- `GrantsGov_Opportunity_Schemas.md`
- `GrantsGov_Common_Types.md`
- `GrantsGov_Eligibility_Extraction_Notes.md`

## What matters most for your use case
For **open opportunity/package discovery**, the best SOAP service is `GetOpportunityList`.

For **search-time eligibility category screening**, the REST endpoints are more useful:
- `search2` exposes an `eligibilities` search parameter and returns eligibility buckets in the response.
- `fetchOpportunity` exposes `synopsis.applicantTypes` and other synopsis metadata.

For **full legal eligibility requirements**, Grants.gov states that you need to read the **Application Instructions** attached to each funding opportunity; awarding agencies may also summarize eligibility in the **Synopsis Details** section.
