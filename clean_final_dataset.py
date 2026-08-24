"""
Cleans final_dhaka_dataset.json and writes final_dhaka_dataset_clean.json.

Fixes applied:
1. Normalize `subreddit` casing (Dhaka/dhaka -> dhaka).
2. Fill missing `permalink` from `url` when `url` is itself a reddit.com
   thread link (covers gallery/comments links); left null when the only
   captured url is external media (i.redd.it/v.redd.it) or a non-reddit
   site, since the true discussion thread link can't be recovered from
   the stored data.
3. Normalize null `body` to empty string (link/gallery posts with no
   selftext) instead of leaving JSON null.
4. Drop exact duplicate posts (same permalink where permalink is known).
"""
import json

SRC = "final_dhaka_dataset.json"
OUT = "final_dhaka_dataset_clean.json"

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

seen_permalinks = set()
cleaned = []
stats = {
    "subreddit_normalized": 0,
    "permalink_filled": 0,
    "permalink_still_missing": 0,
    "body_nulls_fixed": 0,
    "duplicates_dropped": 0,
}

for r in data:
    sub = (r.get("subreddit") or "").strip()
    sub_norm = sub.lower()
    if sub_norm != sub:
        stats["subreddit_normalized"] += 1
    r["subreddit"] = sub_norm

    if r.get("body") is None:
        r["body"] = ""
        stats["body_nulls_fixed"] += 1

    permalink = r.get("permalink")
    url = r.get("url") or ""
    if not permalink:
        if "reddit.com" in url:
            r["permalink"] = url
            stats["permalink_filled"] += 1
        else:
            r["permalink"] = None
            stats["permalink_still_missing"] += 1

    dedup_key = r.get("permalink") or r.get("url")
    if dedup_key in seen_permalinks:
        stats["duplicates_dropped"] += 1
        continue
    seen_permalinks.add(dedup_key)

    cleaned.append(r)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"Input rows:  {len(data)}")
print(f"Output rows: {len(cleaned)}")
print("Stats:")
for k, v in stats.items():
    print(f"  {k}: {v}")

sub_counts = {}
for r in cleaned:
    sub_counts[r["subreddit"]] = sub_counts.get(r["subreddit"], 0) + 1
print("Subreddit breakdown after cleaning:", sub_counts)
