import pandas as pd
import re

# --------------------------------
# INPUT FILE
# --------------------------------

file = r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\microplastics_master_database.xlsx"

df = pd.read_excel(file, sheet_name="Animal_studies")

print("Total animal papers:", len(df))

# --------------------------------
# KEYWORDS
# --------------------------------

species_keywords = {
"mouse":["mouse","mice"],
"rat":["rat"],
"zebrafish":["zebrafish"],
"fish":["fish"],
"shrimp":["shrimp"],
"larvae":["larvae"],
"pig":["pig"]
}

food_keywords = [
"fish","milk","salt","rice","seafood","shrimp",
"tuna","mussels","water","beverage","vegetable",
"fruit","food","meat"
]

# --------------------------------
# DOSE REGEX
# --------------------------------

dose_pattern = re.compile(
r'(\d+\.?\d*)\s*(mg|µg|ug|ng)\s*(\/|\s)?\s*(kg|kg-1|kg−1)',
re.IGNORECASE
)

# --------------------------------
# FUNCTIONS
# --------------------------------

def detect_species(text):

    text = text.lower()

    for sp, words in species_keywords.items():

        if any(w in text for w in words):
            return sp

    return "unknown"


def detect_food(text):

    text = text.lower()

    for food in food_keywords:

        if food in text:
            return food

    return "unknown"


def extract_dose(text):

    match = dose_pattern.search(text)

    if match:

        value = match.group(1)
        unit = match.group(2) + "/" + match.group(4)

        return value, unit

    return None, None


# --------------------------------
# PROCESS PAPERS
# --------------------------------

records = []

for _, row in df.iterrows():

    title = str(row.get("Paper_Title",""))
    text = str(row.get("text",""))

    combined = title + " " + text

    dose_value, dose_unit = extract_dose(combined)

    if dose_value is None:
        continue

    species = detect_species(combined)
    food = detect_food(combined)

    records.append({
        "PMID": row.get("PMID",""),
        "Title": title,
        "Species": species,
        "Food_article": food,
        "Dose_value": dose_value,
        "Dose_unit": dose_unit
    })

dose_df = pd.DataFrame(records)

print("Papers with detected doses:", len(dose_df))

# --------------------------------
# SUMMARY TABLES
# --------------------------------

species_summary = dose_df["Species"].value_counts().reset_index()
species_summary.columns = ["Species","Number_of_Papers"]

food_summary = dose_df["Food_article"].value_counts().reset_index()
food_summary.columns = ["Food_article","Number_of_Papers"]

dose_stats = dose_df["Dose_value"].astype(float).describe()

# --------------------------------
# SAVE EXCEL
# --------------------------------

output = r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\animal_dose_summary.xlsx"

with pd.ExcelWriter(output) as writer:

    dose_df.to_excel(writer,"Animal_dose_papers",index=False)

    species_summary.to_excel(writer,"Species_summary",index=False)

    food_summary.to_excel(writer,"Food_summary",index=False)

    dose_stats.to_frame().to_excel(writer,"Dose_statistics")

print("Excel created:", output)