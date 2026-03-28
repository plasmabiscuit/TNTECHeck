# Grants.gov Applicant S2S Opportunity and Package Services

## Platform/version anchors
- Supported Applicant S2S version: **V2.0**
- Training endpoint: `https://trainingws.grants.gov/grantsws-applicant/services/v2/ApplicantWebServicesSoapPort`
- Production endpoint: `https://ws07.grants.gov/grantsws-applicant/services/v2/ApplicantWebServicesSoapPort`
- WSDL: `ApplicantWebServices-V2.0.wsdl`
- V2.0 uses **MTOM** to support large submissions.

## Recommended Applicant S2S web services
From the Applicant Web Services page, the recommended V2.0 services are:
- `GetOpportunityList`
- `SubmitApplication`
- `GetSubmissionList`
- `GetApplicationInfo`
- `GetApplicationZip`

For your use case, the first three that matter are the following.

---

## GetOpportunityList
**Purpose:** returns a list of open Opportunity Packages matching filter criteria.

### Notes from Grants.gov
- Based on the earlier Get Opportunities Expanded service.
- Adds **PackageID** as an input filter.
- Returns revised **SchemaURL** and **InstructionsURL** using the new submission header V2.0.
- Returns revised **CFDA** handling to allow **multiple CFDAs**.
- Replaces the older `Get Opportunities`, `Get Opportunity Plus Comp Title`, and `Get Opportunities Expanded` services.

### Input parameters
| Input parameter | Required? | Business rules | Schema |
|---|---|---|---|
| `PackageID` | Optional | Must be a valid PackageID | `GrantsCommonElements:PackageID` |
| `OpportunityFilter` | Optional | At least one of `FundingOpportunityNumber`, `CFDANumber`, `CompetitionID`. If `CompetitionID` is specified, it must include `CFDANumber` and/or `FundingOpportunityNumber`. | `ApplicantCommonElements:OpportunityFilter` |

### Return structure
Returns `OpportunityDetails` (may have multiple occurrences), containing:
- `FundingOpportunityNumber`
- `FundingOpportunityTitle`
- `CompetitionID`
- `CompetitionTitle`
- `PackageID`
- `CFDADetails` (`CFDA Number`, `CFDA Title`)
- `OpeningDate`
- `ClosingDate`
- `OfferingAgency`
- `AgencyContactInfo`
- `SchemaURL`
- `InstructionsURL`
- `IsMultiProject`

### Why it matters
This is the cleanest SOAP service for retrieving:
- package identifiers
- competition identifiers/titles
- schema and instructions URLs
- CFDA / ALN metadata
- agency contact and dates

That makes it the best S2S entry point for any workflow that later parses instructions for eligibility.

---

## GetApplicationInfo
**Purpose:** retrieves application status information for a given Grants.gov tracking number.

### Input parameter
| Input parameter | Required? | Business rules | Schema |
|---|---|---|---|
| `GrantsGovTrackingNumber` | Required | Must be a valid Grants.gov tracking number submitted by this certificate or any linked previous certificate | `GrantsCommonElements:GrantsGovTrackingNumber` |

### Return values
| Return value | Notes |
|---|---|
| `GrantsGovTrackingNumber` | Required |
| `StatusDetail` | Required |
| `AgencyNotes` | Optional |

### Why it matters
Useful after submission, but **not** the primary service for opportunity/eligibility discovery.

---

## GetApplicationZip
**Purpose:** returns a zip containing the submitted application XML plus attachments for a given Grants.gov tracking number.

### Notes from Grants.gov
- Supports large submissions.
- V2.0 returns submissions under linked previous certificates as well as the current certificate.

### Why it matters
Useful for archive/audit and downstream parsing of already-submitted applications, but **not** the discovery service you want for package/eligibility screening.

---

## Implementation recommendation
Use this sequence for SOAP/S2S opportunity workflows:
1. `GetOpportunityList` to get package-level metadata and the `InstructionsURL` / `SchemaURL`
2. fetch and parse the instruction package or announcement files for **full legal eligibility**
3. use `GetApplicationInfo` / `GetApplicationZip` only after submission or when you need submission-state data
