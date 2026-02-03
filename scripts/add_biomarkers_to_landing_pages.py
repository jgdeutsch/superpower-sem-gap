#!/usr/bin/env python3
"""
Add featured biomarkers to each SEM landing page in Webflow CMS.
Maps each landing page to 4-5 relevant biomarker IDs based on topic.
"""
import json
import requests
import time

WEBFLOW_API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
LANDING_PAGES_COLLECTION = "6981a714e199bac70776d880"
BIOMARKERS_COLLECTION = "662de62e7a966fa325943816"

HEADERS = {
    "Authorization": f"Bearer {WEBFLOW_API_KEY}",
    "Content-Type": "application/json"
}

# Biomarker name to ID mapping (from API response)
BIOMARKER_IDS = {
    # Thyroid
    "Thyroglobulin Antibodies": "689f4d52b98407fd646415ad",
    "Thyroid peroxidase antibody": "689f4d524fa04e6a3dc14070",
    "Triiodothyronine (T3), Free": "689f4d5438b28a6995170033",
    "Thyroid antibodies": "68e9810f80f27fb1fd4d6c1f",

    # Hormones
    "Cortisol-to-DHEA-S Ratio": "689f4d564600a28424e81e10",
    "Estradiol": "68e9810f436b651ebd1b8f93",
    "FSH": "68e9810fdf09334914b8562a",
    "LH": "68e9810fab0596f61d48b745",
    "Progesterone": "689f4d530eb71d5ba67df407",
    "Prolactin": "689f4d53787e1c7ba42fc3ec",
    "Testosterone/Estradiol Ratio": "689f4d55539004de87f4b487",
    "Free Androgen Index": "689f4d554de5f58d5940d5c3",
    "IGF-1": "689f4d538139de7786e91d0b",

    # Lipids/Heart
    "LDL P": "689f4d53cfaaa51109cc1b2a",
    "LDL Size": "689f4d54a0e81b05c9c396b0",
    "HDL P": "689f4d54f69047a72acc5edb",
    "HDL Size": "689f4d548382ee7ec9bad3e4",
    "Small LDL P": "689f4d542a57d00b20b0e4aa",
    "Lp(a)": "68e98110e9795ee7ed320eb2",
    "Atherogenic Index": "689f4d5423115267319d27b7",
    "Atherogenic Coefficient": "689f4d54b4857a0816703c7c",
    "TG/HDL Ratio": "689f4d54128e6732ea084a43",
    "Non-HDL/ApoB": "689f4d55e3f44760f6af0fd0",
    "LDL/ApoB": "689f4d552a57d00b20b0e4ef",
    "Lipoprotein fractionation": "68e981102744d33e3cda88a4",

    # Metabolic
    "Insulin": "689f4d53c753a5d673361236",
    "Glucose": "68e9810f85ce98b507a1c951",
    "Fructosamine": "68e98111f2e6d57f5b8df6ed",
    "TyG Index": "689f4d55e6a86634e82a4205",
    "Cardio IQ Insulin Resistance": "68e9811144f677337b8cc485",
    "Glycation Gap": "689f4d5698d71ffa6664b4b7",
    "Leptin": "68e981110fe73912039afc3e",
    "Adiponectin": "68e98111dc633c8e8fb9aa93",

    # Inflammation
    "ESR": "689f4d53ef6b434988f88410",
    "CRP/Albumin Ratio": "689f4d568d2659aa4a036453",
    "CRP/DHEA-S Ratio": "689f4d56f3e4f315d7ee3890",
    "NLR": "689f4d566c0681d615d105eb",
    "PLR": "689f4d56a306515abd7e9fc2",
    "SII": "689f4d558139de7786e91f02",
    "SIRI": "689f4d56ab367b947f251d11",

    # Autoimmune
    "ANA": "68e9810ee23b617aa2a8ba34",
    "Rheumatoid factor": "68e9810ec3d9a2a250b7a6f0",
    "CCP antibody": "68e9810edbf25c1ff344d518",
    "dsDNA antibody": "68e9810ec0c8bd03a9a61f75",

    # Vitamins
    "Vitamin B12": "689f4d522336885f967b2e69",
    "Folate": "689f4d52d9383aa1f33a3a2c",
    "Folate RBC": "68e9811115624fc8cbc3cea0",
    "MMA": "68e9811152f61460557debd1",
    "Magnesium": "68e98111aa7b37d09c26858c",
    "Vitamin A": "68e98110fed8bbed492a4e59",
    "Vitamin C": "68e98110bdabca1137b28d73",
    "Vitamin E": "68e98111fcdff82c4a2b8778",
    "Vitamin K": "68e98111b5625ba1efe7b344",
    "Vitamin B6": "68e981113433a63c2a9d02f0",
    "Vitamin B2": "68e9811109094e6956f6bdd1",
    "Selenium": "68e9811120dff9b7218795aa",

    # Liver
    "De Ritis Ratio": "689f4d5545a304e7a16a126c",
    "GGT/ALT": "689f4d5657cc9d60f166d0fb",
    "Bilirubin/Albumin Ratio": "689f4d55849b9a5b9935c07a",
    "I/D Bilirubin Ratio": "689f4d554fbeeb5070f31510",

    # Kidney
    "Cystatin C": "68e98110f789f0bd646b8412",
    "Cockcroft-Gault": "689f4d571d7d5e56f123138f",
    "SDMA": "68e98110ab62c9a6855e5091",

    # Ferritin ratios
    "Ferritin/CRP Ratio": "689f4d55128e6732ea084aa0",
    "Ferritin/Albumin Ratio": "689f4d561209ccd08099eb28",
    "RDW/Ferritin Ratio": "689f4d56ac6ae9bc2cd093d8",

    # Prostate
    "PSA Total": "689f4d5311ad42d4512577bd",
    "PSA Free": "689f4d530dac1d5aaea02aa2",

    # Celiac
    "Celiac Panel": "68e9810f6d8a3699dd37c180",

    # Reproductive
    "AMH": "68e9810fb6b5fad9bfa3e725",
    "17-hydroxyprogesterone": "68e9810f42e1a2f38a6d3497",
    "Ultra-Sensitive Estradiol": "695cc1a17320bcd461c0a775",

    # Mercury
    "Mercury": "68e9810f496a3974408d916c",
}

# Map landing page slugs to biomarker IDs
LANDING_PAGE_BIOMARKERS = {
    # Blood Tests
    "blood-test-general": ["ESR", "NLR", "PLR", "Insulin", "Glucose"],
    "cbc-test": ["ESR", "NLR", "PLR", "RDW/Ferritin Ratio"],
    "blood-test-online": ["ESR", "NLR", "Insulin", "Glucose", "Vitamin B12"],

    # Thyroid
    "hashimotos": ["Thyroglobulin Antibodies", "Thyroid peroxidase antibody", "Triiodothyronine (T3), Free", "Thyroid antibodies"],
    "thyroid-symptoms": ["Thyroglobulin Antibodies", "Thyroid peroxidase antibody", "Triiodothyronine (T3), Free"],
    "hyperthyroidism": ["Triiodothyronine (T3), Free", "Thyroid antibodies", "Thyroglobulin Antibodies"],
    "tsh-test": ["Thyroid antibodies", "Triiodothyronine (T3), Free", "Thyroglobulin Antibodies"],
    "thyroid-panel": ["Thyroid antibodies", "Triiodothyronine (T3), Free", "Thyroglobulin Antibodies", "Thyroid peroxidase antibody"],
    "hypothyroidism": ["Thyroid antibodies", "Triiodothyronine (T3), Free", "Thyroglobulin Antibodies", "Thyroid peroxidase antibody"],
    "thyroid-nodules": ["Thyroglobulin Antibodies", "Thyroid antibodies", "Triiodothyronine (T3), Free"],
    "thyroid-test-at-home": ["Thyroid antibodies", "Triiodothyronine (T3), Free", "Thyroglobulin Antibodies", "Thyroid peroxidase antibody"],
    "thyroid-antibodies": ["Thyroglobulin Antibodies", "Thyroid peroxidase antibody", "Thyroid antibodies"],

    # Hormones - Cortisol
    "cortisol-test": ["Cortisol-to-DHEA-S Ratio", "CRP/DHEA-S Ratio"],
    "cortisol-high-symptoms": ["Cortisol-to-DHEA-S Ratio", "CRP/DHEA-S Ratio", "Insulin"],
    "cortisol-test-at-home": ["Cortisol-to-DHEA-S Ratio", "CRP/DHEA-S Ratio"],
    "cortisol-causes": ["Cortisol-to-DHEA-S Ratio", "CRP/DHEA-S Ratio", "Insulin"],

    # Hormones - Testosterone
    "testosterone-test": ["Free Androgen Index", "Testosterone/Estradiol Ratio", "Estradiol"],
    "testosterone-levels": ["Free Androgen Index", "Testosterone/Estradiol Ratio", "Estradiol", "LH"],
    "testosterone-test-at-home": ["Free Androgen Index", "Testosterone/Estradiol Ratio", "Estradiol"],

    # Hormones - General
    "hormone-panel": ["Estradiol", "FSH", "LH", "Progesterone", "Free Androgen Index"],
    "hormone-imbalance": ["Estradiol", "FSH", "LH", "Cortisol-to-DHEA-S Ratio", "Thyroid antibodies"],
    "dhea-test": ["Cortisol-to-DHEA-S Ratio", "CRP/DHEA-S Ratio", "Free Androgen Index"],
    "prolactin-test": ["Prolactin", "LH", "FSH", "Estradiol"],

    # Heart & Cholesterol
    "triglycerides-high": ["TG/HDL Ratio", "Atherogenic Index", "LDL P", "Small LDL P"],
    "high-cholesterol": ["LDL P", "LDL Size", "Small LDL P", "Lp(a)", "Atherogenic Coefficient"],
    "cholesterol-test": ["LDL P", "HDL P", "LDL Size", "HDL Size", "Atherogenic Index"],
    "cholesterol-foods": ["LDL P", "HDL P", "TG/HDL Ratio", "Atherogenic Index"],
    "apob-test": ["LDL/ApoB", "Non-HDL/ApoB", "LDL P", "Lp(a)"],
    "lipid-panel": ["LDL P", "HDL P", "LDL Size", "HDL Size", "Lipoprotein fractionation"],
    "ldl-hdl": ["LDL P", "HDL P", "LDL Size", "HDL Size", "TG/HDL Ratio"],
    "homocysteine": ["Vitamin B12", "Folate", "MMA", "Folate RBC"],
    "heart-test": ["LDL P", "Lp(a)", "Atherogenic Index", "NLR", "SII"],
    "high-cholesterol-symptoms": ["LDL P", "HDL P", "Small LDL P", "Atherogenic Coefficient"],
    "triglycerides-meaning": ["TG/HDL Ratio", "Atherogenic Index", "LDL P"],
    "triglycerides-causes": ["TG/HDL Ratio", "Insulin", "Glucose", "Atherogenic Index"],
    "ldl-levels": ["LDL P", "LDL Size", "Small LDL P", "LDL/ApoB"],

    # Metabolic / Diabetes
    "metabolic-panel": ["Insulin", "Glucose", "TyG Index", "Cardio IQ Insulin Resistance"],
    "glucose-monitoring": ["Glucose", "Fructosamine", "Glycation Gap", "Insulin"],
    "a1c-test": ["Fructosamine", "Glucose", "Glycation Gap", "Insulin"],
    "a1c-levels": ["Fructosamine", "Glucose", "Glycation Gap", "Cardio IQ Insulin Resistance"],
    "diabetes-test": ["Insulin", "Glucose", "Fructosamine", "TyG Index", "Cardio IQ Insulin Resistance"],
    "metabolic-syndrome": ["TyG Index", "Insulin", "TG/HDL Ratio", "Atherogenic Index"],

    # Inflammation
    "inflammatory-foods": ["ESR", "NLR", "SII", "SIRI", "CRP/Albumin Ratio"],
    "ana-test": ["ANA", "dsDNA antibody", "Rheumatoid factor", "ESR"],
    "crp-test": ["CRP/Albumin Ratio", "CRP/DHEA-S Ratio", "ESR", "NLR"],
    "autoimmune-test": ["ANA", "Rheumatoid factor", "CCP antibody", "dsDNA antibody", "ESR"],
    "inflammation-symptoms": ["ESR", "NLR", "PLR", "SII", "SIRI"],

    # Kidney & Liver
    "adrenal": ["Cortisol-to-DHEA-S Ratio", "CRP/DHEA-S Ratio", "IGF-1"],
    "liver-panel": ["De Ritis Ratio", "GGT/ALT", "Bilirubin/Albumin Ratio"],
    "liver-enzymes": ["De Ritis Ratio", "GGT/ALT", "Bilirubin/Albumin Ratio", "I/D Bilirubin Ratio"],
    "kidney-panel": ["Cystatin C", "Cockcroft-Gault", "SDMA"],
    "gfr-test": ["Cystatin C", "Cockcroft-Gault", "SDMA"],
    "bun-test": ["Cystatin C", "Cockcroft-Gault"],

    # Vitamins & Nutrients
    "ferritin-test": ["Ferritin/CRP Ratio", "Ferritin/Albumin Ratio", "RDW/Ferritin Ratio"],
    "vitamin-d-test": ["Vitamin A", "Vitamin E", "Vitamin K"],
    "vitamin-panel": ["Vitamin B12", "Folate", "Vitamin A", "Vitamin E", "Magnesium"],
    "magnesium-test": ["Magnesium", "Vitamin B6", "Selenium"],
    "b12-test": ["Vitamin B12", "MMA", "Folate", "Folate RBC"],
    "b12-deficiency": ["Vitamin B12", "MMA", "Folate", "Folate RBC"],
    "vitamin-d-deficiency": ["Vitamin A", "Vitamin E", "Vitamin K"],
    "vitamin-d-info": ["Vitamin A", "Vitamin E", "Vitamin K"],
    "vitamin-d-sun": ["Vitamin A", "Vitamin E"],
    "folate-test": ["Folate", "Folate RBC", "Vitamin B12", "MMA"],
    "iron-test": ["Ferritin/CRP Ratio", "Ferritin/Albumin Ratio", "RDW/Ferritin Ratio"],

    # Aging & Longevity
    "telomeres-info": ["IGF-1", "NLR", "SII", "Insulin"],
    "telomere-test": ["IGF-1", "NLR", "SII", "Insulin", "ESR"],
    "biological-age-test": ["IGF-1", "NLR", "SII", "SIRI", "Insulin"],
    "epigenetics-info": ["IGF-1", "NLR", "Insulin", "ESR"],
    "epigenetic-test": ["IGF-1", "NLR", "SII", "Insulin"],
    "longevity": ["IGF-1", "NLR", "SII", "Insulin", "Lp(a)"],

    # Cancer Screening
    "psa-test": ["PSA Total", "PSA Free"],
    "prostate-health": ["PSA Total", "PSA Free", "Free Androgen Index"],

    # Other Health Tests
    "health-screening": ["ESR", "NLR", "Insulin", "Glucose", "LDL P"],
    "celiac-info": ["Celiac Panel"],
    "celiac-test": ["Celiac Panel"],
    "semen-analysis": ["FSH", "LH", "Free Androgen Index", "Testosterone/Estradiol Ratio"],
    "lpa-test": ["Lp(a)", "LDL P", "Small LDL P", "Atherogenic Index"],
    "uric-acid-test": ["Cystatin C", "Insulin", "TG/HDL Ratio"],
    "lyme-test": ["ESR", "NLR", "ANA"],
}


def fetch_landing_pages():
    """Fetch all landing page items from Webflow."""
    url = f"https://api.webflow.com/v2/collections/{LANDING_PAGES_COLLECTION}/items?limit=100"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return {item['fieldData']['slug']: item['id'] for item in data.get('items', [])}


def update_landing_page_biomarkers(item_id, biomarker_ids):
    """Update a landing page with biomarker references."""
    url = f"https://api.webflow.com/v2/collections/{LANDING_PAGES_COLLECTION}/items/{item_id}"
    payload = {
        "fieldData": {
            "featured-biomarkers": biomarker_ids
        }
    }
    response = requests.patch(url, headers=HEADERS, json=payload)
    return response.status_code, response.json()


def main():
    print("Fetching landing pages...")
    landing_pages = fetch_landing_pages()
    print(f"Found {len(landing_pages)} landing pages\n")

    success_count = 0
    error_count = 0
    skipped_count = 0

    for slug, item_id in landing_pages.items():
        if slug not in LANDING_PAGE_BIOMARKERS:
            print(f"⚠️  No biomarker mapping for: {slug}")
            skipped_count += 1
            continue

        # Convert biomarker names to IDs
        biomarker_names = LANDING_PAGE_BIOMARKERS[slug]
        biomarker_ids = []
        for name in biomarker_names:
            if name in BIOMARKER_IDS:
                biomarker_ids.append(BIOMARKER_IDS[name])
            else:
                print(f"   Warning: Biomarker '{name}' not found in mapping")

        if not biomarker_ids:
            print(f"⚠️  No valid biomarker IDs for: {slug}")
            skipped_count += 1
            continue

        # Update the landing page
        status, result = update_landing_page_biomarkers(item_id, biomarker_ids)

        if status == 200:
            print(f"✅ {slug}: Added {len(biomarker_ids)} biomarkers")
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
