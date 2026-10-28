import re
from pathlib import Path

import pandas as pd

from text_cleaner import clean_text

DATA = Path(__file__).parent / "data"


def load_skill_dictionary() -> pd.DataFrame:
    return pd.read_csv(DATA / "skill_dictionary.csv").fillna("")


def _pattern(term: str) -> re.Pattern:
    # boundaries that still work for C++, C#, .NET, Node.js
    return re.compile(r"(?<![a-z0-9+#])" + re.escape(term.lower()) + r"(?![a-z0-9+#])")


def extract_skills(raw_text: str) -> dict:
    """Return {category: [skills found]} using controlled-list keyword matching."""
    text = clean_text(raw_text)
    found: dict[str, list[str]] = {}
    for _, row in load_skill_dictionary().iterrows():
        terms = [row["skill"]] + [a for a in row["aliases"].split("|") if a]
        if any(_pattern(t).search(text) for t in terms):
            found.setdefault(row["category"], []).append(row["skill"])
    return found


def flat_skills(found: dict) -> list[str]:
    return sorted(s for skills in found.values() for s in skills)
