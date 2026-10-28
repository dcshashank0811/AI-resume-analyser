# AI Resume Analyzer & Job Recommendation System

Upload a PDF/DOCX resume, get extracted skills, role match scores, top-3 roles,
missing skills for a target role, and a weekly learning roadmap.

## Setup
    python -m pip install -r requirements.txt
    python -m streamlit run app.py

## How it works
1. `resume_parser.py` - extracts text in memory (nothing saved to disk)
2. `text_cleaner.py` - lowercases, keeps C++, C#, .NET
3. `skill_extractor.py` - matches `data/skill_dictionary.csv` (with aliases)
4. `job_matcher.py` - score = 70% skill coverage + 30% TF-IDF cosine similarity
5. `roadmap_generator.py` - rule-based weekly plan

## Responsible AI
Only job-related skills are scored. Scores are estimates, not hiring decisions.

## Limitations
Keyword matching misses synonyms not in the dictionary; scanned PDFs are unsupported.
