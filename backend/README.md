# NAMO SETU API

FastAPI clean-architecture foundation for identity, temple discovery, live crowd and idempotent bookings.

## Local development

1. Copy `.env.example` to `.env` and replace the JWT secret.
2. Run `docker compose up --build`.
3. Open `/docs` in non-production environments.

All public APIs are versioned under `/api/v1`. Health probes use `/health` and `/ready`.

## Security

Passwords use Argon2id. Access tokens are short-lived JWTs and refresh tokens are stored only as SHA-256 digests. Booking writes require an `Idempotency-Key`. CORS uses an explicit allow-list, validation is strict and responses carry request IDs and defensive browser headers.

## Scaling

The API is stateless and horizontally scalable. PostgreSQL remains the system of record; Redis is reserved for distributed rate limiting, cache, sessions and realtime fan-out. Background tasks and search/vector infrastructure attach through adapters without changing domain services.
