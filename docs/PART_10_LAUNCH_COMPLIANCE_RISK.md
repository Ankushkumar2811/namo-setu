# NAMO SETU — Launch, compliance, risk and maintenance plan

This is an engineering control baseline, not legal or certification advice. Counsel, acquiring bank/QSA and accessibility specialists must confirm scope before launch. Regulatory activation dates are tracked as requirements, not guessed.

## Compliance control map

| Framework | Product/engineering controls | Evidence owner |
|---|---|---|
| India DPDP Act 2023 and Rules 2025 | Clear itemized notice; lawful purpose/consent evidence; withdrawal parity; correction/erasure/grievance; processor register; retention/deletion; child and breach workflows; phased commencement tracker | Privacy lead |
| GDPR where applicable | Article 5 principles; lawful-basis records; rights workflow; privacy by design/default; processor/DPA records; DPIA and transfer mechanism; breach process | DPO/counsel |
| WCAG 2.2 AA target | Keyboard, focus, semantics, contrast, zoom/reflow, captions, error identification and assistive-technology testing | Design/QA |
| PCI DSS v4.0.1 | Hosted/tokenized payment, no card storage, scoped CDE diagram, access/MFA, logging, vulnerability management, ASV/SAQ or QSA validation as applicable | Security/payments |
| OWASP | ASVS-aligned requirements, threat modelling, Top 10 verification, SAST/DAST/dependency/secret/container checks | AppSec |

Official baselines: [MeitY DPDP Rules 2025](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025.pdf), [EU GDPR text](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng/), [PCI DSS](https://www.pcisecuritystandards.org/standards/pci-dss/) and [OWASP Top 10](https://owasp.org/www-project-top-ten/).

## Risk register

| Risk | Category | Early indicator | Mitigation/contingency | Owner |
|---|---|---|---|---|
| Inventory/price mismatch | Technical/operational | Hold failures, complaints | Authoritative locks, snapshot quote, reconciliation, stop-sell | Commerce |
| Duplicate or lost provider event | Technical/financial | Payment-booking variance | Signed idempotent webhooks, outbox, retries/DLQ, reconciliation | Payments |
| AI hallucination/unsafe advice | AI/legal | Citation/safety regression | Filtered RAG, tool boundaries, eval/canary, deterministic fallback | AI governance |
| Partner fraud/poor fulfillment | Business/operational | Disputes, SLA decline | KYB, staged limits, evidence, reserve/suspension and support | Partner ops |
| Sensitive data breach | Security/legal | SIEM/DLP anomaly | Minimize/encrypt/isolate, least privilege, IR and notification decision | Security/privacy |
| Account takeover | Security | OTP abuse/token reuse | Rate/risk controls, rotating tokens, MFA, alerts/revocation | Identity |
| Provider outage | Operational | Timeout/error budget | Circuit breaker, queued work, fallback provider/manual process | SRE |
| Emergency expectation mismatch | Safety/legal | Failed acknowledgement | Clear scope, immediate official call fallback, drills, human closure | Safety |
| Demand below plan | Business | Activation/repeat/CAC | Corridor experiments, stage spend, interview churned users | Growth |
| Regulatory or temple-policy change | Legal/business | Counsel/partner notice | Policy registry, configuration, change review, geographic gating | Legal/product |
| Cloud cost spike | Financial/technical | Cost per journey/model | Budgets, cache, routing, quotas, right-size and graceful limits | FinOps |
| Accessibility exclusion | Product/legal | Failed audits/support | WCAG gates, disabled-user testing and remediation SLA | Product |

## Production launch checklist

### Infrastructure and delivery

- [ ] Production accounts, private network, domains, TLS, WAF and rate limits approved.
- [ ] Infrastructure/configuration versioned; immutable artifact, SBOM and provenance retained.
- [ ] Autoscaling/load test proves forecast plus safety margin; quotas and budgets alert.
- [ ] Staging resembles production without production personal data.
- [ ] Canary, feature flags, rollback and database expand/migrate/contract rehearsed.

### Security and privacy

- [ ] Threat model, tenant/owner authorization tests, MFA and privileged access review complete.
- [ ] SAST, dependency, secret, container and DAST findings meet release policy.
- [ ] Secrets in manager with rotation; encryption and key recovery verified.
- [ ] Notices, consent, grievance, rights, retention/deletion and processor register approved.
- [ ] Incident/breach contacts, evidence preservation and tabletop complete.

### Database, API and reliability

- [ ] Constraints/indexes/migrations, idempotency and concurrency tests pass.
- [ ] OpenAPI/event compatibility and consumer contract tests pass.
- [ ] Backup restore meets RPO/RTO; replica/failover and capacity tested.
- [ ] Cache invalidation, queue retry/DLQ/replay and poison-message runbooks verified.

### AI

- [ ] Knowledge authority/freshness/ownership filters and ingestion scanning verified.
- [ ] Grounding, citation, safety, injection, multilingual and accessibility eval gates pass.
- [ ] Prompt/model/retrieval/embedding versions, cost/latency budget, canary and kill switch ready.
- [ ] Human/action confirmation boundaries and non-AI fallback tested.

### Money and fulfillment

- [ ] Gateway production credentials/webhook signatures, refund and reconciliation validated.
- [ ] PCI scope confirmed with acquiring bank/QSA; no prohibited card data in logs/storage.
- [ ] Ledger balances, settlement/report and duplicate/out-of-order events tested.
- [ ] Inventory expiry, cancellation, oversell and partner escalation rehearsed.

### Experience and growth

- [ ] Notifications honor consent, locale, quiet hours and delivery callbacks.
- [ ] Analytics definitions/consent, data quality and dashboard freshness approved.
- [ ] SEO metadata, canonical/robots/sitemap/structured-data ownership reviewed.
- [ ] Performance budgets and Core Web Vitals measured on representative devices/networks.
- [ ] WCAG 2.2 AA audit and critical assistive-technology journeys pass.

### Operations

- [ ] SLOs, dashboards, synthetic checks, paging and service ownership active.
- [ ] Support macros/tools, status communication and partner/customer SLA trained.
- [ ] SOS cached fallbacks and human escalation tested in every launch geography.
- [ ] Go/no-go sign-offs recorded; hypercare roster and rollback authority explicit.

## Go/no-go

Launch only when all safety, money, identity, backup and critical accessibility gates pass. Noncritical exceptions require owner, quantified risk, compensating control and expiry. A SEV-1, unbalanced ledger, failed restore, cross-tenant access, unreliable emergency fallback or unresolved critical vulnerability is an automatic no-go.

## Post-launch

| Window | Actions |
|---|---|
| First 24 hours | War room; watch SLOs, signup, search, payment/booking variance, SOS/notification and partner fulfillment; freeze unrelated change |
| Days 2–7 | Daily defect/feedback/reconciliation review; fix high-frequency friction; validate cost and alerts |
| Weeks 2–4 | Cohort retention, funnel and support analysis; AI error taxonomy/re-evaluation; capacity tuning |
| Monthly | Planned releases, partner quality, privacy/security/financial control review and roadmap evidence |
| Quarterly | Restore/failover/incident drill, access review, penetration test cadence and architecture/cost review |

## Success metrics

| Metric | Definition |
|---|---|
| DAU/MAU | Unique eligible active users per day/month; exclude bots/internal |
| Retention | Cohort returning for a defined meaningful action at D7/D30 |
| Conversion | Eligible search/plan sessions reaching confirmed booking |
| Booking success | Confirmed bookings / valid checkout attempts; segment provider/failure |
| Donation success | Verified donations / valid donation checkout attempts |
| Revenue | Recognized net revenue, separated from GMV and pass-through funds |
| NPS | Standard likelihood survey with sample size and segment |
| App rating | Store rating plus review volume/recency once native apps launch |
| AI satisfaction | Rated useful grounded responses / rated AI responses, paired with citation/safety |

Every metric has an owner, query/version, denominator, exclusions, freshness, target and alert. Guardrails include cancellation, refund time, oversell, reconciliation variance, safety incidents, accessibility failure and support SLA.

## Maintenance

- Daily: alerts, reconciliation, queues, partner fulfillment and backup completion.
- Weekly: vulnerabilities, dependency/provider health, AI evaluation sample and error budget.
- Monthly: patch release, restore sample, cost/capacity, data-quality and retention jobs.
- Quarterly: access/secret/DR review, penetration/incident exercises and model governance.
- Annually or on material change: architecture threat/privacy impact review, external audits and legal/compliance scope confirmation.

Dependencies follow supported releases with automated advisories and controlled upgrades. Data migrations are backward-compatible. Deprecations publish dates, telemetry and migration help. Incidents and user feedback create owned, prioritized actions with verification.
