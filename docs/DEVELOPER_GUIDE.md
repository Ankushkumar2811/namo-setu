# Developer guide

## Local setup

Install Node 22 and Python 3.13. Run `npm ci`, `npm run typecheck` and `npm run build` for the web app. In `backend`, create a virtual environment and run `pip install ".[test]"`. Copy `.env.example` to `.env`, replace development secrets and start PostgreSQL/Redis with Compose. Apply Alembic migrations before starting Uvicorn.

## Quality gates

Pull requests must pass frontend type/build/audit, backend fatal lint/tests, CodeQL, container build and fixable high/critical vulnerability scanning. Schema changes include migrations, rollback/forward-repair notes and query-plan evidence for large tables. Public API changes update OpenAPI and collections in the same commit.

## Naming

Routes and JSON use snake_case; resource URLs use plural nouns. Python modules and functions use snake_case, classes use PascalCase. Events use `domain.action.vN`. Cache keys start with module and schema version. Database constraints follow the configured naming convention.

## Integration testing

Use provider sandboxes and signed fixtures. Webhook fixtures retain exact raw bytes. Payment tests assert idempotency, replay and reconciliation. AI tests use recorded provider-neutral outputs and separately gated live evals; production keys are never required for unit tests.

## Documentation ownership

Runtime FastAPI OpenAPI is authoritative for implemented endpoints. `docs/openapi.yaml` is the reviewed external subset. Database and system specifications describe target-state boundaries; an architecture decision record is required when implementation intentionally diverges.
