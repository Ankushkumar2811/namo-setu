# NAMO SETU system specification

## Context

```mermaid
flowchart LR
  People[Devotees and families] --> Edge[Web / mobile edge]
  Partners[Temples and partners] --> Edge
  Admins[Government and operations] --> Edge
  Edge --> API[API gateway and FastAPI services]
  API --> PG[(PostgreSQL)]
  API --> Redis[(Redis)]
  API --> Search[(Search + Qdrant)]
  API --> Queue[RabbitMQ / streams]
  Queue --> Workers[Notification, media, AI, reports]
  Workers --> Providers[Payments, maps, weather, messaging, storage]
```

## Service boundaries

Identity controls credentials, sessions, consent and permissions. Catalogue controls temples, festivals, stays, guides and geographic services. Commerce controls booking, inventory, payments, refunds and ledgers. Experience controls crowd, weather, routes and realtime alerts. Engagement controls notifications, CMS, support, CRM and rewards. Intelligence controls RAG, agents, memory and evaluation. Operations controls tenant administration, audit, analytics and reports.

Services initially deploy as a modular monolith with strict internal boundaries and one transaction database. High-throughput projections, media, notifications and AI workers scale independently. A module may become a service only after its data ownership and operational profile require it.

## Critical sequences

### Booking and payment

```mermaid
sequenceDiagram
  participant U as User
  participant B as Booking API
  participant D as Database
  participant P as Payment Provider
  participant W as Webhook API
  participant Q as Outbox Worker
  U->>B: Create booking + idempotency key
  B->>D: Lock and reserve inventory
  B-->>U: Pending booking + payment order
  U->>P: Hosted payment
  P->>W: Signed event
  W->>D: Verify event id, update payment/booking atomically
  D-->>Q: Outbox booking.confirmed
  Q-->>U: Receipt and notifications
```

### AI planner

```mermaid
sequenceDiagram
  participant U as User
  participant O as Orchestrator
  participant K as Knowledge retrieval
  participant A as Specialist agents
  participant M as Model gateway
  U->>O: Travel request
  O->>O: Safety and intent checks
  O->>K: Hybrid retrieval with tenant/date filters
  K-->>O: Evidence with provenance
  par Specialists
    O->>A: Temple, route, stay, health, family
    A->>M: Strict structured requests
  end
  A-->>O: Reports, confidence, proposed actions
  O-->>U: Grounded plan, citations, backup and confirmations
```

### Emergency

The client immediately displays cached emergency guidance and verified national/local numbers. The API records a consented alert, notifies selected family members and routes to the emergency provider. AI may translate or summarize context but never delays, suppresses or autonomously closes the alert.

## Non-functional requirements

- Availability: 99.99% for identity, booking and emergency paths.
- Latency: p95 API reads under 300ms; booking writes under 800ms excluding providers.
- Durability: zero acknowledged ledger loss; commerce RPO ≤5 minutes.
- Capacity: horizontal scaling to 50M monthly API requests without schema redesign.
- Security: least privilege, MFA for privileged roles, encryption in transit/at rest and immutable audit.
- Accessibility: WCAG 2.2 AA across web and mobile.
- Privacy: DPDP purpose limitation, consent evidence, export, correction and deletion workflows.

## Communication

Synchronous internal calls use HTTP with deadlines and request IDs. Durable business changes use an outbox and versioned events. Redis Streams handles low-latency fan-out; RabbitMQ handles durable jobs, priorities, retries and dead letters. Event consumers are idempotent.

## Caching

| Cache | Key pattern | TTL | Invalidation |
|---|---|---:|---|
| Temple | `temple:v1:{id}:{locale}` | 15 min | Catalogue event |
| Search | `search:v1:{hash}` | 2 min | Index version |
| Crowd | `crowd:v1:{temple}` | 30 sec | New observation |
| Weather | `weather:v1:{geohash}` | 10 min | Provider refresh |
| Maps | `route:v1:{origin}:{destination}:{mode}` | 5 min | Road alert |
| AI | `ai:v1:{knowledgeVersion}:{promptHash}` | 1 hour | Knowledge/prompt version |
| User | `profile:v1:{user}` | 5 min | Profile event |

Payment, wallet and available inventory are never trusted solely from cache.

## Search and vector design

Elasticsearch indexes verified catalogue documents with Hindi/English analyzers, edge n-grams for autocomplete and geo points for nearby search. Qdrant collections separate public knowledge from user-private memory. Payload filters enforce locale, authority, validity dates, tenant and user ownership. Embedding versions coexist during migration; indexes record source checksum and model version.
