import pandas as pd
import os

BASE = r"C:\Users\tanishk\OneDrive\Desktop\ToxiView"

# -----------------------------
# FILE GROUPS
# -----------------------------

human_files = [
    "human_health.csv",
    "human_microplastic.csv",
    "human_packaging.csv",
    "human_processing.csv",
    "human_plasticiser.csv",
    "human_ingredients.csv"
]

animal_files = [
    "animal_microplastic.csv"
]

other_files = [
    "analytical_methods.csv",
    "biological_effects.csv",
    "environmental_fate.csv",
    "food_contamination.csv",
    "packaging_release.csv",
    "polymer_material.csv",
    "processing_effects.csv",
    "other_uncategorized.csv"
]

# -----------------------------
# LOAD FILES
# -----------------------------

def load_group(files):

    frames = []

    for name in files:

        path = os.path.join(BASE, name)

        if os.path.exists(path):

            df = pd.read_csv(path)

            print(f"Loaded {name}: {len(df)} papers")

            df["Source_File"] = name

            frames.append(df)

    if frames:
        df = pd.concat(frames, ignore_index=True)

        # remove duplicates by PMID
        if "PMID" in df.columns:
            before = len(df)
            df = df.drop_duplicates(subset="PMID")
            after = len(df)

            print(f"Duplicates removed: {before - after}")

        return df

    return pd.DataFrame()


# -----------------------------
# LOAD GROUPS
# -----------------------------

human_df = load_group(human_files)
animal_df = load_group(animal_files)
other_df = load_group(other_files)

print("\nUPDATED COUNTS AFTER DEDUPLICATION")

print("Human papers:", len(human_df))
print("Animal papers:", len(animal_df))
print("Other papers:", len(other_df))

# -----------------------------
# SUMMARY TABLE
# -----------------------------

summary = pd.DataFrame({
    "Category": ["Human", "Animal", "Other"],
    "Paper_Count": [
        len(human_df),
        len(animal_df),
        len(other_df)
    ]
})

# -----------------------------
# SAVE EXCEL
# -----------------------------

output = os.path.join(BASE, "microplastics_master_database_cleaned.xlsx")

if os.path.exists(output):
    os.remove(output)

with pd.ExcelWriter(output) as writer:

    human_df.to_excel(writer, sheet_name="Human_studies", index=False)
    animal_df.to_excel(writer, sheet_name="Animal_studies", index=False)
    other_df.to_excel(writer, sheet_name="Other_studies", index=False)
    summary.to_excel(writer, sheet_name="Summary_counts", index=False)

print("\nClean Excel created:", output)