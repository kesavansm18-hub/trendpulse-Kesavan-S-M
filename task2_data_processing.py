
import pandas as pd
import os
import glob

# Step 1: load the JSON file from the data/ folder
# find the trends JSON file task 1 created
json_files = glob.glob("data/trends_*.json")
if not json_files:
    print("No JSON file found in data/. Run task1 first.")
else:
    json_file = json_files[0]  # grab the first one found

    df = pd.read_json(json_file)
    print(f"Loaded {len(df)} stories from {json_file}")

    # Step 2: clean the data
    # remove duplicate stories — same post_id means same story
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # drop rows where post_id, title, or score is missing
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # make sure score and num_comments are stored as integers not floats
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # remove low quality stories — anything with a score under 5
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # strip whitespace from the title column
    df["title"] = df["title"].str.strip()

    # Step 3: save as CSV
    output_path = "data/trends_clean.csv"
    df.to_csv(output_path, index=False)

    print(f"\nSaved {len(df)} rows to {output_path}")

    # print how many stories we have per category
    print("\nStories per category:")
    print(df["category"].value_counts().to_string())