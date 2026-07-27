# NAMO SETU UI/UX System

## Product experience

NAMO SETU is designed around three promises: calm discovery before a pilgrimage, dependable assistance during it, and meaningful continuity afterward. The visual language combines warm sacred colour, editorial travel imagery and high-clarity service interfaces.

## Information architecture

- Discover: temples, destinations, festivals, nearby places, map and filters
- Plan: conversational AI planner, itinerary, budget, transport, stays, packing and health
- Book: hotels, dharamshalas, transport, guides, pandits, pujas and donations
- Experience: live darshan, aarti, crowd, weather, traffic and alerts
- Care: family groups, location, expenses, medical information and SOS
- Account: journeys, bookings, wishlist, giving history, rewards and preferences
- Partner workspaces: temple, stay, guide, pandit and travel-agency operations
- Admin: analytics, catalogue, bookings, donations, CMS, users, alerts and reports

## Core journeys

1. Discover → compare live conditions → temple detail → plan → book → QR pass.
2. Natural-language request → AI proposal → customise → save → book components.
3. Family group → invite → share medical and emergency details → live trip view → check-in.
4. Partner onboarding → verification → listing → inventory → fulfilment → payout.
5. Admin review → approve catalogue → monitor operations → resolve alert → report.

## Design tokens

- Spacing: 4, 8, 12, 16, 24, 32, 48, 64 and 96px
- Radius: 8px controls, 12px cards, 20px features, fully rounded badges
- Primary: saffron `#E95C34`; secondary: temple gold `#D9A43B`; accent: royal blue `#3971AB`
- Canvas: warm white `#FFFAF2`; dark canvas: charcoal `#101713`
- Success: `#3C9765`; warning: `#CA7A16`; error: `#BB2E26`
- Body: DM Sans; display: Manrope; spiritual editorial accent: Georgia

## Responsive model

- 1440+: 12-column editorial grid and 1180px content width
- 1024–1439: compressed desktop with 8-column content
- 768–1023: two-column cards and stacked detail sidebars
- 360–767: single-column journeys, bottom navigation and floating AI
- Foldable: treat each pane as a tablet column; never place required actions across the hinge

## Accessibility and states

WCAG AA contrast, semantic landmarks, visible focus, labelled forms, 44px touch targets, large-text and high-contrast preferences, automatic/manual theme and offline journey essentials. Every module must support skeleton loading, first-use and filtered empty states, offline, recoverable error, permission denied and stale-data timestamps. Platform routes include branded 404, 500 and maintenance states.

## Motion

Page transitions use a 180ms fade/translate; card lift is limited to 4px; sheets and modals use 220ms ease-out. Motion respects reduced-motion. Booking uses a labelled resumable stepper. Errors appear inline and move focus to the affected field.

## Authentication and onboarding

Splash → language → accessibility → interests → optional family setup → phone/email → OTP → profile essentials → contextual permission education. Location, notification and microphone permissions are requested only when needed.

## Component hierarchy

- App shell: sticky header, mega navigation, search, content, contextual AI, footer/bottom navigation
- Discovery: search, chips, list/map toggle, cards and comparison drawer
- Temple: media hero, live status, tabs, practical information, facilities, map, reviews and booking rail
- Planner: conversational input, preferences, generated timeline, budget and action rail
- Booking: selection, travellers, review, payment, confirmation and QR pass
- Operations: role navigation, KPI cards, filters, tables, detail drawer, audit timeline and exports
