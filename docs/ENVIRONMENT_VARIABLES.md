# Environment variables

Secrets must be stored in Vercel, Kubernetes/cloud secret managers or CI environments—never in Git.

| Area | Variable | Required | Secret | Description |
|---|---|---:|---:|---|
| Core | `NAMO_ENVIRONMENT` | ✓ | No | `development`, `staging`, `production` |
| Core | `NAMO_DATABASE_URL` | ✓ | Yes | Async PostgreSQL DSN |
| Core | `NAMO_REDIS_URL` | ✓ | Yes | TLS Redis connection |
| Auth | `NAMO_JWT_SECRET` | ✓ | Yes | ≥32 random bytes; rotate with key IDs |
| Auth | `GOOGLE_OAUTH_CLIENT_ID/SECRET` | Optional | Mixed | Google login |
| Auth | `APPLE_TEAM_ID`, `APPLE_KEY_ID`, `APPLE_PRIVATE_KEY` | Optional | Yes | Apple login |
| AI | `NAMO_AI_PROVIDER` | ✓ | No | Approved provider route |
| AI | `NAMO_OPENAI_API_KEY` | By provider | Yes | OpenAI server-side key |
| AI | `NAMO_OPENAI_MODEL` | ✓ | No | Approved model identifier |
| Vector | `NAMO_QDRANT_URL`, `NAMO_QDRANT_API_KEY` | Production | Yes | Vector cluster |
| Payments | `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET` | Commerce | Yes | Orders/webhooks |
| Payments | `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` | Optional | Yes | Stripe-ready path |
| Maps | `GOOGLE_MAPS_SERVER_KEY`, `MAPPLS_CLIENT_ID/SECRET` | Routes | Yes | Server APIs |
| Weather | `WEATHER_PROVIDER_KEY` | Live data | Yes | Weather feed |
| Push | `FIREBASE_PROJECT_ID`, `FIREBASE_SERVICE_ACCOUNT_JSON` | Push | Yes | FCM |
| Email | `SMTP_URL`, `SENDGRID_API_KEY`, `EMAIL_FROM` | Notifications | Mixed | Email adapters |
| SMS | `TWILIO_ACCOUNT_SID/AUTH_TOKEN`, `MSG91_AUTH_KEY` | Optional | Yes | SMS adapters |
| WhatsApp | `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_APP_SECRET` | Optional | Yes | Business messaging |
| Storage | `S3_BUCKET`, `S3_REGION`, `S3_ENDPOINT`, `S3_ACCESS_KEY/SECRET` | Media | Mixed | S3-compatible storage |
| Media | `CLOUDINARY_URL` | Optional | Yes | Image/video pipeline |
| Monitoring | `SENTRY_DSN`, `OTEL_EXPORTER_OTLP_ENDPOINT` | Production | Mixed | Errors and traces |
| Frontend | `VITE_PUBLIC_API_URL` | ✓ | No | Public API base URL |
| Frontend | `VITE_PUBLIC_MAP_STYLE_ID` | Optional | No | Restricted browser map style |

Browser variables are public by definition and must never contain unrestricted provider credentials. Environment validation fails startup on missing production requirements or development defaults.
