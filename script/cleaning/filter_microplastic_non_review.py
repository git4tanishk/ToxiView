# ==========================================
# FILE: filter_microplastic_fast.py
# PURPOSE:
# Fast filtering using batch PubMed requests
# ==========================================

from Bio import Entrez
import pandas as pd
import time
import os

# =========================
# REQUIRED BY NCBI
# =========================
Entrez.email = "msg4tanishk@gmail.com"

INPUT_FILE = r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\csv_files\PMID_Toxicant_Year.xlsx"
OUTPUT_FILE = r"microplastic_food_no_review.csv"

BATCH_SIZE = 200
DELAY = 0.5

# =========================
# LOAD EXCEL
# =========================
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(INPUT_FILE)

print("📂 Loading Excel...")
df = pd.read_excel(INPUT_FILE)

# =========================
# FLEXIBLE MICROPLASTIC FILTER
# =========================
df["Toxicant"] = df["Toxicant"].astype(str).str.lower().str.strip()

# keeps anything containing "microplastic"
df = df[df["Toxicant"].str.contains("microplastic", na=False)]

print("✔ Microplastic rows:", len(df))

if "PMID" not in df.columns:
    raise ValueError("PMID column required")

df = df.dropna(subset=["PMID"])
pmid_list = df["PMID"].astype(str).tolist()

# =========================
# BATCH FETCH FUNCTION
# =========================
def fetch_batch(pmids):
    try:
        time.sleep(DELAY)

        handle = Entrez.efetch(
            db="pubmed",
            id=",".join(pmids),
            rettype="xml"
        )
        records = Entrez.read(handle)
        handle.close()

        results = {}

        for article in records["PubmedArticle"]:
            med = article["MedlineCitation"]
            art = med["Article"]
            pmid = str(med["PMID"])

            # title
            title = art.get("ArticleTitle", "No Title")

            # year
            pub_date = art["Journal"]["JournalIssue"].get("PubDate", {})
            year = pub_date.get("Year", "Unknown")

            # publication type
            pub_types = art.get("PublicationTypeList", [])
            pub_types = [str(p).lower() for p in pub_types]
            is_review = any("review" in p for p in pub_types)

            results[pmid] = (title, year, is_review)

        return results

    except Exception as e:
        print("Batch fetch error:", e)
        return {}


# =========================
# PROCESS IN BATCHES
# =========================
print("\n🚀 Fetching data from PubMed (FAST MODE)...")

all_results = {}

for i in range(0, len(pmid_list), BATCH_SIZE):
    batch = pmid_list[i:i+BATCH_SIZE]

    print(f"Processing batch {i+1} → {i+len(batch)} / {len(pmid_list)}")

    batch_results = fetch_batch(batch)
    all_results.update(batch_results)

print("✔ PubMed fetch completed")

# =========================
# MAP RESULTS BACK TO DATAFRAME
# =========================
titles = []
years = []
reviews = []

for pmid in pmid_list:
    info = all_results.get(pmid, ("Not Found", "Unknown", False))
    titles.append(info[0])
    years.append(info[1])
    reviews.append(info[2])

df["Paper_Title"] = titles
df["Year"] = years
df["Is_Review"] = reviews

# =========================
# REMOVE REVIEW PAPERS
# =========================
df_final = df[df["Is_Review"] == False].drop(columns=["Is_Review"])

print("✔ Non-review papers:", len(df_final))

# =========================
# SAVE OUTPUT
# =========================
df_final.to_csv(OUTPUT_FILE, index=False)

print("\n✅ Saved:", OUTPUT_FILE)
print("⚡ Fast processing completed!")