import pandas as pd

# load remaining papers
df = pd.read_csv(r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\remaining_unclassified_papers.csv")

# define keyword groups
categories = {
    "packaging_release": [
        "packaging", "container", "cup", "bottle", "food container",
        "disposable", "paper cup", "take-out"
    ],
    "processing_effects": [
        "thermal", "heating", "digestion", "fermentation",
        "cooking", "processing", "boiling"
    ],
    "analytical_methods": [
        "detection", "spectroscopy", "raman", "ftir", "sers",
        "sensor", "analysis", "quantification", "method",
        "characterization", "microfluidic"
    ],
    "food_contamination": [
        "salt", "seafood", "milk", "beverages", "water",
        "vegetables", "fruits", "rice", "food", "tuna",
        "mussels", "shrimp"
    ],
    "biological_effects": [
        "toxicity", "stress", "cell", "cells", "macrophage",
        "hep", "growth", "germination", "intestinal",
        "microbiome", "neuron"
    ],
    "environmental_fate": [
        "environment", "transport", "pathway",
        "accumulation", "food web", "ecosystem"
    ],
    "polymer_material": [
        "polymer", "biodegradable", "film",
        "material", "bioplastic"
    ]
}

# classify titles
def classify(title):

    title = str(title).lower()

    for category, words in categories.items():

        for word in words:

            if word in title:
                return category

    return "other_uncategorized"


# apply classification
df["New_Category"] = df["Paper_Title"].apply(classify)

# create summary
summary = df["New_Category"].value_counts().reset_index()
summary.columns = ["Category", "Number_of_Papers"]

# Excel output
output_file = r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\categorized_remaining_papers.xlsx"

with pd.ExcelWriter(output_file) as writer:

    # full dataset
    df.to_excel(writer, sheet_name="All_Papers", index=False)

    # category sheets
    for cat in df["New_Category"].unique():
        df[df["New_Category"] == cat].to_excel(writer, sheet_name=cat[:31], index=False)

    # summary sheet
    summary.to_excel(writer, sheet_name="Summary", index=False)

print("Categorization complete.")
print(summary)
print("Excel file created:", output_file)