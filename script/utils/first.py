from Bio import Entrez
import pandas as pd
import os
import time

# REQUIRED BY NCBI
Entrez.email = "your_email@example.com"   # <-- put your email here

MAX_RESULTS = 3000
DELAY = 0.4


# -------------------------------
# FOOD FILTER MODULE
# -------------------------------
def add_food_filter(keyword: str) -> str:
    """
    For broad keywords, automatically add a strict food filter.
    For specific toxicants, return as-is.
    """
    broad_terms = [
        "toxicity", "stress", "risk", "assessment", "damage", "exposure",
        "oxidative stress", "risk assessment", "toxicology", "genotoxicity",
        "cytotoxicity", "public health", "contamination", "chemical exposure",
        "nanotoxicity", "metal exposure", "digestion", "health risk"
    ]

    if any(term in keyword.lower() for term in broad_terms):
        return (
            f"({keyword}) AND "
            "(food OR foodstuff OR edible OR dietary OR "
            "'food contamination' OR 'food toxicology' OR ingestion)"
        )
    else:
        return keyword


# -------------------------------
# KEYWORD GROUPS
# -------------------------------
GROUPS = {

    "(1)major_food_toxicants.csv": [
        "acrylamide", "aflatoxin b1", "aflatoxin m1",
        "mycotoxin", "mycotoxins", "ochratoxin a",
        "deoxynivalenol", "fumonisins", "zearalenone",
        "3-mcpd", "melamine",
        "benzo[a]pyrene AND food",
        "polycyclic aromatic hydrocarbons AND food",
        "pesticide residues", "pesticides food",
        "heavy metals food", "arsenic food", "lead food",
        "cadmium food", "mercury food", "nickel food",
        "endocrine disruptors food", "bisphenol a food",
        "phthalates food", "microplastic food", "microplastics food"
    ],

    "(2)food_processing_toxicants.csv": [
        "deep frying food contaminants",
        "roasting food contaminants",
        "oxidation",
        "heterocyclic amines",
        "food emulsions contamination",
        "food packaging migration",
        "plastic containers food",
        "preservatives",
        "preservative residues food",
        "food additives toxicity",
        "biogenic amine food",
        "sodium benzoate food"
    ],

    "(3)microbial_food_toxicants.csv": [
        "campylobacter food",
        "clostridium perfringens food",
        "salmonella food",
        "foodborne pathogens",
        "foodborne illness",
        "bacterial contamination",
        "fecal contamination food"
    ],

    "(4)food_matrices.csv": [
        "milk contamination", "dairy contamination",
        "infant formula contamination",
        "imported rice contamination",
        "chicken contamination", "frozen chicken contamination",
        "vegetables contamination", "fruit contamination",
        "cheese contamination", "soybean contamination",
        "wheat contamination", "seafood safety"
    ],

    "(5)exposure_toxicity_terms.csv": [
        "dietary exposure",
        "digestion", "simulated digestion",
        "oral toxicity", "acute toxicity",
        "subacute toxicity", "hepatotoxicity",
        "nephrotoxicity", "genotoxicity",
        "cytotoxicity",
        "oxidative stress",
        "dna damage",
        "mitochondrial dysfunction",
        "reproductive toxicity",
        "health risk", "risk assessment",
        "food safety"
    ],

    "(6)food_related_chemicals.csv": [
        "5-hydroxymethylfurfural",
        "silver nanoparticles food packaging",
        "halloysite nanotubes food",
        "graphene oxide biochar food",
        "nanomaterials", "nanoparticles",
        "nanotoxicity"
    ],

    "(7)food_lab_methods.csv": [
        "gc/ms food", "hplc food",
        "ftir analysis food", "lc-ms/ms food",
        "icp-oes food", "analytical method food",
        "detection method food"
    ],

    "(8)env_to_food_contamination.csv": [
        "soil contamination food crops",
        "groundwater contamination food chain",
        "sewage water food contamination",
        "environmental pollutants food",
        "landfill contamination crops",
        "water safety food",
        "coastal pollution seafood",
        "agroecological safety crops"
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
    # records might not have 'PubmedArticle' key in some cases
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

    # if no data, this returns empty DF (0 rows, 0 columns)
    return pd.DataFrame(data)


# -------------------------------
# MAIN LOOP
# -------------------------------
for filename, keywords in GROUPS.items():

    print(f"\n🔵 Processing file: {filename}")

    # SAFE LOAD (handles empty file case)
    if os.path.exists(filename):
        try:
            df_existing = pd.read_csv(filename)
        except pd.errors.EmptyDataError:
            print(f"⚠ {filename} is empty — creating new structure.")
            df_existing = pd.DataFrame(columns=["Title", "Journal", "Year", "PMID", "Abstract", "Keyword"])
    else:
        df_existing = pd.DataFrame(columns=["Title", "Journal", "Year", "PMID", "Abstract", "Keyword"])

    # ensure correct columns even if file was weird
    for col in ["Title", "Journal", "Year", "PMID", "Abstract", "Keyword"]:
        if col not in df_existing.columns:
            df_existing[col] = ""

    pmid_set = set(df_existing["PMID"].astype(str)) if "PMID" in df_existing.columns else set()

    df_new = pd.DataFrame(columns=["Title", "Journal", "Year", "PMID", "Abstract", "Keyword"])

    for kw in keywords:
        filtered_kw = add_food_filter(kw)
        print(f"   🔍 Searching: {filtered_kw}")

        try:
            ids = search_pubmed(filtered_kw)
        except Exception as e:
            print("     ⚠ Search failed:", e)
            continue

        # remove already extracted PMIDs
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

        # 👉 SKIP if nothing parsed or no PMID column
        if df.empty or "PMID" not in df.columns:
            print("     ⚠ Parsed 0 articles for this keyword.")
            continue

        df["Keyword"] = kw

        df_new = pd.concat([df_new, df], ignore_index=True)
        pmid_set.update(df["PMID"].astype(str))

    # merge old + new
    final_df = pd.concat([df_existing, df_new], ignore_index=True)
    final_df.drop_duplicates(subset="PMID", inplace=True)

    final_df.to_csv(filename, index=False, encoding="utf-8")
    print(f"✔ Updated: {filename} — Total papers: {len(final_df)}")

print("\n🎉 ALL GROUPS UPDATED SUCCESSFULLY!")
