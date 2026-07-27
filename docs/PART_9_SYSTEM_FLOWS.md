# NAMO SETU — System flows and diagrams

## Architecture

```mermaid
flowchart TB
  subgraph Channels
    Web[Web/PWA]
    Mobile[Mobile]
    Admin[Admin portal]
    Partner[Partner portals]
    Scanner[QR scanner]
  end
  Channels --> CDN[CDN/WAF] --> Gateway[API gateway]
  Gateway --> IAM[Identity/policy]
  Gateway --> Catalog[Catalogue/discovery]
  Gateway --> Commerce[Booking/payment/wallet/donation]
  Gateway --> Experience[Planner/crowd/emergency]
  Gateway --> Engage[Notification/support/loyalty]
  Gateway --> Ops[Admin/audit/analytics]
  Experience --> AI[AI orchestrator]
  IAM & Catalog & Commerce & Experience & Engage & Ops --> PG[(PostgreSQL)]
  Catalog & Experience --> Redis[(Redis)]
  Catalog --> Search[(Search)]
  AI --> Vector[(Vector DB)]
  IAM & Catalog & Commerce & Experience & Engage & Ops --> Outbox[Outbox]
  Outbox --> MQ[Queue/stream] --> Workers[Workers] --> Providers[Payment/maps/weather/message/video/calendar]
  PG --> ETL[CDC/ETL] --> Warehouse[(Warehouse)]
```

The initial system is a modular monolith with strict bounded contexts and independently scalable workers. A boundary becomes a microservice only when ownership, scale or fault isolation warrants it.

## Data-flow diagrams

### Level 0

```mermaid
flowchart LR
  U[Devotee/family] <-->|identity, discovery, plan, booking, SOS| N((NAMO SETU))
  P[Partners] <-->|catalogue, inventory, fulfillment, settlement| N
  A[Admin/support] <-->|governance, cases, reports| N
  G[Payment gateway] <-->|orders, signed events, refunds| N
  X[Maps/weather/message/video] <-->|query and delivery status| N
  R[Responders/family] <-->|SOS and acknowledgement| N
```

### Level 1

```mermaid
flowchart TB
  U[User] --> P1((1 Identity/consent))
  U --> P2((2 Discover/plan))
  U --> P3((3 Book/pay))
  U --> P4((4 Engage/emergency))
  PT[Partner] --> P5((5 Supply/fulfill))
  AD[Admin] --> P6((6 Govern/support))
  P1 <--> D1[(Identity)]
  P2 <--> D2[(Catalogue/search/vector)]
  P3 <--> D3[(Commerce/ledger)]
  P4 <--> D4[(Engagement/incidents)]
  P5 <--> D2
  P5 <--> D3
  P6 <--> D5[(Audit/analytics)]
  P1 & P2 & P3 & P4 & P5 & P6 --> E[Events/queues]
```

### Level 2 — booking

```mermaid
flowchart LR
  U[User] --> S[3.1 Search offer] --> C[(Catalogue)]
  U --> H[3.2 Hold inventory] <--> I[(Inventory)]
  H --> Q[3.3 Snapshot quote] --> B[(Booking)]
  Q --> O[3.4 Payment order] --> G[Gateway]
  G --> W[3.5 Verify webhook]
  W --> P[(Payments)]
  W --> L[(Ledger)]
  W --> F[3.6 Confirm] --> B
  F --> E[(Outbox)] --> N[3.7 QR/invoice/notification]
```

## Low-level component design

```mermaid
flowchart LR
  Route[HTTP route] --> Schema[Schema] --> Auth[Authentication]
  Auth --> Policy[RBAC/resource/tenant policy]
  Policy --> App[Application command/query]
  App --> Domain[Aggregate/invariants]
  Domain --> Repo[Repository/UoW] --> DB[(PostgreSQL)]
  Domain --> Event[Domain event] --> Outbox[(Outbox)]
  Outbox --> Consumer[Idempotent consumer]
  Consumer --> Adapter[Provider adapter] --> External[Provider]
  Consumer --> Projection[Cache/search/analytics]
```

Routes handle transport; application services coordinate; aggregates enforce transitions. Adapters have deadlines, bounded retries and circuit breakers. Logs/traces carry request, correlation, actor and tenant identifiers.

## Deployment, network and security

```mermaid
flowchart TB
  Internet --> DNS[DNS/CDN/DDoS] --> WAF[WAF/rate limit] --> LB[Public load balancer]
  subgraph Private application network
    LB --> API[API autoscaling]
    API --> Worker[Worker pools]
    API & Worker --> Cache[(Redis)]
    API & Worker --> DB[(Multi-AZ PostgreSQL)]
    Worker --> Search[(Search/vector)]
    API & Worker --> Egress[NAT/egress allowlist]
  end
  Egress --> SaaS[Approved providers]
  DB --> Replica[(Replica)]
  DB --> Backup[Encrypted cross-region backup]
  API & Worker --> Obs[Metrics/logs/traces/SIEM]
  AdminSSO[Admin SSO/VPN] --> Control[Management plane] --> API
```

Only CDN/WAF and the load balancer accept public ingress. Datastores are private. Workloads use identities instead of static cloud keys. Production and non-production have separate accounts, networks, secrets and data.

```mermaid
flowchart LR
  R[Request] --> E[Bot/WAF/rate] --> N[OIDC/OTP/MFA]
  N --> Z[RBAC+ABAC+tenant] --> V[Schema/domain validation]
  V --> S[Least-privilege service] --> D[Encrypted scoped data]
  S --> A[Immutable audit/SIEM]
  K[Secret manager/KMS] --> S
  B[Signed artifact/SBOM/scans] --> P[Policy deployment] --> S
```

## Sequence diagrams

### Login

```mermaid
sequenceDiagram
  actor U
  participant I as Identity
  participant O as OTP provider
  participant DB
  U->>I: Request OTP
  I->>DB: Hashed challenge + limits
  I->>O: Send localized OTP
  U->>I: Submit OTP
  I->>DB: Verify once, risk, rotate session
  I-->>U: Access token + secure refresh cookie
```

### Booking/payment

```mermaid
sequenceDiagram
  actor U
  participant B as Booking API
  participant DB
  participant G as Gateway
  participant W as Webhook
  participant Q as Worker
  U->>B: Confirm quote + idempotency key
  B->>DB: Lock inventory; create hold/booking/order
  B-->>U: Hosted checkout
  U->>G: Pay
  G->>W: Signed capture
  W->>DB: Dedupe + confirm + ledger + outbox
  DB-->>Q: booking.confirmed
  Q-->>U: QR, invoice, notification
```

### Donation

```mermaid
sequenceDiagram
  actor D as Donor
  participant A as Donation API
  participant G as Gateway
  participant DB
  participant R as Receipt worker
  D->>A: Purpose, amount, tax consent
  A->>DB: Validate trust/create intent
  A-->>D: Hosted checkout
  G->>A: Signed capture webhook
  A->>DB: Donation + ledger + outbox transaction
  DB-->>R: donation.verified
  R-->>D: Receipt/tax certificate
```

### AI planner/chat

```mermaid
sequenceDiagram
  actor U
  participant O as Orchestrator
  participant R as Retrieval
  participant A as Agents
  participant T as Trusted tools
  U->>O: Query/constraints
  O->>O: Intent/safety/consent
  O->>R: Hybrid owner/date filtered search
  R-->>O: Evidence/provenance
  par Specialists
    O->>A: Temple/stay/transport/budget/weather/crowd/emergency
    A->>T: Read-only typed queries
  end
  A-->>O: Findings/confidence
  O-->>U: Grounded plan + alternatives
  U->>O: Explicit save/export/book
```

### Notification

```mermaid
sequenceDiagram
  participant S as Domain service
  participant DB as DB/outbox
  participant N as Worker
  participant P as Provider
  S->>DB: Commit + event
  DB-->>N: Deliver
  N->>N: Consent/template/locale/dedupe
  N->>P: Send
  P-->>N: Signed delivery status
  N->>DB: Delivered/retry/DLQ
```

### Emergency

```mermaid
sequenceDiagram
  actor U
  participant C as Client
  participant E as Emergency API
  participant M as Maps/responders
  participant F as Family
  U->>C: Hold SOS
  C-->>U: Immediate verified guidance
  C->>E: Consented GPS/context
  par Human routes
    E->>M: Facilities/responders
    E->>F: Selected contacts
  end
  M-->>E: Acknowledgement
  F-->>E: Acknowledgement
  E-->>C: Live incident state
```

### QR pass

```mermaid
sequenceDiagram
  participant B as Booking
  participant K as Signing service
  actor U
  participant S as Scanner
  participant V as Validation API
  B->>K: Confirmed entitlement
  K-->>U: Signed minimal QR
  U->>S: Present
  S->>S: Offline signature/expiry
  S->>V: Revocation/replay
  V-->>S: Admit/reject reason
  S->>V: Idempotent scan log
```

### Refund

```mermaid
sequenceDiagram
  actor U as User/admin
  participant C as Commerce
  participant DB
  participant G as Gateway
  participant Q as Reconciliation
  U->>C: Refund request
  C->>DB: Policy/ownership; pending refund
  C->>G: Idempotent refund
  G->>C: Signed refund status
  C->>DB: Compensating ledger + state + outbox
  Q->>G: Reconcile mismatch/timeout
  C-->>U: Status/credit note
```

## Activity diagrams

```mermaid
flowchart TD
  A[Discover] --> B[Verified details] --> C{Plan or transact?}
  C -- Plan --> D[AI itinerary] --> E[Save/share/export]
  C -- Transact --> F[Availability/quote] --> G[Consent/payment]
  G --> H{Verified?}
  H -- No --> I[Pending/failure recovery]
  H -- Yes --> J[Fulfill] --> K[QR/invoice/reminder] --> L[Complete/review/reward]
```

```mermaid
flowchart TD
  P[Partner applies] --> V[Identity/business/bank verification] --> D{Approved?}
  D -- No --> R[Reason/resubmit/appeal]
  D -- Yes --> C[Catalogue/inventory] --> A[Approval] --> O[Fulfill orders]
  O --> S[Settlement/reconciliation] --> Q[Quality/renewal]
```

```mermaid
flowchart TD
  I[Admin/support intake] --> T[Triage severity/tenant] --> E[Audited evidence]
  E --> P{Privileged?}
  P -- Yes --> M[Step-up + maker/checker] --> X[Scoped command]
  P -- No --> X
  X --> N[Notify] --> A[Audit/SLA/close]
```

Critical paths use time budgets and degrade optional enrichment. Writes use row locks or optimistic versions. Consumers dedupe and acknowledge after durable effect. Money reconciliation compares gateway, payment and ledger. Commerce RPO is at most five minutes and critical RTO at most thirty minutes, verified by restore exercises.
