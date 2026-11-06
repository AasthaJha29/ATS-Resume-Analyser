from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber
import nltk
from nltk.corpus import stopwords
import re
from io import BytesIO

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HEALTH ROUTE ----------------
@app.get("/")
def home():
    return {"message": "ATS Resume Analyzer API running"}

# ---------------- LOAD MODEL SAFELY ----------------
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model loaded")
except Exception as e:
    print("❌ Model load failed:", e)
    model = None

# ---------------- STOPWORDS SAFE LOAD ----------------
try:
    STOPWORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    STOPWORDS = set(stopwords.words("english"))

# ---------------- PDF READER (SAFE) ----------------
def extract_text_from_pdf(upload_file):
    try:
        file_bytes = upload_file.file.read()

        if not file_bytes:
            raise Exception("Empty PDF")

        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""

        return text.strip()

    except Exception as e:
        print("❌ PDF ERROR:", e)
        raise Exception("Invalid or unreadable PDF")

# ---------------- KEYWORD EXTRACTOR ----------------
def extract_keywords(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    tokens = text.split()
    return set([w for w in tokens if w not in STOPWORDS and len(w) > 2])

# ---------------- MAIN API ----------------
@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), jd: str = Form(...)):
    try:
        print("📥 Request received")

        if model is None:
            return {"error": "Model not loaded"}

        if not resume:
            return {"error": "Resume file missing"}

        if not jd.strip():
            return {"error": "Job description empty"}

        # Extract text
        print("📄 Reading PDF...")
        resume_text = extract_text_from_pdf(resume)

        if not resume_text:
            return {"error": "Could not extract text from PDF"}

        # Embeddings
        print("🧠 Encoding text...")
        r_vec = model.encode([resume_text])
        jd_vec = model.encode([jd])

        # Similarity
        score = cosine_similarity(r_vec, jd_vec)[0][0]
        ats_score = float(round(score * 100, 2))

        # Keywords
        print("🔍 Extracting keywords...")
        r_keys = extract_keywords(resume_text)
        jd_keys = extract_keywords(jd)

        matched = list(r_keys.intersection(jd_keys))
        missing = list(jd_keys - r_keys)

        print("✅ Success")

        return {
            "score": float(ats_score),
            "matched": [str(x) for x in matched[:20]],
            "missing": [str(x) for x in missing[:20]]
        } 

    except Exception as e:
        print("🔥 FINAL ERROR:", e)
        return {"error": str(e)}