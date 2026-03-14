import pandas as pd

# -----------------------------
# MAIN DATASET (ALL PAPERS)
# -----------------------------
main_df = pd.read_csv(r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\microplastic_food_no_review.csv")

# -----------------------------
# GROUP FILES (already sorted)
# -----------------------------
group_files = [
    r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\human_health.csv",
    r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\human_ingredients.csv",
    r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\human_processing.csv",
    r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\human_packaging.csv",
    r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\human_plasticiser.csv",
    r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\human_microplastic.csv",
    r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\animal_microplastic.csv"
]

classified_pmids = set()

# -----------------------------
# COLLECT PMIDs FROM GROUP FILES
# -----------------------------
for file in group_files:
    df = pd.read_csv(file)

    if "PMID" in df.columns:
        classified_pmids.update(df["PMID"].astype(str))

# -----------------------------
# FIND UNCLASSIFIED PAPERS
# -----------------------------
remaining = main_df[~main_df["PMID"].astype(str).isin(classified_pmids)]

# -----------------------------
# SAVE THEM
# -----------------------------
remaining.to_csv(
    r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\remaining_unclassified_papers.csv",
    index=False
)

print("✅ Remaining papers:", len(remaining))
print("Saved as: remaining_unclassified_papers.csv")