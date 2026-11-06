# JobForge ATS Resume Analyzer

JobForge is an AI-assisted resume analysis application that compares a PDF resume with a job description. It calculates an ATS-style similarity score, identifies matched keywords, and highlights skills or keywords that may be missing from the resume.

## Features

- Upload resumes in PDF format
- Paste any job description
- Calculate a resume-to-job similarity score
- Extract matched and missing keywords
- Run through a Streamlit interface or a FastAPI backend with a browser frontend
- Include evaluation and sensitivity analysis scripts

## How It Works

1. PDF text is extracted with `pdfplumber`.
2. Resume and job-description text are converted into embeddings with the `all-MiniLM-L6-v2` Sentence Transformer model.
3. Cosine similarity produces the ATS match score.
4. Keyword matching identifies overlap and missing terms.

## Important Notes

- Scores depend heavily on resume text quality and job-description wording.
- The model works best with PDF resumes containing selectable text rather than scanned images.
- Keyword lists are simplified exact-token matches; they do not currently use semantic synonyms.
- The similarity score is a screening aid, not a definitive assessment of candidate suitability.
