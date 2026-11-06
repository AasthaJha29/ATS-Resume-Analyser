from scipy.stats import pearsonr
import numpy as np

# -----------------------------
# Human Judgement Scores (1–5 scale)
# 5 = perfect match
# 1 = poor match
# -----------------------------
human_scores = [
    5,  # perfect resume ↔ perfect JD
    4,
    3,
    5,
    2,
    1,
    4,
    3,
    3,
    2,
    4,
    1,
    3,
    5,
    2
]

# -----------------------------
# Model ATS Scores (your system outputs)
# Use real values from your analyzer
# (example realistic values below)
# -----------------------------
model_scores = [
    80,  # strong match
    60,
    65,
    89,
    45,
    28,
    70,
    62,
    91,
    50,
    76,
    25,
    60,
    70,
    42
]

# Convert model scores to 1–5 scale (optional but recommended for research)
def normalize_to_5_scale(scores):
    return [(s / 100) * 5 for s in scores]

model_scaled = normalize_to_5_scale(model_scores)

# -----------------------------
# Pearson Correlation
# Measures agreement between human judgement and model
# -----------------------------
corr, _ = pearsonr(human_scores, model_scaled)

print("\n========== EVALUATION RESULTS ==========")
print("Total Comparisons:", len(human_scores))
print("Human Scores:", human_scores)
print("Model Scores:", model_scores)
print("\nPearson Correlation:", round(corr, 3))

# -----------------------------
# Simple interpretation
# -----------------------------
if corr > 0.8:
    print("Interpretation: Very strong agreement ✅")
elif corr > 0.6:
    print("Interpretation: Strong agreement 👍")
elif corr > 0.4:
    print("Interpretation: Moderate agreement ⚠️")
else:
    print("Interpretation: Weak agreement ❌")


import numpy as np

scores = [59.20, 59.20, 59.20,59.20, 59.20]
print("Std Dev:", np.std(scores))

