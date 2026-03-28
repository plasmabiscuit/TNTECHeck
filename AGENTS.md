# TNTECheck - TTU Grant Data Workbench — AGENTS.md

## Mission
Build a no-auth, TTU-first institutional analytics application for grant-development support.

## Source of truth
The functional spec in this repository is the primary product contract.
Prefer implementing the architecture described there over ad hoc shortcuts.

## Architectural non-negotiables
1. Do not add user authentication or RBAC in v1.
2. Do not hardcode NOFO-specific eligibility logic.
3. Preserve the registry-driven design:
   - source adapters
   - indicator registry
   - program-group registry
   - comparison-group registry
   - eligibility-profile engine
   - preset/report engine
4. Keep TTU as the default institution context.
5. Preserve clean frontend/backend separation.
6. Do not place source-specific query logic in frontend components.

## Data-model expectations
- Public completions are CIP-based, not department-based.
- Department views must flow through local program-group mappings.
- Eligibility profiles are editable starting points, not final compliance truth.

## Preferred implementation order
1. seed registries
2. source adapter contracts
3. metadata endpoints
4. preset/report execution path
5. comparison/program-group handling
6. eligibility editor/evaluator
7. richer exports


## Documentation-first rule for source work
Before developing or debugging any feature that touches a data source, adapter, indicator mapping, or source-backed report:
1. Start at `docs/Reference_Documentation/README.md`.
2. Open the relevant source folder documentation before changing code.
3. Validate fields/constraints/caveats against source docs and preserve provenance in outputs/tests.
4. If docs are missing or outdated, update documentation in the same change as the code fix.

## Coding expectations
- Make the smallest coherent change.
- Add or update tests for anything affecting adapters, registries, eligibility logic, or reporting.
- Keep provenance visible in outputs.
- Prefer summary endpoints where available.
- Handle partial-source failure gracefully.

## Validation steps
Before considering work complete, run the relevant subset of:
- frontend tests
- backend tests
- lint/format
- any source smoke tests
- build/type checks
