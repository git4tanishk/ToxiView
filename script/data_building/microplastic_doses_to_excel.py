import pandas as pd
import os
import re

BASE = r"C:\Users\tanishk\OneDrive\Desktop\ToxiView"

excel_file = os.path.join(BASE,"microplastics_master_database.xlsx")


# -----------------------------
# LOAD SHEETS
# -----------------------------

human_df = pd.read_excel(excel_file,"Human_studies")
animal_df = pd.read_excel(excel_file,"Animal_studies")
other_df = pd.read_excel(excel_file,"Other_studies")


# -----------------------------
# DOSE EXTRACTION
# -----------------------------

dose_pattern = re.compile(
    r'(\d+\.?\d*)\s*(mg|µg|ug|ng)/(kg|g)'
)


def extract_dose(text):

    text = str(text).lower()

    match = dose_pattern.search(text)

    if match:
        return match.group(0)

    return None


# -----------------------------
# CONVERT TO µg/kg
# -----------------------------

def convert_to_ug_per_kg(dose):

    if dose is None:
        return None

    match = dose_pattern.search(dose)

    if not match:
        return None

    value = float(match.group(1))
    unit = match.group(2)
    weight = match.group(3)

    if unit == "mg":
        value = value * 1000

    elif unit == "ng":
        value = value / 1000

    if weight == "g":
        value = value * 1000

    return round(value,3)


# -----------------------------
# PROCESS FUNCTION
# -----------------------------

def process(df):

    title = df["Paper_Title"].fillna("")

    text = df["text"].fillna("") if "text" in df.columns else ""

    combined = title + " " + text

    df["Dose_raw"] = combined.apply(extract_dose)

    df["Dose_ug_per_kg"] = df["Dose_raw"].apply(convert_to_ug_per_kg)

    df = df[df["Dose_ug_per_kg"].notna()]

    return df


# -----------------------------
# APPLY
# -----------------------------

human_dose = process(human_df)
animal_dose = process(animal_df)
other_dose = process(other_df)


print("Human dose papers:",len(human_dose))
print("Animal dose papers:",len(animal_dose))
print("Other dose papers:",len(other_dose))


# -----------------------------
# WRITE TO SAME EXCEL
# -----------------------------

with pd.ExcelWriter(
    excel_file,
    mode="a",
    engine="openpyxl",
    if_sheet_exists="replace"
) as writer:

    human_dose.to_excel(writer,"Human_doses",index=False)
    animal_dose.to_excel(writer,"Animal_doses",index=False)
    other_dose.to_excel(writer,"Other_doses",index=False)


print("\nDose sheets added to master Excel")