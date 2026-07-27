# Events and integrations

## Event envelope

```json
{
  "event_id":"019c0d64-f0c2-7e0e-8f69-42da311dbb33",
  "event_type":"booking.created.v1",
  "occurred_at":"2026-07-27T09:00:00Z",
  "tenant_id":"73ec3d46-cdd5-4981-a397-c15d411b2088",
  "aggregate_id":"5f65d211-c060-4e57-b75a-51bf187edfb8",
  "correlation_id":"4bc6e9cc-6306-4e31-9d89-4bb52b3ea95f",
  "producer":"commerce",
  "data":{"reference":"NS8F42A1","status":"pending_payment"}
}
```

Published events include booking created/confirmed/cancelled, payment captured/failed, refund requested/completed, donation received, temple updated, festival published, weather/crowd alert raised, emergency triggered, AI conversation created, reminder due, notification delivered and webhook accepted.

## Delivery

The producing transaction writes an `outbox_events` row. A relay publishes to RabbitMQ exchanges by domain. Consumers acknowledge only after their idempotency record and side effects commit. Transient errors retry with exponential delay and jitter. Business-invalid events move directly to a dead-letter queue; operators can inspect, repair and replay them with an audit reason.

Priority queues are reserved for emergency, payment and time-sensitive reminders. Analytics receives copies through Redis Streams/Kafka-compatible infrastructure and never blocks commerce.

## Webhook security

Provider webhooks retain raw bytes, validate timestamp and signature before JSON parsing, reject excessive clock skew, deduplicate provider event IDs and return quickly after durable receipt. Processing occurs asynchronously. Secrets rotate with an overlap window.

| Provider | Verification | Primary events |
|---|---|---|
| Razorpay | HMAC-SHA256 raw body | payment captured/failed, refund |
| Stripe | Signed timestamp and payload | payment intent, charge, refund |
| Firebase | OAuth service identity | delivery receipts |
| Cloudinary | SHA signature and timestamp | upload/moderation |
| WhatsApp | Meta signature and challenge | message/status |
| Email/SMS | Provider signature or source allow-list | delivery, bounce, complaint |
| Maps/weather | Service identity and schema validation | road/weather alert ingestion |

## Integration resilience

Every adapter has connection/read timeouts, bounded retries, circuit breaker, bulkhead and metrics. Provider references are stored separately from internal IDs. Reconciliation jobs compare provider exports with internal ledgers daily. A degraded provider cannot disable emergency guidance or access to saved plans.
