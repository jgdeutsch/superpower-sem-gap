#!/usr/bin/env python3
"""
Update hero subheadlines to emphasize the BREADTH of Superpower testing.
The hero subheadline should make clear this isn't just one test - it's 100+ biomarkers.
"""
import json
import requests
import time

WEBFLOW_API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
LANDING_PAGES_COLLECTION = "6981a714e199bac70776d880"

HEADERS = {
    "Authorization": f"Bearer {WEBFLOW_API_KEY}",
    "Content-Type": "application/json"
}

# Hero subheadlines that emphasize breadth
# Format: "<p>Your specific test + 100+ biomarkers. One blood draw. $199/year.</p>"
HERO_SUBHEADLINES = {
    # ===================
    # KIDNEY TESTS
    # ===================
    "bun-test": "<p>BUN plus 100+ biomarkers - heart, hormones, thyroid, inflammation, and more. One blood draw. $199/year.</p>",
    "gfr-test": "<p>GFR plus 100+ biomarkers - heart, hormones, thyroid, inflammation, and more. One blood draw. $199/year.</p>",
    "kidney-panel": "<p>Complete kidney panel plus 100+ biomarkers - heart, hormones, thyroid, inflammation, and more. One draw. $199/year.</p>",

    # ===================
    # LIVER TESTS
    # ===================
    "liver-panel": "<p>Complete liver panel plus 100+ biomarkers - heart, hormones, thyroid, kidney, and more. One draw. $199/year.</p>",
    "liver-enzymes": "<p>Liver enzymes plus 100+ biomarkers - heart, hormones, thyroid, kidney, and more. One blood draw. $199/year.</p>",
    "uric-acid-test": "<p>Uric acid plus 100+ biomarkers - heart, hormones, thyroid, liver, kidney, and more. One draw. $199/year.</p>",

    # ===================
    # CHOLESTEROL/HEART TESTS
    # ===================
    "cholesterol-test": "<p>Advanced cholesterol with ApoB plus 100+ biomarkers - hormones, thyroid, inflammation, and more. One draw. $199/year.</p>",
    "high-cholesterol": "<p>Advanced lipid panel with ApoB plus 100+ biomarkers - hormones, thyroid, inflammation, and more. One draw. $199/year.</p>",
    "high-cholesterol-symptoms": "<p>Complete cardiovascular panel plus 100+ biomarkers - hormones, thyroid, metabolic, and more. One draw. $199/year.</p>",
    "cholesterol-foods": "<p>See how diet affects your lipids - plus 100+ biomarkers including hormones, thyroid, and metabolic. $199/year.</p>",
    "lipid-panel": "<p>Advanced lipid panel with ApoB plus 100+ biomarkers - hormones, thyroid, inflammation, and more. One draw. $199/year.</p>",
    "ldl-levels": "<p>LDL plus ApoB and 100+ biomarkers - hormones, thyroid, inflammation, and more. One blood draw. $199/year.</p>",
    "ldl-hdl": "<p>Complete lipid ratios plus 100+ biomarkers - hormones, thyroid, inflammation, and more. One draw. $199/year.</p>",
    "triglycerides-high": "<p>Triglycerides plus 100+ biomarkers - metabolic, hormones, liver, inflammation, and more. One draw. $199/year.</p>",
    "triglycerides-causes": "<p>Find the cause - triglycerides plus 100+ biomarkers including metabolic, hormones, and liver. $199/year.</p>",
    "triglycerides-meaning": "<p>Understand your triglycerides in context - plus 100+ biomarkers including metabolic and cardiovascular. $199/year.</p>",
    "apob-test": "<p>ApoB (the gold standard) plus 100+ biomarkers - hormones, thyroid, inflammation, and more. One draw. $199/year.</p>",
    "lpa-test": "<p>Lp(a) genetic risk marker plus 100+ biomarkers - ApoB, hormones, thyroid, and more. One draw. $199/year.</p>",
    "heart-test": "<p>Complete cardiac panel plus 100+ biomarkers - hormones, metabolic, thyroid, and more. One draw. $199/year.</p>",
    "homocysteine": "<p>Homocysteine plus 100+ biomarkers - B vitamins, cardiovascular, inflammation, and more. One draw. $199/year.</p>",

    # ===================
    # THYROID TESTS
    # ===================
    "thyroid-panel": "<p>Complete thyroid with antibodies plus 100+ biomarkers - hormones, cardiovascular, metabolic. One draw. $199/year.</p>",
    "tsh-test": "<p>TSH plus full thyroid panel and 100+ biomarkers - hormones, cardiovascular, metabolic. One draw. $199/year.</p>",
    "thyroid-antibodies": "<p>Thyroid antibodies plus 100+ biomarkers - full thyroid, hormones, inflammation, and more. One draw. $199/year.</p>",
    "hypothyroidism": "<p>Full hypothyroid workup plus 100+ biomarkers - hormones, cholesterol, metabolic, and more. One draw. $199/year.</p>",
    "hyperthyroidism": "<p>Complete hyperthyroid panel plus 100+ biomarkers - heart, metabolic, hormones, and more. One draw. $199/year.</p>",
    "thyroid-symptoms": "<p>Fatigued? Full thyroid plus 100+ biomarkers - hormones, iron, B12, metabolic, and more. One draw. $199/year.</p>",
    "thyroid-nodules": "<p>Thyroid function panel plus 100+ biomarkers - hormones, inflammation, metabolic, and more. One draw. $199/year.</p>",
    "hashimotos": "<p>Hashimoto's panel plus 100+ biomarkers - inflammation, nutrients, hormones, and more. One draw. $199/year.</p>",

    # ===================
    # HORMONE TESTS
    # ===================
    "hormone-panel": "<p>Complete hormone panel plus 100+ biomarkers - thyroid, cardiovascular, metabolic, and more. One draw. $199/year.</p>",
    "hormone-imbalance": "<p>Find the imbalance - full hormones plus 100+ biomarkers including thyroid, metabolic, and inflammation. $199/year.</p>",
    "testosterone-test": "<p>Total and free testosterone plus 100+ biomarkers - thyroid, metabolic, cardiovascular, and more. One draw. $199/year.</p>",
    "testosterone-levels": "<p>Complete testosterone panel plus 100+ biomarkers - thyroid, metabolic, hormones, and more. One draw. $199/year.</p>",
    "cortisol-test": "<p>Cortisol plus 100+ biomarkers - DHEA, thyroid, metabolic, hormones, and more. One draw. $199/year.</p>",
    "cortisol-high-symptoms": "<p>Cortisol plus 100+ biomarkers - metabolic, hormones, inflammation, thyroid. See the full stress impact. $199/year.</p>",
    "adrenal": "<p>Adrenal markers plus 100+ biomarkers - thyroid, metabolic, inflammation, hormones. One draw. $199/year.</p>",
    "dhea-test": "<p>DHEA-S plus 100+ biomarkers - cortisol, testosterone, thyroid, metabolic. One draw. $199/year.</p>",
    "prolactin-test": "<p>Prolactin plus 100+ biomarkers - full hormones, thyroid, metabolic, and more. One draw. $199/year.</p>",

    # ===================
    # DIABETES/METABOLIC TESTS
    # ===================
    "metabolic-panel": "<p>Complete metabolic panel plus 100+ biomarkers - hormones, inflammation, cardiovascular. One draw. $199/year.</p>",
    "metabolic-syndrome": "<p>All 5 metabolic syndrome markers plus 100+ biomarkers - hormones, inflammation, liver. One draw. $199/year.</p>",
    "diabetes-test": "<p>Glucose, HbA1c, insulin plus 100+ biomarkers - lipids, inflammation, kidney, and more. One draw. $199/year.</p>",
    "a1c-test": "<p>HbA1c plus 100+ biomarkers - metabolic, cardiovascular, hormones, and more. One draw. $199/year.</p>",
    "a1c-levels": "<p>Understand your A1c in context - plus 100+ biomarkers including metabolic, lipids, and kidney. $199/year.</p>",
    "glucose-monitoring": "<p>Glucose and HbA1c plus 100+ biomarkers - metabolic, cardiovascular, hormones. One draw. $199/year.</p>",

    # ===================
    # INFLAMMATION TESTS
    # ===================
    "crp-test": "<p>hs-CRP plus 100+ biomarkers - cardiovascular, metabolic, hormones, and more. One draw. $199/year.</p>",
    "inflammation-symptoms": "<p>Full inflammation panel plus 100+ biomarkers - autoimmune, metabolic, hormones. One draw. $199/year.</p>",
    "inflammatory-foods": "<p>See diet's impact - hs-CRP plus 100+ biomarkers including metabolic, lipids, and liver. $199/year.</p>",
    "autoimmune-test": "<p>Autoimmune screen plus 100+ biomarkers - inflammation, thyroid, metabolic, and more. One draw. $199/year.</p>",
    "ana-test": "<p>ANA screening plus 100+ biomarkers - inflammation, thyroid, metabolic, and more. One draw. $199/year.</p>",
    "lyme-test": "<p>Lyme screening plus 100+ biomarkers - inflammation, immune, metabolic, and more. One draw. $199/year.</p>",
    "celiac-test": "<p>Celiac antibodies plus 100+ biomarkers - nutrients, inflammation, liver, and more. One draw. $199/year.</p>",
    "celiac-info": "<p>Celiac screen plus 100+ biomarkers - iron, B12, vitamin D, liver, and more. One draw. $199/year.</p>",

    # ===================
    # VITAMIN/NUTRIENT TESTS
    # ===================
    "vitamin-panel": "<p>Key vitamins plus 100+ biomarkers - hormones, thyroid, metabolic, inflammation. One draw. $199/year.</p>",
    "vitamin-d-test": "<p>Vitamin D plus 100+ biomarkers - calcium, thyroid, hormones, inflammation. One draw. $199/year.</p>",
    "vitamin-d-deficiency": "<p>Vitamin D plus 100+ biomarkers - thyroid, hormones, inflammation, metabolic. One draw. $199/year.</p>",
    "vitamin-d-info": "<p>Complete vitamin D assessment plus 100+ biomarkers - thyroid, hormones, calcium. One draw. $199/year.</p>",
    "vitamin-d-sun": "<p>Check your vitamin D plus 100+ biomarkers - thyroid, hormones, inflammation. One draw. $199/year.</p>",
    "b12-test": "<p>B12 plus 100+ biomarkers - folate, iron, thyroid, metabolic, and more. One draw. $199/year.</p>",
    "b12-deficiency": "<p>B12 status plus 100+ biomarkers - folate, iron, thyroid, neurological. One draw. $199/year.</p>",
    "folate-test": "<p>Folate plus 100+ biomarkers - B12, homocysteine, metabolic, and more. One draw. $199/year.</p>",
    "iron-test": "<p>Complete iron panel plus 100+ biomarkers - thyroid, hormones, inflammation. One draw. $199/year.</p>",
    "ferritin-test": "<p>Ferritin plus 100+ biomarkers - full iron panel, inflammation, thyroid. One draw. $199/year.</p>",
    "magnesium-test": "<p>Magnesium plus 100+ biomarkers - metabolic, thyroid, hormones, cardiovascular. One draw. $199/year.</p>",

    # ===================
    # BLOOD TESTS
    # ===================
    "cbc-test": "<p>Complete CBC plus 100+ biomarkers - iron, B12, thyroid, metabolic, and more. One draw. $199/year.</p>",
    "blood-test-general": "<p>100+ biomarkers in one draw - heart, metabolic, hormones, thyroid, liver, kidney, inflammation. $199/year.</p>",
    "blood-test-online": "<p>Order online, draw at 2,000+ labs - 100+ biomarkers including heart, hormones, metabolic. $199/year.</p>",
    "health-screening": "<p>Comprehensive screening - 100+ biomarkers covering heart, metabolic, hormones, inflammation. $199/year.</p>",

    # ===================
    # LONGEVITY/AGING TESTS
    # ===================
    "longevity": "<p>100+ longevity biomarkers - inflammation, metabolic, hormones, cardiovascular. One draw. $199/year.</p>",
    "biological-age-test": "<p>Calculate biological age with 100+ biomarkers - inflammation, metabolic, cardiovascular, hormones. $199/year.</p>",
    "epigenetic-test": "<p>Epigenetic insights through 100+ biomarkers - inflammation, metabolic, hormones, cardiovascular. $199/year.</p>",
    "epigenetics-info": "<p>Track lifestyle impact - 100+ biomarkers reveal how diet, sleep, and stress affect your health. $199/year.</p>",
    "telomere-test": "<p>Cellular aging markers plus 100+ biomarkers - inflammation, metabolic, cardiovascular. One draw. $199/year.</p>",
    "telomeres-info": "<p>Understand aging - 100+ biomarkers including inflammation, metabolic, and cardiovascular. One draw. $199/year.</p>",

    # ===================
    # MEN'S HEALTH
    # ===================
    "psa-test": "<p>PSA plus 100+ biomarkers - full hormones, inflammation, metabolic, and more. One draw. $199/year.</p>",
    "prostate-health": "<p>Prostate markers plus 100+ biomarkers - testosterone, inflammation, metabolic. One draw. $199/year.</p>",
    "semen-analysis": "<p>Fertility markers plus 100+ biomarkers - hormones, thyroid, metabolic, and more. One draw. $199/year.</p>",
}


def fetch_landing_pages():
    """Fetch all landing page items from Webflow."""
    url = f"https://api.webflow.com/v2/collections/{LANDING_PAGES_COLLECTION}/items?limit=100"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data.get('items', [])


def update_landing_page(item_id, updates):
    """Update a landing page with new field data."""
    url = f"https://api.webflow.com/v2/collections/{LANDING_PAGES_COLLECTION}/items/{item_id}"
    payload = {"fieldData": updates}
    response = requests.patch(url, headers=HEADERS, json=payload)
    return response.status_code, response.json()


def main():
    print("Fetching landing pages...")
    items = fetch_landing_pages()
    print(f"Found {len(items)} landing pages\n")

    print("Updating hero subheadlines with BREADTH messaging...\n")

    success_count = 0
    error_count = 0
    skipped_count = 0

    for item in items:
        slug = item.get('fieldData', {}).get('slug', '') or ''
        item_id = item.get('id', '')

        if slug not in HERO_SUBHEADLINES:
            print(f"  Skipped {slug}: No hero copy defined")
            skipped_count += 1
            continue

        updates = {
            "hero-subheadline": HERO_SUBHEADLINES[slug]
        }

        status, result = update_landing_page(item_id, updates)

        if status == 200:
            print(f"  Updated {slug}")
            success_count += 1
        else:
            print(f"  ERROR {slug}: {result}")
            error_count += 1

        time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"Complete!")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Skipped: {skipped_count}")


if __name__ == '__main__':
    main()
