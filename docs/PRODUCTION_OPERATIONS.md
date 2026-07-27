# Production operations

## Environments

Development uses local Compose with disposable data. Staging mirrors production topology with reduced capacity and synthetic accounts. Production uses separate cloud accounts, networks, keys and databases. No production secret or personal data is copied to lower environments.

## Cloud portability

The reference implementation uses Vercel for the web edge and AWS for managed Kubernetes, Aurora PostgreSQL, ElastiCache, object storage, queues, KMS and observability. Equivalent mappings are GKE/Cloud SQL/Memorystore/GCS, AKS/Azure Database/Cache/Blob, DigitalOcean Kubernetes/Managed Databases/Spaces, or a container service on Railway/Render. Cloudflare provides DNS, WAF, bot controls and CDN independently of the workload cloud.

## Deployment

Images are immutable and addressed by Git SHA. CI runs type checks, unit tests, dependency audit, CodeQL, container build and Trivy. Staging deploys automatically after main passes. Production requires approval and deploys a canary at 5%, then 25%, 50% and 100% while SLOs remain healthy. Database migrations are backward-compatible and run before traffic shifts.

## Rollback

Stop rollout, route traffic to the previous healthy ReplicaSet, and disable new feature flags. Never roll back a destructive database migration; use a forward repair. Confirm booking/payment reconciliation, queue depth and error rate before declaring recovery.

## Backup and disaster recovery

PostgreSQL uses continuous point-in-time recovery, 35 daily snapshots, 12 monthly archives and cross-region encrypted copies. Object storage uses versioning and cross-region replication. Restore tests run quarterly. Target RPO is 5 minutes for commerce and 24 hours for regenerable analytics; target RTO is 30 minutes for core booking and 4 hours for secondary reporting.

## Incident response

1. Acknowledge and assign incident commander, operations lead and communications lead.
2. Protect life and financial integrity first; disable risky writes through feature flags.
3. Establish impact, affected tenants, first bad deployment and data consistency.
4. Mitigate by rollback, failover, traffic shedding or provider isolation.
5. Communicate internally every 15 minutes and externally with verified facts.
6. Preserve logs and audit evidence; rotate credentials if compromise is suspected.
7. Run a blameless review within 72 hours with owned remediation dates.

## Security baseline

TLS 1.3 at the edge, HSTS, CSP, WAF managed rules, rate limits and bot protection are mandatory. Workloads use short-lived identities, private subnets, default-deny network policies and encrypted storage. Secrets live in a cloud secret manager and rotate automatically. Admin access requires phishing-resistant MFA, device posture and just-in-time permissions. Audit records are immutable and retained according to DPDP/legal policy.

## Cost controls

Autoscale on request concurrency and queue delay, schedule non-production capacity, use CDN caching and image transforms, apply object lifecycle policies, reserve predictable database capacity and cap AI spend per tenant. Cost anomalies page finance/platform owners when daily spend exceeds forecast by 20%.

## Production checklist

- DNS, certificate, HSTS and WAF verified
- Secrets rotated and no defaults present
- Restore, rollback and payment-webhook replay tested
- Dashboards, alerts and on-call schedules active
- Capacity test passes 2× forecast peak
- DPDP data map, retention and deletion paths reviewed
- Accessibility and Core Web Vitals release gates pass
