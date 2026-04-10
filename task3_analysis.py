
import pandas as pd
import numpy as np

# Step 1: load and explore

df = pd.read_csv("data/trends_clean.csv")

# print shape first like the expected output shows
print(f"Loaded data: {df.shape}")

print("\nFirst 5 rows:")
print(df.head().to_string(index=False))

# average score and comments across all stories
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

# Step 2: NumPy stats

# convert score column to a numpy array so we can use numpy functions
scores = np.array(df["score"])

print("\n--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):,.0f}")
print(f"Median score : {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score    : {np.max(scores):,}")
print(f"Min score    : {np.min(scores):,}")

# which category has the most stories
top_cat = df["category"].value_counts().idxmax()
top_cat_count = df["category"].value_counts().max()
print(f"\nMost stories in: {top_cat} ({top_cat_count} stories)")

# which story has the most comments
most_comments_idx = df["num_comments"].idxmax()
most_comments_title = df.loc[most_comments_idx, "title"]
most_comments_count = df.loc[most_comments_idx, "num_comments"]
print(f'\nMost commented story: "{most_comments_title}" --- {most_comments_count} comments')

# Step 3: add new columns

# engagement = how much discussion per upvote
# adding 1 to score to avoid dividing by zero
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if the story's score is above the average score
df["is_popular"] = df["score"] > avg_score

# Step 4: save the updated dataframe

df.to_csv("data/trends_analysed.csv", index=False)
print("\nSaved to data/trends_analysed.csv")