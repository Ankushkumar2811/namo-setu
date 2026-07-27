# NAMO SETU AI operating system

```text
User → safety gate → intent router → retrieval → specialist agents (parallel)
                                  ↘ consented memory
Specialists → evidence/confidence/action proposals → master synthesis → output guard
                                                         ↘ trace, cost and quality metrics
```

The master remains responsible for the user-facing answer. Specialists are bounded tools: temple intelligence, planner, stays, transport, emergency, festival, puja, health, family and multilingual voice. Financial, booking, location-sharing and emergency actions require deterministic authorization outside the model.

## Knowledge and RAG

Sources are admitted through provenance rules: temple-trust and government feeds, internal verified catalogue, provider APIs and reviewed editorial content. Documents are normalised, chunked by semantic section, enriched with geography/date/authority metadata and embedded. Retrieval combines keyword, vector and knowledge-graph signals, then reranks for authority, freshness and destination relevance. Every live claim carries a source and retrieval time.

## Knowledge graph

Primary nodes: Temple, Deity, Tradition, Festival, Ritual, Place, Route, Stay, Facility, EmergencyService and AccessibilityFeature. Edges are typed and dated: `OBSERVES`, `LOCATED_IN`, `NEAR`, `ACCESSIBLE_BY`, `HAS_FACILITY`, `CELEBRATES`, `REQUIRES`, `OPERATED_BY`. Operational edges keep validity windows and source provenance.

## Memory

Working memory is conversation-scoped. Profile memory stores only explicit, revocable preferences. Sensitive health and precise location memory is opt-in, encrypted, purpose-bound and expires. Users can inspect, correct and delete memories. Retrieval is filtered by user, consent category and expiry.

## Model routing

The provider contract supports OpenAI, Gemini, Claude, local/open models and OpenRouter adapters. Routing considers capability, language, latency, health, data policy and budget. OpenAI uses the Responses API with strict JSON schemas and `store=false`. A circuit breaker retries transient failures, then selects an approved fallback. Emergency output never waits for a model fallback before showing deterministic help.

## Evaluation and monitoring

Offline suites cover factuality, citation entailment, itinerary feasibility, cultural respect, prompt injection, language quality, accessibility and medical escalation. Online metrics include task success, citation coverage, unsafe-output rate, p50/p95 latency, agent/tool failure, token cost and user corrections. Releases use shadow traffic, canary rollout and automated regression gates.

## Cost controls

Cache stable grounded answers by locale and knowledge version. Use deterministic routing before model calls, retrieve narrowly, cap parallel specialists, compact conversation state and reserve premium reasoning for complex plans. Daily provider budgets and per-user quotas fail closed without affecting emergency guidance.

## Offline strategy

The mobile app ships verified emergency numbers, saved itineraries, passes, essential temple rules, phrase packs and deterministic reminders. On-device intent recognition handles navigation, saved-plan queries and SOS shortcuts. Generative answers are clearly unavailable when no approved local model is present.
