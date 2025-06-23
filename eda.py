import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# loading cleaned data
df = pd.read_csv("data/cleaned_data.csv")

# setup
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# overview
print("\n Columns:", df.columns.tolist())
print("Shape:", df.shape)
print("Unique Crops:", df['crop'].nunique())
print("Year Range:", df['year'].min(), "→", df['year'].max())

# top 10 crops by frequency
top_crops = df['crop'].value_counts().nlargest(10)
top_crops.plot(kind="bar", title="TOP 10 CROPS BY FRERQUENCY")
plt.xlabel("crop")
plt.ylabel("count")
plt.tight_layout()
plt.savefig("plots/top_crops.png")
plt.show()

# Clipping unrealistic yields or outliers (keep rows with yield < 20 t/ha)
df = df[df["yield"] < 20]


# yeild distribution
sns.histplot(df['yield'], bins=50, kde=True)
plt.title("Distribution of Crop Yeild")
plt.xlabel("Yeild(tonnes/hectare)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("plots/yield_distribution.png")
plt.show()

# avg yield per crop (top 10)
avg_yield_crop = df.groupby("crop")['yield'].mean().nlargest(10)
avg_yield_crop.plot(kind="bar", title="Top 10 Crops by Avg Yield")
plt.ylabel("Avg Yield (tonnes/hectares)")
plt.tight_layout()
plt.savefig("plots/top_crops_avg_yield.png")
plt.show()

# yield trend over years (for major crops)
major_crop = "Rice"
df_major = df[df["crop"] == major_crop]
sns.lineplot(data=df_major, x="year", y="yield")
plt.title(f"Yield Trend of {major_crop} Over Time")
plt.tight_layout()
plt.savefig(f"plots/yield_trend_major_{major_crop.lower()}.png")
plt.show()

# yield trend over years (for a specific state)
state = "Bihar"
df_state = df[df["state"].str.lower() == state.lower()]
df_state = df_state[df_state["yield"] > 0]  # Only valid yields

plt.figure(figsize=(10, 6))
sns.lineplot(data=df_state, x="year", y="yield")
plt.title(f"Yield Trend in {state} Over Time")
plt.xlabel("Year")
plt.ylabel("Yield (tonnes/hectare)")
plt.tight_layout()
plt.savefig(f"plots/yield_trend_{state.lower()}_all_crops.png")
plt.show()