#!/usr/bin/env python3
"""
Link existing SEM FAQs to landing pages via the custom-faqs MultiReference field.
"""
import json
import requests
import time

WEBFLOW_API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
SEM_FAQS_COLLECTION = "6981cbbfb6102bfdf7d05094"
LANDING_PAGES_COLLECTION = "6981a714e199bac70776d880"

HEADERS = {
    "Authorization": f"Bearer {WEBFLOW_API_KEY}",
    "Content-Type": "application/json"
}

# Map FAQ questions to categories (for matching to landing pages)
FAQ_CATEGORIES = {
    # General FAQs
    "How does Superpower testing work?": ["general"],
    "What's included in my membership?": ["general"],
    "How accurate are the results?": ["general"],

    # Kidney FAQs
    "What does my BUN level tell me?": ["kidney"],
    "Why test GFR instead of just creatinine?": ["kidney"],
    "Can kidney problems be reversed?": ["kidney"],

    # Liver FAQs
    "What do elevated liver enzymes mean?": ["liver"],
    "How common is fatty liver disease?": ["liver"],

    # Cholesterol FAQs
    "Why test more than just total cholesterol?": ["cholesterol"],
    "What is ApoB and why does it matter?": ["cholesterol"],
    "What is Lp(a) and should I be tested?": ["cholesterol"],

    # Thyroid FAQs
    "Why test more than just TSH?": ["thyroid"],
    "What are thyroid antibodies?": ["thyroid"],
    "Can thyroid problems cause weight gain?": ["thyroid"],

    # Hormone FAQs
    "What hormones does Superpower test?": ["hormone"],
    "Why do hormone levels matter?": ["hormone"],
    "Can hormone imbalances be fixed?": ["hormone"],

    # Testosterone FAQs
    "What's a normal testosterone level?": ["testosterone"],
    "Why does testosterone decline with age?": ["testosterone"],

    # Cortisol FAQs
    "What does cortisol tell me about my health?": ["cortisol"],
    "When should cortisol be tested?": ["cortisol"],

    # Diabetes FAQs
    "What's the difference between glucose and HbA1c?": ["diabetes"],
    "What is prediabetes?": ["diabetes"],
    "Can prediabetes be reversed?": ["diabetes"],

    # Inflammation FAQs
    "Why test inflammation markers?": ["inflammation"],
    "What causes chronic inflammation?": ["inflammation"],

    # Vitamin FAQs
    "Which vitamin deficiencies are most common?": ["vitamin"],
    "Can I test vitamin levels with a blood test?": ["vitamin"],

    # Longevity FAQs
    "What is biological age?": ["longevity"],
    "Can you actually slow aging?": ["longevity"],

    # Autoimmune FAQs
    "What is an ANA test?": ["autoimmune"],
    "Can autoimmune disease be detected early?": ["autoimmune"],
}

# Map landing page slugs to which FAQ categories they should get
SLUG_TO_CATEGORIES = {
    # Kidney
    "bun-test": ["general", "kidney"],
    "gfr-test": ["general", "kidney"],
    "kidney-panel": ["general", "kidney"],

    # Liver
    "liver-panel": ["general", "liver"],
    "liver-enzymes": ["general", "liver"],
    "uric-acid-test": ["general", "liver"],

    # Cholesterol/Heart
    "cholesterol-test": ["general", "cholesterol"],
    "high-cholesterol": ["general", "cholesterol"],
    "high-cholesterol-symptoms": ["general", "cholesterol"],
    "cholesterol-foods": ["general", "cholesterol"],
    "lipid-panel": ["general", "cholesterol"],
    "ldl-levels": ["general", "cholesterol"],
    "ldl-hdl": ["general", "cholesterol"],
    "triglycerides-high": ["general", "cholesterol"],
    "triglycerides-causes": ["general", "cholesterol"],
    "triglycerides-meaning": ["general", "cholesterol"],
    "apob-test": ["general", "cholesterol"],
    "lpa-test": ["general", "cholesterol"],
    "heart-test": ["general", "cholesterol"],
    "homocysteine": ["general", "cholesterol"],

    # Thyroid
    "thyroid-panel": ["general", "thyroid"],
    "tsh-test": ["general", "thyroid"],
    "thyroid-antibodies": ["general", "thyroid"],
    "hypothyroidism": ["general", "thyroid"],
    "hyperthyroidism": ["general", "thyroid"],
    "thyroid-symptoms": ["general", "thyroid"],
    "thyroid-nodules": ["general", "thyroid"],
    "hashimotos": ["general", "thyroid", "autoimmune"],

    # Hormones
    "hormone-panel": ["general", "hormone"],
    "hormone-imbalance": ["general", "hormone"],
    "testosterone-test": ["general", "hormone", "testosterone"],
    "testosterone-levels": ["general", "hormone", "testosterone"],
    "cortisol-test": ["general", "hormone", "cortisol"],
    "cortisol-high-symptoms": ["general", "hormone", "cortisol"],
    "adrenal": ["general", "hormone", "cortisol"],
    "dhea-test": ["general", "hormone"],
    "prolactin-test": ["general", "hormone"],

    # Metabolic/Diabetes
    "metabolic-panel": ["general", "diabetes"],
    "metabolic-syndrome": ["general", "diabetes"],
    "diabetes-test": ["general", "diabetes"],
    "a1c-test": ["general", "diabetes"],
    "a1c-levels": ["general", "diabetes"],
    "glucose-monitoring": ["general", "diabetes"],

    # Inflammation
    "crp-test": ["general", "inflammation"],
    "inflammation-symptoms": ["general", "inflammation"],
    "inflammatory-foods": ["general", "inflammation"],
    "autoimmune-test": ["general", "inflammation", "autoimmune"],
    "ana-test": ["general", "autoimmune"],
    "lyme-test": ["general", "autoimmune"],
    "celiac-test": ["general", "autoimmune"],
    "celiac-info": ["general", "autoimmune"],

    # Vitamins
    "vitamin-panel": ["general", "vitamin"],
    "vitamin-d-test": ["general", "vitamin"],
    "vitamin-d-deficiency": ["general", "vitamin"],
    "vitamin-d-info": ["general", "vitamin"],
    "vitamin-d-sun": ["general", "vitamin"],
    "b12-test": ["general", "vitamin"],
    "b12-deficiency": ["general", "vitamin"],
    "folate-test": ["general", "vitamin"],
    "iron-test": ["general", "vitamin"],
    "ferritin-test": ["general", "vitamin"],
    "magnesium-test": ["general", "vitamin"],

    # Blood tests
    "cbc-test": ["general"],
    "blood-test-general": ["general"],
    "blood-test-online": ["general"],
    "health-screening": ["general"],

    # Longevity/Aging
    "longevity": ["general", "longevity"],
    "biological-age-test": ["general", "longevity"],
    "epigenetic-test": ["general", "longevity"],
    "epigenetics-info": ["general", "longevity"],
    "telomere-test": ["general", "longevity"],
    "telomeres-info": ["general", "longevity"],

    # Men's health
    "psa-test": ["general"],
    "prostate-health": ["general"],
    "semen-analysis": ["general"],
}


def fetch_faqs():
    """Fetch all FAQ items."""
    url = f"https://api.webflow.com/v2/collections/{SEM_FAQS_COLLECTION}/items?limit=100"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data.get('items', [])


def fetch_landing_pages():
    """Fetch all landing page items."""
    url = f"https://api.webflow.com/v2/collections/{LANDING_PAGES_COLLECTION}/items?limit=100"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data.get('items', [])


def update_landing_page_faqs(item_id, faq_ids):
    """Update a landing page with FAQ references."""
    url = f"https://api.webflow.com/v2/collections/{LANDING_PAGES_COLLECTION}/items/{item_id}"
    payload = {
        "fieldData": {
            "custom-faqs": faq_ids
        }
    }
    response = requests.patch(url, headers=HEADERS, json=payload)
    return response.status_code, response.json()


def main():
    # Step 1: Fetch all FAQs and organize by category
    print("Fetching FAQs...")
    faqs = fetch_faqs()
    print(f"Found {len(faqs)} FAQs\n")

    # Build FAQ ID to category mapping
    faq_ids_by_category = {}
    for faq in faqs:
        question = faq.get('fieldData', {}).get('question', '')
        faq_id = faq.get('id')

        if question in FAQ_CATEGORIES:
            for category in FAQ_CATEGORIES[question]:
                if category not in faq_ids_by_category:
                    faq_ids_by_category[category] = []
                faq_ids_by_category[category].append(faq_id)

    print("FAQs by category:")
    for cat, ids in faq_ids_by_category.items():
        print(f"  {cat}: {len(ids)} FAQs")

    # Step 2: Fetch landing pages and link FAQs
    print("\nFetching landing pages...")
    items = fetch_landing_pages()
    print(f"Found {len(items)} landing pages\n")

    print("Linking FAQs to landing pages...")
    success_count = 0
    error_count = 0
    skipped_count = 0

    for item in items:
        slug = item.get('fieldData', {}).get('slug', '') or ''
        item_id = item.get('id', '')

        if slug not in SLUG_TO_CATEGORIES:
            print(f"  ⏭️  {slug}: No FAQ mapping defined")
            skipped_count += 1
            continue

        # Collect FAQ IDs for this landing page's categories
        categories = SLUG_TO_CATEGORIES[slug]
        faq_ids = []

        for cat in categories:
            if cat in faq_ids_by_category:
                faq_ids.extend(faq_ids_by_category[cat])

        # Remove duplicates while preserving order
        seen = set()
        unique_faq_ids = []
        for faq_id in faq_ids:
            if faq_id not in seen:
                seen.add(faq_id)
                unique_faq_ids.append(faq_id)

        # Limit to 6 FAQs per page
        unique_faq_ids = unique_faq_ids[:6]

        if not unique_faq_ids:
            print(f"  ⏭️  {slug}: No FAQs found for categories {categories}")
            skipped_count += 1
            continue

        # Update the landing page
        status, result = update_landing_page_faqs(item_id, unique_faq_ids)

        if status == 200:
            print(f"  ✅ {slug}: Linked {len(unique_faq_ids)} FAQs")
            success_count += 1
        else:
            print(f"  ❌ {slug}: Error - {result}")
            error_count += 1

        time.sleep(0.3)

    print(f"\n{'='*60}")
    print(f"Complete!")
    print(f"Landing pages updated: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Skipped: {skipped_count}")


if __name__ == '__main__':
    main()
