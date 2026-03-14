import pandas as pd
import matplotlib.pyplot as plt

# =========================
# INPUT FILE
# =========================
INPUT_FILE = "group1_safe_dose_summary_stats.csv"

# =========================
# LOAD YOUR DATA
# =========================
df_lit = pd.read_csv(INPUT_FILE)

# =========================
# OFFICIAL SAFE DOSES (WHO/EFSA) in µg/kg bw/day
# =========================
official_safe_dose = {
    "acrylamide": 0.17,
    "arsenic": 3.0,
    "cadmium": 0.8,
    "mercury": 0.1,
    "nickel": 2.8,
    "bisphenol": 0.0002,
    "phthalates": 50.0,
    "lead": 0.0,         # no safe threshold
    "aflatoxin": 0.0,    # no safe dose
    "mycotoxin": 0.014,  # ochratoxin A example
    "pesticide": 1.0     # generic reference
}

df_official = pd.DataFrame(
    official_safe_dose.items(),
    columns=["Toxicant", "Official_Safe_Dose"]
)

# =========================
# MERGE
# =========================
df_compare = pd.merge(df_lit, df_official, on="Toxicant", how="inner")

# =========================
# PLOT
# =========================
plt.figure(figsize=(8,6))

plt.plot(df_compare["Toxicant"], df_compare["mean"], marker="o", label="Literature Mean Dose")
plt.plot(df_compare["Toxicant"], df_compare["Official_Safe_Dose"], marker="s", label="Official Safe Dose")

plt.xticks(rotation=45, ha="right")
plt.ylabel("Dose (µg/kg body weight/day)")
plt.title("Literature-Reported Dose vs Official Safe Dose (WHO/EFSA)")
plt.legend()
plt.tight_layout()
plt.show()
