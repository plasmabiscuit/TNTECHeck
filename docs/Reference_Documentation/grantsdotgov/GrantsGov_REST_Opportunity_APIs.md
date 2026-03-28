# Grants.gov REST Opportunity APIs

## Applicant API overview
The Applicant API currently highlights two opportunity-facing endpoints:
- `search2`
- `fetchOpportunity`

---

## search2
**Endpoint:** `POST https://api.grants.gov/v1/api/search2`

### Authentication
Grants.gov states that authentication and authorization are **not required** for `search2`.

### Example request body fields shown in docs
| Field | Purpose |
|---|---|
| `rows` | number of rows to return |
| `keyword` | keyword search |
| `oppNum` | opportunity number filter |
| `eligibilities` | eligibility category filter |
| `agencies` | agency filter |
| `oppStatuses` | status filter (`forecasted`, `posted`, etc.) |
| `aln` | ALN / CFDA filter |
| `fundingCategories` | funding activity category filter |

### Response elements shown in docs
| Field | Notes |
|---|---|
| `data.searchParams` | echoed/normalized search params |
| `data.hitCount` | total hits |
| `data.oppHits[]` | compact opportunity list |
| `oppHits[].id` | opportunity id |
| `oppHits[].number` | opportunity number |
| `oppHits[].title` | opportunity title |
| `oppHits[].agencyCode` / `agencyName` | agency metadata |
| `oppHits[].openDate` / `closeDate` | date metadata |
| `oppHits[].oppStatus` | status |
| `oppHits[].docType` | synopsis, etc. |
| `oppHits[].alnist[]` | ALN values |
| `data.eligibilities[]` | response bucket of eligibility categories |
| `data.fundingCategories[]` | response bucket of funding categories |
| `data.fundingInstruments[]` | response bucket of funding instruments |

### Why it matters
This is the fastest public-facing search endpoint for:
- opportunity discovery
- coarse eligibility category filtering
- pre-screening before you pull package/instruction assets

---

## fetchOpportunity
**Endpoint:** `https://api.grants.gov/v1/api/fetchOpportunity`

### Request body
| Field | Purpose |
|---|---|
| `opportunityId` | numeric Grants.gov opportunity id |

### Response areas shown in docs
Top-level:
- `id`
- `revision`
- `opportunityNumber`
- `opportunityTitle`
- `owningAgencyCode`
- `listed`
- `publisherUid`
- `flag2006`
- `opportunityCategory`

Nested `synopsis` object (sample response fields shown by Grants.gov):
- `agencyCode`
- `agencyName`
- `agencyPhone`
- `agencyAddressDesc`
- `agencyDetails`
- `topAgencyDetails`
- `agencyContactPhone`
- `agencyContactName`
- `agencyContactDesc`
- `agencyContactEmail`
- `agencyContactEmailDesc`
- `synopsisDesc`
- `responseDateDesc`
- `postingDate`
- `costSharing`
- `awardCeiling`
- `awardCeilingFormatted`
- `awardFloor`
- `awardFloorFormatted`
- `sendEmail`
- `createTimeStamp`
- `createdDate`
- `lastUpdatedDate`
- `applicantTypes[]`
- `fundingInstruments[]`
- `fundingActivityCategories[]`

Other arrays/objects shown in the sample response:
- `synopsisAttachmentFolders[]`
- `synopsisAttachments[]`
- `synopsisDocumentURLs[]`
- `alns[]`
- `opportunityPkgs[]`
- `closedOpportunityPkgs[]`
- `relatedOpps[]`
- `errorMessages[]`

### Why it matters
This endpoint is more useful than `search2` when you want:
- richer synopsis text
- applicant/eligibility category codes (`synopsis.applicantTypes`)
- funding instrument categories
- synopsis attachments and related documents metadata
- award ceiling/floor and cost-sharing indicators

---

## Practical split: SOAP vs REST
Use **SOAP `GetOpportunityList`** when you need:
- `PackageID`
- `CompetitionID`
- `CompetitionTitle`
- `SchemaURL`
- `InstructionsURL`

Use **REST `search2` / `fetchOpportunity`** when you need:
- public discovery
- quick filters by eligibility / funding category / status / ALN
- synopsis-level metadata that may help infer eligibility before downloading instruction documents
