import os
import shutil

base_path = r"C:\Users\tanishk\OneDrive\Desktop\ToxiView"
csv_path = os.path.join(base_path, "csv_files")

folders = {
    "data/raw_data": [
        "microplastics_master_database",
        "microplastic_food_no_review",
        "PMID_Toxicant_Year"
    ],

    "data/cleaned_data": [
        "microplastics_master_database_cleaned"
    ],

    "data/categorized_papers": [
        "animal_microplastic",
        "human_microplastic",
        "human_packaging",
        "human_processing",
        "human_plasticiser",
        "human_health",
        "human_ingredients",
        "food_contamination",
        "environmental_fate",
        "biological_effects",
        "processing_effects",
        "packaging_release",
        "analytical_methods"
    ],

    "data/toxicant_dose_analysis": [
        "group1_safe_dose_papers",
        "group1_safe_dose_table",
        "group1_safe_dose_converted_ug",
        "group1_safe_dose_summary_stats",
        "toxicant_dose_summary_table"
    ],

    "data/remaining_papers": [
        "categorized_remaining_papers",
        "remaining_unclassified_papers",
        "other_uncategorized"
    ]
}

# Create folders
for folder in folders:
    os.makedirs(os.path.join(base_path, folder), exist_ok=True)

# Move files
for folder, files in folders.items():
    for file in files:
        for ext in [".csv", ".xlsx"]:
            source = os.path.join(csv_path, file + ext)
            if os.path.exists(source):
                dest = os.path.join(base_path, folder, file + ext)
                shutil.move(source, dest)
                print(f"Moved {file+ext} → {folder}")

print("\nToxiView files organized successfully!")