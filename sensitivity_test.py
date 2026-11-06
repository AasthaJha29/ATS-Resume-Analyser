from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# Load same model as backend
model = SentenceTransformer("all-MiniLM-L6-v2")

# Use your real resume text here
resume = """
Final year Computer Engineering student with experience in Python, SQL,
Power BI dashboards, data analysis, and AI-driven applications like JobForge.
Built full-stack projects using JavaScript, Firebase, and machine learning tools.
"""

# Progressive JDs (increasing content)
jds = [
    "Data analyst intern",
    
    "Data analyst intern with Python and SQL skills",
    
    """Data analyst intern with Python, SQL, and data analysis experience.
    Experience working on datasets and dashboards.""",
    
    """Data analyst intern with Python, SQL, data visualization, and dashboards.
    Experience with Power BI, real-world datasets, and analytics projects.""",
    
]

scores = []

for jd in jds:
    r_vec = model.encode([resume])
    jd_vec = model.encode([jd])
    score = cosine_similarity(r_vec, jd_vec)[0][0] * 100
    scores.append(round(score, 2))

# Labels for graph
steps = [
    "1-line JD",
    "Short JD",
    "Medium JD",
    "Detailed JD"
]

# Plot graph
plt.figure(figsize=(8,5))
plt.plot(steps, scores, marker='o')
plt.title("Sensitivity Analysis: JD Content vs ATS Score")
plt.ylabel("ATS Score")
plt.xlabel("JD Length / Detail Level")
plt.grid(True)
plt.show()

print("Scores:", scores)