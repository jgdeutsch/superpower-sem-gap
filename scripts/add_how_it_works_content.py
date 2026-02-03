#!/usr/bin/env python3
"""
Add "How Superpower Works" section content to all 75 SEM landing pages.
Also fixes "5 days" → "10 days" timing in existing content.
"""
import json
import requests
import time
import re

WEBFLOW_API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
LANDING_PAGES_COLLECTION = "6981a714e199bac70776d880"

HEADERS = {
    "Authorization": f"Bearer {WEBFLOW_API_KEY}",
    "Content-Type": "application/json"
}

# How It Works content mapped by landing page slug
# Each entry has: test_name, body_system, condition_focus
HOW_IT_WORKS_CONTENT = {
    # Blood Tests
    "blood-test-general": {
        "test_name": "comprehensive blood test",
        "body_system": "overall health",
        "condition_focus": "hidden health issues",
        "marker_type": "blood biomarkers"
    },
    "cbc-test": {
        "test_name": "CBC test",
        "body_system": "blood cell health",
        "condition_focus": "anemia and blood disorders",
        "marker_type": "blood cell markers"
    },
    "blood-test-online": {
        "test_name": "blood test",
        "body_system": "overall health",
        "condition_focus": "hidden conditions",
        "marker_type": "biomarkers"
    },

    # Thyroid
    "hashimotos": {
        "test_name": "Hashimoto's test",
        "body_system": "thyroid health",
        "condition_focus": "autoimmune thyroid disease",
        "marker_type": "thyroid antibodies and hormones"
    },
    "thyroid-symptoms": {
        "test_name": "thyroid test",
        "body_system": "thyroid function",
        "condition_focus": "thyroid disorders",
        "marker_type": "thyroid markers"
    },
    "hyperthyroidism": {
        "test_name": "hyperthyroidism test",
        "body_system": "thyroid function",
        "condition_focus": "overactive thyroid",
        "marker_type": "thyroid hormones"
    },
    "tsh-test": {
        "test_name": "TSH test",
        "body_system": "thyroid function",
        "condition_focus": "thyroid disorders",
        "marker_type": "thyroid markers"
    },
    "thyroid-panel": {
        "test_name": "thyroid panel",
        "body_system": "thyroid health",
        "condition_focus": "thyroid conditions",
        "marker_type": "thyroid hormones and antibodies"
    },
    "hypothyroidism": {
        "test_name": "hypothyroidism test",
        "body_system": "thyroid function",
        "condition_focus": "underactive thyroid",
        "marker_type": "thyroid markers"
    },
    "thyroid-nodules": {
        "test_name": "thyroid test",
        "body_system": "thyroid health",
        "condition_focus": "thyroid nodule monitoring",
        "marker_type": "thyroid function markers"
    },
    "thyroid-test-at-home": {
        "test_name": "thyroid test",
        "body_system": "thyroid function",
        "condition_focus": "thyroid disorders",
        "marker_type": "thyroid hormones and antibodies"
    },
    "thyroid-antibodies": {
        "test_name": "thyroid antibody test",
        "body_system": "thyroid health",
        "condition_focus": "autoimmune thyroid disease",
        "marker_type": "thyroid antibodies"
    },

    # Hormones - Cortisol
    "cortisol-test": {
        "test_name": "cortisol test",
        "body_system": "stress hormone levels",
        "condition_focus": "cortisol imbalance",
        "marker_type": "adrenal hormones"
    },
    "cortisol-high-symptoms": {
        "test_name": "cortisol test",
        "body_system": "stress hormones",
        "condition_focus": "high cortisol",
        "marker_type": "cortisol and DHEA"
    },
    "cortisol-test-at-home": {
        "test_name": "cortisol test",
        "body_system": "stress hormone levels",
        "condition_focus": "cortisol imbalance",
        "marker_type": "adrenal markers"
    },
    "cortisol-causes": {
        "test_name": "cortisol test",
        "body_system": "adrenal function",
        "condition_focus": "cortisol imbalance",
        "marker_type": "stress hormones"
    },

    # Hormones - Testosterone
    "testosterone-test": {
        "test_name": "testosterone test",
        "body_system": "hormone levels",
        "condition_focus": "testosterone optimization",
        "marker_type": "sex hormones"
    },
    "testosterone-levels": {
        "test_name": "testosterone test",
        "body_system": "hormone balance",
        "condition_focus": "testosterone levels",
        "marker_type": "hormone markers"
    },
    "testosterone-test-at-home": {
        "test_name": "testosterone test",
        "body_system": "hormone health",
        "condition_focus": "testosterone optimization",
        "marker_type": "sex hormones"
    },

    # Hormones - General
    "hormone-panel": {
        "test_name": "hormone panel",
        "body_system": "hormonal health",
        "condition_focus": "hormone imbalances",
        "marker_type": "hormone markers"
    },
    "hormone-imbalance": {
        "test_name": "hormone test",
        "body_system": "hormonal balance",
        "condition_focus": "hormone imbalances",
        "marker_type": "hormone markers"
    },
    "dhea-test": {
        "test_name": "DHEA test",
        "body_system": "adrenal function",
        "condition_focus": "DHEA optimization",
        "marker_type": "adrenal hormones"
    },
    "prolactin-test": {
        "test_name": "prolactin test",
        "body_system": "hormone levels",
        "condition_focus": "prolactin balance",
        "marker_type": "reproductive hormones"
    },

    # Heart & Cholesterol
    "triglycerides-high": {
        "test_name": "triglycerides test",
        "body_system": "cardiovascular health",
        "condition_focus": "triglyceride management",
        "marker_type": "lipid markers"
    },
    "high-cholesterol": {
        "test_name": "cholesterol test",
        "body_system": "heart health",
        "condition_focus": "cholesterol management",
        "marker_type": "lipid markers"
    },
    "cholesterol-test": {
        "test_name": "cholesterol test",
        "body_system": "cardiovascular health",
        "condition_focus": "heart disease prevention",
        "marker_type": "lipid markers"
    },
    "cholesterol-foods": {
        "test_name": "cholesterol test",
        "body_system": "cardiovascular health",
        "condition_focus": "diet impact on cholesterol",
        "marker_type": "lipid markers"
    },
    "apob-test": {
        "test_name": "ApoB test",
        "body_system": "cardiovascular health",
        "condition_focus": "heart disease risk",
        "marker_type": "advanced lipid markers"
    },
    "lipid-panel": {
        "test_name": "lipid panel",
        "body_system": "cardiovascular health",
        "condition_focus": "heart disease prevention",
        "marker_type": "lipid markers"
    },
    "ldl-hdl": {
        "test_name": "cholesterol test",
        "body_system": "heart health",
        "condition_focus": "LDL/HDL optimization",
        "marker_type": "cholesterol markers"
    },
    "homocysteine": {
        "test_name": "homocysteine test",
        "body_system": "cardiovascular health",
        "condition_focus": "heart and brain health",
        "marker_type": "cardiovascular markers"
    },
    "heart-test": {
        "test_name": "heart health test",
        "body_system": "cardiovascular health",
        "condition_focus": "heart disease prevention",
        "marker_type": "cardiac markers"
    },
    "high-cholesterol-symptoms": {
        "test_name": "cholesterol test",
        "body_system": "heart health",
        "condition_focus": "cholesterol management",
        "marker_type": "lipid markers"
    },
    "triglycerides-meaning": {
        "test_name": "triglycerides test",
        "body_system": "cardiovascular health",
        "condition_focus": "triglyceride levels",
        "marker_type": "lipid markers"
    },
    "triglycerides-causes": {
        "test_name": "triglycerides test",
        "body_system": "metabolic health",
        "condition_focus": "triglyceride management",
        "marker_type": "lipid and metabolic markers"
    },
    "ldl-levels": {
        "test_name": "LDL test",
        "body_system": "cardiovascular health",
        "condition_focus": "LDL cholesterol management",
        "marker_type": "cholesterol markers"
    },

    # Metabolic / Diabetes
    "metabolic-panel": {
        "test_name": "metabolic panel",
        "body_system": "metabolic health",
        "condition_focus": "metabolic function",
        "marker_type": "metabolic markers"
    },
    "glucose-monitoring": {
        "test_name": "glucose test",
        "body_system": "blood sugar control",
        "condition_focus": "glucose optimization",
        "marker_type": "glucose and insulin markers"
    },
    "a1c-test": {
        "test_name": "A1C test",
        "body_system": "blood sugar control",
        "condition_focus": "diabetes prevention",
        "marker_type": "blood sugar markers"
    },
    "a1c-levels": {
        "test_name": "A1C test",
        "body_system": "metabolic health",
        "condition_focus": "blood sugar management",
        "marker_type": "glycemic markers"
    },
    "diabetes-test": {
        "test_name": "diabetes test",
        "body_system": "metabolic health",
        "condition_focus": "diabetes screening",
        "marker_type": "blood sugar markers"
    },
    "metabolic-syndrome": {
        "test_name": "metabolic panel",
        "body_system": "metabolic health",
        "condition_focus": "metabolic syndrome",
        "marker_type": "metabolic markers"
    },

    # Inflammation
    "inflammatory-foods": {
        "test_name": "inflammation test",
        "body_system": "inflammatory status",
        "condition_focus": "diet-related inflammation",
        "marker_type": "inflammatory markers"
    },
    "ana-test": {
        "test_name": "ANA test",
        "body_system": "immune function",
        "condition_focus": "autoimmune screening",
        "marker_type": "autoimmune markers"
    },
    "crp-test": {
        "test_name": "CRP test",
        "body_system": "inflammatory status",
        "condition_focus": "inflammation management",
        "marker_type": "inflammatory markers"
    },
    "autoimmune-test": {
        "test_name": "autoimmune panel",
        "body_system": "immune function",
        "condition_focus": "autoimmune conditions",
        "marker_type": "autoimmune markers"
    },
    "inflammation-symptoms": {
        "test_name": "inflammation test",
        "body_system": "inflammatory status",
        "condition_focus": "chronic inflammation",
        "marker_type": "inflammatory markers"
    },

    # Kidney & Liver
    "adrenal": {
        "test_name": "adrenal test",
        "body_system": "adrenal function",
        "condition_focus": "adrenal health",
        "marker_type": "adrenal hormones"
    },
    "liver-panel": {
        "test_name": "liver panel",
        "body_system": "liver function",
        "condition_focus": "liver health",
        "marker_type": "liver enzymes"
    },
    "liver-enzymes": {
        "test_name": "liver enzyme test",
        "body_system": "liver health",
        "condition_focus": "liver function",
        "marker_type": "liver markers"
    },
    "kidney-panel": {
        "test_name": "kidney panel",
        "body_system": "kidney function",
        "condition_focus": "kidney health",
        "marker_type": "kidney markers"
    },
    "gfr-test": {
        "test_name": "GFR test",
        "body_system": "kidney function",
        "condition_focus": "kidney health",
        "marker_type": "kidney filtration markers"
    },
    "bun-test": {
        "test_name": "BUN test",
        "body_system": "kidney function",
        "condition_focus": "kidney health",
        "marker_type": "kidney markers"
    },

    # Vitamins & Nutrients
    "ferritin-test": {
        "test_name": "ferritin test",
        "body_system": "iron stores",
        "condition_focus": "iron optimization",
        "marker_type": "iron markers"
    },
    "vitamin-d-test": {
        "test_name": "vitamin D test",
        "body_system": "vitamin D levels",
        "condition_focus": "vitamin D optimization",
        "marker_type": "vitamin markers"
    },
    "vitamin-panel": {
        "test_name": "vitamin panel",
        "body_system": "nutritional status",
        "condition_focus": "vitamin deficiencies",
        "marker_type": "vitamin and mineral markers"
    },
    "magnesium-test": {
        "test_name": "magnesium test",
        "body_system": "mineral levels",
        "condition_focus": "magnesium optimization",
        "marker_type": "mineral markers"
    },
    "b12-test": {
        "test_name": "B12 test",
        "body_system": "B12 levels",
        "condition_focus": "B12 optimization",
        "marker_type": "vitamin markers"
    },
    "b12-deficiency": {
        "test_name": "B12 test",
        "body_system": "B12 status",
        "condition_focus": "B12 deficiency",
        "marker_type": "vitamin B12 markers"
    },
    "vitamin-d-deficiency": {
        "test_name": "vitamin D test",
        "body_system": "vitamin D status",
        "condition_focus": "vitamin D deficiency",
        "marker_type": "vitamin D markers"
    },
    "vitamin-d-info": {
        "test_name": "vitamin D test",
        "body_system": "vitamin D levels",
        "condition_focus": "vitamin D optimization",
        "marker_type": "vitamin markers"
    },
    "vitamin-d-sun": {
        "test_name": "vitamin D test",
        "body_system": "vitamin D status",
        "condition_focus": "sun exposure and vitamin D",
        "marker_type": "vitamin D markers"
    },
    "folate-test": {
        "test_name": "folate test",
        "body_system": "folate levels",
        "condition_focus": "folate optimization",
        "marker_type": "B vitamin markers"
    },
    "iron-test": {
        "test_name": "iron test",
        "body_system": "iron status",
        "condition_focus": "iron optimization",
        "marker_type": "iron markers"
    },

    # Aging & Longevity
    "telomeres-info": {
        "test_name": "longevity panel",
        "body_system": "cellular aging",
        "condition_focus": "healthy aging",
        "marker_type": "aging markers"
    },
    "telomere-test": {
        "test_name": "longevity panel",
        "body_system": "cellular health",
        "condition_focus": "biological age optimization",
        "marker_type": "aging markers"
    },
    "biological-age-test": {
        "test_name": "biological age test",
        "body_system": "overall aging",
        "condition_focus": "biological age optimization",
        "marker_type": "longevity markers"
    },
    "epigenetics-info": {
        "test_name": "longevity panel",
        "body_system": "epigenetic health",
        "condition_focus": "healthy aging",
        "marker_type": "aging markers"
    },
    "epigenetic-test": {
        "test_name": "epigenetic test",
        "body_system": "epigenetic age",
        "condition_focus": "biological age optimization",
        "marker_type": "epigenetic markers"
    },
    "longevity": {
        "test_name": "longevity panel",
        "body_system": "overall health",
        "condition_focus": "lifespan optimization",
        "marker_type": "longevity markers"
    },

    # Cancer Screening
    "psa-test": {
        "test_name": "PSA test",
        "body_system": "prostate health",
        "condition_focus": "prostate cancer screening",
        "marker_type": "prostate markers"
    },
    "prostate-health": {
        "test_name": "prostate panel",
        "body_system": "prostate health",
        "condition_focus": "prostate wellness",
        "marker_type": "prostate markers"
    },

    # Other Health Tests
    "health-screening": {
        "test_name": "health screening",
        "body_system": "overall health",
        "condition_focus": "comprehensive wellness",
        "marker_type": "biomarkers"
    },
    "celiac-info": {
        "test_name": "celiac test",
        "body_system": "digestive health",
        "condition_focus": "celiac disease",
        "marker_type": "celiac markers"
    },
    "celiac-test": {
        "test_name": "celiac test",
        "body_system": "digestive health",
        "condition_focus": "celiac screening",
        "marker_type": "celiac antibodies"
    },
    "semen-analysis": {
        "test_name": "semen analysis",
        "body_system": "reproductive health",
        "condition_focus": "male fertility",
        "marker_type": "fertility markers"
    },
    "lpa-test": {
        "test_name": "Lp(a) test",
        "body_system": "cardiovascular health",
        "condition_focus": "genetic heart risk",
        "marker_type": "advanced lipid markers"
    },
    "uric-acid-test": {
        "test_name": "uric acid test",
        "body_system": "metabolic health",
        "condition_focus": "gout prevention",
        "marker_type": "metabolic markers"
    },
    "lyme-test": {
        "test_name": "Lyme test",
        "body_system": "immune health",
        "condition_focus": "Lyme disease screening",
        "marker_type": "infectious disease markers"
    },
}


def generate_how_it_works(slug, content):
    """Generate How It Works subheadings for a landing page."""
    test_name = content["test_name"]
    body_system = content["body_system"]
    condition_focus = content["condition_focus"]
    marker_type = content["marker_type"]

    return {
        "how-it-works-1-subheading": f"Your {test_name} is just one of 100+ advanced biomarkers you get—all for $199/year.",
        "how-it-works-2-subheading": f"See exactly where your {body_system} stands with clear, visual results and what they mean for your health.",
        "how-it-works-3-subheading": f"Get a personalized plan to optimize your {body_system} based on your {marker_type} and related markers.",
        "how-it-works-4-subheading": f"Our care team is available 24/7 to answer questions about your {condition_focus} results."
    }


def fix_timing_in_field(value):
    """Replace '5 days' with '10 days' in a field value."""
    if not value:
        return value
    if isinstance(value, str):
        # Replace various forms of "5 days"
        value = re.sub(r'\b5 days\b', '10 days', value, flags=re.IGNORECASE)
        value = re.sub(r'\bResults in 5 days\b', 'Results in 10 days', value, flags=re.IGNORECASE)
        value = re.sub(r'\bwithin 5 days\b', 'within 10 days', value, flags=re.IGNORECASE)
        # Also fix $17/month to $199/year
        value = re.sub(r'\$17/month', '$199/year', value)
        value = re.sub(r'\$17/mo', '$199/year', value)
        value = re.sub(r'Only \$17/month', 'Only $199/year', value)
    return value


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

    # Fields to check for timing fixes
    text_fields = [
        "hero-subheadline", "meta-description", "condition-overview",
        "why-test", "what-is-included", "next-steps",
        "faq-1-answer", "faq-2-answer", "faq-3-answer", "faq-4-answer",
        "stat-3-text"  # Often contains "X days to get results"
    ]

    for item in items:
        slug = item.get('fieldData', {}).get('slug', '')
        item_id = item.get('id', '')
        field_data = item.get('fieldData', {})

        updates = {}

        # 1. Add How It Works content if we have mapping
        if slug in HOW_IT_WORKS_CONTENT:
            how_it_works = generate_how_it_works(slug, HOW_IT_WORKS_CONTENT[slug])
            updates.update(how_it_works)
        else:
            print(f"⚠️  No How It Works mapping for: {slug}")
            skipped_count += 1

        # 2. Fix timing in existing fields
        for field in text_fields:
            original_value = field_data.get(field, '')
            if original_value:
                fixed_value = fix_timing_in_field(original_value)
                if fixed_value != original_value:
                    updates[field] = fixed_value
                    print(f"   Fixed timing in {field}")

        # Also fix stat-3-number if it says "5 days"
        stat3_num = field_data.get('stat-3-number', '')
        if stat3_num and '5 day' in stat3_num.lower():
            updates['stat-3-number'] = '10 days'
            print(f"   Fixed stat-3-number")

        if not updates:
            print(f"⏭️  {slug}: No updates needed")
            continue

        # Update the landing page
        status, result = update_landing_page(item_id, updates)

        if status == 200:
            update_types = []
            if any(k.startswith('how-it-works') for k in updates):
                update_types.append("How It Works")
            if any(k in text_fields or k == 'stat-3-number' for k in updates):
                update_types.append("timing fixes")
            print(f"✅ {slug}: Updated ({', '.join(update_types)})")
            success_count += 1
        else:
            print(f"❌ {slug}: Error - {result}")
            error_count += 1

        # Rate limiting
        time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"Complete! Success: {success_count}, Errors: {error_count}, Skipped: {skipped_count}")


if __name__ == '__main__':
    main()
