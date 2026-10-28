from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA = Path(__file__).parent / "data"


def load_roles() -> dict[str, list[str]]:
    df = pd.read_csv(DATA / "job_roles.csv")
    return {r.role: [s.strip() for s in r.required_skills.split(";")] for r in df.itertuples()}


def _doc(skills):
    return " ".join(s.lower().replace(" ", "_") for s in skills)


def rank_roles(candidate_skills: list[str]) -> pd.DataFrame:
    """Score = 70% skill coverage + 30% TF-IDF cosine similarity (both explainable)."""
    roles = load_roles()
    docs = [_doc(candidate_skills)] + [_doc(s) for s in roles.values()]
    tfidf = TfidfVectorizer(token_pattern=r"\S+").fit_transform(docs)
    cos = cosine_similarity(tfidf[0], tfidf[1:]).flatten()
    have = {s.lower() for s in candidate_skills}
    rows = []
    for (role, req), c in zip(roles.items(), cos):
        coverage = sum(s.lower() in have for s in req) / len(req)
        rows.append({"Role": role, "Coverage": coverage, "Cosine": c,
                     "Score": round((0.7 * coverage + 0.3 * c) * 100, 1)})
    return pd.DataFrame(rows).sort_values("Score", ascending=False).reset_index(drop=True)


def skill_gap(candidate_skills: list[str], role: str):
    have = {s.lower() for s in candidate_skills}
    req = load_roles()[role]
    return [s for s in req if s.lower() in have], [s for s in req if s.lower() not in have]
