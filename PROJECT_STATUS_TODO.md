# TNTECheck Project Status & To-Do (Static Review)

_Date: 2026-03-28_

This checklist summarizes what appears complete vs. incomplete based on static inspection of the repository (no runtime verification).

## 1) Completed / In Place

### Core architecture foundations
- [x] Registry-driven backend metadata model exists (`backend/app/data/*.json`, `backend/app/main.py`, `backend/app/registry.py`).
- [x] Source adapter contract and registry are present (`src/tntecheck/adapters/base.py`, `src/tntecheck/adapters/registry.py`).
- [x] TTU-first default identity is encoded in adapter models/normalization (`src/tntecheck/adapters/models.py`, `src/tntecheck/adapters/normalization.py`).

### Backend API surface
- [x] Metadata endpoints implemented:
  - `/api/meta/sources`
  - `/api/meta/indicators`
  - `/api/meta/program-groups`
  - `/api/meta/comparison-groups`
  - `/api/meta/presets`
  - `/api/meta/docs`
  - `/api/meta/eligibility-profiles`
- [x] Program-group CRUD and preview endpoints implemented.
- [x] Comparison-group CRUD endpoints implemented.
- [x] Report run endpoint exists (`POST /api/report/run`) with validation and explicit error responses.

### Frontend scaffolding and flows
- [x] App shell and primary navigation wired (`src/App.jsx`, `src/components/AppLayout.jsx`).
- [x] Preset Catalog page supports filter + launch flow (`src/pages/PresetCatalogPage.jsx`).
- [x] Report Workspace page renders KPI/table/chart/provenance from report payload (`src/pages/ReportWorkspacePage.jsx`).
- [x] Program Group and Comparison Group management UIs are implemented (`src/pages/ProgramGroupsPage.jsx`, `src/pages/ComparisonGroupsPage.jsx`).

### Test coverage present
- [x] Adapter contract tests exist (`tests/test_adapter_contract.py`).
- [x] Backend metadata and report tests exist (`backend/tests/test_meta_endpoints.py`, `backend/tests/test_report_run.py`, CRUD test files).
- [x] Frontend UI tests exist for key pages/flows (`src/test/*.test.jsx`).

---

## 2) Not Completed / Gaps

### Product modules still placeholder-only
- [ ] Explore Builder route is placeholder-only (`/explore-builder`).
- [ ] Eligibility Profile Editor route is placeholder-only (`/eligibility-profiles`).
- [ ] Funding History route is placeholder-only (`/funding-history`).
- [ ] Settings/Admin route is placeholder-only (`/settings`).

### Reporting depth
- [ ] Only `institutional_profile_core` executes in `backend/app/reporting.py`; other presets are not implemented.
- [ ] Report values are seeded/stubbed (no live adapter-backed query execution).
- [ ] Chart output is described as preview-only; no full charting/report rendering pipeline.

### Adapter execution
- [ ] All source adapters are currently stub implementations (`src/tntecheck/adapters/sources/_stub_base.py`).
- [ ] No live remote data pulls, throttling, retries, or partial-failure merge behavior yet.

### Source/registry completeness
- [ ] Registry seed data is intentionally narrow for v1 scaffolding (limited indicators, docs links, presets).
- [ ] Documentation registry currently includes only Urban + NIH entries; missing NCES/IPEDS, College Scorecard, NSF, and NIFA reference links in `backend/app/data/docs.json`.

---

## 3) Known Bugs / Defects to Fix

- [ ] **Home page API mismatch:** frontend calls `/api/metadata/workbench` (`src/services/api.js`) but backend does not define that endpoint (`backend/app/main.py`).
- [ ] **Preset execution mismatch:** `biology_capacity_snapshot` is in preset registry but has no execution path in reporting service, returning PRESET_NOT_IMPLEMENTED.
- [ ] **Comparison group “rule_based_placeholder” cannot resolve to institutions yet:** persisted structure exists, but downstream evaluation/resolution is deferred.

---

## 4) Missing Reference Documentation

- [ ] Add a top-level `README.md` describing architecture, local dev workflow, and backend/frontend startup commands.
- [ ] Add API reference for:
  - program-group CRUD + preview
  - comparison-group CRUD
  - report-run request/response contract and error codes
- [ ] Add developer docs for adapter lifecycle:
  - query model mapping
  - normalization expectations
  - provenance requirements
  - partial-source failure behavior
- [ ] Expand source documentation catalog in `backend/app/data/docs.json` for all declared sources.
- [ ] Add release/status notes describing what is scaffolded vs production-ready.

---

## 5) Recommended Sequencing (What to Focus on Next)

Ordered to align with repository AGENTS guidance and current implementation state:

1. [ ] **Close endpoint contract gaps**
   - implement `/api/metadata/workbench` (or refactor frontend to existing endpoints)
   - ensure frontend/backed contract parity for Home and app-shell bootstrap

2. [ ] **Implement remaining preset execution paths**
   - start with `biology_capacity_snapshot`
   - enforce strict validation of preset-indicator-program/comparison references

3. [ ] **Add adapter-backed data retrieval (incremental)**
   - begin with Urban summary endpoint path for institutional profile metrics
   - keep stubs for other sources but introduce feature flags + partial-failure handling

4. [ ] **Implement rule-based comparison-group resolver**
   - convert placeholder rules into resolved institution sets at run time (or persisted snapshots)

5. [ ] **Build Eligibility Profile editor/evaluator module**
   - editable criteria UI + backend evaluate endpoint
   - include provenance, override notes, and non-final-compliance disclaimer

6. [ ] **Expand documentation + provenance guarantees**
   - fill docs registry coverage
   - publish API and adapter docs
   - include calculation/source notes consistently in report outputs

7. [ ] **Richer exports and reporting polish**
   - CSV/JSON export hardening
   - narrative generation templates
   - print/PDF packet generation

---

## 6) Tracking Checklist (Actionable)

### Immediate (1–2 sprints)
- [ ] Fix `/api/metadata/workbench` contract.
- [ ] Execute second preset end-to-end (`biology_capacity_snapshot`).
- [ ] Add docs registry entries for all seeded sources.
- [ ] Add README + API contract docs.

### Near-term (3–5 sprints)
- [ ] Introduce first live adapter integration (Urban summary path).
- [ ] Implement eligibility editor + evaluator.
- [ ] Resolve rule-based comparison groups beyond placeholder storage.

### Later
- [ ] Build advanced explore/query builder.
- [ ] Implement sponsor-focused funding history module.
- [ ] Add richer exports and report packet assembly.
