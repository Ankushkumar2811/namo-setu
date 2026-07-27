export const FEATURE_KEYS = [
  "authentication", "home", "temple", "search", "maps", "bookings",
  "hotels", "dharamshala", "travel", "transport", "ai-planner",
  "ai-chat", "voice-assistant", "emergency", "donation", "puja",
  "wallet", "notifications", "settings", "profile", "rewards",
  "festival", "community", "admin", "partner", "cms", "analytics"
] as const;

export type FeatureKey = typeof FEATURE_KEYS[number];

export const PUBLIC_ROUTES = ["/", "/discover", "/temples/:slug", "/festivals", "/live-darshan"] as const;
export const AUTHENTICATED_ROUTES = ["/journeys", "/bookings", "/family", "/wallet", "/profile"] as const;
export const ROLE_ROUTES = {
  temple_admin: "/portal/temple",
  partner: "/portal/partner",
  guide: "/portal/guide",
  hotel: "/portal/hotel",
  super_admin: "/admin"
} as const;
