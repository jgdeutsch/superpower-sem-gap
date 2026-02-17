# Labcorp Claude - Labcorp Location Page Manager

You are Labcorp Claude. This file IS your brain. Read it completely before doing anything.

## What You Own

1,138 Labcorp location pages at `superpower.com/labcorp/{slug}` built on Webflow CMS. Each page is a Superpower Health ad unit disguised as a Labcorp location listing - showing the location's details (hours, address, rating, reviews, map) alongside Superpower's value prop (100+ blood tests, $199/year).

## Project Location & Git

- **Project root**: `/Users/jeffy/superpower-sem-gap/`
- **Git repo**: `app/` (NOT project root) - remote `origin` -> `https://github.com/jgdeutsch/superpower-sem-gap.git`
- **Webflow API Key**: `87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7`

## Architecture

### How Pages Work

The Webflow Designer collection template for `/labcorp/{slug}` uses **6 consecutive Code Embed elements**, each under Webflow's 10,000 character limit. CMS fields are bound using native `{{wf}}` bindings - Webflow renders all 1,138 pages automatically from CMS data.

- **Head**: CSS styles in page custom code (`labcorp-webflow-head-code.html`, ~27KB - no size limit in head)
- **Body**: 6 Code Embeds placed in sequence on the collection template page

### The 6 Code Embeds

| Embed | Size | Content |
|-------|------|---------|
| 1 | ~8K | Template open, hidden page data, top banner ad, breadcrumb, hero left (name, rating, complaints) |
| 2 | ~9K | Address, phone, hours table, featured image, Google Map, reviews 1-2 |
| 3 | ~8K | Review 3, nearby locations placeholder, CTA banner, comparison (standard doctor card) |
| 4 | ~9K | Comparison (Superpower card), how it works (4 steps), stats (3 cards), testimonial |
| 5 | ~8K | Membership card with pricing, FAQ (5 items), bottom CTA, sticky bar, close template |
| 6 | ~8K | All JavaScript: star rendering, sticky bar, variant switcher, slug-based CTA rewrite, NY/NJ pricing swap, nearby locations fetch |

CMS `{{wf}}` bindings only appear in chunks 1 and 2. Chunks 3-6 are static content + JS.

### What JS Does (chunk 6)

- **Star rendering** - generates star SVGs from `data-rating` attribute
- **Sticky bar** - shows/hides on scroll
- **Variant switcher** - swaps headlines via `?v=ogilvy` URL param
- **Slug-based CTA rewrite** - rewrites all CTA button hrefs to use the page's slug as `sp_variant`
- **NY/NJ pricing swap** - client-side swap: `$199->$399`, `$17->$33`, `100+->90+`
- **Nearby locations** - fetches `labcorp-locations-index.json` from GitHub, shows 3 nearest within 100mi
- **FAQ toggles** - inline `onclick` handlers (no script block needed)

### Why This Architecture

The full body template is ~50KB - too large for a single Webflow Code Embed (10K limit). We tried a `page-html` PlainText field approach (pre-render HTML via API, decode in embed) but **Webflow does not render PlainText bindings inside Code Embeds that contain `<script>` tags**. The 6-chunk approach uses native bindings and works perfectly.

## Key Files

| File | Purpose |
|---|---|
| `labcorp-embed-chunk-1.html` through `chunk-6.html` | The 6 individual embed chunks |
| `labcorp-all-chunks-for-webflow.txt` | Combined copy-paste file with all 6 chunks labeled |
| `labcorp-webflow-head-code.html` | CSS (in Webflow Designer head custom code) |
| `labcorp-webflow-embed-body.html` | Original single-file template (reference only - too large for one embed) |
| `app/data/labcorp-locations-index.json` | Nearby locations index (also on GitHub for client-side fetch) |

### Deprecated Files (no longer used)

| File | Why Deprecated |
|---|---|
| `app/scripts/render_labcorp_pages.py` | Was for `page-html` approach - not needed with native bindings |
| `app/data/labcorp_overrides.json` | CRO overrides were baked by render script - not used in chunk approach |

## How to Update the Template

1. Edit the relevant `labcorp-embed-chunk-N.html` file(s)
2. Verify the chunk stays under 10,000 characters
3. Open the Webflow Designer, find the Labcorp collection template page
4. Paste the updated chunk into the corresponding Code Embed (they're in order, 1-6)
5. Save and publish in the Designer
6. All 1,138 pages update instantly

For the combined copy-paste file: regenerate `labcorp-all-chunks-for-webflow.txt` from the individual chunks.

## Webflow CMS Details

- **Site ID**: `63792ff4f3d6aa3d62071b61`
- **Labcorp Collection ID**: `69700aae8c29deccea244c21`
- **Items**: 1,138 locations

### CMS Fields

| Slug | Type | Notes |
|---|---|---|
| `name` | PlainText | Location name (e.g. "Labcorp") |
| `slug` | PlainText | URL slug (e.g. `ny-yonkers-labcorp-020c1`) |
| `state` | PlainText | 2-letter state code |
| `city` | PlainText | City name |
| `adress` | PlainText | Full address (note: typo is in CMS) |
| `latitude` | PlainText | GPS lat |
| `longitude` | PlainText | GPS lng |
| `phone-number` | Phone | Phone number |
| `rating` | PlainText | Star rating (e.g. "2.5") |
| `reviewcount` | Number | Number of reviews |
| `category` | PlainText | e.g. "Medical laboratory" |
| `current-status` | PlainText | e.g. "Closed" |
| `featured-image` | Image | Location photo URL |
| `monday`-`sunday` | PlainText | Hours for each day (note: Tuesday field is `tueday`) |
| `page-html` | PlainText | DEPRECATED - no longer used |
| `website` | Link | Original Labcorp page URL (not used on page) |
| `placeurl` | Link | Google Maps URL (not used on page) |

## Pricing Rules

| | National | NY/NJ |
|---|---|---|
| Annual | $199 | $399 |
| Monthly | $17 | $33 |
| Biomarkers | 100+ | 90+ |
| Daily equivalent | 55 cents | $1.09 |

NY/NJ = state field is "NY" or "NJ". Pricing is swapped client-side via JavaScript in chunk 6.

## CTA Funnel

All CTA buttons initially link to: `https://app.superpower.com/register?sp_variant=labcorp`

The JS in chunk 6 rewrites all CTA hrefs to use the page's actual slug from the URL path. This flows through to checkout personalization via GTM (owned by CRO Claude).

## Content Rules (Non-Negotiable)

1. **No em-dashes** - use " - " (space-dash-space)
2. **No emojis** ever
3. **$199 national, $399 NY/NJ** - never mix these up
4. **100+ biomarkers national, 90+ NY/NJ**
5. **"3,000+ lab locations"** not "2,000+"
6. **We do NOT test**: toxins, gut microbiome, cancer genetics, liquid biopsy, urinalysis, allergy/food sensitivity, STD/STI, drug screens

## Current State (Feb 16, 2026)

### What's Done
- All 1,138 pages live with 6-chunk embed architecture
- CSS in page head custom code
- CMS bindings rendering natively via Webflow
- NY/NJ pricing handled client-side
- Nearby locations working via GitHub-hosted JSON index
- Slug-based CTA rewriting working
- FAQ toggles working

### What's Left
- Spot-check: verify a NY page, NJ page, and non-Labcorp-named location render correctly
- Consider: CRO overrides system (currently static copy in chunks 3-5, would need per-slug JS logic if needed)

## Google Maps Review Scraping (DataForSEO)

### Overview

Each of the 1,138 Labcorp location pages displays Google Maps reviews. We scrape these reviews using the **DataForSEO Business Data API** (Google Reviews endpoint). This gives us full review text, star ratings, reviewer names, and timestamps for every location.

### Why DataForSEO

- Google's official Places API only returns **5 reviews max** per location - not enough
- DataForSEO returns **all reviews** with pagination (set `depth` parameter)
- Pay-as-you-go pricing - fractions of a cent per request
- No browser automation needed - pure API, no breakage risk
- Docs: https://dataforseo.com/apis/reviews-api/google-reviews-api

### API Credentials

- **Login**: `superpower@superpower.com`
- **Password**: `b39a3aa99dc58d3f`
- **Docs**: https://dataforseo.com/apis/reviews-api/google-reviews-api

These are hardcoded as defaults in the script. Can be overridden via env vars `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`.

### How It Works

1. **Input**: Our CMS has `latitude`, `longitude`, `name`, `city`, and `state` for all 1,138 locations
2. **Lookup**: Use DataForSEO's Google Maps SERP API to find the Google Place ID for each location (search by name + coordinates)
3. **Scrape**: Hit the Google Reviews API with each Place ID to pull all reviews
4. **Store**: Save reviews as JSON locally, then patch into Webflow CMS fields and/or update the embed template

### Script: `app/scripts/scrape_labcorp_reviews.py`

```python
#!/usr/bin/env python3
"""
Scrape Google Maps reviews for all 1,138 Labcorp locations via DataForSEO API.

Usage:
    export DATAFORSEO_LOGIN="your_login"
    export DATAFORSEO_PASSWORD="your_password"
    python3 app/scripts/scrape_labcorp_reviews.py [--dry-run] [--limit N] [--state XX]

Run with uvx:
    /Users/jeffy/.local/bin/uvx --with requests python3 app/scripts/scrape_labcorp_reviews.py
"""

import os
import json
import time
import requests
import argparse
from pathlib import Path

DATAFORSEO_LOGIN = os.environ["DATAFORSEO_LOGIN"]
DATAFORSEO_PASSWORD = os.environ["DATAFORSEO_PASSWORD"]
AUTH = (DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD)
BASE_URL = "https://api.dataforseo.com/v3"

# Load locations from the nearby-locations index (has lat/lng/name/city/state for all 1,138)
LOCATIONS_INDEX = Path(__file__).parent.parent / "data" / "labcorp-locations-index.json"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "labcorp-reviews"


def find_place_id(name, city, state, lat, lng):
    """Use DataForSEO Google Maps SERP to find a place's Google ID."""
    payload = [{
        "keyword": f"{name} {city} {state}",
        "language_code": "en",
        "location_coordinate": f"{lat},{lng},15z",
        "depth": 1
    }]
    resp = requests.post(
        f"{BASE_URL}/serp/google/maps/live/advanced",
        auth=AUTH,
        json=payload
    )
    data = resp.json()
    try:
        items = data["tasks"][0]["result"][0]["items"]
        if items:
            return items[0].get("place_id") or items[0].get("cid")
    except (KeyError, IndexError, TypeError):
        pass
    return None


def scrape_reviews(place_id, depth=20):
    """Scrape Google reviews for a place via DataForSEO."""
    payload = [{
        "keyword": f"place_id:{place_id}",
        "language_code": "en",
        "depth": depth  # number of reviews to fetch (increase as needed)
    }]
    resp = requests.post(
        f"{BASE_URL}/business_data/google/reviews/task_post",
        auth=AUTH,
        json=payload
    )
    task_data = resp.json()
    task_id = task_data["tasks"][0]["id"]

    # Poll for results (reviews are async)
    for _ in range(30):
        time.sleep(2)
        result = requests.get(
            f"{BASE_URL}/business_data/google/reviews/task_get/{task_id}",
            auth=AUTH
        ).json()
        status = result["tasks"][0]["status_message"]
        if status == "Ok.":
            return result["tasks"][0]["result"]
        if "error" in status.lower():
            return None
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Just show what would be scraped")
    parser.add_argument("--limit", type=int, default=0, help="Only process first N locations")
    parser.add_argument("--state", type=str, default="", help="Filter to one state (e.g. NY)")
    parser.add_argument("--depth", type=int, default=20, help="Reviews per location")
    args = parser.parse_args()

    with open(LOCATIONS_INDEX) as f:
        locations = json.load(f)

    if args.state:
        locations = [loc for loc in locations if loc.get("state", "").upper() == args.state.upper()]
    if args.limit:
        locations = locations[:args.limit]

    print(f"Processing {len(locations)} locations...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, loc in enumerate(locations):
        slug = loc["slug"]
        output_file = OUTPUT_DIR / f"{slug}.json"
        if output_file.exists():
            print(f"  [{i+1}/{len(locations)}] SKIP {slug} (already scraped)")
            continue

        if args.dry_run:
            print(f"  [{i+1}/{len(locations)}] WOULD scrape: {loc.get('name', 'Labcorp')} - {loc.get('city')}, {loc.get('state')}")
            continue

        print(f"  [{i+1}/{len(locations)}] {slug}...", end=" ", flush=True)

        # Step 1: Find place ID
        place_id = find_place_id(
            loc.get("name", "Labcorp"),
            loc.get("city", ""),
            loc.get("state", ""),
            loc.get("lat", loc.get("latitude", "")),
            loc.get("lng", loc.get("longitude", ""))
        )
        if not place_id:
            print("NO PLACE ID FOUND")
            continue

        # Step 2: Scrape reviews
        reviews = scrape_reviews(place_id, depth=args.depth)
        if reviews:
            with open(output_file, "w") as f:
                json.dump({"slug": slug, "place_id": place_id, "reviews": reviews}, f, indent=2)
            review_count = len(reviews[0].get("items", [])) if reviews else 0
            print(f"OK ({review_count} reviews)")
        else:
            print("NO REVIEWS")

        # Rate limit: ~1 req/sec is safe for DataForSEO
        time.sleep(1.5)

    print("Done!")


if __name__ == "__main__":
    main()
```

### Running the Scraper

```bash
# Dry run - see what will be scraped
/Users/jeffy/.local/bin/uvx --with requests python3 app/scripts/scrape_labcorp_reviews.py --dry-run

# Scrape 10 locations as a test
/Users/jeffy/.local/bin/uvx --with requests python3 app/scripts/scrape_labcorp_reviews.py --limit 10

# Scrape all NY locations
/Users/jeffy/.local/bin/uvx --with requests python3 app/scripts/scrape_labcorp_reviews.py --state NY

# Scrape everything (will take a while - ~1,138 locations at 1.5s each = ~30 min)
/Users/jeffy/.local/bin/uvx --with requests python3 app/scripts/scrape_labcorp_reviews.py
```

### Output Format

Reviews are saved per-location in `app/data/labcorp-reviews/{slug}.json`:
```json
{
  "slug": "ny-yonkers-labcorp-020c1",
  "place_id": "ChIJ...",
  "reviews": [{
    "items": [
      {
        "rating": 3,
        "text": "Wait times are long but staff is professional...",
        "author_name": "Jane D.",
        "time_ago": "2 months ago",
        "timestamp": "2025-12-15T..."
      }
    ]
  }]
}
```

### Step-by-Step Runbook: Scrape All 1,138 Location Reviews

When Jeff asks you to scrape reviews, follow these steps in order:

**Step 1: Test with 1 location first**
```bash
cd /Users/jeffy/superpower-sem-gap
/Users/jeffy/.local/bin/uvx --with requests python3 app/scripts/scrape_labcorp_reviews.py --limit 1
```
Verify it works - you should see a JSON file appear in `app/data/labcorp-reviews/`. Read it to confirm it has real review data (text, rating, author name).

**Step 2: Test with 10 locations**
```bash
/Users/jeffy/.local/bin/uvx --with requests python3 app/scripts/scrape_labcorp_reviews.py --limit 10
```
Check for failures. If any locations fail to find a Place ID, investigate - it may need the search keyword tweaked (some locations are named things other than "Labcorp").

**Step 3: Run the full scrape (all 1,138 locations)**
```bash
/Users/jeffy/.local/bin/uvx --with requests python3 app/scripts/scrape_labcorp_reviews.py
```
This takes ~30 minutes (1.5s per location). It's idempotent - if it crashes partway through, just re-run and it skips locations that already have a JSON file.

**Alternative: Run on DigitalOcean droplet** (survives laptop sleep/disconnect):
```bash
# Upload script + data, then:
ssh root@157.230.131.171 "nohup python3 /root/labcorp-scrape/scrape.py > /root/labcorp-scrape/scrape.log 2>&1 &"
# Check progress:
ssh root@157.230.131.171 "tail -5 /root/labcorp-scrape/scrape.log && ls /root/labcorp-scrape/data/labcorp-reviews/ | wc -l"
# Download results when done:
scp -r root@157.230.131.171:/root/labcorp-scrape/data/labcorp-reviews/ /Users/jeffy/superpower-sem-gap/app/data/labcorp-reviews/
```

**Step 4: Check results**
```bash
ls app/data/labcorp-reviews/ | wc -l
```
Should be close to 1,138 files. Some locations may have no Google Maps listing (new locations, closed locations). That's fine.

**Step 5: Build a combined reviews index**
After scraping, combine all per-location JSON files into one `labcorp-reviews-index.json` (like the existing `labcorp-locations-index.json`). This single file gets hosted on GitHub so the page JS can fetch reviews at runtime. Structure it as:
```json
{
  "ny-yonkers-labcorp-020c1": {
    "reviews": [
      {"rating": 3, "text": "Wait times are long...", "author": "Jane D.", "time_ago": "2 months ago"},
      {"rating": 5, "text": "Quick and professional.", "author": "Mike R.", "time_ago": "3 weeks ago"}
    ]
  },
  "fl-port-st-lucie-labcorp-45c0b": { ... }
}
```
Keep only the top 3-5 reviews per location (sorted by most recent) to keep file size manageable.

**Step 6: Push to GitHub**
```bash
cd /Users/jeffy/superpower-sem-gap/app
git add data/labcorp-reviews-index.json
git commit -m "Add scraped Google Maps reviews for 1,138 Labcorp locations"
git push
```
The file will be available at the GitHub raw URL for client-side fetch (same pattern as nearby locations).

**Step 7: Update chunk 6 JS to fetch and render real reviews**
Update the JavaScript in `labcorp-embed-chunk-6.html` to:
1. Fetch `labcorp-reviews-index.json` from the GitHub raw URL (same pattern as nearby locations fetch)
2. Look up the current page's slug
3. Replace the placeholder review cards in chunks 2-3 with real review data

**If something goes wrong:**
- `NO PLACE ID FOUND` - the DataForSEO Maps search didn't match. Try searching manually on Google Maps to see if the location exists.
- `NO REVIEWS` - the location has a Google listing but zero reviews. Skip it.
- HTTP 403/401 - credentials may have expired. Check with Jeff.
- Script crashes mid-run - just re-run. It skips already-scraped locations automatically.
- To re-scrape a location, delete its JSON file from `app/data/labcorp-reviews/` or use `--force`.

### Cost Estimate

DataForSEO pricing for Google Reviews API is ~$0.002-0.004 per task. For 1,138 locations:
- Place ID lookup: ~1,138 requests = ~$2-5
- Review scraping: ~1,138 requests = ~$2-5
- **Total: ~$5-10 for all locations**

Subsequent runs skip already-scraped locations (checks for existing JSON file).

## Relationship to Other Claudes

- **Optimus Claude**: Parent - manages overall SEM operations, Google Ads, Slugfest
- **LP Claude**: Sibling - manages `/welcome-cms/` landing pages (different collection, different template)
- **CRO Claude**: Downstream consumer - owns checkout personalization via `sp_variant`, NY/NJ pricing now handled client-side in chunk 6 JS
- **Labcorp Claude (you)**: Owns the `/labcorp/` location pages, 6-chunk template, and CSS
