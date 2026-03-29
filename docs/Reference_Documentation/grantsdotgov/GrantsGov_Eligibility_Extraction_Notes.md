# Grants.gov Eligibility Extraction Notes

## The uncomfortable truth
Grants.gov itself says the **full legal eligibility requirements** are in the **Application Instructions attached to every funding opportunity**. The awarding agency may also summarize eligibility in the **Synopsis Details** section.

That means:
- package/synopsis APIs are useful for **screening**
- instruction attachments are necessary for **full legal eligibility extraction**

## Best extraction path by need

### A) Quick eligibility filtering across many opportunities
Use REST `search2`.

**Useful request fields**
- `eligibilities`
- `agencies`
- `oppStatuses`
- `aln`
- `fundingCategories`
- `keyword`
- `oppNum`

**Useful response fields**
- `data.eligibilities[]`
- `data.oppHits[]`
- `oppHits[].id`
- `oppHits[].number`
- `oppHits[].title`
- `oppHits[].agencyCode`
- `oppHits[].openDate`
- `oppHits[].closeDate`
- `oppHits[].docType`
- `oppHits[].alnist[]`

### B) Opportunity-level detail / synopsis extraction
Use REST `fetchOpportunity` with `opportunityId`.

**Highest-value eligibility-adjacent fields**
- `synopsis.applicantTypes[]`  ← closest structured eligibility category field in the sample response
- `synopsis.synopsisDesc`
- `synopsis.agencyContactName`
- `synopsis.agencyContactEmail`
- `synopsis.costSharing`
- `synopsis.awardCeiling`
- `synopsis.awardFloor`
- `synopsis.fundingInstruments[]`
- `synopsis.fundingActivityCategories[]`
- `alns[]`

### C) Package metadata + instruction/schema URLs
Use SOAP `GetOpportunityList`.

**Highest-value return fields**
- `PackageID`
- `CompetitionID`
- `CompetitionTitle`
- `FundingOpportunityNumber`
- `FundingOpportunityTitle`
- `CFDADetails`
- `OpeningDate`
- `ClosingDate`
- `OfferingAgency`
- `AgencyContactInfo`
- `SchemaURL`
- `InstructionsURL`
- `IsMultiProject`

### D) Full legal eligibility extraction
Follow `InstructionsURL` from `GetOpportunityList` and parse the attached instruction package / announcement files.

## Practical implementation recommendation
For a dashboard or eligibility harvester:

1. **REST `search2`**
   - broad search
   - filter by agency, status, ALN, keyword, eligibility buckets

2. **REST `fetchOpportunity`**
   - collect structured synopsis fields and applicant type codes
   - capture award ceiling/floor, cost-sharing, categories, attachments metadata

3. **SOAP `GetOpportunityList`**
   - retrieve the official `PackageID`, `CompetitionID`, `CompetitionTitle`, `SchemaURL`, and `InstructionsURL`

4. **Download and parse instructions / attachments**
   - extract legal eligibility text
   - store alongside the structured synopsis/applicant type data

## What to persist in your own data model
At minimum, store:
- `opportunityId`
- `FundingOpportunityNumber`
- `FundingOpportunityTitle`
- `PackageID`
- `CompetitionID`
- `CompetitionTitle`
- `CFDA/ALN`
- `OpeningDate`
- `ClosingDate`
- `OfferingAgency`
- `AgencyContactInfo`
- `SchemaURL`
- `InstructionsURL`
- `applicantTypes`
- `synopsisDesc`
- `fundingInstruments`
- `fundingActivityCategories`
- `awardCeiling`
- `awardFloor`
- `costSharing`
- extracted free-text eligibility language from instructions

## Limits to be aware of
- `applicantTypes` gives **category-level** eligibility, not always the full legal rule.
- synopsis text may summarize eligibility but may not capture all exclusions/conditions.
- the application instructions remain the authoritative source for edge cases, exceptions, consortia rules, cost-sharing requirements tied to applicant type, or agency-specific carve-outs.

## TNTECheck implementation artifact (current repo)

TNTECheck now includes a harvest utility that operationalizes the workflow above:

- Module: `backend/app/grants_eligibility_harvester.py`
- Output file: `backend/app/data/grants_gov_instruction_eligibility_extracts.json`
- Output fields include: funder, opportunity number, title, package id, instructions URL, and extracted eligibility sections.

Run with:

```bash
cd backend
python -m app.grants_eligibility_harvester
```

Notes:
- The harvester targets all currently `posted` open opportunities (no keyword restriction).
- Full legal eligibility text is parsed from `InstructionsURL` documents when available.
- When `InstructionsURL` yields no eligibility text, the harvester lazily fetches `fundingDescLinkUrl` from the REST `fetchOpportunity` endpoint as a fallback.
- Failures are preserved in the output payload for provenance and partial-source resilience.
