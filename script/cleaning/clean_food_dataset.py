import pandas as pd
import os

# --------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------

# Path to your food CSV files
FOLDER = "data/food/"      # ← change if needed

# Keywords REQUIRED to confirm the paper is about FOOD
REQUIRED_FOOD = [
    "food", "diet", "edible", "consumption", "meal",
    "milk", "dairy", "cheese", "butter", "cream",
    "rice", "wheat", "grain", "flour",
    "vegetable", "fruit", "meat", "poultry", "fish",
    "seafood", "legume", "soybean",
    "cereal", "bread",
    "packaging", "food packaging", "contamination",
    "food safety", "food processing", "cooking", "frying",
    "boiling", "roasting", "baking"
]

# Keywords REQUIREMENT to confirm paper is about FOOD TOXICANTS
REQUIRED_TOXICANTS = [
    "acrylamide", "aflatoxin", "mycotoxin", "ochratoxin",
    "deoxynivalenol", "fumonisin", "zearalenone",
    "3-mcpd", "melamine",
    "benzopyrene", "benzo[a]pyrene", "pah", "pahs",
    "pesticide", "pesticide residue", "residue",
    "heavy metal", "arsenic", "lead", "cadmium",
    "mercury", "nickel", "chromium",
    "bisphenol", "bisphenol a", "bpa",
    "phthalate", "microplastic", "nanoplastic"
]

# IRRELEVANT → COSMETICS (REMOVE)
COSMETIC_BANNED = [
    "skin", "cosmetic", "cream", "lotion", "sunscreen",
    "spf", "hair", "shampoo", "dermatology",
    "makeup", "fragrance", "nail", "whitening"
]

# IRRELEVANT → ENVIRONMENT-ONLY (REMOVE)
ENVIRONMENT_BANNED = [
    "soil", "groundwater", "air pollution", "atmospheric",
    "ecosystem", "aquatic", "marine", "sediment",
    "wastewater", "rainwater"
]

# IRRELEVANT → MEDICAL (REMOVE)
MEDICAL_BANNED = [
    "clinical trial", "cohort", "patient", "therapy", "survival",
    "cancer treatment", "metastasis", "oncology",
    "biomarker", "pharmacokinetics", "autophagy",
    "mental", "neurological", "cardiac", "insulin"
]

# --------------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------------

def contains_any(text, terms):
    text = text.lower()
    return any(t in text for t in terms)

# --------------------------------------------------------
# MAIN CLEANING LOGIC
# --------------------------------------------------------

files = [f for f in os.listdir(FOLDER) if f.endswith(".csv")]

print("\n🔵 STARTING FOOD DATASET CLEANING...\n")

for file in files:

    print(f"📄 Processing file: {file}")

    df = pd.read_csv(os.path.join(FOLDER, file), dtype=str)
    df.fillna("", inplace=True)
    df["Status"] = ""

    clean_rows = []

    for _, row in df.iterrows():

        text = (row["Title"] + " " + row["Abstract"]).lower()

        # 1️⃣ Remove empty abstracts
        if len(row["Abstract"].split()) < 10:
            row["Status"] = "REMOVE - Empty abstract"
            continue

        # 2️⃣ Must contain toxicant keyword
        if not contains_any(text, REQUIRED_TOXICANTS):
            row["Status"] = "REMOVE - No toxicant found"
            continue

        # 3️⃣ Must contain food-related keyword
        if not contains_any(text, REQUIRED_FOOD):
            row["Status"] = "REMOVE - Not food related"
            continue

        # 4️⃣ Remove cosmetics-related papers
        if contains_any(text, COSMETIC_BANNED):
            row["Status"] = "REMOVE - Cosmetic related"
            continue

        # 5️⃣ Remove environment-only papers
        if contains_any(text, ENVIRONMENT_BANNED):
            row["Status"] = "REMOVE - Environment only"
            continue

        # 6️⃣ Remove medical/clinical unrelated papers
        if contains_any(text, MEDICAL_BANNED):
            row["Status"] = "REMOVE - Medical/clinical"
            continue

        # PASS
        row["Status"] = "PASS"
        clean_rows.append(row)

    clean_df = pd.DataFrame(clean_rows).drop_duplicates(subset="PMID")

    # Save cleaned version
    output_file = file.replace(".csv", "_CLEAN.csv")
    clean_df.to_csv(os.path.join(FOLDER, output_file), index=False, encoding="utf-8")

    print(f"✔ DONE → {output_file}  (Kept {len(clean_df)} records)\n")

print("\n🎉 ALL FOOD DATA FILES CLEANED SUCCESSFULLY!")
