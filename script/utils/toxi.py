import os
import pandas as pd
import re

# ----------- TOXICANT DICTIONARY ---------------- #

TOXICANTS = [
    "acrylamide", "aflatoxin", "aflatoxin b1", "aflatoxin m1",
    "mycotoxin", "mycotoxins", "ochratoxin", "deoxynivalenol",
    "fumonisin", "zearalenone", "3-mcpd", "melamine",
    "benzo[a]pyrene", "polycyclic aromatic hydrocarbons", "pah",
    "pesticide", "pesticide residues", "pesticides",
    "heavy metals", "arsenic", "lead", "cadmium", "mercury", "nickel",
    "bisphenol", "bisphenol a", "phthalate",
    "microplastic", "microplastics",
    "nanoparticle", "nanoparticles", "nanotoxicity",
    "pfas", "perfluoro", "endocrine disruptor"
]

# Normalize toxicants (lowercase)
TOXICANTS = [t.lower() for t in TOXICANTS]


# ----------- FUNCTION TO EXTRACT TOXICANTS ---------------- #

def find_toxicants_in_text(text):
    if not isinstance(text, str):
        return []
    text = text.lower()

    found = []
    for tox in TOXICANTS:
        if tox in text:
            found.append(tox)

    return found


# ----------- MAIN SCRIPT ---------------- #

DATA_FOLDER = "data/food/clean"  # <<< CHANGE IF NEEDED

csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]

for file in csv_files:
    print(f"Processing {file} ...")
    
    df = pd.read_csv(os.path.join(DATA_FOLDER, file))
    
    all_toxicants = set()

    for _, row in df.iterrows():
        combined_text = f"{row.get('Title','')} {row.get('Abstract','')} {row.get('Keyword','')}"
        found = find_toxicants_in_text(combined_text)
        all_toxicants.update(found)

    # Save toxicants to .txt file
    output_file = file.replace(".csv", "_TOXICANTS.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for tox in sorted(all_toxicants):
            f.write(tox + "\n")

    print(f"✔ Saved toxicant list → {output_file}")

print("\n🎉 DONE — All toxicants extracted!")
