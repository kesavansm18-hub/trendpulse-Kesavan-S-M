
import requests
import json
import os
import time
from datetime import datetime

# the header they told us to add
headers = {"User-Agent": "TrendPulse/1.0"}

# keywords for each category (case-insensitive check later)
categories = {
    "technology":    ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":        ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"],
}

# Step 1: get the top 500 story IDs

print("Fetching top story IDs from HackerNews...")

try:
    response = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json",
        headers=headers,
        timeout=10
    )
    story_ids = response.json()[:500]  # only need the first 500
    print(f"Got {len(story_ids)} story IDs")
except Exception as e:
    print(f"Failed to get story IDs: {e}")
    story_ids = []

# Step 2: fetch story details and collect by category
# loop through each category one at a time
# for each category we go through story IDs until we have 25 matching stories
# then sleep 2 seconds before moving to the next category

all_stories = []
collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # same timestamp for all

for category, keywords in categories.items():
    print(f"\nCollecting stories for: {category}")
    count = 0  # how many stories we have for this category so far

    for story_id in story_ids:
        if count >= 25:
            break  # we already have 25 for this category, stop

        # fetch the individual story details
        try:
            r = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                headers=headers,
                timeout=10
            )
            story = r.json()
        except Exception as e:
            print(f"  Failed to fetch story {story_id}: {e}")
            continue  # skip this one and move on, don't crash

        # skip if story has no title (some posts are job listings or deleted)
        if not story or not story.get("title"):
            continue

        title = story.get("title", "")

        # check if any keyword for this category appears in the title
        title_lower = title.lower()
        matched = False
        for keyword in keywords:
            if keyword in title_lower:
                matched = True
                break

        if not matched:
            continue  # doesn't belong to this category

        # pull out all 7 required fields
        record = {
            "post_id":      story.get("id"),
            "title":        title,
            "category":     category,
            "score":        story.get("score", 0),
            "num_comments": story.get("descendants", 0),  # HN calls comments "descendants"
            "author":       story.get("by", ""),
            "collected_at": collected_at,
        }

        all_stories.append(record)
        count += 1
        print(f"  [{count}/25] {title[:70]}")

    # sleep 2 seconds between each category — one sleep per category loop
    print(f"  Done with {category} ({count} stories). Sleeping 2s...")
    time.sleep(2)

# Step 3: save everything to a JSON file

# make the data/ folder if it doesn't already exist
os.makedirs("data", exist_ok=True)

# include today's date in the filename
date_str = datetime.now().strftime("%Y%m%d")
filename = f"data/trends_{date_str}.json"

with open(filename, "w") as f:
    json.dump(all_stories, f, indent=2)

print(f"\nCollected {len(all_stories)} stories. Saved to {filename}")