# NAMO SETU — Technical interview guide

Answers are concise speaking prompts; expand with the linked architecture and workflow evidence.

## Product and architecture

1. **What is NAMO SETU?** A trusted pilgrimage operating system joining verified discovery, AI planning, commerce, devotion, family safety and partner operations.
2. **What core problem does it solve?** Fragmentation and weak accountability across information, availability, payment and fulfillment.
3. **Who are the actors?** Pilgrims/families, temple trusts, local providers, admins/support, enterprise/government partners and external providers.
4. **What is the architectural style?** A modular monolith with explicit bounded contexts and independently scalable asynchronous workers.
5. **Why not microservices immediately?** The monolith preserves simple transactions and operations; extraction follows proven ownership, scale or isolation needs.
6. **What are the bounded contexts?** Identity, catalogue, commerce, experience, engagement, intelligence and operations.
7. **What is the source of truth?** PostgreSQL for transactional state and ledgers; caches, search, vectors and analytics are projections.
8. **What are the critical invariants?** No oversell, no duplicate financial effect, balanced ledgers, allowed state transitions and tenant/owner isolation.
9. **How do modules communicate?** In-process typed interfaces synchronously and versioned outbox events asynchronously.
10. **How would you evolve the design?** Measure contention, team ownership and failure domains, then extract a context with contracts and data migration.

## Frontend and mobile

11. **Why TypeScript?** It catches interface errors early and creates shared, reviewable contracts around complex journeys.
12. **Why the current Vite web stack?** It is fast and simple for the implemented responsive product slice; framework changes require SSR/product evidence.
13. **Why might Next.js be chosen later?** Server rendering, routing and metadata can help large public SEO pages, but migration cost must be justified.
14. **Why React Native on the roadmap?** Shared React skills with native GPS, notification, camera and offline integration for mobile-heavy journeys.
15. **How is accessibility handled?** Semantic structure, keyboard/focus, contrast, reflow, captions, error association and assistive-technology testing.
16. **How is poor connectivity handled?** Cached public data and emergency guidance, saved itineraries, retryable commands and explicit freshness/offline states.
17. **How does the UI avoid duplicate submission?** Disable/reconcile pending intent locally and send a server-enforced idempotency key.
18. **How is localization designed?** Stable message keys, locale-aware dates/currency/content and partner-owned verified translations.
19. **What state belongs in the client?** Presentation and ephemeral draft state; authoritative identity, inventory, money and entitlement remain server-side.
20. **How do you test the frontend?** Unit/component accessibility checks plus browser journeys for identity, search, booking simulation, QR and SOS fallback.

## Backend and API

21. **Why FastAPI?** Typed validation, OpenAPI, async I/O and Python’s AI ecosystem; performance is validated rather than assumed.
22. **How are backend layers separated?** Routes transport, application services coordinate, domain objects enforce invariants, repositories persist and adapters integrate.
23. **How are APIs versioned?** `/api/v1`; additive compatible changes stay, breaking changes get a new version and migration window.
24. **How are errors represented?** Stable machine code, safe user message, request ID and optional field details; internals stay in logs.
25. **How is pagination done?** Cursor pagination for mutable large lists; stable sort and filters are encoded in the cursor contract.
26. **How is idempotency implemented?** Scope key to actor/operation, hash request, persist response/effect and reject mismatched reuse.
27. **How are long tasks handled?** Durable queue job returning an operation ID, with status, callback/notification and retry/DLQ.
28. **How are third parties isolated?** Provider adapters with typed contracts, deadlines, circuit breakers, bounded retries and reconciliation.
29. **How do you prevent cascading failure?** Time budgets, concurrency limits, circuit breakers, bulkheads and optional-feature degradation.
30. **What API documentation exists?** OpenAPI 3.1, examples, standards, Postman collection and event/integration documentation.

## Data, database and cache

31. **Why PostgreSQL?** ACID transactions, constraints, relational integrity, indexes, JSON/geospatial extensions and mature operations.
32. **Why not MongoDB as the core store?** Booking and ledger relationships benefit from strong constraints/transactions; MongoDB is optional only for a justified document workload.
33. **How are relationships modeled?** Normalized foreign keys around users, partners, catalogue, inventory, bookings, payments and ledgers.
34. **How is overselling prevented?** Transactional row/capacity lock with expiry and conditional version checks.
35. **How are financial records modeled?** Immutable double-entry ledger entries tied to payment/refund/donation references.
36. **How do you correct a ledger error?** Add a compensating entry with reason/approval; never update historical entries.
37. **Why Redis?** Low-latency bounded cache, rate limits, locks where safe and realtime fan-out—not durable financial truth.
38. **How is cache invalidated?** Versioned keys, explicit TTL and domain-event invalidation; freshness is exposed.
39. **How do you choose indexes?** From query plans and cardinality: composite indexes match filter/equality/order, with partial/unique constraints where useful.
40. **How is data partitioned?** High-volume time-series/audit/event tables by time after measured need; business entities stay simple.
41. **How are migrations released?** Expand schema, deploy compatible code, backfill in checkpoints, switch reads, then contract later.
42. **What is soft deletion for?** Recoverable lifecycle and reference integrity; privacy erasure still anonymizes/deletes where law permits.
43. **How is analytics isolated?** CDC/ETL into a governed warehouse; operational requests do not run arbitrary analytical joins.
44. **How are backups validated?** Point-in-time and offsite encrypted backups plus scheduled restore/failover exercises measuring RPO/RTO.

## Booking, payment and donation

45. **How does booking work?** Validate listing, lock inventory, snapshot quote/policy, create pending booking/payment, verify webhook, atomically confirm and emit.
46. **What confirms payment?** A verified signed provider webhook or authoritative reconciliation—not the browser redirect.
47. **How are duplicate webhooks handled?** Persist provider event ID and transition atomically; duplicate delivery returns success without duplicate effect.
48. **What if the webhook is late?** Booking remains pending, hold policy applies, reconciliation queries provider and safely advances or compensates.
49. **What if payment succeeds after inventory expires?** Reaccommodate if approved or issue a traceable refund via policy; never silently oversell.
50. **How are refunds handled?** Authorized command, policy/amount validation, idempotent provider refund, signed status and compensating ledger entries.
51. **How do coupons work?** Eligibility/usage are transactionally checked; discount is snapshotted into the immutable quote.
52. **How does wallet recharge work?** Capture verification credits a closed-loop double-entry ledger; pending funds are not spendable.
53. **How are donations different?** Approved beneficiary/purpose, donor/tax consent, immutable donation receipt and trust-scoped reporting.
54. **How is PCI scope reduced?** Hosted/tokenized gateway checkout, no card data storage/logging and documented CDE with assessor/acquirer validation.

## Authentication, security and privacy

55. **How does OTP authentication work?** Rate-limited challenge with hashed single-use code, expiry, generic errors, risk checks and session issuance.
56. **How are sessions secured?** Short access JWT, secure HttpOnly refresh cookie, rotation/reuse detection and device/all-session revocation.
57. **RBAC or ABAC?** Both: roles grant capability; attributes enforce owner, tenant, verification, purpose and resource state.
58. **How is tenant isolation tested?** Negative cross-tenant API/repository tests, scoped queries and audit alerts.
59. **How are admin actions protected?** MFA, least privilege, step-up, maker-checker for high impact, reason and immutable audit.
60. **How are secrets managed?** External secret manager/KMS, workload identities, rotation and no secrets in source/images/logs.
61. **How is sensitive data protected?** Minimize, encrypt transit/at rest/selected fields, mask support views, scope access and delete by policy.
62. **How are webhooks secured?** Raw-body signature, timestamp/replay window, allowlist where appropriate, dedupe and secret rotation.
63. **How do you address OWASP risks?** Threat models, validation/encoding, strong authz, secure headers, SSRF/egress controls, scans and security tests.
64. **How is consent modeled?** Purpose-specific versioned evidence with notice version, timestamp, channel and equal withdrawal path.
65. **How are privacy requests executed?** Identity verification, discovery, legal retention exceptions, export/correction/deletion across derived stores and evidence.
66. **How are children handled?** Age-aware flow, verifiable guardian controls as required and disabled profiling/advertising defaults.
67. **What gets audited?** Privileged and sensitive commands: actor, tenant, purpose, target, reason, correlation, outcome and protected evidence.

## AI, RAG and memory

68. **Why RAG?** Pilgrimage facts change and require provenance; retrieval grounds generation in verified, dated sources.
69. **What is the RAG pipeline?** Safety/rewrite, embedding, hybrid search, authority/tenant/date filters, rerank, bounded context, generation and grounding validation.
70. **Why a vector database?** Semantic retrieval with payload ownership/authority filters and embedding-version lifecycle.
71. **How does AI memory work?** Opt-in preferences become owner-scoped encrypted records/vectors with purpose, source, confidence, expiry and deletion.
72. **Why multi-agent?** Typed specialists isolate temple, stay, transport, budget, weather, crowd and emergency reasoning while one orchestrator resolves.
73. **Why LangGraph?** It can model explicit stateful graphs, checkpoints and controlled branching; adopt only if simpler orchestration becomes inadequate.
74. **Why CrewAI?** It can accelerate role-based prototypes, but production choice depends on control, observability, evaluation and maintenance.
75. **How are tools authorized?** Least-privilege typed adapters; AI can read facts/create drafts, while user/policy service authorizes actions.
76. **How do you prevent prompt injection?** Treat retrieved text as data, isolate instructions/tools, filter egress/ownership and test adversarial corpora.
77. **How do you reduce hallucination?** Authority-filtered evidence, required citations, structured output, deterministic validation and honest insufficiency.
78. **How is AI evaluated?** Grounding, citation, constraint satisfaction, unsafe actions, injection, multilingual quality, latency, cost and satisfaction.
79. **How are model changes released?** Version prompt/model/retrieval/embedding, offline gate, shadow/canary, guardrail monitoring and rollback.
80. **What if AI is unavailable?** Deterministic search, booking, saved plans and support remain; optional AI degrades visibly.
81. **Can AI trigger emergency or payment?** No. It may translate/summarize and prepare a draft, never delay/dispatch/confirm/close without deterministic human-authorized flow.

## Events, scalability and reliability

82. **Why an outbox?** It commits state and event intent in one database transaction, avoiding lost events after successful writes.
83. **How are events shaped?** Name/version, event ID, occurred time, correlation, actor/tenant and typed payload.
84. **How are consumers idempotent?** Store consumed event/effect key with the transaction and make handlers safe to retry.
85. **RabbitMQ or streams?** Durable priority jobs/retries in RabbitMQ; low-latency fan-out can use Redis Streams; choose per delivery semantics.
86. **How do workers scale?** Independently by queue depth, age, service time and provider quotas, with per-task concurrency limits.
87. **How does horizontal API scaling work?** Stateless instances behind load balancing; session/data externalized and shared dependencies capacity-planned.
88. **What is backpressure?** Limit intake/concurrency, prioritize critical queues and shed optional work before dependencies collapse.
89. **How are hot reads scaled?** CDN, bounded Redis/search projections and replicas; money/inventory correctness stays primary-bound.
90. **How is realtime handled?** Event-driven projections and WebSocket/SSE where useful, with reconnect/resync from durable state.
91. **What are critical SLOs?** Identity/commerce/emergency availability and latency, booking success, queue age and money reconciliation.
92. **What are RPO and RTO?** Maximum acceptable data loss and restoration time; current target is commerce RPO ≤5m and critical RTO ≤30m, verified by drills.

## DevOps, monitoring and operations

93. **What does CI check?** Type/build/tests, lint/static errors, API artifacts, dependency audit, container vulnerability policy and CodeQL.
94. **How is deployment done?** Immutable artifact through staging, compatible migration, canary, SLO/business guardrails and gradual promotion.
95. **How do you roll back?** Revert app/config with feature flags/artifact; data changes use forward fix or tested compensation.
96. **What is observed?** RED for services, USE for resources, queue/provider health, traces, structured redacted logs and business invariants.
97. **How are alerts designed?** Symptom/SLO based, actionable, deduplicated, routed to an owner and linked to a runbook.
98. **How do you investigate one booking?** Correlation/request ID links API trace, state timeline, outbox/event, provider reference and ledger.
99. **How is a payment incident handled?** Protect users, stop risky transitions, reconcile evidence, compensate—not edit—communicate and review.
100. **How are containers secured?** Minimal non-root image, pinned dependencies/base, SBOM/signing/scanning and restricted runtime identity/network.
101. **How do you control cloud cost?** Unit-cost dashboards, budgets, autoscaling, cache, storage lifecycle, model routing/quotas and load forecasts.
102. **What is the disaster plan?** Multi-AZ, PITR/offsite backups, replayable events, documented restore/failover, degraded modes and exercises.

## Business, trade-offs and leadership

103. **How does NAMO SETU earn?** Fulfilled-service commissions, temple/partner SaaS, premium AI, governed ads, disclosed donation processing, analytics and enterprise licenses.
104. **What is the initial go-to-market?** Anchor a temple corridor, verify nearby supply, pilot family journeys, grow referral/repeat, then replicate.
105. **What is the moat?** Verified supply/fulfillment graph, workflow integration, trust/audit and consented preference learning.
106. **What is the largest risk?** Trust failure in information, money, AI or safety; each has deterministic controls, evidence and human escalation.
107. **How do you prioritize?** User/safety outcome, evidence, risk, dependency and effort; safety/compliance invariants are gates, not score modifiers.
108. **What would you build next?** The capability that removes the largest validated pilot bottleneck while preserving reliability—not the flashiest roadmap item.
109. **What would you not build yet?** Face recognition, blockchain or costly immersive tech without necessity, legal basis, partner demand and measurable benefit.
110. **How do you communicate uncertainty?** Separate implemented, tested, planned and hypothesized claims; attach evidence dates and owners.
111. **How do you measure product success?** Meaningful activation/retention, booking/donation success, partner SLA, satisfaction and safety/cost guardrails.
112. **How do you handle disagreement with a stakeholder?** Restate outcome and constraints, expose evidence/trade-offs, run a reversible experiment and document the decision.

