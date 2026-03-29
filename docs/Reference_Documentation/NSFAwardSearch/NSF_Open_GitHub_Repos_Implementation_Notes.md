# NSF Open GitHub Repositories — Implementation Notes for TNTECheck

Last verified: **2026-03-28 (UTC)**

This document summarizes useful patterns from three official NSF Open GitHub repositories and maps them to TNTECheck's registry-driven, no-auth v1 architecture.

## Repositories reviewed

1. `nsf-open/nsf-rest-api`
2. `nsf-open/ms-sb-archetype`
3. `nsf-open/nsf-ember-psm`

---

## Why these repositories matter

Even though these repositories are older and not drop-in for TNTECheck, they provide reusable patterns for:

- API client layering and response extraction.
- Error envelope conventions.
- Property/endpoint registry style frontend configuration.
- Service boundaries between UI and source-specific transport logic.

These patterns align with TNTECheck non-negotiables to preserve clean frontend/backend separation and avoid source-specific query logic in frontend components.

---

## Repo 1: `nsf-rest-api` (Java REST client component)

### Observed structure

- Contains reusable REST client, authorization strategies, response extractors, and envelope models under `gov.nsf.components.rest`.
- Includes test/example `AwardServiceClientImpl` and `AwardService` interface for `/awards` interactions.

### Useful patterns for TNTECheck

1. **Client abstraction + extractors**
   - Pattern: keep transport and parsing logic centralized (`NsfRestClient`, extractor classes) rather than scattering parse logic.
   - TNTECheck application:
     - Keep NSF adapter normalization in backend adapter modules.
     - Avoid duplicating field extraction logic across report handlers.

2. **Model/collection response extraction by path**
   - Pattern: typed extractors (`ModelExtractor`, `ListExtractor`) target response members like `award` or `awards`.
   - TNTECheck application:
     - Keep a deterministic normalization map from NSF payload keys to internal indicator keys.

3. **Config-driven base URL in client wiring**
   - Pattern: endpoint base URL injected in XML test config (`awardServiceURL`).
   - TNTECheck application:
     - Keep NSF source base URL and version in backend environment/config registry, not in frontend components.

### Caveats

- Uses older Spring/Jackson stack and legacy build assumptions.
- Example code sets PDF content type in one GET method; treat examples as structural, not canonical API behavior.

---

## Repo 2: `ms-sb-archetype` (NSF microservice Spring Boot template)

### Observed structure

- Maven archetype creates multi-module service layout (`-service`, `-service-api`, `-service-impl`, `-service-client`, `-service-war`).
- Controller templates emit Ember-style JSON wrappers via `EmberModel`.
- Includes Swagger setup and standardized exception-to-response mapping.

### Useful patterns for TNTECheck

1. **Clear layer boundaries**
   - Pattern: separate API model, service implementation, and client concerns.
   - TNTECheck application:
     - Preserve adapter contracts and keep report/preset execution orchestration separate from source call details.

2. **Consistent error envelope**
   - Pattern: base controller maps validation/not-found/server exceptions to structured response messages.
   - TNTECheck application:
     - Standardize backend source-failure payloads so partial-source failures are explainable and machine-readable.

3. **Generated controller conventions**
   - Pattern: canonical CRUD route naming and API annotation conventions.
   - TNTECheck application:
     - Reuse consistency principle for metadata endpoints and report execution APIs (predictable path grammar, error shapes).

### Caveats

- Archetype template includes optional/basic auth pattern under `/auth/**` and `security.basic.*`.
- **Do not adopt authentication pattern for TNTECheck v1**, per project non-negotiables.

---

## Repo 3: `nsf-ember-psm` (Ember frontend reference)

### Observed structure

- README explicitly notes open-source version is reference-only (required URLs/config removed).
- Frontend service layer centralizes HTTP calls (`app/api/service.js`) and reads endpoint templates from a properties service.
- Business services (example: `funding-opportunities`) call the API service rather than issuing direct ad hoc requests.

### Useful patterns for TNTECheck

1. **Frontend endpoint registry/config indirection**
   - Pattern: property keys -> URL template expansion (`getReplace`).
   - TNTECheck application:
     - Keep metadata-driven endpoint selection in one place in frontend service utilities.

2. **Centralized auth/header and transport hook point**
   - Pattern: one API service applies headers/options for every request.
   - TNTECheck application:
     - Even in no-auth v1, central transport wrapper can enforce trace headers, timeout defaults, and consistent error translation.

3. **Service-per-domain UI integration**
   - Pattern: domain services consume the API abstraction.
   - TNTECheck application:
     - Keep UI feature modules consuming backend metadata/report endpoints only, with no source-specific request syntax in components.

### Caveats

- Stack is old (Node 6/Ember 2.18 era) and not directly modernizable by copy/paste.
- `mirage/config.js` is removed in public snapshot, so mock API behavior is incomplete.

---

## TNTECheck-focused action items derived from these repos

1. **Document and enforce adapter response envelopes**
   - Add/confirm a shared backend error/warning schema for source adapters (including partial-failure provenance).

2. **Strengthen source-config centralization**
   - Ensure NSF base URLs/version knobs live only in backend source config (plus metadata visibility), not UI code.

3. **Keep frontend service-only data access pattern**
   - Ensure frontend components consume metadata/report services and never construct NSF query strings directly.

4. **Add regression tests around normalized NSF shapes**
   - Introduce fixtures for award list/single response extraction mapped into indicator registry IDs.

---

## Retrieval evidence (commands used)

```bash
curl -s https://api.github.com/repos/nsf-open/nsf-rest-api | jq -r '.default_branch, .pushed_at, .description'
curl -s https://api.github.com/repos/nsf-open/ms-sb-archetype | jq -r '.default_branch, .pushed_at, .description'
curl -s https://api.github.com/repos/nsf-open/nsf-ember-psm | jq -r '.default_branch, .pushed_at, .description'

curl -L -s https://raw.githubusercontent.com/nsf-open/nsf-rest-api/main/pom.xml
curl -L -s https://raw.githubusercontent.com/nsf-open/nsf-rest-api/main/src/test/java/gov/nsf/components/rest/example/client/AwardServiceClientImpl.java
curl -L -s https://raw.githubusercontent.com/nsf-open/nsf-rest-api/main/src/test/resources/config/awardservice-client-config.xml

curl -L -s https://raw.githubusercontent.com/nsf-open/ms-sb-archetype/main/src/main/resources/META-INF/maven/archetype-metadata.xml
curl -L -s https://raw.githubusercontent.com/nsf-open/ms-sb-archetype/main/src/main/resources/archetype-resources/__artifactIdInLowerCase__-service/src/main/java/__artifactIdInLowerCase__/config/SecurityConfiguration.java
curl -L -s https://raw.githubusercontent.com/nsf-open/ms-sb-archetype/main/src/main/resources/archetype-resources/__artifactIdInLowerCase__-service/src/main/java/__artifactIdInLowerCase__/controller/__mainPojo__ServiceBaseController.java

curl -L -s https://raw.githubusercontent.com/nsf-open/nsf-ember-psm/master/README.md
curl -L -s https://raw.githubusercontent.com/nsf-open/nsf-ember-psm/master/app/api/service.js
curl -L -s https://raw.githubusercontent.com/nsf-open/nsf-ember-psm/master/app/services/properties.js
curl -L -s https://raw.githubusercontent.com/nsf-open/nsf-ember-psm/master/package.json
```

---

## Provenance and trust notes

- All three repositories are under the official `nsf-open` GitHub organization.
- Latest upstream push timestamps (as of 2026-03-28 UTC) indicate these are best treated as **reference architecture artifacts**, not current runtime dependencies.
