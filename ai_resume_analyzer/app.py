import plotly.express as px
import streamlit as st

from job_matcher import load_roles, rank_roles, skill_gap
from resume_parser import extract_text, validate_file
from roadmap_generator import generate_roadmap
from skill_extractor import extract_skills, flat_skills

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.title("📄 AI Resume Analyzer & Job Recommendation")
st.caption("Guidance tool only. Scores are estimates, not recruiter decisions, "
           "and a missing keyword does not mean missing ability.")

uploaded = st.file_uploader("Upload your resume (PDF or DOCX, max 5 MB)", type=["pdf", "docx"])
target = st.selectbox("Target role", list(load_roles().keys()))

if uploaded:
    error = validate_file(uploaded)
    if error:
        st.error(error)
        st.stop()
    st.success(f"Uploaded: {uploaded.name}")

    text = extract_text(uploaded)
    if not text.strip():
        st.warning("No text found. Scanned/image resumes are not supported.")
        st.stop()

    found = extract_skills(text)
    skills = flat_skills(found)

    st.subheader("Extracted skills")
    if not skills:
        st.info("No known skills detected.")
    for cat, items in found.items():
        st.markdown(f"**{cat}:** " + ", ".join(items))

    ranking = rank_roles(skills)
    st.subheader("Match scores")
    fig = px.bar(ranking, x="Role", y="Score", range_y=[0, 100], text="Score")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 3 recommended roles")
    for i, row in ranking.head(3).iterrows():
        st.write(f"{i + 1}. **{row.Role}** - {row.Score}%")

    have, missing = skill_gap(skills, target)
    score = float(ranking.loc[ranking.Role == target, "Score"].iloc[0])
    st.subheader(f"Skill gap for {target} ({score}%)")
    c1, c2 = st.columns(2)
    c1.markdown("**Found**\n\n" + ("\n".join(f"- {s}" for s in have) or "_none_"))
    c2.markdown("**Missing**\n\n" + ("\n".join(f"- {s}" for s in missing) or "_none_"))

    roadmap = generate_roadmap(missing)
    st.subheader("Learning roadmap")
    for step in roadmap or ["You cover all listed skills for this role. Build projects to show them."]:
        st.write(step)

    report = "\n".join(
        [f"Target Role: {target}", f"Match Score: {score}%", "", "Skills Found:"]
        + [f"- {s}" for s in have] + ["", "Missing Skills:"] + [f"- {s}" for s in missing]
        + ["", "Recommended Roles:"]
        + [f"{i + 1}. {r.Role} - {r.Score}%" for i, r in ranking.head(3).iterrows()]
        + ["", "Roadmap:"] + roadmap
    )
    st.download_button("Download report", report, file_name="resume_report.txt")
