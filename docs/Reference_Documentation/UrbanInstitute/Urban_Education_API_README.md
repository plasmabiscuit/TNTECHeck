# Urban Institute Education Data API Reference Pack for TNTECHeck

This pack is a project-oriented reference for the **Urban Institute Education Data Portal API**, with emphasis on the **college-university** section and the datasets/endpoints most relevant to institutional grant work for **TNTECHeck**.

## Primary sources used

Official Urban Institute documentation and Urban-maintained repositories:

- Documentation overview: https://educationdata.urban.org/documentation/
- Colleges documentation page: https://educationdata.urban.org/documentation/colleges.html
- Urban Data Catalog: Colleges data: https://datacatalog.urban.org/dataset/education-data-portal-colleges-data
- Summary endpoints repository: https://github.com/UrbanInstitute/education-data-summary-endpoints
- R package repository: https://github.com/UrbanInstitute/education-data-package-r
- Stata package repository: https://github.com/UrbanInstitute/education-data-package-stata
- Summary endpoint engineering writeup: https://datacatalog.urban.org/building-summary-endpoints-for-the-education-data-portal-139eb7f34fc6

## What is in this pack

1. **Urban_Colleges_API_Overview.md**  
   High-level documentation on API structure, data sources, request patterns, filters, summary endpoints, licensing, and citation guidance.

2. **Urban_Colleges_Endpoint_Inventory.md**  
   College-university endpoint inventory derived from Urban's maintained R package endpoint table.

3. **Urban_Summary_Endpoints.md**  
   Detailed notes on summary endpoint syntax, supported statistics, grouping behavior, filters, and implications for dashboard performance.

4. **Urban_Client_Packages_and_Usage.md**  
   Notes on official R and Stata packages, plus practical Python/JavaScript access patterns for direct URL use.

5. **Urban_TNTECHeck_Implementation_Guide.md**  
   Implementation-focused guidance for how TNTECHeck should use the Urban API for institution profiles, enrollment, completions, finance/aid, and peer/summary views.

## Practical takeaways

- The Urban API is useful as a **normalized institutional-data layer** for colleges, especially around **IPEDS** and selected **College Scorecard** surfaces.
- The **college-university** namespace is the one TNTECHeck should treat as primary for institutional eligibility/profile analysis.
- The official documentation site explains the raw URL structure, while the **R package repo is the most compact source for a usable endpoint inventory**.
- The **summary endpoints** are especially important for dashboard performance, because they let you request aggregated statistics directly instead of pulling large raw files and summarizing them in the app.

## Recommended read order

1. `Urban_Colleges_API_Overview.md`
2. `Urban_Colleges_Endpoint_Inventory.md`
3. `Urban_Summary_Endpoints.md`
4. `Urban_TNTECHeck_Implementation_Guide.md`

## Notes for this project

This pack is written for **TNTECHeck**, not as a generic data-science tutorial. It emphasizes:
- institutional and capacity-grant use cases
- college-level endpoints
- filters and groupings relevant to proposal support
- adapter design and endpoint prioritization for future development
