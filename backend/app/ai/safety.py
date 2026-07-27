import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    risk: str
    reason: str | None = None


class SafetyGuard:
    """Deterministic guardrails applied before and after model execution."""

    injection_patterns = (
        r"ignore (all|any|the) previous instructions",
        r"reveal (the )?(system|developer) prompt",
        r"print .*api.?key",
        r"bypass .*safety",
    )
    emergency_patterns = (
        r"\b(chest pain|not breathing|unconscious|severe bleeding|suicid|heart attack)\b",
        r"\b(immediate danger|trapped|missing child)\b",
    )

    def inspect_input(self, text: str) -> SafetyDecision:
        normalized = text.casefold()
        if any(re.search(pattern, normalized) for pattern in self.injection_patterns):
            return SafetyDecision(False, "prompt_injection", "Unsafe instruction pattern detected")
        if any(re.search(pattern, normalized) for pattern in self.emergency_patterns):
            return SafetyDecision(True, "emergency")
        return SafetyDecision(True, "normal")

    def sanitize_evidence(self, text: str) -> str:
        cleaned = re.sub(r"<script.*?>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)
        return cleaned[:4_000].replace("\x00", "")
