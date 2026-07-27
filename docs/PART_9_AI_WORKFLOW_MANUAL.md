# NAMO SETU — AI workflow manual

```mermaid
flowchart TD
  Q[User query] --> I[Intent/language/safety]
  I --> P[Planner agent]
  P --> T[Temple agent]
  P --> H[Hotel agent]
  P --> X[Transport agent]
  P --> B[Budget agent]
  P --> W[Weather agent]
  P --> C[Crowd agent]
  P --> E[Emergency agent]
  T & H & X & B & W & C & E --> M[Memory/evidence merge]
  M --> R[Recommendation engine]
  R --> G[Grounded response]
  G --> S[Booking suggestions]
  G --> D[PDF]
  G --> K[Calendar sync]
  G --> N[Notifications]
```

The orchestrator owns the final answer and authorization. Specialists return typed facts, constraints, confidence and provenance. Booking output is a suggestion or draft; explicit user confirmation starts deterministic Commerce.

| Step | Processing | Output/guardrail |
|---|---|---|
| Intent | Classify plan/search/support/emergency and missing slots | Typed intent; emergency exposes human help immediately |
| Planner | Decompose dates, people, origin, budget and accessibility | Execution graph/clarifications |
| Temple | Verified catalogue, festivals and timing | Ranked candidates with source/version |
| Hotel | Availability snapshot and policy | Options, never a lock claim |
| Transport | Maps/transit/cab tools | Legs, time and fallback |
| Budget | Deterministic cost ranges/totals | Transparent estimate/contingency |
| Weather | Geo/date provider and seasonal evidence | Timestamp and confidence |
| Crowd | Observation and historical projection | Confidence-labelled advice |
| Emergency | Verified facilities/precautions | No diagnosis or autonomous dispatch |
| Memory | Owner/purpose/consent-filtered retrieval | Minimum relevant private context |
| Recommendation | Feasibility, diversity and preference score | Explainable primary/alternatives |
| Response | Citation/conflict/schema/safety validation | Grounded stream or honest insufficiency |
| Export/action | User-approved plan | Audited PDF/ICS/draft intents |

## Memory

```mermaid
flowchart LR
  P[Preference + consent] --> D[Classify/minimize]
  D --> E[Embedding] --> V[(Private vectors)]
  D --> M[(Encrypted memory)]
  Q[Query] --> R[Owner-scoped retrieval]
  V --> R
  M --> R
  R --> C[Context + provenance] --> A[Response]
  U[View/edit/delete] --> M
  U --> V
```

Memory records owner, purpose, consent/source, confidence, timestamps, expiry and embedding version. Sensitive traits are not inferred. Users can inspect, correct and delete memory.

## RAG

```mermaid
flowchart LR
  Q[Question] --> G[Safety/query rewrite] --> E[Embedding]
  E --> S[Hybrid vector+keyword search]
  S --> F[Authority/tenant/locale/date filters]
  F --> K[(Knowledge base)] --> R[Rerank/dedupe]
  R --> C[Bounded context/citations] --> L[LLM]
  L --> V[Grounding/schema/safety] --> A[Answer or insufficiency]
```

Ingestion malware-scans, verifies authority, chunks semantically and records checksum/effective/version metadata. Retrieved content is untrusted data, never instruction.

Tool timeouts yield labelled partial plans. Agent disagreement is surfaced or clarified. Invalid structure gets one bounded repair. Model outage preserves deterministic search/booking and saved plans. Prompt injection and exfiltration are constrained through isolated tool permissions and ownership filters. Prompt/model/retrieval/embedding releases pass citation, constraint, injection, multilingual, safety, latency and cost evaluations, then canary with rollback.
