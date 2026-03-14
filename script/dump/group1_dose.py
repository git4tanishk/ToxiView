from Bio import Entrez
import pandas as pd
import os
import time

# REQUIRED BY NCBI
Entrez.email = "msg4tanishk@gmail.com"   # put your email here

MAX_RESULTS = 3000
DELAY = 0.4

# -------------------------------
# GROUP 1: MAJOR TOXICANTS (DOSE)
# -------------------------------
GROUP1_DOSE = {
    "(1a)_major_food_toxicants_dose.csv": [
        "acrylamide AND (dose OR dose-response OR dietary intake OR NOAEL OR LOAEL)",
        "aflatoxin b1 AND (dose-response OR daily intake OR tolerable daily intake OR risk assessment)",
        "aflatoxin m1 AND (dietary exposure OR acceptable daily intake OR MRL)",
        "mycotoxins AND (dose OR dietary exposure OR risk assessment)",
        "benzo[a]pyrene AND food AND (dose OR margin of exposure)",
        "polycyclic aromatic hydrocarbons AND food AND (dietary intake OR dose-response)",
        "pesticide residues AND food AND (dietary exposure OR acceptable daily intake)",
        "arsenic food AND (daily intake OR benchmark dose OR risk assessment)",
        "lead food AND (blood level OR dietary exposure OR NOAEL)",
        "cadmium food AND (bioavailability OR oral dose OR benchmark dose)",
        "mercury food AND (dietary intake OR biomonitoring OR dose-response)",
        "nickel food AND (exposure level OR tolerable daily intake)",
        "bisphenol a food AND (dose-response OR acceptable daily intake)",
        "phthalates food AND (daily intake OR biomonitoring)",
        "microplastics food AND (dose dependent OR ingestion exposure)"
    ]
}

# -------------------------------
# PubMed helper functions
# -------------------------------
def search_pubmed(query: str):
    time.sleep(DELAY)
    handle = Entrez.esearch(db="pubmed", term=query, retmax=MAX_RESULTS)
    record = Entrez.read(handle)
    handle.close()
    return record.get("IdList", [])


def fetch_details(id_list):
    ids = ",".join(id_list)
    handle = Entrez.efetch(db="pubmed", id=ids, rettype="xml")
    records = Entrez.read(handle)
    handle.close()
    return records


def parse_records(records):
    data = []
    articles = records.get("PubmedArticle", [])

    for article in articles:
        med = article["MedlineCitation"]
        art = med["Article"]

        title = art.get("ArticleTitle", "No Title")

        abstract = ""
        if "Abstract" in art:
            abstract = " ".join(str(x) for x in art["Abstract"].get("AbstractText", []))

        journal = art["Journal"].get("Title", "No Journal")
        pub_date = art["Journal"]["JournalIssue"].get("PubDate", {})
        year = pub_date.get("Year", "Unknown")
        pmid = med.get("PMID", "")

        data.append({
            "Title": title,
            "Journal": journal,
            "Year": year,
            "PMID": str(pmid),
            "Abstract": abstract
        })

    return pd.DataFrame(data)


# -------------------------------
# MAIN LOOP
# -------------------------------
for filename, keywords in GROUP1_DOSE.items():

    print(f"\n🔵 Processing file: {filename}")

    if os.path.exists(filename):
        try:
            df_existing = pd.read_csv(filename)
        except pd.errors.EmptyDataError:
            df_existing = pd.DataFrame(columns=["Title", "Journal", "Year", "PMID", "Abstract", "Keyword"])
    else:
        df_existing = pd.DataFrame(columns=["Title", "Journal", "Year", "PMID", "Abstract", "Keyword"])

    pmid_set = set(df_existing["PMID"].astype(str)) if "PMID" in df_existing.columns else set()
    df_new = pd.DataFrame(columns=["Title", "Journal", "Year", "PMID", "Abstract", "Keyword"])

    for kw in keywords:
        print(f"   🔍 Searching: {kw}")

        try:
            ids = search_pubmed(kw)
        except Exception as e:
            print("     ⚠ Search failed:", e)
            continue

        ids = [i for i in ids if i not in pmid_set]

        if not ids:
            print("     ❌ No new results.")
            continue

        try:
            records = fetch_details(ids)
        except Exception as e:
            print("     ⚠ Fetch failed:", e)
            continue

        df = parse_records(records)

        if df.empty:
            print("     ⚠ No parsed articles.")
            continue

        df["Keyword"] = kw
        df_new = pd.concat([df_new, df], ignore_index=True)
        pmid_set.update(df["PMID"].astype(str))

    final_df = pd.concat([df_existing, df_new], ignore_index=True)
    final_df.drop_duplicates(subset="PMID", inplace=True)

    final_df.to_csv(filename, index=False, encoding="utf-8")
    print(f"✔ Updated: {filename} — Total papers: {len(final_df)}")

print("\n🎉 GROUP 1 (DOSE) EXTRACTION DONE!")
