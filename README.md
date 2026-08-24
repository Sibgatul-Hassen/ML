# Dhaka/Bangladesh Reddit Data Pipeline

A data-collection and sentiment-analysis pipeline built entirely around **Reddit** posts from **r/dhaka** and **r/bangladesh**. It crawls posts, cleans and deduplicates them into a single dataset, runs sentiment/emotion/topic analysis over that dataset, and generates human-readable HTML/Markdown reports.

There is no Quora, Twitter, or other platform involved anywhere in this project — Reddit is the only data source.

## Project status

- **The dataset is complete and clean.** [`final_dhaka_dataset_clean.json`](final_dhaka_dataset_clean.json) / [`.csv`](final_dhaka_dataset_clean.csv) is the canonical output: **1,854 unique, deduplicated posts** spanning 2013–2025 (most of it Aug–Nov 2025), covering r/dhaka and r/bangladesh.
- **The sentiment/topic analysis pipeline runs against that final dataset**, not an old snapshot — every script and every output file under `sentiment_analysis/`, `advanced_sentiment_analysis/`, `general_bangladesh_analysis/`, and `formatted_output/` reflects the full 1,854-post dataset.
- **Crawling is currently blocked.** Reddit's public JSON API now returns `403 Forbidden` for unauthenticated requests from this environment. The crawler scripts (`crawl*.py`) are left as-is; extending the dataset further would require setting up a Reddit OAuth app (see [Known limitations](#known-limitations)).

## Pipeline overview

```
crawl*.py                    → raw Reddit posts (JSON/CSV snapshots)
        ↓
to_json.py / clean_final_dataset.py → final_dhaka_dataset_clean.json/.csv (deduplicated, canonical dataset)
        ↓
sentiment_analysis.py, advanced_sentiment_analysis.py, format_csv.py, filter_dhaka_people_posts.py
        ↓ (advanced_sentiment_analysis.py output feeds these)
check_dhaka_relevance.py → analyze_general_bangladesh_posts.py
                          → what_are_people_talking_about.py
        ↓
generate_dataset_html.py, generate_dataset_markdown.py, generate_json_report.py, generate_sentiment_html.py
        → dataset_overview.html/.md, sentiment_overview.html, combined_dhaka_overview.html
```

`analyze_location_based_posts.py` is a separate branch — it analyzes `location_based_posts_20251119_232939.csv`, a different dataset built from `crawl_by_user_location.py` (posts from users whose profile location is Dhaka, rather than keyword/subreddit matches). It isn't merged into the main final dataset.

## The dataset

| File | Rows | Notes |
|---|---|---|
| `final_dhaka_dataset_clean.json` / `.csv` | 1,854 | **Canonical dataset.** Deduplicated by URL, subreddit casing normalized, permalinks backfilled where recoverable, null bodies normalized to `""`. |
| `final_dhaka_dataset.json` | 1,854 | Pre-cleaning version (mixed subreddit casing, some null permalinks). |
| `dhaka_extended_posts.json`, `combined_dhaka_posts.json`, `reddit_data*.json`, `dhaka_posts_*.csv`, `dhaka_json_data.csv` | varies | Raw snapshots from individual crawl runs, later merged into `final_dhaka_dataset.json`. Kept for provenance. |
| `location_based_posts_20251119_232939.csv` | ~613 | Separate dataset: posts from users with a Dhaka profile location. |

Each post record has: `title`, `body`, `url`, `author`, `upvotes`, `comments`, `date`, `subreddit`, `permalink`.

**Known data caveat:** 60 of the 1,854 posts (3%) have `permalink: null` — their only captured link was a direct media URL (`i.redd.it`/`v.redd.it`) or an external site, so the actual Reddit discussion thread can't be recovered from the stored data alone.

## Scripts

### Crawling (currently non-functional — see [Known limitations](#known-limitations))
- `crawl.py` — keyword search across subreddits via Reddit's public JSON API.
- `crawl_by_dhaka_areas.py` — searches by named Dhaka neighborhoods (Uttara, Mirpur, Gulshan, etc.).
- `crawl_by_user_location.py` — finds posts from users with a Dhaka profile location.
- `crawl_dhaka_extended.py` — extended keyword/area crawl.

### Dataset assembly
- `to_json.py` — merges two raw JSON snapshots and dedupes by URL → `final_dhaka_dataset.json`.
- `clean_final_dataset.py` — normalizes subreddit casing, backfills missing permalinks, fixes null bodies → `final_dhaka_dataset_clean.json`.
- `filter_dhaka_people_posts.py` — filters to posts from r/dhaka or mentioning a named Dhaka area.

### Sentiment / topic analysis (TextBlob-based)
- `sentiment_analysis.py` — polarity/sentiment + keyword topic categorization → `sentiment_analysis/`.
- `advanced_sentiment_analysis.py` — adds subjectivity scoring and keyword-based emotion detection → `advanced_sentiment_analysis/`.
- `check_dhaka_relevance.py` — flags posts that don't actually mention Dhaka/Bangladesh; writes the Dhaka-only subset.
- `analyze_general_bangladesh_posts.py` — compares Dhaka-focused vs. general Bangladesh posts.
- `what_are_people_talking_about.py` — topic breakdown, top problems, top positive themes, question types.
- `analyze_location_based_posts.py` — same style of analysis, run against the separate location-based dataset.
- `enhanced_sentiment_analysis.py` — transformer-based version (RoBERTa sentiment + emotion models via HuggingFace). **Not run as part of this pipeline** — requires downloading ~800MB of models. Path is kept in sync with the other scripts if you want to run it yourself.

### Formatting / reporting
- `format_csv.py` — splits the dataset into summary/top-posts/by-subreddit/by-date CSVs → `formatted_output/`.
- `generate_dataset_html.py` / `generate_dataset_markdown.py` — dataset overview report → `dataset_overview.html` / `.md`.
- `generate_sentiment_html.py` — sentiment dashboard → `sentiment_overview.html` (auto-picks the richest available sentiment CSV).
- `generate_json_report.py` — overview report built directly from the JSON dataset → `combined_dhaka_overview.html`.

### Media
- `gallery-dl.conf` — config for [gallery-dl](https://github.com/mikf/gallery-dl), used to download images/galleries attached to Reddit posts.
- `gallery-dl/reddit/bangladesh/` — 7 downloaded images from one gallery post. Image 07 is a partially-recovered file (truncated near the end — the original download was interrupted, and re-downloading is currently blocked by the same Reddit API restriction described below).

## Setup

```bash
pip install pandas numpy requests textblob
python -m textblob.download_corpora   # one-time NLTK corpora download
```

Run the pipeline in this order (each stage depends on the previous one's output):

```bash
python clean_final_dataset.py          # only needed if final_dhaka_dataset.json changes
python sentiment_analysis.py
python advanced_sentiment_analysis.py
python check_dhaka_relevance.py
python analyze_general_bangladesh_posts.py
python what_are_people_talking_about.py
python format_csv.py
python filter_dhaka_people_posts.py
python generate_dataset_html.py
python generate_dataset_markdown.py
python generate_json_report.py
python generate_sentiment_html.py
```

`enhanced_sentiment_analysis.py` additionally needs `transformers` and `sentence-transformers`, and will download models from HuggingFace on first run.

## Known limitations

- **Reddit API access is blocked.** As of this writing, `reddit.com/.../.json` returns `403 Forbidden` for unauthenticated requests from this environment, and `old.reddit.com` resets the connection outright. This means `crawl*.py` cannot currently pull new data. To resume crawling, you'd need to register a Reddit API app at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) and switch the crawlers (or `gallery-dl.conf`) to authenticated OAuth requests.
- **Sentiment methodology differs slightly between scripts.** In `analyze_general_bangladesh_posts.py`, the Dhaka-focused subset's sentiment is inherited from `advanced_sentiment_analysis.py` (computed on post *body* text), while the general-Bangladesh subset's sentiment is recomputed from *title* text only. This is a pre-existing quirk in the original script design, not a bug introduced later — worth knowing when comparing the two groups directly.
- **`enhanced_sentiment_analysis.py` has never been run** in this repo (no output folder exists for it) — it's included for anyone who wants transformer-quality sentiment/emotion scoring and is willing to download the models.
