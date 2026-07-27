# NAMO SETU

A premium, responsive product experience for an AI-powered pilgrimage ecosystem.

## Included

- Temple and destination discovery
- AI journey planner with generated itinerary
- Stay and dharamshala marketplace
- Live darshan hub
- Family safety and emergency experience
- Voice-assistant interaction
- Dark mode, offline indicator and mobile navigation

## Run locally

```bash
npm install
npm run dev
```

Create a production build with `npm run build`.

## Architecture direction

This front-end product slice is intentionally API-ready. Production services should be split by identity, catalog, journeys, bookings, payments, live media, safety and notifications, with PostgreSQL as the transactional store, Redis for caching and queues, and object storage/CDN for media.
