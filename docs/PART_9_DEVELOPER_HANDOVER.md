# NAMO SETU — Developer workflow and handover

```mermaid
flowchart LR
  O[Business outcome] --> J[Journey/acceptance]
  J --> T[Threat/privacy model] --> C[Command/query]
  C --> A[API/event contract] --> D[Schema/migration]
  D --> I[Implementation] --> X[Tests]
  X --> R[Review/CI] --> P[Progressive release] --> M[Metrics/audit/feedback]
```

Before coding, identify aggregate owner, valid states, authorization/resource policy, idempotency boundary, PII class, audit event and failure recovery. UI, cache and provider redirects are never authoritative.

## Ready and done

Ready means purpose, actors, preconditions, main/alternative/error/edge flows, contracts, data owner/retention/indexes, migration, SLO/capacity, observability, security/privacy/accessibility/localization, and provider timeout/retry/reconciliation/fallback are testable.

Done means server-side invariants, unit/database/contract/E2E tests, concurrency/idempotency/out-of-order tests, negative tenant/owner authorization tests, logs/metrics/traces/runbook, compatible migration/recovery, updated API/workflow docs, accessibility/performance and security checks all pass.

## Local development

```text
npm install
npm run typecheck
npm run build
npm run dev

cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Use the environment inventory only as a template and retrieve development secrets through the approved manager. Seed data must be synthetic; never copy production identities, money data, prompts or tickets.

| Layer | Required evidence |
|---|---|
| Domain | Transitions, price/ledger arithmetic, policy/time edges |
| API | Schema, auth, idempotency, pagination, errors/rate limit |
| Database | Constraints, indexes, isolation and migration compatibility |
| Events | Compatibility, dedupe, retry, poison/out-of-order |
| Providers | Signature, timeout, breaker, reconciliation, sandbox |
| AI | Grounding/citations/constraints/injection/language/fallback |
| UI/E2E | Registration, discovery, simulated payment, QR, SOS, accessibility |
| Operations | Dashboard, alert, restore, rollback and incident drill |

Additive APIs remain in-version; breaking contracts get a version/migration window. Financial corrections are compensations. Schema evolution adds, backfills with checkpoints, switches reads, then removes after compatibility. AI releases identify prompt/model/retrieval/embedding versions.

Handover includes decisions, contracts, classification, provider contacts, SLOs, alerts, runbooks, restore evidence, risks, costs, release/rollback, access and open incidents. Ownership completes after the receiving team performs a supervised deployment and incident exercise.
