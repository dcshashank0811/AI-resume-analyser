import re


def clean_text(text: str) -> str:
    """Lowercase, drop stray symbols, keep C++, C#, .NET, node.js style tokens."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\-/\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
