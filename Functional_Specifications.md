# TNTECheck - TTU Grant Data Workbench

## Functional Specification

**Version:** 0.9
**Scope:** no-auth, TTU-first internal analytics application for institutional/capacity-grant support
**Primary institution:** Tennessee Technological University (**UNITID 221847**) ([National Center for Education Statistics][1])

---

## 1. Purpose

Build a no-auth internal web application that gives proposal developers and analysts a **TTU-preconfigured** interface for institutional data retrieval, comparison, summarization, export, and proposal-ready reporting.

The application is optimized for **capacity-building, institutional-development, infrastructure, and graduate or undergraduate-focused research proposals**, where recurring data needs usually include institutional profile, student demographics, equity disaggregation, field/CIP completions, retention/graduation, research-capacity indicators, and prior sponsor funding history. Public source coverage should center on Urban’s Education Data API, IPEDS/NCES, College Scorecard, NIH RePORTER, NSF Award Search, and USDA/NIFA Data Gateway. Urban’s API returns JSON and supports both raw endpoint access and summary endpoints; IPEDS officially exposes tools/downloads such as Data Explorer, Compare Institutions, Custom Data Files, Complete Data Files, and Access Database downloads rather than a normal API-first public interface. NIH RePORTER exposes award/project data via API; NSF exposes an Award Search API; NIFA exposes public award/project information through the Data Gateway.

---

## 2. Product Goals

### 2.1 Primary goals

1. Give TTU staff a **single interface** for recurring institutional-grant data work.
2. Avoid manual reconstruction of the same tables for each NOFO.
3. Support **proposal-oriented presets** rather than generic data browsing alone.
4. Make **eligibility profiles editable**, since NOFO thresholds and definitions change.
5. Support **comparison groups**, **program/CIP groups**, and **narrative-ready exports**.
6. Permit use by experienced analysts without user accounts, SSO, or permissions.

### 2.2 Non-goals for v1

1. No end-user authentication or role management.
2. No general multi-institution self-service portal.
3. No direct grants-submission workflow.
4. No institutional system-of-record replacement.
5. No promise of full reproducibility from public APIs alone for every sponsor-specific need.

---

## 3. Users and Use Cases

### 3.1 Primary users

* Research development / proposal development staff
* Sponsored programs analysts
* Institutional research collaborators
* Faculty PIs needing institutional context
* Grant writers preparing boilerplate institutional sections

### 3.2 Representative use cases

1. Generate a **TTU institutional profile** for an NIH/NSF capacity proposal.
2. Pull **biology-related completions** by CIP and award level over 10 years.
3. Compare TTU to a **peer group** or **state/sector benchmark**.
4. Build a **student success/equity snapshot** by subgroup.
5. Produce a **research-capacity funding history** by sponsor.
6. Save an output as:

   * chart
   * CSV
   * JSON
   * narrative summary
   * print/PDF report packet

---

## 4. External Source Inventory and Official Documentation

The app should be source-driven. Each source gets an adapter, metadata profile, and capability flags.

Local source documentation index: `docs/Reference_Documentation/README.md` (required starting point for source-related development/debugging).

### 4.1 Urban Institute Education Data API

Use as the **primary public institutional data API** for IPEDS-derived and related higher-ed data. Urban documents direct API access, JSON responses, and summary endpoints from the same documentation surface.

**Documentation links**

* Urban Education Data API documentation
* Urban colleges data documentation
* Urban summary endpoints reference
* Urban Explorer usage docs

### 4.2 NCES / IPEDS

Use as:

* authoritative semantics reference
* fallback/manual-import source
* peer-group and data-feedback workflows
* backup source when Urban coverage/normalization is insufficient

IPEDS’ official access pattern is through data tools and downloadable files, including Data Explorer, Compare Institutions, Custom Data Files, Complete Data Files, and Access Database.

**Documentation links**

* IPEDS main portal
* IPEDS Use The Data
* IPEDS overview of data/use tools
* TTU institution profile / reported data starting points ([National Center for Education Statistics][1])

### 4.3 College Scorecard

Use for:

* cost/price
* net price
* aid
* debt/repayment/earnings/outcomes context
* additional institution-level measures complementary to IPEDS

College Scorecard exposes downloadable data and technical data documentation, and its official site exposes API documentation from the data/resources surface.

**Documentation links**

* College Scorecard data home
* College Scorecard data documentation
* College Scorecard home/resources entry points to API docs

### 4.4 NIH RePORTER API

Use for:

* NIH funding history
* organization-level award discovery
* PI/project history
* sponsor-specific research-capacity reporting

NIH documents RePORTER as a programmatic API for awards data, with interactive endpoint docs, JSON outputs, and a recommendation to limit usage to about one request per second.

**Documentation links**

* NIH RePORTER API home/docs
* NIH RePORTER Project API data elements dictionary
* NIH RePORT / RePORTER FAQ / bulk export references

### 4.5 NSF Award Search API / Developer Resources

Use for:

* NSF funding history
* award counts and trend
* sponsor-specific research-capacity reporting

NSF’s developer resources explicitly identify the Award Search API and open-data resources.

**Documentation links**

* NSF Developer Resources
* NSF Award Search overview
* NSF open data resources

### 4.6 USDA / NIFA Data Gateway

Use for:

* NIFA funding history
* award/project metrics
* education/research/extension project discovery

NIFA documents the Data Gateway as a public tool for finding funding data, metrics, and project information, alongside REEIS and related public data tools.

**Documentation links**

* NIFA Data page / Data Gateway entry point
* NIFA Grant Funding Dashboard / Data Gateway access surface

---

## 5. Sponsorship Context for Presets

The preset system should map to recurring sponsor needs rather than abstract endpoints.

NIH AREA explicitly ties review to strengthening the institutional research environment and involving undergraduates in research. ED Title V DHSI explicitly frames the program around expanding educational opportunity, improving attainment, and strengthening institutional stability. NSF capacity/infrastructure programs emphasize building broadly useful research capacity. USDA/NIFA strengthening/resident-instruction programs emphasize institutional educational capacity, curriculum, faculty, student recruitment/retention, and related capacity indicators. ([Grants.gov][2])

**Implication:** the app must not be just an endpoint browser. It must encode reusable grant-support views.

---

## 6. Core Product Principles

### 6.1 TTU-first

The app opens in TTU context by default. Institution switching is not part of v1 UX. Peer institutions are handled through comparison-group configuration, not through freeform institution search.

### 6.2 No-auth

No user login, no RBAC, no session-based permission model.

### 6.3 Editable eligibility logic

Eligibility profiles are **configurable templates**, not hardcoded rules. Each profile must support:

* editable criteria
* editable thresholds
* editable narrative labels
* editable source mappings
* manual override fields
* provenance notes

### 6.4 Source abstraction

Every source must be normalized behind a common adapter interface.

### 6.5 Proposal-ready outputs

Every report must support:

* chart
* tabular export
* metric summary
* narrative summary
* citation/source notes
* query provenance

---

## 7. Functional Scope

## 7.1 App modules

### Module A — Dashboard / Home

Purpose:

* launch common tasks quickly
* show recent preset runs
* expose latest available data-year metadata
* highlight source health

Required elements:

* preset launcher cards
* source status panel
* recent report history
* latest-year-by-source widget
* quick links: Institutional Overview, Biology Completions, Funding History, Benchmark Builder

### Module B — Preset Reports

Purpose:

* expose curated proposal-oriented reports
* encode common data bundles and views

Required features:

* filter controls
* save/shareable query state
* chart + table + narrative summary
* export actions
* source attribution block
* calculation notes

### Module C — Explore / Query Builder

Purpose:

* permit advanced users to build custom reports from normalized indicators

Required features:

* source selector
* topic selector
* variable/indicator selector
* disaggregation selector
* time controls
* comparison group controls
* output mode: raw / summary / report

### Module D — Eligibility Profiles

Purpose:

* editable grant-eligibility or NOFO-profile definitions

Required features:

* create/edit/delete profiles
* attach indicators and data sources
* define pass/fail logic
* define “requires manual confirmation” logic
* store assumptions and notes
* render exportable eligibility worksheet

### Module E — Program Groups

Purpose:

* map departments/disciplinary concepts to CIP-driven public data

Required features:

* group builder
* named group registry
* strict vs broad definitions
* versioning and notes
* test run preview

### Module F — Comparison Groups

Purpose:

* define reusable peer/benchmark groups

Required features:

* saved TTU vs state/public sector groups
* custom institution lists
* metadata tags
* median/percentile/rank options
* import/export group definitions

### Module G — Funding History

Purpose:

* sponsor-specific research-capacity reporting

Required features:

* NIH / NSF / NIFA subviews
* annual totals
* award counts
* PI/project search
* sponsor/program filters
* organization-level TTU aggregation
* exportable award list

### Module H — Export / Report Builder

Purpose:

* generate proposal-ready outputs

Required features:

* chart export
* CSV/JSON export
* markdown/plain text narrative export
* print-friendly HTML/PDF
* source notes and timestamps
* inclusion of filter state and calculation metadata

### Module I — Settings / Admin (No-auth local admin only)

Purpose:

* app configuration, not user management

Required features:

* source endpoint config
* cache settings
* environment metadata
* eligibility profile registry
* indicator registry
* program-group registry
* comparison-group registry
* preset registry
* optional key injection config for future source adapters without user auth

---

## 8. Data Domains

## 8.1 Institution domain

Fields:

* unitid
* institution_name
* aliases
* sector
* control
* carnegie/research category if available
* state
* city
* campus metadata
* source-specific identifiers

For TTU, seed with:

* `unitid: 221847`
* name aliases including Tennessee Technological University / Tennessee Tech ([National Center for Education Statistics][1])

## 8.2 Indicator domain

Every displayed metric must be registered as an **Indicator**.

Required fields:

* `id`
* `name`
* `label`
* `description`
* `domain`
* `source`
* `source_topic`
* `source_variable`
* `allowed_years`
* `allowed_filters`
* `aggregation_modes`
* `format`
* `unit`
* `default_chart`
* `notes`
* `provenance`
* `is_public_source`
* `supports_comparison`
* `supports_disaggregation`

## 8.3 Eligibility profile domain

Required fields:

* `id`
* `name`
* `funder`
* `program`
* `version_label`
* `effective_date`
* `criteria[]`
* `manual_fields[]`
* `decision_logic`
* `status`
* `notes`
* `citations[]`

Each criterion:

* `criterion_id`
* `label`
* `type` (`computed`, `manual`, `hybrid`)
* `source_indicators[]`
* `operator`
* `threshold`
* `direction`
* `confidence`
* `manual_override_allowed`
* `narrative_template`

## 8.4 Program group domain

Required fields:

* `id`
* `name`
* `scope` (`strict`, `broad`, `custom`)
* `cip_codes[]`
* `award_levels[]`
* `notes`
* `version`

This is essential because IPEDS completions are by **6-digit CIP** and award level, not by department.

## 8.5 Comparison group domain

Required fields:

* `id`
* `name`
* `definition_type` (`manual_list`, `sector_rule`, `state_rule`, `saved_ipeds_peer`, `hybrid`)
* `unitids[]`
* `selection_logic`
* `notes`
* `version`

## 8.6 Report preset domain

Required fields:

* `id`
* `name`
* `category`
* `funder_tags[]`
* `description`
* `default_filters`
* `required_indicators[]`
* `required_sources[]`
* `charts[]`
* `tables[]`
* `narrative_templates[]`
* `exports[]`
* `comparison_behavior`
* `eligibility_profile_ref?`

## 8.7 Report run domain

Required fields:

* `run_id`
* `preset_id?`
* `query_payload`
* `source_requests[]`
* `source_responses_meta[]`
* `computed_results`
* `rendered_artifacts`
* `timestamp_utc`
* `cache_hit`
* `errors[]`

---

## 9. Preset Library Specification

## 9.1 Global preset categories

1. Institutional Overview
2. Student Profile and Equity
3. Enrollment / Pipeline
4. Completions by Program/CIP
5. Student Success / Attainment
6. Price / Aid / Affordability
7. Staffing / Faculty Capacity
8. Research Funding Capacity
9. Benchmark / Peer Comparison
10. Eligibility Worksheet

## 9.2 Funder-specific preset bundles

### NIH bundle

Target use:

* AREA
* SuRE
* other limited-research-capacity / institutional-environment narratives

Required presets:

1. NIH Eligibility Snapshot
2. Graduate and Undergraduate-Focused Environment
3. Biomedical/Relevant Program Production
4. NIH Funding History
5. Research Environment Support Packet

Source stack:

* Urban/IPEDS
* NIH RePORTER
* local editable/manual fields

Rationale: NIH AREA emphasizes institutional research environment, undergraduate involvement in research, and limited prior NIH funding. ([Grants.gov][2])

### NSF bundle

Target use:

* capacity/infrastructure
* broadening participation
* institutional transformation
* STEM pipeline proposals

Required presets:

1. STEM Pipeline and Completions
2. Equity-Disaggregated Student Need
3. NSF Funding History
4. Research Capacity Snapshot
5. Benchmark Against Peer Cluster

Source stack:

* Urban/IPEDS
* NSF Award Search
* optional local data

Rationale: NSF capacity programs and developer resources align with research-capacity and award-history analysis; many NSF institutional arguments depend on disaggregated need and STEM production context. ([NSF - U.S. National Science Foundation][3])

### USDA / NIFA bundle

Target use:

* strengthening / resident instruction / agricultural education capacity

Required presets:

1. Agriculture-Related Program Production
2. NIFA Funding History
3. Student Recruitment/Retention Baseline
4. Curriculum/Capacity Support Snapshot
5. Extension/Project Activity Summary

Source stack:

* Urban/IPEDS
* NIFA Data Gateway
* optional local/manual program metrics

Rationale: NIFA resident-instruction/capacity programs focus on educational capacity, curriculum, faculty, instrumentation, and student recruitment/retention; Data Gateway is the public funding/project surface. ([Nation Institute of Food and Agriculture][4])

### ED Title III / Title V bundle

Target use:

* institutional development
* student opportunity / attainment
* academic offerings / institutional stability

Required presets:

1. Opportunity and Access Profile
2. Retention / Graduation / Attainment
3. Price, Aid, and Affordability
4. Institutional Stability Snapshot
5. Demographic and Low-Income Context

Source stack:

* Urban/IPEDS
* College Scorecard
* optional local student-support data

Rationale: DHSI explicitly cites educational opportunity, attainment, academic offerings, program quality, and institutional stability. ([U.S. Department of Education][5])

---

## 10. Required Screens

## 10.1 Home

Components:

* quick-start cards
* latest data-year indicators
* recent report runs
* source status badges
* “edit eligibility profiles” shortcut

## 10.2 Preset Catalog

Components:

* search
* filter by funder
* filter by domain
* filter by source
* preset detail drawer
* launch action

## 10.3 Report Workspace

Components:

* filter rail
* header with preset name / funder tag / source chips
* KPI strip
* chart area
* table area
* narrative area
* export panel
* calculation notes / source notes

## 10.4 Explore Builder

Components:

* source selector
* topic/subtopic selector
* variable/indicator selector
* group-by / disaggregation selector
* year range selector
* comparison selector
* output toggle
* raw JSON inspector
* generated request preview

## 10.5 Eligibility Profile Editor

Components:

* profile metadata form
* criteria list
* criterion logic editor
* manual-field editor
* preview evaluator
* narrative template editor
* export worksheet

## 10.6 Program Group Manager

Components:

* CIP code search/add
* strict/broad toggle
* preview summary
* version notes
* import/export

## 10.7 Comparison Group Manager

Components:

* institution list builder
* rules builder
* peer-median options
* TTU-vs-group preview
* import/export

## 10.8 Funding History

Components:

* sponsor tabs
* annual trend chart
* award table
* PI/project filters
* sponsor/program filters
* export actions

## 10.9 Settings / Admin

Components:

* source config
* registry editors
* cache controls
* diagnostics
* environment info

---

## 11. Source Adapter Architecture

Use an adapter-driven backend.

### 11.1 Common adapter contract

```ts
interface SourceAdapter {
  id: string;
  label: string;
  capabilities: {
    rawQuery: boolean;
    summaryQuery: boolean;
    comparisons: boolean;
    pagination: boolean;
    exportCsv: boolean;
    metadataDiscovery: boolean;
  };
  fetchMetadata(): Promise<SourceMetadata>;
  executeRaw(query: NormalizedQuery): Promise<NormalizedResult>;
  executeSummary(query: NormalizedSummaryQuery): Promise<NormalizedSummaryResult>;
  validateQuery(query: NormalizedQuery): ValidationResult;
  healthcheck(): Promise<HealthcheckResult>;
}
```

### 11.2 Adapters required in v1

* `urbanAdapter`
* `scorecardAdapter`
* `nihReporterAdapter`
* `nsfAwardAdapter`
* `nifaGatewayAdapter`
* `ipedsImportAdapter` (manual upload / offline imports)

### 11.3 Adapter responsibilities

Each adapter must:

1. translate internal query objects into source-native requests
2. normalize source-native responses
3. expose metadata/capability descriptions
4. handle pagination/retries
5. tag provenance on all records/results
6. preserve source-native identifiers

---

## 12. Query Model

## 12.1 Normalized query object

```ts
interface NormalizedQuery {
  source: string;
  dataset: string;
  topic?: string;
  subtopic?: string;
  institution: {
    unitid: string;
    aliases?: string[];
  };
  years?: number[];
  filters?: QueryFilter[];
  dimensions?: string[];
  measures?: string[];
  mode: "raw" | "summary" | "report";
  comparisonGroupId?: string;
  programGroupId?: string;
  pagination?: {
    page?: number;
    pageSize?: number;
  };
}
```

## 12.2 Filter object

```ts
interface QueryFilter {
  field: string;
  operator: "eq" | "neq" | "in" | "not_in" | "gte" | "lte" | "between" | "contains";
  value: string | number | string[] | number[] | [number, number];
}
```

## 12.3 Summary query object

```ts
interface NormalizedSummaryQuery extends NormalizedQuery {
  summary: {
    variable: string;
    statistic: "sum" | "count" | "avg" | "min" | "max" | "variance" | "stddev";
    by?: string[];
  };
}
```

Urban explicitly supports summary endpoints with variable/statistic/grouping behavior; use this as the reference design for internal summary-query abstraction.

---

## 13. Data Normalization Rules

### 13.1 Institution identity

All source data must normalize to:

* `unitid`
* `institution_name`
* source-specific institution identifier(s)

TTU should always resolve to UNITID 221847. ([National Center for Education Statistics][1])

### 13.2 Time normalization

Store:

* `source_year`
* `source_collection_year` if applicable
* `display_year`
* `year_type` (`academic`, `fiscal`, `calendar`, `cohort`)

### 13.3 Program normalization

Programs must normalize to:

* `cip_code`
* `cip_title`
* `award_level`
* `program_group_ids[]`

### 13.4 Demographic normalization

Normalize subgroup dimensions to common internal enums where source semantics permit:

* sex
* race_ethnicity
* residency
* attendance_status
* student_level

### 13.5 Funding normalization

For NIH/NSF/NIFA funding records:

* sponsor
* sponsor_program
* project_id
* project_title
* PI
* organization
* fiscal_year
* amount
* award_type/activity code where available
* source_url

---

## 14. Eligibility Profiles: Functional Detail

Eligibility profiles are editable start points, not deterministic final truth.

## 14.1 Profile types

* sponsor-specific
* NOFO-specific
* internal reusable template
* draft/custom

## 14.2 Criterion types

* computed from source data
* manual input only
* hybrid computed + confirmed
* advisory only

## 14.3 Required behavior

1. Every criterion must declare:

   * source-backed or manual
   * confidence level
   * data freshness
   * whether it blocks a pass/fail decision
2. Profiles must support:

   * partial completion
   * “unknown”
   * “requires institutional confirmation”
   * manual narrative notes
3. Evaluation output:

   * pass
   * fail
   * indeterminate
   * manual review required

### 14.4 Example profile object

```ts
interface EligibilityProfile {
  id: string;
  name: string;
  funder: string;
  program: string;
  editable: true;
  criteria: EligibilityCriterion[];
  manualFields: ManualField[];
  evaluationMode: "strict" | "advisory" | "hybrid";
  narrativeTemplates: NarrativeTemplate[];
}
```

---

## 15. Comparison Engine

The comparison system must support:

1. **TTU vs own trend**
2. **TTU vs custom peer list**
3. **TTU vs NCES/IPEDS-style peer group**
4. **TTU vs state public 4-year sector**
5. **TTU percentile/rank within group**
6. **TTU difference from median/mean**

Where the user wants traditional IPEDS context, NCES Data Feedback Report logic is a useful reference point because DFRs are explicitly built around institutional comparison groups and customizable peer comparisons. ([National Center for Education Statistics][6])

---

## 16. Reporting Outputs

Every report must generate:

### 16.1 KPI strip

Example:

* current value
* prior-year value
* percent change
* peer-group median
* delta to peer median

### 16.2 Chart output

Allowed chart types:

* line
* grouped bar
* stacked bar
* heatmap
* dot/lollipop
* small multiples

### 16.3 Table output

Required features:

* sortable
* downloadable
* export to CSV
* optional transposed layout for proposal appendix formatting

### 16.4 Narrative output

Every preset must include a narrative template engine.

Example template:

> Tennessee Tech enrolled `{metric_total_enrollment}` students in `{year}`, including `{metric_undergrad_pct}` undergraduate students. Compared with the selected peer group median of `{peer_median}`, TTU was `{delta_pct}` on `{indicator_name}`.

### 16.5 Provenance block

Each export must include:

* run timestamp
* source(s)
* years
* filters
* comparison group
* calculation notes
* data freshness note

---

## 17. Suggested Tech Stack

### 17.1 Frontend

Recommended:

* React + Vite + TypeScript
* TanStack Query
* Zustand or Redux Toolkit
* ECharts or Chart.js
* AG Grid or TanStack Table
* Zod for runtime validation

### 17.2 Backend

Recommended:

* FastAPI or Express/NestJS
* source adapters as service layer
* Redis or SQLite/Postgres-backed cache
* scheduled metadata refresh
* queue optional but not required in v1

### 17.3 Storage

Recommended:

* Postgres for registries and saved runs
* Redis for transient query/result cache
* object storage optional for exported artifacts

### 17.4 Why backend is still required despite no-auth

Because the backend must:

* centralize source adapters
* normalize source responses
* handle pagination/retries
* protect against brittle client-side API wiring
* persist preset/config registries
* own report generation and provenance

---

## 18. No-Auth Security and Operational Model


No end-user authentication does **not** mean no operational controls. CollegeScorecard will use  API key, which will be in the codex env secrets.
### 18.1 Requirements

* expose no write endpoints without CSRF mitigation
* validate all registry edits server-side
* sanitize exported narrative templates
* rate-limit backend calls to external APIs
* log source errors and adapter failures

### 18.2 Out of scope

* SSO
* user roles
* per-user saved workspaces
* audit by user identity

---

## 19. Caching and Refresh

### 19.1 Metadata cache

Cache:

* source capability metadata
* variable dictionaries
* available years
* source health status

### 19.2 Query cache

Cache key dimensions:

* source
* dataset/topic
* years
* filters
* summary params
* comparison group
* program group
* app version

### 19.3 Expiration

Recommended defaults:

* metadata: 24 hours
* public-source report results: 24 hours
* funding history queries: 24 hours
* manual imports: immutable by checksum

### 19.4 Freshness tagging

Every result must surface:

* data source
* fetched_at
* source_last_updated if available
* cache status

---

## 20. Error Handling

### 20.1 Source error classes

* adapter validation error
* external API unavailable
* source schema drift
* partial results
* no data for filters
* pagination failure
* comparison group empty
* program-group definition invalid

### 20.2 UX behavior

* always preserve filter state
* expose raw source error details in expandable panel
* show user-facing summary message
* provide retry action
* allow export of partial data only with explicit warning metadata

---

## 21. API Documentation / Link Registry Requirement

The app must ship with a **Documentation Registry** containing, at minimum:

```ts
interface ExternalDocLink {
  id: string;
  source: string;
  label: string;
  url: string;
  category: "api" | "data_dictionary" | "download" | "help" | "terms";
}
```

Seed it with:

* Urban API docs
* Urban summary endpoints docs
* Urban colleges docs
* IPEDS Use The Data
* College Scorecard data home/docs/resources entry points
* NIH RePORTER API docs and data dictionary
* NSF Developer Resources / Award Search docs
* NIFA Data Gateway / data page

This registry must be editable from Settings.

---

## 22. Reporting and Preset Definitions

Each preset definition should be declarative.

```ts
interface ReportPreset {
  id: string;
  title: string;
  description: string;
  funderTags: string[];
  requiredSources: string[];
  indicators: string[];
  defaultFilters: QueryFilter[];
  charts: ChartSpec[];
  tables: TableSpec[];
  narrativeTemplates: NarrativeTemplate[];
  supportsComparison: boolean;
  supportsProgramGroups: boolean;
  supportsEligibilityProfile: boolean;
}
```

### 22.1 Mandatory v1 presets

1. Institutional Overview
2. Student Profile and Equity
3. Program Completions by CIP
4. Student Success / Attainment
5. Price / Aid / Affordability
6. NIH Funding History
7. NSF Funding History
8. NIFA Funding History
9. Benchmark Builder
10. Eligibility Worksheet



## 23. Internal API for Frontend/Backend Boundary

Recommended internal endpoints:

### 23.1 Metadata

* `GET /api/meta/sources`
* `GET /api/meta/indicators`
* `GET /api/meta/program-groups`
* `GET /api/meta/comparison-groups`
* `GET /api/meta/presets`
* `GET /api/meta/docs`

### 23.2 Reporting

* `POST /api/report/run`
* `GET /api/report/{runId}`
* `POST /api/report/export`

### 23.3 Eligibility

* `GET /api/eligibility/profiles`
* `POST /api/eligibility/profiles`
* `PUT /api/eligibility/profiles/{id}`
* `POST /api/eligibility/evaluate`

### 23.4 Program groups

* `GET /api/program-groups`
* `POST /api/program-groups`
* `PUT /api/program-groups/{id}`

### 23.5 Comparison groups

* `GET /api/comparison-groups`
* `POST /api/comparison-groups`
* `PUT /api/comparison-groups/{id}`

### 23.6 Source debugging

* `POST /api/source/query`
* `GET /api/source/health`
* `GET /api/source/capabilities`

---

## 24. Non-Functional Requirements

### 24.1 Performance

* common preset render under 3s from warm cache
* cold-cache public-source preset under 10s in normal conditions
* chart/table render under 1s after response normalization

### 24.2 Reliability

* degraded mode must still permit:

  * cached results
  * local config editing
  * report export from previous runs

### 24.3 Traceability

Every report run must be reproducible from stored query state.

### 24.4 Maintainability

No source-specific logic should leak into the frontend except source labels and debug views.

### 24.5 Accessibility

Use semantic HTML and keyboard-navigable controls even though the target audience is internal.

---

## 25. Testing Requirements

### 25.1 Unit tests

* adapter query mapping
* response normalization
* eligibility evaluation logic
* narrative template substitution
* comparison calculations
* program-group aggregation

### 25.2 Integration tests

* live smoke tests against public docs/examples where stable
* cached fixture tests for source adapters
* export generation tests

### 25.3 Contract tests

Each adapter must have contract tests validating:

* required fields
* pagination behavior
* error normalization
* missing-data handling

### 25.4 Regression tests

Required for:

* indicator registry changes
* program-group changes
* source schema changes
* eligibility profile revisions

---

## 26. Acceptance Criteria for v1

The product is acceptable for v1 when:

1. App launches in TTU context without login.
2. User can run at least 10 mandatory presets.
3. User can edit and evaluate at least one eligibility profile.
4. User can create/edit program groups and comparison groups.
5. User can export chart/table/narrative outputs.
6. User can retrieve funding history from NIH, NSF, and NIFA through source adapters or graceful fallback.
7. User can inspect provenance, source notes, and filter state for every run.
8. If an external source is unavailable, the app degrades gracefully and surfaces a clear diagnostic.

---

## 27. Recommended Delivery Plan

### Phase 1

* architecture skeleton
* registries
* Urban adapter
* TTU seed metadata
* 3 presets:

  * Institutional Overview
  * Program Completions by CIP
  * Benchmark Builder

### Phase 2

* College Scorecard adapter
* eligibility profile editor
* program groups
* comparison groups
* narrative export

### Phase 3

* NIH / NSF / NIFA funding adapters
* sponsor-specific presets
* print/PDF reporting
* diagnostics/admin tooling

### Phase 4

* manual import tooling for IPEDS/CSV
* more advanced benchmark logic
* local custom indicator formulas
* richer report builder

---

## 28. Implementation Notes

### 28.1 Do not hardcode NOFO logic

Eligibility must remain configurable.

### 28.2 Do not equate “department” with public data categories

Public completions data are CIP-based. Department proxies require local mapping.

### 28.3 Prefer summary endpoints where available

Urban summary endpoints should be used first for dashboard/report speed; raw mode exists for unsupported aggregations. Urban’s API supports both raw endpoint access and summary-request generation.

### 28.4 Respect source usage expectations

NIH explicitly recommends roughly one request per second and limiting large jobs to off-hours/weekends. Implement rate limiting and caching accordingly.

### 28.5 Treat College Scorecard as complementary, not redundant

It complements IPEDS/Urban for cost, aid, debt, and outcomes surfaces.

### 28.6 Documentation-first implementation requirement

For any feature development or debugging that involves a source adapter, source-backed indicator, eligibility extraction input, or report calculation:

1. Developers must consult `docs/Reference_Documentation/README.md` first.
2. Developers must review the relevant source-specific local documentation before code changes.
3. Any newly discovered source constraints/caveats must be added back into the source documentation corpus as part of the same change.

This requirement exists to keep adapter behavior, registry mappings, and reporting logic synchronized with source semantics over time.

---

## 29. Recommended Seed Registries

### 29.1 Seed comparison groups

* TTU vs own history
* TTU vs Tennessee public 4-year
* TTU vs NCES-style selected peers
* TTU vs custom STEM/research peers

### 29.2 Seed eligibility profiles

* NIH AREA-like template
* NSF institutional-capacity template
* USDA/NIFA strengthening template
* ED Title V institutional-development template
* blank custom profile

### 29.3 Seed report presets

* Institutional Overview
* Student Profile and Equity
* Biology Completions Trend
* Program Production by CIP
* Student Success Snapshot
* Affordability Snapshot
* NIH Funding History
* NSF Funding History
* NIFA Funding History
* Benchmark Packet
* Eligibility Worksheet

---

## 30. Final Recommendation

Build this as a **configuration-driven reporting platform**, not a pile of bespoke charts. The durable assets are:

* source adapters
* indicator registry
* program-group registry
* comparison-group registry
* eligibility-profile engine
* preset/report engine

Those are the pieces that survive changing NOFOs, changing sponsor priorities, and changing analyst requests.

The next concrete artifact should be either:

1. a **JSON schema package** for all registries and preset definitions, or
2. a **technical architecture document** with sequence diagrams, adapter contracts, and deployment topology.

[1]: https://nces.ed.gov/ipeds/reported-data/221847?utm_source=chatgpt.com "IPEDS - Department of Education"
[2]: https://grants.nih.gov/grants/guide/pa-files/PAR-25-134.html?utm_source=chatgpt.com "PAR-25-134: Academic Research Enhancement Award ..."
[3]: https://www.nsf.gov/funding/opportunities/capacity-infrastructure-capacity-biological-research/nsf23-580/solicitation?utm_source=chatgpt.com "NSF 23-580: Infrastructure Capacity for Biological ..."
[4]: https://www.nifa.usda.gov/grants/funding-opportunities/resident-instruction-grants-program-institutions-higher-education?utm_source=chatgpt.com "Resident Instruction Grants Program for Institutions ..."
[5]: https://www.ed.gov/grants-and-programs/grants-special-populations/grants-hispanic-students/developing-hispanic-serving-institutions-program-title-v?utm_source=chatgpt.com "Developing Hispanic-Serving Institutions Program - Title V"
[6]: https://nces.ed.gov/ipeds/dfr/2025/ReportHTML.aspx?unitId=221847&utm_source=chatgpt.com "DFR Report HTML - Department of Education"
