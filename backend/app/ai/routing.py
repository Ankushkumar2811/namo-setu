import re


class IntentRouter:
    """Select the smallest useful specialist set using deterministic domain signals."""

    signals: dict[str, tuple[str, ...]] = {
        "temple": ("temple", "mandir", "darshan", "history", "timing", "dress"),
        "planner": ("trip", "plan", "itinerary", "days", "budget", "yatra"),
        "hotel": ("hotel", "stay", "room", "dharamshala"),
        "transport": ("train", "flight", "bus", "cab", "route", "parking"),
        "emergency": ("emergency", "hospital", "police", "sos", "lost"),
        "festival": ("festival", "mela", "deepawali", "event", "calendar"),
        "puja": ("puja", "pandit", "donation", "prasad", "muhurat"),
        "health": ("health", "medicine", "altitude", "senior", "wheelchair"),
        "family": ("family", "parents", "group", "expense", "location"),
        "voice": ("translate", "speak", "hindi", "tamil", "gujarati"),
    }

    def route(self, query: str, maximum: int = 4) -> tuple[str, ...]:
        words = set(re.findall(r"[\w₹]+", query.casefold()))
        scores = {
            agent: sum(2 if signal in words else 1 if signal in query.casefold() else 0 for signal in signals)
            for agent, signals in self.signals.items()
        }
        selected = [agent for agent, score in sorted(scores.items(), key=lambda item: item[1], reverse=True) if score]
        return tuple((selected or ["temple"])[:maximum])
