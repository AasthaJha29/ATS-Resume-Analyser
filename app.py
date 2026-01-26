import streamlit as st
import pdfplumber
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

# -------------------------------
# Load model once
# -------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# -------------------------------
# PDF Text Extraction
# -------------------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# -------------------------------
# Keyword Extraction
# -------------------------------
STOPWORDS = set(stopwords.words("english"))

def extract_keywords(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    tokens = text.split()
    keywords = [word for word in tokens if word not in STOPWORDS and len(word) > 2]
    return set(keywords)

# -------------------------------
# UI
# -------------------------------
st.set_page_config(page_title="JobForge ATS Analyzer", layout="centered")
st.title("📄 JobForge – ATS Resume Analyzer")

st.write("Upload your resume and paste a job description to calculate ATS match score.")

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])
job_description = st.text_area("Paste Job Description", height=200)

if uploaded_file and job_description:

    with st.spinner("Analyzing resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

        # Embeddings
        resume_embedding = model.encode([resume_text])
        jd_embedding = model.encode([job_description])

        similarity_score = cosine_similarity(resume_embedding, jd_embedding)[0][0]
        ats_score = round(similarity_score * 100, 2)

        # Keyword extraction
        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(job_description)

        matched_skills = sorted(list(resume_keywords.intersection(jd_keywords)))
        missing_skills = sorted(list(jd_keywords - resume_keywords))

    # ---------------- Results ----------------
    st.success("✅ Analysis Complete")
    st.metric("📊 ATS Match Score", f"{ats_score}%")

    if ats_score > 75:
        st.success("Excellent match! Your resume fits this role well.")
    elif ats_score > 50:
        st.warning("Good match, but improvement is possible.")
    else:
        st.error("Low match. Consider improving your resume.")

    # ---------------- Skills Output ----------------
    st.subheader("✅ Matched Skills")
    if matched_skills:
        st.write(", ".join(matched_skills[:30]))
    else:
        st.write("No strong matches found.")

    st.subheader("❌ Missing / Weak Skills")
    if missing_skills:
        st.write(", ".join(missing_skills[:30]))
    else:
        st.write("Great! No major missing skills detected.")

    # ---------------- Suggestions ----------------
    st.subheader("💡 Suggestions to Improve Resume")
    if missing_skills:
        st.info("Consider adding or highlighting these skills in your resume:")
        st.write(", ".join(missing_skills[:10]))
    else:
        st.success("Your resume already matches this role very well!")

