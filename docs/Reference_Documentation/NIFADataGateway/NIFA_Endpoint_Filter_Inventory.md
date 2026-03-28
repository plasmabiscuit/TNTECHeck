# NIFA Data Gateway Endpoint and Filter Inventory

## Provenance

All entries below were validated against official USDA/NIFA pages and portal assets retrieved on **March 28, 2026 (UTC)**.

## 1) Official module-level surfaces

### A. Data Gateway public page
- URL: https://www.nifa.usda.gov/data/data-gateway
- Official scope statement: Data Gateway provides access to NIFA-funded project and award information and related metrics.
- Public modules listed from this page include:
  - Recent Awards
  - Congressional District
  - Knowledge Area
  - Subject of Investigation
  - Field of Science
  - Award Trends
  - Enterprise Search launch

### B. Data Gateway Resource Page
- URL: https://www.nifa.usda.gov/data/data-gateway/data-gateway-resource-page
- Official support docs linked from this page include:
  - Project Details Search Highlights (PDF)
  - Financial Details Search Highlights (PDF)
  - Advanced Search Highlights (PDF)

## 2) Public endpoint patterns observed from portal page source

> Important: these are **observed public endpoint patterns** from NIFA-managed pages, not a separately published OpenAPI contract.

### A. Recent Awards page and data endpoint
- UI page: `https://portal.nifa.usda.gov/lmd4/recent_awards`
- Data JSON endpoint pattern: `https://portal.nifa.usda.gov/lmd4/recent_awards/get_data.js`
- CSV endpoint pattern: `https://portal.nifa.usda.gov/lmd4/recent_awards/get_data.csv`

Observed default payload metadata includes:
- headers: `Award Date`, `Grant Number`, `Proposal Number`, `Grant Title`, `State Name`, `Grantee Name`, `Award Dollars`, `Program Name`, `Program Area Name`, `Public Flag`
- total row count key: `totalRows`
- page key: `page`
- column filter object: `columnFilters`

Observed default request-side query model (from page script init):
- `filters`
- `row_filter`
- `column_filter`
- `measure_name`

### B. Projects page and data endpoint pattern
- UI page: `https://portal.nifa.usda.gov/lmd4/projects`
- Data JSON endpoint pattern in page script: `/projects/get_data.js`
- CSV endpoint pattern in page script: `/projects/get_data.csv`

Observed configured filterable columns in page script include:
- `Accession Number`, `Type`, `Grantee Name`, `Title`, `Keywords`, `Program Code`, `Program Code Name`, `Program Area Code`, `Program Area Name`, `Multistate Project Number`, and recency counters (`Most Recent Progress`, `Most Recent Impact`, `Most Recent Publications`, `All Progress`, `All Impact`, `All Publications`).

## 3) Filter dimensions and cube metadata observed from official page script

The `/lmd4/projects` page script publishes data-cube metadata used by the UI. This includes:

- `MEASURES` across cubes such as `Awards`, `Budget`, `Budgeted Awards`, `Projects`, `Areera Pow Annual Financials`, and `Areera Pow Outcomes`.
- `YEAR_DIMENSIONS_BY_CUBE` enumerating available fiscal/calendar ranges by cube.
- `FILTER_NAMES_TO_DIMENSIONS` mapping user-facing filter names to underlying dimension keys.

High-value filter names for adapter design (Awards/Projects cubes):

- Awards: Appropriation Fiscal Year, Award Fiscal Year, Submission Fiscal Year, Award Grantee Name, Award Grantee Location, Award Grantee Type, Grant Program, Treasury Symbol, Earmark Flag, Mandatory Funding Flag.
- Projects: Year, State, Grantee Name, Grantee Location, Grantee Type, Sponsoring Agency, Science, Subject, Grant Program, Portfolio, Funding Source.

## 4) Query behavior notes from official PDFs

From **Advanced Search Highlights** and **LMD Basic Navigation**:

- Advanced search supports field conditions including OR, NOT, exact query expression matching, and missing-value tests.
- Wildcards are allowed in query-expression style matching.
- Users can append nested groups of conditions (group-level Boolean logic).
- Export to CSV is a first-class workflow in project-level result pages.

## 5) Adapter-facing cautions

1. Treat endpoint structures as operationally discoverable and monitor for changes; there is no public OpenAPI schema in the official docs above.
2. Distinguish between:
   - interactive module pages (`/lmd4/<module>`), and
   - data payload routes (`/lmd4/<module>/get_data.js` and `/get_data.csv`).
3. Persist source provenance in output metadata whenever feasible:
   - module/page URL,
   - retrieval date,
   - applied filters.
