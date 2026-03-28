# NIFA Data Gateway Status and Fiscal-Year Handling Notes

## Why this exists

NIFA Data Gateway surfaces combine project, award, and financial contexts. Fiscal-year semantics and status timing differ by context, so adapter/report logic must preserve those distinctions.

## Official signals from NIFA documentation

### A. Fiscal-year range and history claims
- Data Gateway page states Recent Awards history runs from FY2002 to present.
- Data Gateway page describes Award Trends as FY02 to present.
- Data Gateway Fact Sheet (2015) also describes FY2002-to-present coverage for Recent Awards.

### B. Status/timing behavior from LMD user guidance
From the Basic Navigation in LMD guide:
- Capacity/formula data is reported as **expenditures** after fiscal-year closeout.
- Non-capacity/competitive award data is reported as **obligations** during fiscal year.
- Some financial data remains estimated until closeout/cross-cut processes finalize actuals.

## Observed cube-specific year dimensions (from official portal script)

From `/lmd4/projects` page script metadata:

- `Awards` cube year dimensions include:
  - `Appropriation Fiscal Year` (2002..2026 observed)
  - `Award Fiscal Year` (2002..2026 observed)
  - `Submission Fiscal Year` (2001..2026 observed)
- `Budget` cube year dimension includes `Appropriation Fiscal Year`.
- `Projects` cube uses `Year` (2007..2023 observed in the inspected payload).

## Adapter rules (recommended)

1. Keep fiscal-year dimensions separate in normalized output:
   - `appropriation_fiscal_year`
   - `award_fiscal_year`
   - `submission_fiscal_year`
   - `project_year` (where applicable)
2. Add provenance flags for timing/closure assumptions when a record comes from a financial cube that may contain estimated values.
3. Avoid mixing project-year trend lines with award-fiscal-year trend lines without explicit conversion rules.
4. Surface partial-source warning states if one module responds and another fails.

## Known inconsistency/risk notes (current)

- Public module data endpoints are not documented with a formal API contract in the official docs above; endpoint behavior should be smoke-tested periodically.
- At retrieval time, module pages expose endpoint paths in script configuration, but some data routes can return server errors depending on required query context.

## Verification stamp

Validated against official pages and docs on **March 28, 2026 (UTC)**.
