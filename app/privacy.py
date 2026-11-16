"""Mask Kenyan telephone numbers and emails before model, embedding, or tool calls.

This is a teaching example, not a complete PII detection or legal compliance system.
"""
import re
from dataclasses import dataclass, field

EMAIL = re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])")
# +2547..., +254 7..., 2547..., 07..., 01..., including common separators.
PHONE = re.compile(
    r"(?<![\w+])(?:\+?254[\s.-]?|0)(?:[17][\s.-]?(?:\d[\s.-]?){8})(?!\d)"
)
PLACEHOLDER = re.compile(r"\[(?:EMAIL|PHONE)_\d+\]")


@dataclass
class MaskingSession:
    """Private mapping for one conversation; never send mapping to the LLM."""
    mapping: dict[str, str] = field(default_factory=dict)
    _reverse: dict[str, str] = field(default_factory=dict)

    def _token(self, match: re.Match[str], kind: str) -> str:
        raw = match.group(0)
        if raw in self._reverse:
            return self._reverse[raw]
        number = 1 + sum(k.startswith(f"[{kind}_") for k in self.mapping)
        token = f"[{kind}_{number}]"
        self.mapping[token] = raw
        self._reverse[raw] = token
        return token

    def mask(self, text: str) -> str:
        """Replace supported identifiers with stable per-session placeholders."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        # Existing tokens remain tokens. Protect them before processing to prevent remasking.
        protected: dict[str, str] = {}
        def protect(match: re.Match[str]) -> str:
            key = f"__MASKEDTOKEN{len(protected)}__"
            protected[key] = match.group(0)
            return key
        text = PLACEHOLDER.sub(protect, text)
        text = EMAIL.sub(lambda m: self._token(m, "EMAIL"), text)
        text = PHONE.sub(lambda m: self._token(m, "PHONE"), text)
        for key, token in protected.items():
            text = text.replace(key, token)
        return text

    def restore_approved(self, text: str, *, authorized: bool = False) -> str:
        """Restore ONLY known tokens, only when caller explicitly authorizes output."""
        if not authorized:
            return text
        return PLACEHOLDER.sub(lambda m: self.mapping.get(m.group(0), m.group(0)), text)

    def clear(self) -> None:
        """Delete in-memory mapping at the end of a session."""
        self.mapping.clear()
        self._reverse.clear()
