# NAMO SETU — Installation and deployment guide

## Prerequisites

- Node.js 22+ and npm
- Python 3.11+
- Docker with Compose for local backing services
- PostgreSQL, Redis and RabbitMQ (local containers or managed equivalents)
- A secrets manager and sandbox credentials for optional providers

## Local development

```powershell
git clone https://github.com/Ankushkumar2811/namo-setu.git
cd namo-setu
npm ci
npm run typecheck
npm run dev
```

Backend:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[test]"
uvicorn app.main:app --reload
```

Copy the documented environment key inventory into a local ignored file and obtain values through approved channels. Never commit secrets. Use `docker compose up` to run declared backing services, then apply the backend migration command adopted by the release environment.

## Commands and tests

| Command | Purpose |
|---|---|
| `npm run dev` | Web development server |
| `npm run typecheck` | TypeScript validation |
| `npm run build` | Production web build |
| `pytest` in `backend` | Backend test suite |
| `python -m compileall -q app scripts` | Backend syntax/import compilation |
| `docker compose up --build` | Local container stack |

## Environment promotion

| Environment | Data/integration | Deployment rule |
|---|---|---|
| Development | Synthetic data, provider sandboxes | Developer-controlled, no production secrets |
| Staging | Production-like scale/schema, synthetic or anonymized data | Main candidate, migrations, contract/load/security/smoke tests |
| Production | Real data and live providers | Approved immutable artifact, canary, guarded promotion and rollback |

## Platform guides

### Vercel

Use Vercel for the static/Vite web deployment. Connect the GitHub repository, set framework/build command `npm run build`, output `dist`, and inject public frontend configuration only. Use preview deployments for review and promote an already-tested commit. Backend secrets and privileged APIs do not belong in a public client bundle.

```powershell
npx vercel
npx vercel --prod
```

### Docker

Build pinned frontend/backend images, run as non-root, expose only required ports, inject secrets at runtime, add health/readiness checks and scan/sign the resulting digest. Compose is appropriate for local/staging smoke tests, not a substitute for production orchestration, backups and observability.

### Railway and Render

Deploy the backend as a Docker/web service with a managed PostgreSQL/Redis where supported. Set health check, start command, region, autoscaling, secret variables and migration release step. Verify private connectivity, backup/PITR, egress/provider allowlists and data-location requirements before production. Never rely on ephemeral disk for uploads or state.

### AWS

Reference topology: Route 53/CloudFront/WAF → ALB → ECS/Fargate or EKS services; RDS PostgreSQL Multi-AZ, ElastiCache, Amazon MQ/MSK where justified, OpenSearch, S3/CloudFront media, Secrets Manager/KMS, CloudWatch/X-Ray/SIEM and cross-region backup. Use private subnets/endpoints, workload IAM and IaC.

### Azure

Reference topology: Front Door/WAF → Container Apps or AKS; Azure Database for PostgreSQL, Azure Cache for Redis, Service Bus, AI Search/vector choice, Blob/CDN, Key Vault, Managed Identity, Monitor/Application Insights and Recovery Services. Use private endpoints, zones and IaC.

### GCP

Reference topology: Cloud CDN/Armor/load balancer → Cloud Run or GKE; Cloud SQL PostgreSQL HA, Memorystore, Pub/Sub, managed search/vector choice, Cloud Storage/CDN, Secret Manager/KMS, Cloud Monitoring/Trace and cross-region backups. Use private service access and workload identity.

Cloud examples are deployment patterns, not one-click claims. Select region and service after privacy, latency, availability, skill and cost review.

## CI/CD

Pull request → review → frontend/backend/API/security checks → immutable artifact/SBOM → staging deploy/migrate/smoke → approval → canary production → SLO/business verification → promotion. Production migration uses expand/migrate/contract and a database advisory lock. Failed gates stop promotion.

## Production readiness

Before any platform deployment, complete [launch controls](PART_10_LAUNCH_COMPLIANCE_RISK.md), configure domain/TLS/WAF, secrets/KMS, private databases, backups/restore, provider webhooks, observability, on-call, privacy/retention and cost budgets. Record artifact digest, migration revision, configuration version and approver.
