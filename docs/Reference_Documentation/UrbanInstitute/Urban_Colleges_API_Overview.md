# Urban Colleges API Overview

## 1. What the Urban API is

The Urban Institute's **Education Data Portal API** exposes education data in **JSON** and supports direct browser/URL access as well as access through Urban-maintained **R** and **Stata** packages. The documentation also notes direct use from **Python** and **JavaScript** by calling endpoint URLs.

At the college level, the portal's **college-university** section combines institutional data from multiple sources, especially:

- **IPEDS** (Integrated Postsecondary Education Data System)
- **College Scorecard**
- other college-related sources such as **FSA**, **EADA**, **NACUBO**, **NCCS**, **NHGIS**, and campus crime data

The Urban Data Catalog describes the colleges database as an **institution-level** database built around **IPEDS**, and notes that the scorecard portion is kept distinct because College Scorecard itself includes information from multiple sources, including IPEDS.

## 2. College-level subject matter

Urban's colleges documentation and data catalog describe the college-university coverage as including topics such as:

- institutional characteristics
- admissions
- enrollment
- completions
- graduation rates
- program charges / tuition
- student financial aid
- faculty and staff
- finances
- student loan repayment and earnings (via College Scorecard)

For TNTECHeck, that means Urban is suitable as a core public-data layer for:
- institutional profiles
- student pipeline/enrollment context
- completions by field
- affordability/aid context
- selected outcomes and repayment/earnings context
- peer comparison and time-series summaries

## 3. General endpoint structure

Urban's documentation gives the raw endpoint pattern as:

```text
https://educationdata.urban.org/api/v1/{topic}/{source}/{endpoint}/{year}/[additional_specifiers_or_disaggregators]/[optional filters]
```

Examples from the documentation:

```text
https://educationdata.urban.org/api/v1/schools/ccd/directory/2013/
https://educationdata.urban.org/api/v1/schools/ccd/enrollment/2013/grade-3/
```

For colleges, the first path component is generally:

```text
college-university
```

So the mental model for TNTECHeck should be:

```text
/api/v1/college-university/{source}/{topic}/{year}/...
```

Examples based on the college endpoint inventory include paths such as:

```text
/api/v1/college-university/ipeds/directory/2022/
/api/v1/college-university/ipeds/completions-cip-6/2022/
/api/v1/college-university/scorecard/default/2020/
```

## 4. Specifiers, disaggregators, and filters

Urban distinguishes between:
- **path components** that act as required specifiers or disaggregators
- **query-string filters** appended at the end of the URL

The documentation states that filters are appended as:

```text
?filter_variable=filter_value
```

and multiple filters are joined with `&`, for example:

```text
?charter=1&fips=11
```

This matters because many college endpoints have required subtopics/disaggregators such as:
- `race`
- `sex`
- `age`
- `residence`
- `level_of_study`
- `aid-applicants`
- `home-neighborhood`

TNTECHeck should therefore model an Urban endpoint as a combination of:
1. section (`college-university`)
2. source
3. topic
4. year
5. optional path subtopic(s)
6. optional filter set

## 5. Summary endpoints

Urban provides **summary endpoints** for selected datasets, allowing users to request statistics such as sums, averages, medians, and counts without retrieving the raw detail table.

This is important for dashboard work because summary endpoints are designed to avoid pulling large record sets just to aggregate them client-side.

See `Urban_Summary_Endpoints.md` for details.

## 6. Data sources that matter most for TNTECHeck

### 6.1 IPEDS
This is the core source for institutional grant-support analytics:
- directory
- institutional characteristics
- admissions
- enrollment
- completions
- graduation and retention
- student financial aid
- tuition / room / board / program charges
- finance
- staffing and faculty-related measures

### 6.2 College Scorecard
Urban includes scorecard slices such as:
- default
- earnings
- institutional-characteristics
- student-characteristics / aid-applicants
- student-characteristics / home-neighborhood
- repayment

This makes the Urban API useful as a bridge between IPEDS institutional metrics and selected scorecard outcome/repayment context.

### 6.3 FSA and other adjunct sources
Urban's endpoint inventory also includes:
- FSA grants, loans, financial responsibility, campus-based volume, and 90/10 revenue percentages
- EADA institutional characteristics
- NACUBO endowments
- NCCS 990 forms
- NHGIS census-linked contextual endpoints
- campus crime data

These are not your first-line endpoints for every NOFO, but they are highly relevant for institutional-capacity and context narratives.

## 7. Access methods

Urban's official documentation explicitly supports:
- direct URL/API access
- R package access
- Stata package access

The docs also note Python and JavaScript examples that directly access endpoint URLs. For TNTECHeck, that means you do **not** need a special SDK to use the API from a web app; plain HTTP requests are enough.

## 8. Pagination and response size

Urban's FAQ notes that the API limits responses to **10,000 records per page**. Full retrieval across multiple pages requires iterating through additional pages / `next` links, while Urban's R and Stata tooling handles this automatically.

For TNTECHeck, this means:
- raw endpoint pulls can require pagination
- summary endpoints are preferable where possible
- your adapter layer should own pagination so frontend code does not need to

## 9. Licensing and citation

Urban's documentation states that Education Data Portal data are licensed under the **Open Data Commons Attribution License (ODC-By) v1.0** and provides recommended citation language.

TNTECHeck should preserve:
- source dataset name
- Urban portal reference
- version/date accessed
- endpoint URL or derived query metadata

## 10. Recommended interpretation for TNTECHeck

Urban should be treated as:
- a **primary public data adapter** for institution-level college reporting
- a faster/more convenient alternative to wrangling many raw federal source files directly
- the best first stop for **IPEDS + selected Scorecard** use cases
- a source that still requires a registry of endpoint capabilities, years, filters, and caveats

It should **not** be treated as a magical abstraction that eliminates the need to understand IPEDS/Scorecard semantics. Urban makes access easier; it does not remove the need for domain interpretation.
