#!/usr/bin/env python3
"""
Populate the SEM FAQs collection and link FAQs to landing pages.
"""
import json
import requests
import time
import re

WEBFLOW_API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
SEM_FAQS_COLLECTION = "6981cbbfb6102bfdf7d05094"
LANDING_PAGES_COLLECTION = "6981a714e199bac70776d880"

HEADERS = {
    "Authorization": f"Bearer {WEBFLOW_API_KEY}",
    "Content-Type": "application/json"
}

# FAQs organized by category - these will be linked to relevant landing pages
# Format: {slug_pattern: [list of FAQs]}
FAQS_BY_CATEGORY = {
    # General blood testing FAQs
    "general": [
        {
            "question": "How does Superpower testing work?",
            "answer": "<p>Sign up for membership, schedule a blood draw at a local lab or add at-home phlebotomist visit for $99. We test 90+ biomarkers from one draw, and you get results with personalized insights in about 10 days.</p>"
        },
        {
            "question": "What's included in my membership?",
            "answer": "<p>Your $199/year membership includes one comprehensive blood panel with 90+ biomarkers, AI-powered health insights, a personalized action plan, and ongoing support from our clinical team. Additional tests and consultations available.</p>"
        },
        {
            "question": "How accurate are the results?",
            "answer": "<p>All samples are processed at CLIA-certified, CAP-accredited laboratories—the same labs used by major health systems. Our biomarker analysis meets the highest clinical standards.</p>"
        },
    ],

    # Kidney tests
    "kidney": [
        {
            "question": "What does my BUN level tell me?",
            "answer": "<p>BUN (Blood Urea Nitrogen) measures how well your kidneys filter waste. We test it alongside creatinine, eGFR, and electrolytes to give you the complete kidney picture—not just one number in isolation.</p>"
        },
        {
            "question": "Why test GFR instead of just creatinine?",
            "answer": "<p>GFR (Glomerular Filtration Rate) is the gold standard for kidney function. Creatinine alone can be misleading based on muscle mass, age, and diet. We calculate eGFR to show your actual kidney filtration rate.</p>"
        },
        {
            "question": "Can kidney problems be reversed?",
            "answer": "<p>Early-stage kidney dysfunction is often reversible with lifestyle changes. That's why 90% of people with early CKD don't know they have it—no symptoms until it's advanced. Regular testing catches problems early.</p>"
        },
    ],

    # Liver tests
    "liver": [
        {
            "question": "What do elevated liver enzymes mean?",
            "answer": "<p>Elevated ALT or AST can indicate liver inflammation, fatty liver, medication effects, or other conditions. We test 7 liver markers together to identify the pattern and likely cause—not just flag a single high number.</p>"
        },
        {
            "question": "How common is fatty liver disease?",
            "answer": "<p>1 in 4 adults has non-alcoholic fatty liver disease (NAFLD), often without knowing it. Our liver panel can detect early signs before symptoms appear, when it's most reversible.</p>"
        },
    ],

    # Cholesterol/Heart tests
    "cholesterol": [
        {
            "question": "Why test more than just total cholesterol?",
            "answer": "<p>50% of heart attacks occur in people with 'normal' cholesterol. We test LDL, HDL, triglycerides, ApoB, Lp(a), and other advanced markers because the ratio and particle type matter more than the total number.</p>"
        },
        {
            "question": "What is ApoB and why does it matter?",
            "answer": "<p>ApoB measures the actual number of atherogenic particles in your blood—the ones that cause plaque buildup. It's a better predictor of cardiovascular risk than LDL cholesterol alone.</p>"
        },
        {
            "question": "What is Lp(a) and should I be tested?",
            "answer": "<p>Lp(a) is a genetic risk factor for heart disease that affects 1 in 5 people. Unlike cholesterol, it doesn't respond to diet or exercise. You only need to test it once—it's largely inherited and stable throughout life.</p>"
        },
    ],

    # Thyroid tests
    "thyroid": [
        {
            "question": "Why test more than just TSH?",
            "answer": "<p>TSH alone misses thyroid problems in up to 20% of cases. We test TSH, Free T4, Free T3, and thyroid antibodies to catch Hashimoto's, subclinical hypothyroidism, and conversion issues that TSH-only testing misses.</p>"
        },
        {
            "question": "What are thyroid antibodies?",
            "answer": "<p>TPO and thyroglobulin antibodies indicate autoimmune thyroid disease (Hashimoto's or Graves'). You can have elevated antibodies for years before TSH becomes abnormal—early detection allows earlier intervention.</p>"
        },
        {
            "question": "Can thyroid problems cause weight gain?",
            "answer": "<p>Yes. Hypothyroidism slows metabolism and can cause weight gain, fatigue, brain fog, and cold intolerance. But these symptoms are common, so testing is the only way to know if your thyroid is the cause.</p>"
        },
    ],

    # Hormone tests
    "hormone": [
        {
            "question": "What hormones does Superpower test?",
            "answer": "<p>Our comprehensive panel includes cortisol, DHEA-S, testosterone (total and free), estradiol, progesterone (for women), thyroid hormones, and insulin—giving you a complete picture of your hormonal health.</p>"
        },
        {
            "question": "Why do hormone levels matter?",
            "answer": "<p>Hormones control energy, mood, sleep, metabolism, and aging. Even 'normal' levels may not be optimal for you. 52% of our members discover hormone imbalances they didn't know they had.</p>"
        },
        {
            "question": "Can hormone imbalances be fixed?",
            "answer": "<p>Many hormone imbalances respond to lifestyle changes—sleep, stress management, exercise, and nutrition. For others, supplementation or hormone therapy may help. First step is knowing your levels.</p>"
        },
    ],

    # Testosterone tests
    "testosterone": [
        {
            "question": "What's a normal testosterone level?",
            "answer": "<p>Reference ranges say 300-1000 ng/dL for men, but 'normal' isn't always optimal. We look at free testosterone, SHBG, and symptoms together—because a 35-year-old at 350 ng/dL may feel very different than at 650.</p>"
        },
        {
            "question": "Why does testosterone decline with age?",
            "answer": "<p>Testosterone drops about 1% per year after 30. By 45, 40% of men have levels below optimal. But lifestyle factors—sleep, stress, weight, exercise—have a bigger impact than age alone.</p>"
        },
    ],

    # Cortisol tests
    "cortisol": [
        {
            "question": "What does cortisol tell me about my health?",
            "answer": "<p>Cortisol is your primary stress hormone. Chronically high or low cortisol affects energy, sleep, weight, immune function, and mood. 47% of our members find cortisol imbalances they weren't aware of.</p>"
        },
        {
            "question": "When should cortisol be tested?",
            "answer": "<p>Cortisol follows a daily rhythm—highest in morning, lowest at night. We test AM cortisol to catch both high stress patterns and adrenal fatigue. Timing matters for accurate results.</p>"
        },
    ],

    # Diabetes/Metabolic tests
    "diabetes": [
        {
            "question": "What's the difference between glucose and HbA1c?",
            "answer": "<p>Glucose is a snapshot of right now. HbA1c shows your average blood sugar over 2-3 months. We test both, plus insulin, because you can have normal glucose but high insulin—an early warning sign most doctors miss.</p>"
        },
        {
            "question": "What is prediabetes?",
            "answer": "<p>Prediabetes means HbA1c between 5.7-6.4%—blood sugar is elevated but not yet diabetic. 96 million Americans have it, and 80% don't know. Without intervention, 70% will progress to type 2 diabetes.</p>"
        },
        {
            "question": "Can prediabetes be reversed?",
            "answer": "<p>Yes. Prediabetes is highly reversible with diet, exercise, and weight loss. That's why catching it early matters—you can prevent diabetes entirely instead of managing it for life.</p>"
        },
    ],

    # Inflammation tests
    "inflammation": [
        {
            "question": "Why test inflammation markers?",
            "answer": "<p>Chronic inflammation is linked to heart disease, diabetes, cancer, and autoimmune conditions. hs-CRP and other markers detect silent inflammation years before symptoms appear.</p>"
        },
        {
            "question": "What causes chronic inflammation?",
            "answer": "<p>Poor diet, stress, lack of sleep, excess weight, and environmental toxins all drive inflammation. The good news: 70% of members see inflammation improve with targeted lifestyle changes.</p>"
        },
    ],

    # Vitamin tests
    "vitamin": [
        {
            "question": "Which vitamin deficiencies are most common?",
            "answer": "<p>67% of our members find at least one vitamin deficiency. Vitamin D (58%), B12 (43%), and magnesium (48%) are most common. Even with 'healthy' diets, modern food and indoor lifestyles create gaps.</p>"
        },
        {
            "question": "Can I test vitamin levels with a blood test?",
            "answer": "<p>Yes. We test vitamin D, B12, folate, iron/ferritin, and other key nutrients. Blood tests show what's actually in your body—not just what you're eating or supplementing.</p>"
        },
    ],

    # Longevity/Aging tests
    "longevity": [
        {
            "question": "What is biological age?",
            "answer": "<p>Biological age measures how old your body acts, not how many birthdays you've had. 70% of our members slow their biological age through targeted interventions based on their biomarker data.</p>"
        },
        {
            "question": "Can you actually slow aging?",
            "answer": "<p>Yes. Research shows 80% of aging is influenced by lifestyle, not genetics. Our testing identifies your specific aging drivers—inflammation, metabolic dysfunction, hormone decline—so you can target what matters.</p>"
        },
    ],

    # Autoimmune tests
    "autoimmune": [
        {
            "question": "What is an ANA test?",
            "answer": "<p>ANA (Antinuclear Antibody) screens for autoimmune conditions like lupus, Sjogren's, and rheumatoid arthritis. It takes an average of 7 years to diagnose autoimmune disease—ANA testing can accelerate that timeline.</p>"
        },
        {
            "question": "Can autoimmune disease be detected early?",
            "answer": "<p>Yes. Autoantibodies often appear years before symptoms. Early detection allows lifestyle interventions that may prevent or delay disease progression.</p>"
        },
    ],
}

# Map landing page slugs to FAQ categories
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


def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')[:256]


def create_faq(question, answer):
    """Create a FAQ item in the SEM FAQs collection."""
    url = f"https://api.webflow.com/v2/collections/{SEM_FAQS_COLLECTION}/items"

    name = question[:256]
    slug = slugify(question)[:256]

    payload = {
        "fieldData": {
            "name": name,
            "slug": slug,
            "question": question,
            "answer": answer
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    return response.status_code, response.json()


def fetch_landing_pages():
    """Fetch all landing page items from Webflow."""
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
    # Step 1: Create all FAQ items and track their IDs by category
    print("Creating FAQ items...")
    faq_ids_by_category = {}
    all_faqs_created = []

    for category, faqs in FAQS_BY_CATEGORY.items():
        faq_ids_by_category[category] = []

        for faq in faqs:
            status, result = create_faq(faq["question"], faq["answer"])

            if status in [200, 201]:
                faq_id = result.get('id')
                faq_ids_by_category[category].append(faq_id)
                all_faqs_created.append(faq_id)
                print(f"  ✅ Created: {faq['question'][:50]}...")
            else:
                print(f"  ❌ Error creating FAQ: {result}")

            time.sleep(0.3)

    print(f"\nCreated {len(all_faqs_created)} FAQ items total")

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
    print(f"FAQs created: {len(all_faqs_created)}")
    print(f"Landing pages updated: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Skipped: {skipped_count}")


if __name__ == '__main__':
    main()
