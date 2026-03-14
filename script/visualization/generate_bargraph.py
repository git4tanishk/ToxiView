import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import defaultdict

# -----------------------------------------------------
# CONFIG
# -----------------------------------------------------
CSV_FILE = "data/food/clean/(2)food_processing_toxicants_CLEAN.csv"
OUTPUT_FOLDER = "food_processing/"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

plt.style.use("seaborn-v0_8-colorblind")  # clean scientific style

# -----------------------------------------------------
# STEP 1 — LOAD FILE
# -----------------------------------------------------
df = pd.read_csv(CSV_FILE)

# Keep important columns
df = df[["Keyword", "Year", "PMID"]].dropna()

# Convert Year to int
def convert_year(x):
    try:
        return int(str(x).strip()[:4])
    except:
        return None

df["Year"] = df["Year"].apply(convert_year)
df = df.dropna(subset=["Year"])

# -----------------------------------------------------
# STEP 2 — Count papers for each toxicant per year
# -----------------------------------------------------
toxicant_counts = defaultdict(lambda: defaultdict(int))

for _, row in df.iterrows():
    tox = str(row["Keyword"]).strip()
    year = int(row["Year"])
    toxicant_counts[tox][year] += 1

# Get sorted toxicants
toxicants = sorted(toxicant_counts.keys())

# Group into sets of 4
groups_of_4 = [toxicants[i:i+4] for i in range(0, len(toxicants), 4)]

# -----------------------------------------------------
# STEP 3 — Generate solid bar graphs (rectangular bars)
# -----------------------------------------------------
for idx, group in enumerate(groups_of_4, start=1):

    plt.figure(figsize=(14, 8))

    # Collect all years used by any of the 4 toxicants
    all_years = sorted({year for tox in group for year in toxicant_counts[tox].keys()})

    bar_width = 0.18  
    positions = range(len(all_years))

    for i, tox in enumerate(group):
        counts = [toxicant_counts[tox][y] if y in toxicant_counts[tox] else 0 for y in all_years]

        # Offset each bar group
        offset_positions = [p + bar_width * i for p in positions]

        plt.bar(offset_positions, counts, width=bar_width, label=tox)

    plt.title(f"Processing Toxicants — Group {idx} (Bar Graph)", fontsize=16, weight="bold")
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Number of Papers", fontsize=14)

    # X-axis year labels
    plt.xticks([p + bar_width for p in positions], all_years, rotation=45)

    plt.legend(title="Food Processing–Related Contaminants", fontsize=10)
    plt.grid(axis="y", alpha=0.3)

    # Save chart
    save_path = os.path.join(OUTPUT_FOLDER, f"processing_group_{idx}.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✔ Saved: {save_path}")

print("\n🎉 All solid bar charts generated for PROCESSSING toxicants!")
