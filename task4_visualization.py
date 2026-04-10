
import pandas as pd
import matplotlib.pyplot as plt
import os

# Step 1: load the data and create outputs folder

df = pd.read_csv("data/trends_analysed.csv")
print(f"Loaded {len(df)} rows from data/trends_analysed.csv")

os.makedirs("outputs", exist_ok=True)  # create outputs/ if it doesn't exist

# Chart 1: Top 10 Stories by Score (horizontal bar)
# get the top 10 stories sorted by score
top10 = df.nlargest(10, "score").sort_values("score")

# shorten titles that are longer than 50 characters
titles = []
for t in top10["title"]:
    if len(t) > 50:
        titles.append(t[:50] + "...")
    else:
        titles.append(t)

fig, ax = plt.subplots(figsize=(12, 6))

ax.barh(titles, top10["score"], color="steelblue")

ax.set_title("Top 10 Stories by Score")
ax.set_xlabel("Score (upvotes)")
ax.set_ylabel("Story Title")

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")  # save before show
plt.show()
print("Saved outputs/chart1_top_stories.png")

# Chart 2: Stories per Category (bar chart)
cat_counts = df["category"].value_counts()

# different colour for each bar as instructed
colours = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"]

fig, ax = plt.subplots(figsize=(8, 5))

ax.bar(cat_counts.index, cat_counts.values, color=colours)

ax.set_title("Number of Stories per Category")
ax.set_xlabel("Category")
ax.set_ylabel("Number of Stories")

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")  # save before show
plt.show()
print("Saved outputs/chart2_categories.png")

# Chart 3: Score vs Comments scatter plot
# split into popular and non-popular using the is_popular column from task 3
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig, ax = plt.subplots(figsize=(9, 6))

# different colours for popular vs non-popular
ax.scatter(not_popular["score"], not_popular["num_comments"],
           color="cornflowerblue", alpha=0.6, label="Not Popular", s=50)
ax.scatter(popular["score"], popular["num_comments"],
           color="tomato", alpha=0.8, label="Popular", s=60)

ax.set_title("Score vs Number of Comments")
ax.set_xlabel("Score")
ax.set_ylabel("Number of Comments")
ax.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")  # save before show
plt.show()
print("Saved outputs/chart3_scatter.png")

# Bonus: Dashboard — all 3 charts in one figure

fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight="bold")

# panel 1 — top 10 stories
axes[0].barh(titles, top10["score"], color="steelblue")
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].tick_params(axis="y", labelsize=7)

# panel 2 — stories per category
axes[1].bar(cat_counts.index, cat_counts.values, color=colours)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Count")
axes[1].tick_params(axis="x", rotation=15)

# panel 3 — score vs comments
axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                color="cornflowerblue", alpha=0.6, label="Not Popular", s=30)
axes[2].scatter(popular["score"], popular["num_comments"],
                color="tomato", alpha=0.8, label="Popular", s=40)
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend(fontsize=8)

plt.tight_layout()
plt.savefig("outputs/dashboard.png")  # save before show
plt.show()
print("Saved outputs/dashboard.png")

print("\nAll done!")
print("outputs/")
print("  chart1_top_stories.png")
print("  chart2_categories.png")
print("  chart3_scatter.png")
print("  dashboard.png")