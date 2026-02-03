#!/usr/bin/env python3
"""
Update stats section for all landing pages with test-specific content.
- Stat 1: Normal reference range for the biomarker
- Stat 2: What panel/assessment it's part of
- Stat 3: 10 days to get results (consistent across all)
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

# Stats content for each landing page slug
# Format: {slug: {"stat-1-number": range, "stat-1-text": text, "stat-2-number": "Part of", "stat-2-text": panel}}
STATS_CONTENT = {
    # Kidney & Liver Tests
    "bun-test": {
        "stat-1-number": "7-20 mg/dL",
        "stat-1-text": "is normal BUN range",
        "stat-2-number": "Part of",
        "stat-2-text": "standard kidney assessment",
    },
    "gfr-test": {
        "stat-1-number": ">90 mL/min",
        "stat-1-text": "is normal GFR range",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive kidney panel",
    },
    "kidney-panel": {
        "stat-1-number": "5 markers",
        "stat-1-text": "in complete kidney panel",
        "stat-2-number": "Part of",
        "stat-2-text": "90+ biomarker screening",
    },
    "liver-panel": {
        "stat-1-number": "7 markers",
        "stat-1-text": "in complete liver panel",
        "stat-2-number": "Part of",
        "stat-2-text": "90+ biomarker screening",
    },
    "liver-enzymes": {
        "stat-1-number": "7-56 U/L",
        "stat-1-text": "is normal ALT range",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive liver panel",
    },
    "uric-acid-test": {
        "stat-1-number": "3.5-7.2 mg/dL",
        "stat-1-text": "is normal uric acid range",
        "stat-2-number": "Part of",
        "stat-2-text": "metabolic health panel",
    },

    # Heart & Cholesterol Tests
    "cholesterol-test": {
        "stat-1-number": "<200 mg/dL",
        "stat-1-text": "is optimal total cholesterol",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced lipid panel",
    },
    "high-cholesterol": {
        "stat-1-number": "<200 mg/dL",
        "stat-1-text": "is optimal total cholesterol",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced lipid panel",
    },
    "high-cholesterol-symptoms": {
        "stat-1-number": "<200 mg/dL",
        "stat-1-text": "is optimal total cholesterol",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced lipid panel",
    },
    "cholesterol-foods": {
        "stat-1-number": "<200 mg/dL",
        "stat-1-text": "is optimal total cholesterol",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced lipid panel",
    },
    "lipid-panel": {
        "stat-1-number": "8 markers",
        "stat-1-text": "in advanced lipid panel",
        "stat-2-number": "Part of",
        "stat-2-text": "90+ biomarker screening",
    },
    "ldl-levels": {
        "stat-1-number": "<100 mg/dL",
        "stat-1-text": "is optimal LDL level",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced lipid panel",
    },
    "ldl-hdl": {
        "stat-1-number": "<3.5 ratio",
        "stat-1-text": "is optimal LDL/HDL ratio",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced lipid panel",
    },
    "triglycerides-high": {
        "stat-1-number": "<150 mg/dL",
        "stat-1-text": "is normal triglyceride level",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced lipid panel",
    },
    "triglycerides-causes": {
        "stat-1-number": "<150 mg/dL",
        "stat-1-text": "is normal triglyceride level",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced lipid panel",
    },
    "triglycerides-meaning": {
        "stat-1-number": "<150 mg/dL",
        "stat-1-text": "is normal triglyceride level",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced lipid panel",
    },
    "apob-test": {
        "stat-1-number": "<90 mg/dL",
        "stat-1-text": "is optimal ApoB level",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced lipid panel",
    },
    "lpa-test": {
        "stat-1-number": "<75 nmol/L",
        "stat-1-text": "is low-risk Lp(a) level",
        "stat-2-number": "Part of",
        "stat-2-text": "advanced cardiovascular panel",
    },
    "heart-test": {
        "stat-1-number": "12+ markers",
        "stat-1-text": "in cardiac risk panel",
        "stat-2-number": "Part of",
        "stat-2-text": "90+ biomarker screening",
    },
    "homocysteine": {
        "stat-1-number": "<10 µmol/L",
        "stat-1-text": "is optimal homocysteine",
        "stat-2-number": "Part of",
        "stat-2-text": "cardiovascular risk panel",
    },

    # Thyroid Tests
    "thyroid-panel": {
        "stat-1-number": "6 markers",
        "stat-1-text": "in complete thyroid panel",
        "stat-2-number": "Part of",
        "stat-2-text": "90+ biomarker screening",
    },
    "tsh-test": {
        "stat-1-number": "0.4-4.0 mIU/L",
        "stat-1-text": "is normal TSH range",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive thyroid panel",
    },
    "thyroid-antibodies": {
        "stat-1-number": "<35 IU/mL",
        "stat-1-text": "is normal TPO antibodies",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive thyroid panel",
    },
    "hypothyroidism": {
        "stat-1-number": ">4.0 mIU/L",
        "stat-1-text": "TSH suggests hypothyroidism",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive thyroid panel",
    },
    "hyperthyroidism": {
        "stat-1-number": "<0.4 mIU/L",
        "stat-1-text": "TSH suggests hyperthyroidism",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive thyroid panel",
    },
    "thyroid-symptoms": {
        "stat-1-number": "6 markers",
        "stat-1-text": "reveal thyroid function",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive thyroid panel",
    },
    "thyroid-nodules": {
        "stat-1-number": "6 markers",
        "stat-1-text": "assess thyroid health",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive thyroid panel",
    },
    "hashimotos": {
        "stat-1-number": ">35 IU/mL",
        "stat-1-text": "TPO suggests Hashimoto's",
        "stat-2-number": "Part of",
        "stat-2-text": "autoimmune thyroid panel",
    },

    # Hormone Tests
    "hormone-panel": {
        "stat-1-number": "10+ markers",
        "stat-1-text": "in comprehensive hormone panel",
        "stat-2-number": "Part of",
        "stat-2-text": "90+ biomarker screening",
    },
    "hormone-imbalance": {
        "stat-1-number": "10+ markers",
        "stat-1-text": "reveal hormone balance",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive hormone panel",
    },
    "testosterone-test": {
        "stat-1-number": "300-1000 ng/dL",
        "stat-1-text": "is normal male testosterone",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive hormone panel",
    },
    "testosterone-levels": {
        "stat-1-number": "300-1000 ng/dL",
        "stat-1-text": "is normal male testosterone",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive hormone panel",
    },
    "cortisol-test": {
        "stat-1-number": "10-20 mcg/dL",
        "stat-1-text": "is normal AM cortisol",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive hormone panel",
    },
    "cortisol-high-symptoms": {
        "stat-1-number": ">20 mcg/dL",
        "stat-1-text": "AM cortisol may indicate stress",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive hormone panel",
    },
    "adrenal": {
        "stat-1-number": "4 markers",
        "stat-1-text": "assess adrenal function",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive hormone panel",
    },
    "dhea-test": {
        "stat-1-number": "280-640 mcg/dL",
        "stat-1-text": "is normal DHEA-S range",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive hormone panel",
    },
    "prolactin-test": {
        "stat-1-number": "2-18 ng/mL",
        "stat-1-text": "is normal prolactin range",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive hormone panel",
    },

    # Metabolic & Diabetes Tests
    "metabolic-panel": {
        "stat-1-number": "14 markers",
        "stat-1-text": "in comprehensive metabolic panel",
        "stat-2-number": "Part of",
        "stat-2-text": "90+ biomarker screening",
    },
    "metabolic-syndrome": {
        "stat-1-number": "5 criteria",
        "stat-1-text": "define metabolic syndrome",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive metabolic panel",
    },
    "diabetes-test": {
        "stat-1-number": "<5.7%",
        "stat-1-text": "HbA1c is non-diabetic",
        "stat-2-number": "Part of",
        "stat-2-text": "diabetes risk panel",
    },
    "a1c-test": {
        "stat-1-number": "<5.7%",
        "stat-1-text": "is normal HbA1c range",
        "stat-2-number": "Part of",
        "stat-2-text": "diabetes risk panel",
    },
    "a1c-levels": {
        "stat-1-number": "5.7-6.4%",
        "stat-1-text": "HbA1c indicates prediabetes",
        "stat-2-number": "Part of",
        "stat-2-text": "diabetes risk panel",
    },
    "glucose-monitoring": {
        "stat-1-number": "70-100 mg/dL",
        "stat-1-text": "is normal fasting glucose",
        "stat-2-number": "Part of",
        "stat-2-text": "comprehensive metabolic panel",
    },

    # Inflammation Tests
    "crp-test": {
        "stat-1-number": "<1.0 mg/L",
        "stat-1-text": "is low-risk hs-CRP level",
        "stat-2-number": "Part of",
        "stat-2-text": "inflammation panel",
    },
    "inflammation-symptoms": {
        "stat-1-number": "4 markers",
        "stat-1-text": "reveal inflammation levels",
        "stat-2-number": "Part of",
        "stat-2-text": "inflammation panel",
    },
    "inflammatory-foods": {
        "stat-1-number": "<1.0 mg/L",
        "stat-1-text": "is low-risk hs-CRP level",
        "stat-2-number": "Part of",
        "stat-2-text": "inflammation panel",
    },
    "autoimmune-test": {
        "stat-1-number": "6+ markers",
        "stat-1-text": "screen for autoimmunity",
        "stat-2-number": "Part of",
        "stat-2-text": "autoimmune panel",
    },
    "ana-test": {
        "stat-1-number": "<1:40 titer",
        "stat-1-text": "is negative ANA result",
        "stat-2-number": "Part of",
        "stat-2-text": "autoimmune panel",
    },
    "lyme-test": {
        "stat-1-number": "2-tier testing",
        "stat-1-text": "confirms Lyme diagnosis",
        "stat-2-number": "Part of",
        "stat-2-text": "infectious disease panel",
    },
    "celiac-test": {
        "stat-1-number": "<4 U/mL",
        "stat-1-text": "is negative tTG-IgA",
        "stat-2-number": "Part of",
        "stat-2-text": "celiac screening panel",
    },
    "celiac-info": {
        "stat-1-number": "<4 U/mL",
        "stat-1-text": "is negative tTG-IgA",
        "stat-2-number": "Part of",
        "stat-2-text": "celiac screening panel",
    },

    # Vitamins & Nutrients
    "vitamin-panel": {
        "stat-1-number": "8 markers",
        "stat-1-text": "in vitamin/mineral panel",
        "stat-2-number": "Part of",
        "stat-2-text": "90+ biomarker screening",
    },
    "vitamin-d-test": {
        "stat-1-number": "30-100 ng/mL",
        "stat-1-text": "is optimal vitamin D range",
        "stat-2-number": "Part of",
        "stat-2-text": "vitamin panel",
    },
    "vitamin-d-deficiency": {
        "stat-1-number": "<20 ng/mL",
        "stat-1-text": "indicates vitamin D deficiency",
        "stat-2-number": "Part of",
        "stat-2-text": "vitamin panel",
    },
    "vitamin-d-info": {
        "stat-1-number": "30-100 ng/mL",
        "stat-1-text": "is optimal vitamin D range",
        "stat-2-number": "Part of",
        "stat-2-text": "vitamin panel",
    },
    "vitamin-d-sun": {
        "stat-1-number": "30-100 ng/mL",
        "stat-1-text": "is optimal vitamin D range",
        "stat-2-number": "Part of",
        "stat-2-text": "vitamin panel",
    },
    "b12-test": {
        "stat-1-number": "200-900 pg/mL",
        "stat-1-text": "is normal B12 range",
        "stat-2-number": "Part of",
        "stat-2-text": "vitamin panel",
    },
    "b12-deficiency": {
        "stat-1-number": "<200 pg/mL",
        "stat-1-text": "indicates B12 deficiency",
        "stat-2-number": "Part of",
        "stat-2-text": "vitamin panel",
    },
    "folate-test": {
        "stat-1-number": ">3 ng/mL",
        "stat-1-text": "is normal folate level",
        "stat-2-number": "Part of",
        "stat-2-text": "vitamin panel",
    },
    "iron-test": {
        "stat-1-number": "60-170 mcg/dL",
        "stat-1-text": "is normal iron range",
        "stat-2-number": "Part of",
        "stat-2-text": "iron studies panel",
    },
    "ferritin-test": {
        "stat-1-number": "30-300 ng/mL",
        "stat-1-text": "is normal ferritin range",
        "stat-2-number": "Part of",
        "stat-2-text": "iron studies panel",
    },
    "magnesium-test": {
        "stat-1-number": "1.7-2.2 mg/dL",
        "stat-1-text": "is normal magnesium range",
        "stat-2-number": "Part of",
        "stat-2-text": "mineral panel",
    },

    # Blood Tests
    "cbc-test": {
        "stat-1-number": "15 markers",
        "stat-1-text": "in complete blood count",
        "stat-2-number": "Part of",
        "stat-2-text": "90+ biomarker screening",
    },
    "blood-test-general": {
        "stat-1-number": "90+ markers",
        "stat-1-text": "in comprehensive panel",
        "stat-2-number": "Part of",
        "stat-2-text": "$199/year membership",
    },
    "blood-test-online": {
        "stat-1-number": "90+ markers",
        "stat-1-text": "in comprehensive panel",
        "stat-2-number": "Part of",
        "stat-2-text": "$199/year membership",
    },
    "health-screening": {
        "stat-1-number": "90+ markers",
        "stat-1-text": "in comprehensive screening",
        "stat-2-number": "Part of",
        "stat-2-text": "$199/year membership",
    },

    # Aging & Longevity Tests
    "longevity": {
        "stat-1-number": "90+ markers",
        "stat-1-text": "track longevity factors",
        "stat-2-number": "Part of",
        "stat-2-text": "longevity panel",
    },
    "biological-age-test": {
        "stat-1-number": "Years vs age",
        "stat-1-text": "reveals biological age",
        "stat-2-number": "Part of",
        "stat-2-text": "longevity panel",
    },
    "epigenetic-test": {
        "stat-1-number": "DNA methylation",
        "stat-1-text": "reveals biological age",
        "stat-2-number": "Part of",
        "stat-2-text": "epigenetic aging panel",
    },
    "epigenetics-info": {
        "stat-1-number": "DNA methylation",
        "stat-1-text": "reveals biological age",
        "stat-2-number": "Part of",
        "stat-2-text": "epigenetic aging panel",
    },
    "telomere-test": {
        "stat-1-number": "Telomere length",
        "stat-1-text": "indicates cellular age",
        "stat-2-number": "Part of",
        "stat-2-text": "longevity panel",
    },
    "telomeres-info": {
        "stat-1-number": "Telomere length",
        "stat-1-text": "indicates cellular age",
        "stat-2-number": "Part of",
        "stat-2-text": "longevity panel",
    },

    # Cancer & Prostate Tests
    "psa-test": {
        "stat-1-number": "<4.0 ng/mL",
        "stat-1-text": "is normal PSA range",
        "stat-2-number": "Part of",
        "stat-2-text": "men's health panel",
    },
    "prostate-health": {
        "stat-1-number": "<4.0 ng/mL",
        "stat-1-text": "is normal PSA range",
        "stat-2-number": "Part of",
        "stat-2-text": "men's health panel",
    },

    # Fertility Tests
    "semen-analysis": {
        "stat-1-number": ">15M/mL",
        "stat-1-text": "is normal sperm concentration",
        "stat-2-number": "Part of",
        "stat-2-text": "male fertility panel",
    },
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

    success_count = 0
    error_count = 0
    skipped_count = 0

    for item in items:
        slug = item.get('fieldData', {}).get('slug', '') or ''
        item_id = item.get('id', '')

        if slug not in STATS_CONTENT:
            print(f"⏭️  {slug}: No stats content defined")
            skipped_count += 1
            continue

        stats = STATS_CONTENT[slug]

        # Build the update payload with all 6 stat fields
        updates = {
            "stat-1-number": stats["stat-1-number"],
            "stat-1-text": stats["stat-1-text"],
            "stat-2-number": stats["stat-2-number"],
            "stat-2-text": stats["stat-2-text"],
            "stat-3-number": "10 days",
            "stat-3-text": "to get results",
        }

        # Update the landing page
        status, result = update_landing_page(item_id, updates)

        if status == 200:
            print(f"✅ {slug}: Updated stats ({stats['stat-1-number']} | {stats['stat-2-text']})")
            success_count += 1
        else:
            print(f"❌ {slug}: Error - {result}")
            error_count += 1

        time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"Complete! Success: {success_count}, Errors: {error_count}, Skipped: {skipped_count}")


if __name__ == '__main__':
    main()
