import os
import shutil

base = r"C:\Users\tanishk\OneDrive\Desktop\ToxiView\script"

folders = {
    "data_building": [
        "build_microplastic_excel",
        "build_microplastic_master_excel",
        "microplastic_doses_to_excel"
    ],
    "cleaning": [
        "clean_food_dataset",
        "filter_microplastic_non_review"
    ],
    "classification": [
        "categorize_files",
        "categorize_remaining_papers",
        "classify_microplastic_papers",
        "find_unclassified_papers"
    ],
    "toxicant_analysis": [
        "extract_animal_doses"
    ],
    "visualization": [
        "generate_bargraph"
    ],
    "utils": [
        "organize_toxiview",
        "first",
        "toxi"
    ]
}

for folder in folders:
    os.makedirs(os.path.join(base, folder), exist_ok=True)

for folder, files in folders.items():
    for file in files:
        src = os.path.join(base, file + ".py")
        dst = os.path.join(base, folder, file + ".py")

        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"Moved {file}.py -> {folder}")

print("Scripts organized successfully 🚀")