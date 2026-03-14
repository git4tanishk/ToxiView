# ==========================================
# FILE: classify_microplastic_papers.py
# PURPOSE:
# Classify microplastic papers into:
# - Human / Animal
# - Human → processing / packaging / plasticiser /
#           ingredients / health
# Uses strong research keywords
# Safe handling if Abstract column missing
# ==========================================

import pandas as pd
import os

INPUT_FILE = r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\microplastic_food_no_review.csv"

# =========================
# CHECK FILE
# =========================
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(INPUT_FILE)

print("📂 Loading file...")
df = pd.read_csv(INPUT_FILE)

if "Paper_Title" not in df.columns:
    raise ValueError("Paper_Title column required")

# =========================
# CREATE SEARCH TEXT (SAFE)
# =========================
# Use title + abstract if available, otherwise title only
if "Abstract" in df.columns:
    df["text"] = (
        df["Paper_Title"].astype(str) + " " +
        df["Abstract"].astype(str)
    ).str.lower()
else:
    print("⚠ Abstract column not found → using title only")
    df["text"] = df["Paper_Title"].astype(str).str.lower()

# =========================
# STRONG RESEARCH KEYWORDS
# =========================

# ---- HUMAN ----
human_kw = [
    "human", "humans", "population", "subjects", "patients",
    "clinical", "clinical study", "clinical trial", "cohort",
    "epidemiology", "epidemiological", "biomonitoring",
    "dietary exposure", "dietary intake", "exposure assessment",
    "adult", "children", "infant", "pregnant women",
    "volunteer", "public health"
]

# ---- ANIMAL ----
animal_kw = [
    "rat", "rats", "mouse", "mice", "murine",
    "zebrafish", "fish", "rodent", "rabbit",
    "in vivo", "animal model", "toxicity study",
    "experimental study"
]

# ---- FOOD PROCESSING ----
processing_kw = [
    "food processing", "thermal processing", "heat treatment",
    "processing conditions", "processing method",
    "cooking", "frying", "roasting", "baking",
    "food production", "food manufacturing",
    "industrial processing", "processing contamination",
    "processing induced", "food preparation"
]

# ---- FOOD PACKAGING ----
packaging_kw = [
    "food packaging", "packaging material",
    "plastic packaging", "polymer packaging",
    "packaging migration", "chemical migration",
    "migration study", "leaching",
    "food contact material", "fcm",
    "plastic container", "bottle", "packaged food",
    "storage container"
]

# ---- PLASTICISER ----
plasticiser_kw = [
    "bisphenol a", "bpa", "phthalate", "phthalates",
    "plasticizer", "plasticiser",
    "endocrine disruptor", "endocrine disrupting",
    "diethylhexyl phthalate", "dehp",
    "polymer additive", "plastic additive"
]

# ---- FOOD INGREDIENTS ----
ingredient_kw = [
    "food additive", "food additives",
    "food ingredient", "food component",
    "chemical additive", "additive exposure",
    "emulsifier", "preservative",
    "stabilizer", "colorant",
    "food formulation", "food composition"
]

# ---- HUMAN HEALTH ----
health_kw = [
    "toxicity", "health effect", "health effects",
    "risk assessment", "health risk",
    "disease", "inflammation", "oxidative stress",
    "cytotoxicity", "genotoxicity", "neurotoxicity",
    "carcinogenic", "metabolic disorder",
    "immune response", "biological effect",
    "adverse effect", "pathological"
]

# =========================
# HELPER FUNCTION
# =========================
def contains_any(text, keywords):
    return any(k in text for k in keywords)

# =========================
# HUMAN / ANIMAL SPLIT
# =========================
print("🔍 Classifying human vs animal...")

human_df = df[df["text"].apply(lambda x: contains_any(x, human_kw))]
animal_df = df[df["text"].apply(lambda x: contains_any(x, animal_kw))]

animal_df.to_csv("animal_microplastic.csv", index=False)

# =========================
# HUMAN SUBDIVISION
# =========================
print("🔍 Classifying human categories...")

human_processing = human_df[human_df["text"].apply(lambda x: contains_any(x, processing_kw))]
human_packaging = human_df[human_df["text"].apply(lambda x: contains_any(x, packaging_kw))]
human_plasticiser = human_df[human_df["text"].apply(lambda x: contains_any(x, plasticiser_kw))]
human_ingredient = human_df[human_df["text"].apply(lambda x: contains_any(x, ingredient_kw))]
human_health = human_df[human_df["text"].apply(lambda x: contains_any(x, health_kw))]

# =========================
# SAVE FILES
# =========================
human_df.to_csv("human_microplastic.csv", index=False)
human_processing.to_csv("human_processing.csv", index=False)
human_packaging.to_csv("human_packaging.csv", index=False)
human_plasticiser.to_csv("human_plasticiser.csv", index=False)
human_ingredient.to_csv("human_ingredients.csv", index=False)
human_health.to_csv("human_health.csv", index=False)

# =========================
# SUMMARY
# =========================
print("\n✅ Classification Complete")
print("Human papers:", len(human_df))
print("Animal papers:", len(animal_df))
print("Processing:", len(human_processing))
print("Packaging:", len(human_packaging))
print("Plasticiser:", len(human_plasticiser))
print("Ingredients:", len(human_ingredient))
print("Human Health:", len(human_health))

print("\n📁 All CSV files created successfully!")