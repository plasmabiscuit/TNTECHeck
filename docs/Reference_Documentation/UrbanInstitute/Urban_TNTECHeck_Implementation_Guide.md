# TNTECHeck Implementation Guide for the Urban Colleges API

This document is the project-facing interpretation of Urban's college-university API surfaces.

## 1. What Urban should do in TNTECHeck

Urban should be the **primary adapter** for public college-level institutional data used in:
- opportunity profiling
- institutional capability narratives
- benchmark/peer tables
- proposal support dashboards
- eligibility profile starting points

Urban is especially strong when TNTECHeck needs to answer questions like:

- What is the institution's profile and control/sector context?
- What is the enrollment mix by level, race, sex, age, or residence?
- What program completions support a field/discipline narrative?
- What are the retention/graduation/outcome measures?
- What are the tuition, aid, net price, and selected Scorecard repayment/earnings indicators?
- How does TTU compare with peer or state benchmarks over time?

## 2. What Urban should not do alone

Urban is not the full answer for:
- legal funding opportunity eligibility language
- institution-specific internal research administration data
- NOFO logic that depends on local policies, sponsor nuances, or manually interpreted requirements
- every derived grant metric without some calculation layer on top

In other words: Urban is a public data substrate, not a full grant-analysis engine.

## 3. Recommended endpoint tiers

### Tier 1: required for v1
These should be in the first implementation wave.

#### Institutional identity and profile
- `college-university/ipeds/directory`
- `college-university/ipeds/institutional-characteristics`
- `college-university/ipeds/admissions-enrollment`
- `college-university/ipeds/admissions-requirements`

#### Enrollment and student profile
- `college-university/ipeds/enrollment-headcount`
- `college-university/ipeds/enrollment-full-time-equivalent`
- `college-university/ipeds/fall-enrollment/race/sex`
- `college-university/ipeds/fall-enrollment/age/sex`
- `college-university/ipeds/fall-enrollment/residence`

#### Program production
- `college-university/ipeds/completions-cip-6`
- `college-university/ipeds/completions-cip-2`
- `college-university/ipeds/completers`

#### Student success
- `college-university/ipeds/fall-retention`
- `college-university/ipeds/grad-rates`
- `college-university/ipeds/outcome-measures`

#### Affordability and aid
- `college-university/ipeds/academic-year-tuition`
- `college-university/ipeds/program-year-tuition-cip`
- `college-university/ipeds/sfa-ftft`
- `college-university/ipeds/sfa-grants-and-net-price`
- `college-university/ipeds/sfa-all-undergraduates`

### Tier 2: strongly recommended
- `college-university/scorecard/default`
- `college-university/scorecard/repayment`
- `college-university/scorecard/earnings`
- `college-university/scorecard/student-characteristics/aid-applicants`
- `college-university/nacubo/endowments`
- `college-university/ipeds/student-faculty-ratio`
- `college-university/ipeds/salaries-instructional-staff`

### Tier 3: situational / specialized
- `college-university/fsa/grants`
- `college-university/fsa/loans`
- `college-university/fsa/financial-responsibility`
- `college-university/eada/institutional-characteristics`
- `college-university/campus/crime/hate-crimes`
- `college-university/nccs/990-forms`
- `college-university/nhgis/*`

## 4. How TNTECHeck should model Urban metadata

You need an endpoint registry. Not optional.

Suggested fields:

```json
{
  "id": "urban.ipeds.completions-cip-6",
  "section": "college-university",
  "source": "ipeds",
  "topic": "completions-cip-6",
  "subtopics": [],
  "years_available": "1983-2022",
  "supports_summary": true,
  "primary_use_cases": [
    "program production",
    "cip mapping",
    "grant narrative support"
  ],
  "notes": "Use for field-level completions and CIP grouping"
}
```

Add project-specific metadata such as:
- default filters
- peer-comparison eligibility
- proposal relevance tags
- whether an endpoint should appear in the UI by default

## 5. Indicator design for TNTECHeck

Do not expose raw Urban endpoints directly to users as the main abstraction.

Instead, define **Indicators** and map them back to Urban.

Example:

```json
{
  "indicator_id": "ttu_undergrad_enrollment_total",
  "label": "Total undergraduate enrollment",
  "urban_source": {
    "section": "college-university",
    "source": "ipeds",
    "topic": "enrollment-headcount"
  },
  "summary": {
    "var": "enrollment",
    "stat": "sum"
  },
  "filters": {
    "level_of_study": "undergraduate"
  }
}
```

This will keep the UI usable when the underlying source complexity grows.

## 6. Summary-first design

Urban's summary endpoints should drive:
- KPI cards
- proposal-ready trend charts
- state and peer summaries
- institution-vs-group comparisons
- top-line demographic/programmatic views

Raw endpoints should drive:
- detailed downloads
- QA screens
- advanced analyst views
- custom calculations not available from summary mode

## 7. College Scorecard through Urban

Urban includes college-university scorecard slices such as:
- `default`
- `earnings`
- `repayment`
- `institutional-characteristics`
- `student-characteristics`

That matters for TNTECHeck because it means you can keep **IPEDS-like** and **Scorecard-like** public indicators under one adapter instead of separately wiring multiple public APIs for every use case.

Still, do not collapse provenance. Display clearly whether a value comes from:
- IPEDS via Urban
- Scorecard via Urban
- another Urban-supported source

## 8. CIP strategy

For grant work, CIP mapping is central. By default, CIP's should be grouped into the same categories used by IPEDS with a future feature toggle each one individually. 

Use:
- `completions-cip-6` for detailed field alignment
- `completions-cip-2` for higher-level family/grouping
- a local **Program Group Registry** that maps proposal concepts to one or more CIP codes

That registry is where the real application value lives. Urban supplies the public data; TNTECHeck must supply the reusable mappings.

## 9. Institutional comparisons

Urban is a strong fit for:
- TTU vs Tennessee public institutions
- TTU vs selected peers
- TTU vs self over time

Recommended approach:
1. use Urban for institution-level measures
2. maintain comparison-group definitions in TNTECHeck
3. calculate peer median/mean/rank in your own app layer
4. cache the resulting summaries

Do not hardcode peer logic into one-off charts.

## 10. Opportunity-support use cases

For the broader TNTECHeck project, Urban should support these recurring proposal tasks:

### Institutional overview packet
- directory
- institutional characteristics
- admissions
- enrollment
- aid/net price

### Pipeline/equity packet
- fall enrollment by race/sex
- age/sex where relevant
- residence
- Pell/net price related endpoints
- selected scorecard student-characteristics

### Program strength packet
- completions-cip-6
- completions-cip-2
- related tuition/program charge endpoints if needed

### Student success packet
- retention
- graduation rates
- outcome measures
- selected scorecard default/repayment/earnings

## 11. Defensive design recommendations

### Cache aggressively
Urban is public infrastructure. Treat it respectfully and avoid repeated identical calls.

### Store year availability by endpoint
A missing year is often a data-availability issue, not an application bug.

### Preserve raw request URLs
You will need them for reproducibility and troubleshooting.

### Surface source provenance in UI/export
Public grant support tools become untrustworthy the minute the source lineage is ambiguous.

### Expect semantic variation by endpoint
`year` does not always mean the same thing across all sources/endpoints. Your metadata layer needs room for notes and caveats.

## 12. Final recommendation

Use Urban as the **default public institutional data backbone** for TNTECHeck's college analytics.

But build the product around:
- endpoint metadata
- indicator definitions
- program/CIP mapping
- comparison groups
- summary-first reporting

If you just expose a pile of raw endpoints, you will have documentation, not a usable grant-support system. The point is not to let users browse Urban. The point is to operationalize Urban for proposal work.
