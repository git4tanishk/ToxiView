import pandas as pd
import matplotlib.pyplot as plt

# =========================
# SETTINGS
# =========================
INPUT_FILE = "group1_safe_dose_summary_stats.csv"
UNIT = "µg/kg bw/day"   # change if needed

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(INPUT_FILE)

# sort by safe dose (mean)
df = df.sort_values("mean")

values = df["mean"]
labels = df["Toxicant"]

# =========================
# CREATE RULER SCALE
# =========================
plt.figure(figsize=(4, 10))

# Main vertical scale line
plt.plot([0, 0], [values.min(), values.max()], linewidth=2)

# Create ruler ticks
max_val = values.max()
step = max_val / 10

plt.yticks([round(i,2) for i in list(range(0, int(max_val)+1, int(step)))])
plt.xticks([])

# Plot toxicants with exact values + unit
for v, name in zip(values, labels):
    label_text = f"{name} ({v:.3f} {UNIT})"
    plt.scatter(0, v, s=40)
    plt.text(0.1, v, label_text, va="center", fontsize=9)

# Axis labels and title
plt.ylabel(f"Safe dose scale ({UNIT})", fontsize=11)
plt.title("Relative Safe Dose Scale of Major Food Toxicants", fontsize=12)

# Clean professional look
plt.box(False)
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()
