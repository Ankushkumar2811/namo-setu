# Backend architecture

```text
Client → CDN/WAF → API gateway → FastAPI services → PostgreSQL
                            ↘ Redis cache/event fan-out
                            ↘ worker queue → notifications/media/AI
                            ↘ search index and vector store
```

Controllers validate transport DTOs. Services own business transactions. Repositories isolate persistence. Events publish only after database commit through an outbox worker. External payments, maps, messages, media and AI providers are accessed through replaceable adapters.

## Data domains

Identity owns users, roles, permissions, sessions, devices, OTP and refresh tokens. Catalogue owns temples, stays, guides, pujas, festivals and geographic data. Commerce owns bookings, items, payments, invoices, refunds, coupons and wallet ledger. Engagement owns notifications, community, content, reviews and rewards. Intelligence owns conversations, preferences, memory and generated plans. Operations owns audit, feature flags, analytics and reporting.

## Reliability

- Multi-AZ PostgreSQL with point-in-time recovery and tested restore drills
- Redis cluster with graceful cache bypass
- Idempotent writes and provider webhooks
- Transactional outbox for at-least-once event delivery
- Exponential retry with dead-letter queues
- Request IDs propagated into logs, jobs and downstream calls
- SLOs: 99.95% API availability; p95 reads under 300ms

## Payment sequence

Client creates booking → API reserves inventory → payment order created → client completes hosted payment → signed webhook verified → payment and booking updated atomically → outbox emits confirmation → receipt and notifications generated asynchronously.

## API conventions

Resources are plural, versioned under `/api/v1`, and return structured errors. Collections support `page`, `page_size`, filters and stable sorting. Mutating commerce endpoints require idempotency keys. Administrative routes require role and permission checks in both service and repository queries.
