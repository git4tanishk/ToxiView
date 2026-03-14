import pandas as pd
import os
import re

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
# LOAD FILE FUNCTION
# -----------------------------

def load_group(files):

    frames = []

    for f in files:

        path = os.path.join(BASE,f)

        if os.path.exists(path):

            df = pd.read_csv(path)

            print(f"Loaded {f}: {len(df)} papers")

            df["Source_File"] = f

            frames.append(df)

    df = pd.concat(frames,ignore_index=True)

    if "PMID" in df.columns:

        before = len(df)

        df = df.drop_duplicates(subset="PMID")

        print("Duplicates removed:",before-len(df))

    return df


# -----------------------------
# LOAD DATA
# -----------------------------

human_df = load_group(human_files)
animal_df = load_group(animal_files)
other_df = load_group(other_files)

print("\nCounts after deduplication")

print("Human:",len(human_df))
print("Animal:",len(animal_df))
print("Other:",len(other_df))


# -----------------------------
# COMBINE ALL PAPERS
# -----------------------------

all_df = pd.concat([human_df,animal_df,other_df],ignore_index=True)


# -----------------------------
# FOOD DETECTION
# -----------------------------

foods = [
"milk","fish","seafood","shrimp","crab","salt","rice",
"vegetable","fruit","water","beverage","tea","coffee",
"meat","egg","oil","honey","sugar"
]

def detect_food(text):

    text = str(text).lower()

    for f in foods:

        if f in text:
            return f

    return "unknown"


# -----------------------------
# MODEL DETECTION
# -----------------------------

models = {
"human":"human",
"mouse":"mouse",
"mice":"mouse",
"rat":"rat",
"zebrafish":"fish",
"fish":"fish",
"cell":"cell culture",
"caco":"cell culture",
"hep":"cell culture"
}

def detect_model(text):

    text = str(text).lower()

    for k,v in models.items():

        if k in text:
            return v

    return "other"


# -----------------------------
# DOSE EXTRACTION
# -----------------------------

def extract_dose(text):

    text = str(text).lower()

    match = re.search(r'(\d+\.?\d*\s*(mg|µg|ug|ng|particles)[^\s]*)',text)

    if match:
        return match.group(1)

    return None


# -----------------------------
# APPLY EXTRACTION
# -----------------------------

combined_text = all_df["Paper_Title"].fillna("") + " " + all_df["text"].fillna("")

all_df["Food Article"] = combined_text.apply(detect_food)

all_df["Model System"] = combined_text.apply(detect_model)

all_df["Dose"] = combined_text.apply(extract_dose)

all_df["Reference"] = all_df["Paper_Title"]

all_df["Key Inference"] = ""


food_table = all_df[
[
"Food Article",
"Model System",
"Dose",
"Key Inference",
"Reference"
]
]


# -----------------------------
# SUMMARY
# -----------------------------

summary = food_table.groupby(
["Food Article","Model System"]
).size().reset_index(name="No_of_Papers")


counts = pd.DataFrame({

"Category":["Human","Animal","Other"],

"Papers":[
len(human_df),
len(animal_df),
len(other_df)
]

})


# -----------------------------
# SAVE EXCEL
# -----------------------------

output = os.path.join(BASE,"microplastics_master_database.xlsx")

if os.path.exists(output):

    os.remove(output)


with pd.ExcelWriter(output) as writer:

    human_df.to_excel(writer,"Human_studies",index=False)

    animal_df.to_excel(writer,"Animal_studies",index=False)

    other_df.to_excel(writer,"Other_studies",index=False)

    counts.to_excel(writer,"Summary_counts",index=False)

    food_table.to_excel(writer,"Food_Model_Table",index=False)

    summary.to_excel(writer,"Food_Model_Summary",index=False)


print("\nExcel created successfully")
print(output)