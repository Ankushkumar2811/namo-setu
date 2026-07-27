# NAMO SETU REST API reference

## Standards

Base URL is `/api/v1`. JSON uses UTF-8 and snake_case. Access tokens use `Authorization: Bearer <token>`. Commerce writes require `Idempotency-Key` (16–80 characters). `X-Request-ID` is accepted and returned. Default rate limit is 120 requests/minute/IP with stricter OTP, authentication, AI and payment policies.

Collection parameters are `page` (default 1), `page_size` (default 20, maximum 100), `sort`, `query` and module-specific filters. Successful deletion returns `204`. Errors use:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": []
  },
  "request_id": "4bc6e9cc-6306-4e31-9d89-4bb52b3ea95f"
}
```

## Endpoint catalogue

| Module | Method and route | Auth | Purpose |
|---|---|---|---|
| Auth | `POST /auth/register`, `POST /auth/login`, `POST /auth/otp/request`, `POST /auth/otp/verify`, `POST /auth/refresh`, `POST /auth/logout` | Public/refresh | Account and session lifecycle |
| Profile | `GET /profile`, `PUT /profile`, `GET /profile/devices`, `DELETE /profile/devices/{id}` | User | Profile and trusted devices |
| Temples | `GET /temples`, `GET /temples/{id}`, `GET /temples/{id}/crowd`, `GET /temples/{id}/timings`, `GET /temples/{id}/facilities`, `GET /temples/{id}/reviews` | Public | Discovery and operational detail |
| Search | `GET /search`, `GET /search/autocomplete`, `GET /search/nearby` | Public | Full text, autocomplete and geo discovery |
| Festivals | `GET /festivals`, `GET /festivals/{id}`, `GET /events` | Public | Calendar and live events |
| Stays | `GET /hotels`, `GET /hotels/{id}`, `GET /hotels/{id}/availability`, `GET /dharamshalas` | Public | Stay catalogue and inventory |
| Mobility | `GET /transport/search`, `GET /routes`, `GET /parking`, `GET /local-services` | User | Multi-modal journey data |
| Bookings | `POST /bookings`, `GET /bookings`, `GET /bookings/{id}`, `POST /bookings/{id}/cancel` | User | Unified order lifecycle |
| Payments | `POST /payments/orders`, `GET /payments/{id}`, `POST /payments/{id}/refund` | User/Finance | Provider order and refund lifecycle |
| Donations | `POST /donations`, `GET /donations`, `GET /donations/{id}/receipt` | User | Verified giving and receipts |
| Puja | `GET /pujas`, `GET /pujas/{id}/slots`, `POST /puja-bookings` | User | Puja catalogue and booking |
| Guides | `GET /guides`, `GET /guides/{id}/availability`, `POST /guide-bookings` | User | Verified guide booking |
| Wallet | `GET /wallet`, `GET /wallet/entries`, `POST /wallet/recharge` | User | Balance and immutable ledger |
| Family | `POST /family-groups`, `POST /family-groups/{id}/invites`, `POST /family-groups/{id}/check-ins` | User | Consent-based family coordination |
| AI | `POST /ai/chat`, `POST /ai/planner`, `GET /ai/conversations`, `DELETE /ai/memories/{id}` | User | Grounded agent workflows and memory |
| Notifications | `GET /notifications`, `POST /notifications/{id}/read`, `POST /devices/push-token` | User | Inbox and push registration |
| Support | `POST /support/tickets`, `GET /support/tickets`, `POST /support/tickets/{id}/messages` | User/Support | Omnichannel support |
| Admin | `GET /admin/dashboard`, `GET /admin/partners`, `POST /admin/partners/{id}/review`, `GET /admin/audit` | Admin | Enterprise operations |
| Partner | `GET /partner/dashboard`, `GET /partner/inventory`, `PUT /partner/inventory/{id}`, `GET /partner/settlements` | Partner | Tenant-scoped operations |
| CMS | `GET /admin/content`, `POST /admin/content`, `POST /admin/content/{id}/publish` | Editor | Versioned publishing |
| Analytics | `GET /admin/analytics`, `POST /admin/reports`, `GET /admin/reports/{id}` | Admin | Aggregates and asynchronous exports |
| Webhooks | `POST /webhooks/razorpay`, `/stripe`, `/firebase`, `/cloudinary`, `/whatsapp` | Signature | Provider event ingestion |

## Implemented request examples

### Register

`POST /api/v1/auth/register` — public, 5 requests/hour/address.

```json
{"email":"meera@example.in","full_name":"Meera Sharma","password":"A-long-unique-passphrase"}
```

Returns `201` with access and refresh tokens. Errors: `409 email_registered`, `422 validation_error`, `429 rate_limited`.

### List temples

`GET /api/v1/temples?page=1&page_size=20&state=Uttar%20Pradesh&query=Kashi`

Returns `200` with `items` and `{page,page_size,total}` metadata. Public caching: 60 seconds; live crowd is never served from this cache.

### Create booking

`POST /api/v1/bookings`, user authentication and `Idempotency-Key` required.

```json
{
  "product_type":"puja",
  "product_id":"550e8400-e29b-41d4-a716-446655440000",
  "service_date":"2026-11-24",
  "amount_inr":"1100.00"
}
```

Returns `201`; a repeated identical idempotency key returns the original booking. Errors: `401`, `409 idempotency_conflict`, `422`, `429`.

### AI chat

`POST /api/v1/ai/chat`, user authentication, 30 requests/hour/user.

```json
{"message":"Plan a senior-friendly three-day Kashi journey","language":"en-IN"}
```

Response includes `answer`, `confidence`, contributing `agents`, sources and follow-up suggestions. `actions_executed` is empty unless a separately confirmed deterministic action completes.

## Versioning and deprecation

Compatible fields may be added within v1; fields are never retyped or removed. Breaking semantics require `/api/v2`. Deprecation is announced through documentation, `Deprecation` and `Sunset` headers at least six months before removal. Security retirement can be accelerated with direct client notification.
