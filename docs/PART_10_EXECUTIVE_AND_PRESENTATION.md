# NAMO SETU — Executive, product story and presentation pack

## Executive summary

Pilgrimage travel is a high-intent, trust-sensitive journey fragmented across temple websites, phone calls, travel marketplaces, cash processes and informal advice. Pilgrims struggle to verify timings, accessibility, crowds, accommodation, rituals, transport, payments and emergency support as one coherent trip. Temples and local partners struggle with discoverability, digital operations, demand forecasting, reconciliation and service quality.

NAMO SETU is a multilingual, accessibility-first pilgrimage operating system. It unifies verified temple discovery, evidence-grounded AI itinerary planning, stays, transport, guides, pandits, puja, donations, live darshan, signed QR access, family coordination and SOS. The platform begins India-first, where spiritual travel is large but digitally fragmented; the exact serviceable market and financial case must be established through city-level primary research rather than unsupported headline estimates.

The market gap is not another listing directory. It is trusted orchestration: authoritative information, real availability, auditable commerce, human-governed AI and coordinated fulfillment. The opportunity is a network connecting devotees, temple trusts, local businesses, travel operators and public services through shared standards and workflows.

**Vision:** make every sacred journey trusted, accessible, personal and safe.  
**Mission:** connect pilgrims and verified spiritual-travel providers through transparent information, reliable transactions and responsible AI.

| Dimension | Strategy |
|---|---|
| Target users | Pilgrims, families, senior citizens, international visitors, temple trusts, hotels/dharamshalas, guides, pandits, cab operators, agencies, restaurants, support/admin and government partners |
| Business value | Higher conversion and repeat visits; digitized partner supply; traceable settlements/donations; lower support effort; actionable capacity insight |
| Technical innovation | Modular domain architecture, transactional outbox, idempotent commerce, offline-verifiable QR, realtime projections, tenant-scoped governance |
| AI innovation | Specialist-agent planning, hybrid RAG with provenance, owner-scoped memory, deterministic tool boundaries, evaluation/canary/rollback |
| Future scope | Temple passport, AR/VR, privacy-preserving IoT crowd intelligence, wearables, offline AI and international sacred destinations |

## Project story

A pilgrimage is not a normal holiday. A family may coordinate elderly parents, children, accessibility needs, rituals, festival crowds, uncertain timings, regional language and a strict budget. Today the organizer repeatedly searches, calls, screenshots, transfers money and hopes every source is current. A missed update can become a financial loss or safety incident.

Existing travel platforms solve generic inventory; temple pages solve isolated information; messaging groups solve informal coordination. None establishes one accountable journey from intent through verified discovery, planning, payment, fulfillment and support.

NAMO SETU was built around that missing continuity. Verified providers own operational facts. Deterministic services own identity, inventory and money. AI turns preferences and evidence into an editable itinerary, but never fabricates availability or commits an action. Family mode coordinates consented needs. QR, notifications and support carry the traveler through fulfillment; SOS exposes human help immediately. The impact sought is measurable: fewer planning hours, fewer failed bookings, safer journeys, stronger local-provider economics and better trust governance.

## Audience narratives

| Audience | Lead with | Evidence to show | Avoid |
|---|---|---|---|
| CTO/interviewer | Invariants, boundaries, failure handling and trade-offs | Architecture, state models, CI/security, reconciliation | Feature-only tour |
| Investor | Pain, wedge, network economics and milestones | Cohort/conversion pilots, verified supply, unit economics | Unsupported TAM certainty |
| Temple/client | Trust, control, settlement and service quality | Approval, content, donation, reports, audit | AI jargon |
| Government | Accessibility, safety, privacy and interoperable governance | Consent, audit, SOS boundaries, capacity analytics | Claiming integration before agreement |
| Developers | Contracts, ownership and operability | OpenAPI, data model, runbooks, tests | Ambiguous “smart” behavior |

## Product demo scripts

### 15-minute executive demo

| Time | Screen/action | Narrative and proof |
|---:|---|---|
| 0:00–1:00 | Problem slide and home | A sacred journey is fragmented; NAMO SETU is the trusted coordination layer. |
| 1:00–2:00 | Login/guest | Demonstrate OTP-ready identity, guest discovery, Hindi/English, accessibility and consent. |
| 2:00–4:00 | Temple search/detail | Search, filters, verified timing, facilities, weather/crowd freshness and route. |
| 4:00–7:00 | AI planner | Enter family, budget and mobility constraints; show sourced plan, alternatives and editability. |
| 7:00–9:00 | Booking/payment | Select stay; explain inventory hold, immutable quote, hosted gateway and webhook confirmation. |
| 9:00–10:00 | QR/invoice | Show signed pass, offline validation concept, confirmation and reminder. |
| 10:00–11:00 | Donation | Select approved temple/purpose; explain receipt, tax choice and double-entry ledger. |
| 11:00–12:30 | Family/SOS | Shared itinerary and consented emergency contact/location; AI never delays human response. |
| 12:30–14:00 | Admin/analytics | Verification queue, audit trail, reconciliation, AI quality and governed metrics. |
| 14:00–15:00 | Roadmap/ask | State pilot scope, success gates and requested partnership/funding. |

### 30-minute product and architecture demo

Use the 15-minute flow, then spend five minutes on partner onboarding and fulfillment, five on the modular architecture/payment reconciliation/RAG, and five on security, launch gates, roadmap and questions. Show degraded behavior: stale crowd label, expired inventory hold, duplicate webhook safety and AI evidence insufficiency.

### 60-minute technical deep dive

| Segment | Minutes | Content |
|---|---:|---|
| Context and outcomes | 0–7 | Story, users, value and measurable pilot hypotheses |
| End-to-end product | 7–22 | Login, discovery, planner, booking, donation, family, SOS |
| Partner/admin | 22–30 | Verification, catalogue, inventory, fulfillment, settlement, support |
| Architecture | 30–40 | Contexts, API, PostgreSQL, Redis/search/vector, outbox/queues/workers |
| Critical internals | 40–48 | Booking states, payment webhook, ledger, RAG, memory and QR |
| Production readiness | 48–54 | CI/CD, observability, security, privacy, backup/restore and incident response |
| Strategy | 54–57 | Roadmap, go-to-market, economics and risks |
| Discussion | 57–60 | Invite challenge on assumptions and trade-offs |

## Presenter notes

- Before demo, use synthetic accounts and gateway sandbox; preload a saved plan and failure scenario.
- Never present prototype inventory, emergency contacts, revenue forecasts or provider integrations as production facts.
- For every AI result, show source, timestamp, uncertainty and the explicit confirmation boundary.
- For every payment result, state that the signed webhook—not the browser redirect—confirms money.
- Close with one decision: pilot partner, technical review, investment diligence or implementation milestone.

## Technical interview narrative

NAMO SETU uses a typed web client and a FastAPI modular backend. Bounded contexts separate identity, catalogue, commerce, experience, engagement, intelligence and operations. PostgreSQL is the transaction and ledger authority; Redis accelerates bounded data, search handles discovery, and a vector store supports filtered RAG/private memory. The first release favors a modular monolith to keep transactions and operational complexity manageable, while workers scale notifications, indexing, media, reports and AI independently.

Authentication uses OTP/OIDC-ready flows, short access tokens and rotating refresh tokens. Authorization combines roles with resource ownership and tenant/purpose policy. Commerce locks inventory, snapshots price and policy, creates a provider order, and confirms only after a signed idempotent webhook atomically updates payment, ledger, booking and outbox. Consumers are idempotent and reconciliation compares provider, payment and ledger state.

The AI orchestrator classifies intent, retrieves authority/date/tenant-filtered evidence, calls least-privilege specialist tools and validates structured results. Memory is opt-in, owner-scoped and deletable. Model or tool failure degrades to deterministic discovery and booking. Production uses reviewed changes, CI, dependency/container/code scanning, immutable artifacts, progressive delivery, metrics/logs/traces, SLO alerts, encrypted backups and tested recovery.

## Technical deep-dive map

| Topic | Design | Trade-off |
|---|---|---|
| Frontend | Vite/TypeScript responsive PWA slice; accessible, offline-aware | Current repository is web-first; native parity remains roadmap |
| Backend | FastAPI modules, schema validation, commands/queries and UoW | Modular monolith now; extract only on ownership/scale evidence |
| API | `/api/v1`, consistent errors, cursor pagination, idempotency and OpenAPI | Versioning cost accepted for consumer stability |
| Database | Normalized PostgreSQL, constraints, indexes, partitions, ledger/outbox | Strong consistency on money/inventory over maximal write throughput |
| Cache | Explicit TTL/key version/invalidation; never ledger authority | Some stale discovery is acceptable and labelled |
| Queues/workers | Outbox, durable jobs, retries, DLQ, dedupe | Eventual projections require freshness UX |
| Monitoring | RED/USE metrics, traces, structured/redacted logs, business invariants | Telemetry cost controlled by sampling/retention |
| Deployment | Containers, policy CI, canary and expand/migrate/contract | More release discipline for safer rollback |

