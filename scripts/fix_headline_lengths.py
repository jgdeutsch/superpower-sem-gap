#!/usr/bin/env python3
"""
Fix headline and subheadline lengths for all SEM landing pages.

Rules:
- Headline (max 45 chars): Agitate the problem/pain point
- Subheadline (max 115 chars): Solution - what Superpower testing offers

Pattern:
- Headline: Short, punchy problem statement
- Subheadline: "100+ biomarkers in one blood draw. [Relevant markers]. Results in ~10 days. $199/year."
"""

import requests
import json
import time
import re

API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
COLLECTION_ID = "6981a714e199bac70776d880"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "accept": "application/json",
    "content-type": "application/json"
}

# Rewrites for all pages - headline max 45 chars, subheadline max 115 chars
# Format: "slug": ("headline", "subheadline")
REWRITES = {
    # Original SEM pages
    "a1c-levels": (
        "Your A1C Reveals More Than Blood Sugar.",
        "100+ biomarkers in one blood draw. A1C, fasting glucose, insulin, and metabolic markers. Results in ~10 days. $199/year."
    ),
    "a1c-test": (
        "Prediabetes Has No Symptoms. A1C Does.",
        "100+ biomarkers in one blood draw. A1C, fasting glucose, insulin resistance markers. Results in ~10 days. $199/year."
    ),
    "adrenal": (
        "Exhausted by 2pm Every Day?",
        "100+ biomarkers in one blood draw. Cortisol, DHEA, thyroid, and stress hormones. Results in ~10 days. $199/year."
    ),
    "ana-test": (
        "Autoimmune Disease Takes Years to Diagnose.",
        "100+ biomarkers in one blood draw. ANA, inflammation markers, thyroid antibodies. Results in ~10 days. $199/year."
    ),
    "anemia-test": (
        "Tired All the Time? It Might Be Iron.",
        "100+ biomarkers in one blood draw. CBC, ferritin, iron panel, B12, folate. Results in ~10 days. $199/year."
    ),
    "antibody-test": (
        "Your Body May Be Attacking Itself.",
        "100+ biomarkers in one blood draw. ANA, thyroid antibodies, inflammation markers. Results in ~10 days. $199/year."
    ),
    "apob-test": (
        "LDL Misses Half the Heart Risk.",
        "100+ biomarkers in one blood draw. ApoB, Lp(a), lipid panel, inflammation markers. Results in ~10 days. $199/year."
    ),
    "autoimmune-test": (
        "Autoimmune Takes 4+ Years to Diagnose.",
        "100+ biomarkers in one blood draw. ANA, thyroid antibodies, CRP, ESR. Results in ~10 days. $199/year."
    ),
    "b12-deficiency": (
        "Tired, Foggy, Forgetful? Check B12.",
        "100+ biomarkers in one blood draw. B12, folate, iron, thyroid, metabolic panel. Results in ~10 days. $199/year."
    ),
    "b12-test": (
        "40% of Adults Have Low B12.",
        "100+ biomarkers in one blood draw. B12, folate, iron studies, thyroid panel. Results in ~10 days. $199/year."
    ),
    "biological-age-test": (
        "How Old Is Your Body Really?",
        "100+ biomarkers in one blood draw. Biological age markers, inflammation, metabolic health. Results in ~10 days. $199/year."
    ),
    "blood-test-at-home": (
        "Lab-Quality Testing. At Home.",
        "100+ biomarkers. Licensed phlebotomist comes to you. Not a finger-prick kit. Results in ~10 days. $199/year."
    ),
    "blood-test-general": (
        "Your Annual Physical Misses 90%.",
        "100+ biomarkers in one blood draw. Heart, metabolic, hormones, thyroid, vitamins. Results in ~10 days. $199/year."
    ),
    "blood-test-online": (
        "Order Blood Tests Without a Doctor.",
        "100+ biomarkers in one blood draw. No prescription needed. No waiting room. Results in ~10 days. $199/year."
    ),
    "bun-test": (
        "Your Kidneys Work in Silence.",
        "100+ biomarkers in one blood draw. BUN, creatinine, eGFR, full metabolic panel. Results in ~10 days. $199/year."
    ),
    "cbc-test": (
        "Your Blood Cells Tell a Story.",
        "100+ biomarkers in one blood draw. Complete blood count, iron, B12, inflammation. Results in ~10 days. $199/year."
    ),
    "celiac-info": (
        "83% of Celiac Cases Go Undiagnosed.",
        "100+ biomarkers in one blood draw. Celiac antibodies, iron, B12, vitamin D. Results in ~10 days. $199/year."
    ),
    "celiac-test": (
        "Could Gluten Be Destroying Your Gut?",
        "100+ biomarkers in one blood draw. tTG-IgA celiac screening, iron, B12, vitamins. Results in ~10 days. $199/year."
    ),
    "celiac-test-at-home": (
        "Test for Celiac Disease. At Home.",
        "100+ biomarkers in one blood draw. tTG-IgA screening. Licensed phlebotomist. Results in ~10 days. $199/year."
    ),
    "cgm-cost": (
        "CGMs Cost $300/Month. We Cost $199/Year.",
        "100+ biomarkers in one blood draw. HbA1c, fasting insulin catches what CGMs miss. Results in ~10 days."
    ),
    "cgm-non-diabetic": (
        "CGMs Show Spikes. We Show Root Cause.",
        "100+ biomarkers in one blood draw. Fasting insulin, HbA1c, metabolic panel. Results in ~10 days. $199/year."
    ),
    "cholesterol-diet": (
        "You Can't Diet Away Bad Cholesterol.",
        "100+ biomarkers in one blood draw. ApoB, Lp(a), advanced lipids, liver panel. Results in ~10 days. $199/year."
    ),
    "cholesterol-foods": (
        "Diet Is Only 20% of Cholesterol.",
        "100+ biomarkers in one blood draw. Full lipid panel, ApoB, Lp(a), inflammation. Results in ~10 days. $199/year."
    ),
    "cholesterol-levels-women": (
        "After 45, Your Cholesterol Changes Fast.",
        "100+ biomarkers in one blood draw. Lipids, ApoB, Lp(a), hormones together. Results in ~10 days. $199/year."
    ),
    "cholesterol-test": (
        "Standard Cholesterol Tests Miss Half.",
        "100+ biomarkers in one blood draw. LDL, ApoB, Lp(a), HDL, triglycerides. Results in ~10 days. $199/year."
    ),
    "cortisol-high-symptoms": (
        "High Cortisol Wrecks Everything.",
        "100+ biomarkers in one blood draw. Cortisol, DHEA, thyroid, metabolic panel. Results in ~10 days. $199/year."
    ),
    "cortisol-test": (
        "Stress Is Measurable. Test It.",
        "100+ biomarkers in one blood draw. Cortisol, DHEA, thyroid, inflammation markers. Results in ~10 days. $199/year."
    ),
    "cortisol-test-at-home": (
        "Lab Visits Spike Cortisol. Test at Home.",
        "100+ biomarkers. Licensed phlebotomist. Accurate cortisol without lab anxiety. Results in ~10 days. $199/year."
    ),
    "crp-test": (
        "Inflammation Is the Silent Killer.",
        "100+ biomarkers in one blood draw. hsCRP, ESR, metabolic and cardiovascular panel. Results in ~10 days. $199/year."
    ),
    "dhea-test": (
        "DHEA Declines 2% Every Year After 30.",
        "100+ biomarkers in one blood draw. DHEA-S, cortisol, testosterone, thyroid. Results in ~10 days. $199/year."
    ),
    "diabetes-test": (
        "88 Million Have Prediabetes. 84% Don't Know.",
        "100+ biomarkers in one blood draw. A1C, fasting glucose, insulin, metabolic panel. Results in ~10 days. $199/year."
    ),
    "disease-screening": (
        "Most Disease Is Silent for Years.",
        "100+ biomarkers in one blood draw. Screen for 40+ conditions in one test. Results in ~10 days. $199/year."
    ),
    "epigenetic-test": (
        "Your Lifestyle Changes Your Genes.",
        "100+ biomarkers in one blood draw. Epigenetic age, inflammation, metabolic health. Results in ~10 days. $199/year."
    ),
    "epigenetics-info": (
        "Genes Load the Gun. Lifestyle Pulls It.",
        "100+ biomarkers in one blood draw. Biological aging markers, inflammation, metabolic health. Results in ~10 days."
    ),
    "fatty-liver-test": (
        "1 in 4 Adults Has Fatty Liver Disease.",
        "100+ biomarkers in one blood draw. ALT, AST, GGT, metabolic panel. Results in ~10 days. $199/year."
    ),
    "ferritin-test": (
        "Your Iron Looks Normal. Is It?",
        "100+ biomarkers in one blood draw. Ferritin, iron panel, CBC, inflammation. Results in ~10 days. $199/year."
    ),
    "folate-test": (
        "Low Folate Affects Everything.",
        "100+ biomarkers in one blood draw. Folate, B12, iron, homocysteine, CBC. Results in ~10 days. $199/year."
    ),
    "gfr-test": (
        "Kidneys Lose 50% Before Symptoms.",
        "100+ biomarkers in one blood draw. eGFR, creatinine, BUN, metabolic panel. Results in ~10 days. $199/year."
    ),
    "glucose-monitoring": (
        "That Meal Spiked You to 180.",
        "100+ biomarkers in one blood draw. Fasting glucose, insulin, HbA1c, metabolic panel. Results in ~10 days. $199/year."
    ),
    "hashimotos": (
        "Your Thyroid May Be Under Attack.",
        "100+ biomarkers in one blood draw. TSH, T3, T4, TPO and thyroglobulin antibodies. Results in ~10 days. $199/year."
    ),
    "health-screening": (
        "What If You Caught It 10 Years Early?",
        "100+ biomarkers in one blood draw. Heart, metabolic, hormones, vitamins, inflammation. Results in ~10 days. $199/year."
    ),
    "health-test-at-home": (
        "Your Annual Physical. But Better.",
        "100+ biomarkers in one blood draw. Licensed phlebotomist comes to you. Results in ~10 days. $199/year."
    ),
    "heart-disease-screening": (
        "Half of Heart Attacks Miss Standard Tests.",
        "100+ biomarkers in one blood draw. ApoB, Lp(a), hsCRP, advanced lipids. Results in ~10 days. $199/year."
    ),
    "heart-test": (
        "Normal Cholesterol. Heart Attack Anyway.",
        "100+ biomarkers in one blood draw. ApoB, Lp(a), hsCRP, complete lipid panel. Results in ~10 days. $199/year."
    ),
    "high-cholesterol": (
        "High Cholesterol Has No Symptoms.",
        "100+ biomarkers in one blood draw. LDL, HDL, ApoB, Lp(a), triglycerides. Results in ~10 days. $199/year."
    ),
    "high-cholesterol-symptoms": (
        "You Can't Feel High Cholesterol.",
        "100+ biomarkers in one blood draw. LDL, ApoB, Lp(a), HDL, triglycerides. Results in ~10 days. $199/year."
    ),
    "homocysteine": (
        "The Heart Risk Doctors Don't Test.",
        "100+ biomarkers in one blood draw. Homocysteine, B12, folate, lipid panel. Results in ~10 days. $199/year."
    ),
    "hormone-imbalance": (
        "It's Not Stress. It's Hormones.",
        "100+ biomarkers in one blood draw. Thyroid, cortisol, testosterone, estrogen, DHEA. Results in ~10 days. $199/year."
    ),
    "hormone-panel": (
        "Your Hormones Control Everything.",
        "100+ biomarkers in one blood draw. Thyroid, testosterone, estrogen, cortisol, DHEA. Results in ~10 days. $199/year."
    ),
    "hormone-panel-female": (
        "12 Hormones Matter. Doctors Test 2.",
        "100+ biomarkers in one blood draw. Estrogen, testosterone, thyroid, cortisol, DHEA, insulin. Results in ~10 days."
    ),
    "hyperthyroidism": (
        "Racing Heart? Can't Sit Still?",
        "100+ biomarkers in one blood draw. TSH, Free T3, Free T4, thyroid antibodies. Results in ~10 days. $199/year."
    ),
    "hypothyroidism": (
        "Exhausted and Told Labs Are 'Normal'?",
        "100+ biomarkers in one blood draw. TSH, Free T3, Free T4, thyroid antibodies. Results in ~10 days. $199/year."
    ),
    "inflammation-causes": (
        "3 in 5 Adults Have Hidden Inflammation.",
        "100+ biomarkers in one blood draw. hsCRP, ESR, ANA, metabolic markers. Results in ~10 days. $199/year."
    ),
    "inflammation-symptoms": (
        "You Can't Feel Chronic Inflammation.",
        "100+ biomarkers in one blood draw. hsCRP, ESR, ANA, metabolic panel. Results in ~10 days. $199/year."
    ),
    "inflammation-test": (
        "Inflammation Drives Most Chronic Disease.",
        "100+ biomarkers in one blood draw. hsCRP, ANA, thyroid antibodies, ESR. Results in ~10 days. $199/year."
    ),
    "inflammatory-foods": (
        "Some Foods Trigger Silent Inflammation.",
        "100+ biomarkers in one blood draw. hsCRP, ESR, metabolic panel, liver function. Results in ~10 days. $199/year."
    ),
    "insulin-resistance-test": (
        "Glucose Normal. Insulin 3x Too High.",
        "100+ biomarkers in one blood draw. Fasting insulin, glucose, HbA1c, metabolic panel. Results in ~10 days. $199/year."
    ),
    "iron-test": (
        "Low Iron Hides Behind Normal Labs.",
        "100+ biomarkers in one blood draw. Iron, ferritin, TIBC, CBC, B12. Results in ~10 days. $199/year."
    ),
    "kidney-disease-test": (
        "90% of Kidney Disease Goes Undiagnosed.",
        "100+ biomarkers in one blood draw. eGFR, creatinine, BUN, metabolic panel. Results in ~10 days. $199/year."
    ),
    "kidney-panel": (
        "Your Kidneys Work in Silence.",
        "100+ biomarkers in one blood draw. eGFR, creatinine, BUN, full metabolic panel. Results in ~10 days. $199/year."
    ),
    "ldl-hdl": (
        "The LDL/HDL Ratio Matters Most.",
        "100+ biomarkers in one blood draw. LDL, HDL, ApoB, Lp(a), triglycerides. Results in ~10 days. $199/year."
    ),
    "ldl-levels": (
        "'Normal' LDL May Not Be Safe.",
        "100+ biomarkers in one blood draw. LDL, ApoB, Lp(a), HDL, triglycerides. Results in ~10 days. $199/year."
    ),
    "lipid-panel": (
        "Standard Lipid Panels Miss Half.",
        "100+ biomarkers in one blood draw. LDL, HDL, ApoB, Lp(a), triglycerides. Results in ~10 days. $199/year."
    ),
    "liver-enzymes": (
        "Elevated Liver Enzymes Are Warning Signs.",
        "100+ biomarkers in one blood draw. ALT, AST, ALP, GGT, bilirubin. Results in ~10 days. $199/year."
    ),
    "liver-panel": (
        "Your Liver Processes Everything.",
        "100+ biomarkers in one blood draw. ALT, AST, ALP, GGT, bilirubin, albumin. Results in ~10 days. $199/year."
    ),
    "longevity": (
        "Live Longer. Test Smarter.",
        "100+ biomarkers in one blood draw. Inflammation, metabolic, hormones, vitamins. Results in ~10 days. $199/year."
    ),
    "longevity-peter-attia": (
        "Every Test from Outlive. One Draw.",
        "100+ biomarkers. ApoB, Lp(a), fasting insulin, hsCRP, liver enzymes. Results in ~10 days. $199/year."
    ),
    "lpa-test": (
        "Lp(a) Is Genetic. And Deadly.",
        "100+ biomarkers in one blood draw. Lp(a), ApoB, hsCRP, complete lipid panel. Results in ~10 days. $199/year."
    ),
    "lupus-test": (
        "Lupus Takes 6 Years to Diagnose.",
        "100+ biomarkers in one blood draw. ANA, inflammation markers, CBC, metabolic. Results in ~10 days. $199/year."
    ),
    "lyme-test": (
        "Lyme Hides for Years.",
        "100+ biomarkers in one blood draw. Lyme antibodies, inflammation, CBC, metabolic. Results in ~10 days. $199/year."
    ),
    "magnesium-test": (
        "Cramps, Anxiety, Poor Sleep?",
        "100+ biomarkers in one blood draw. Magnesium, calcium, vitamin D, metabolic panel. Results in ~10 days. $199/year."
    ),
    "metabolic-panel": (
        "Your Metabolism Tells the Whole Story.",
        "100+ biomarkers in one blood draw. Glucose, kidney, liver, electrolytes, and more. Results in ~10 days. $199/year."
    ),
    "metabolic-syndrome": (
        "Belly Fat + High Triglycerides = Trouble.",
        "100+ biomarkers in one blood draw. Glucose, insulin, lipids, inflammation. Results in ~10 days. $199/year."
    ),
    "osteoporosis-test": (
        "DEXA Shows Loss. We Show Why.",
        "100+ biomarkers in one blood draw. Vitamin D, calcium, thyroid, inflammation. Results in ~10 days. $199/year."
    ),
    "pcos-test": (
        "1 in 10 Women Has PCOS. 70% Don't Know.",
        "100+ biomarkers in one blood draw. Testosterone, insulin, DHEA, thyroid. Results in ~10 days. $199/year."
    ),
    "prediabetes-test": (
        "84% of Prediabetics Don't Know It.",
        "100+ biomarkers in one blood draw. HbA1c, fasting glucose, fasting insulin. Results in ~10 days. $199/year."
    ),
    "prolactin-test": (
        "Low Libido? Irregular Periods?",
        "100+ biomarkers in one blood draw. Prolactin, thyroid, testosterone, estrogen. Results in ~10 days. $199/year."
    ),
    "prostate-health": (
        "1 in 8 Men Gets Prostate Cancer.",
        "100+ biomarkers in one blood draw. PSA, testosterone, metabolic panel. Results in ~10 days. $199/year."
    ),
    "psa-test": (
        "Prostate Cancer Has No Early Symptoms.",
        "100+ biomarkers in one blood draw. PSA, testosterone, inflammation markers. Results in ~10 days. $199/year."
    ),
    "semen-analysis": (
        "Male Factor Is Half of Infertility.",
        "Comprehensive semen analysis. Sperm count, motility, morphology. Plus hormone panel if needed. Results in ~10 days."
    ),
    "specialty-tests": (
        "Skip the Specialist Wait.",
        "100+ biomarkers in one blood draw. PSA, celiac, Lyme, uric acid, and more. Results in ~10 days. $199/year."
    ),
    "telomere-test": (
        "Your Telomeres Are Your Biological Clock.",
        "100+ biomarkers in one blood draw. Telomere length, inflammation, metabolic markers. Results in ~10 days. $199/year."
    ),
    "telomeres-info": (
        "Every Cell Division Shortens Telomeres.",
        "100+ biomarkers in one blood draw. Biological aging markers, inflammation, metabolic health. Results in ~10 days."
    ),
    "testosterone-levels": (
        "Low T Isn't Just About Sex Drive.",
        "100+ biomarkers in one blood draw. Total and free testosterone, SHBG, estrogen. Results in ~10 days. $199/year."
    ),
    "testosterone-test": (
        "Total T Misses Half the Picture.",
        "100+ biomarkers in one blood draw. Total T, free T, SHBG, estrogen, DHEA. Results in ~10 days. $199/year."
    ),
    "thyroid-antibodies": (
        "TSH Normal. Still Feel Terrible.",
        "100+ biomarkers in one blood draw. TPO, thyroglobulin antibodies, TSH, T3, T4. Results in ~10 days. $199/year."
    ),
    "thyroid-nodules": (
        "Half of Adults Have Thyroid Nodules.",
        "100+ biomarkers in one blood draw. Complete thyroid panel, antibodies, inflammation. Results in ~10 days. $199/year."
    ),
    "thyroid-panel": (
        "TSH Alone Misses Most Thyroid Issues.",
        "100+ biomarkers in one blood draw. TSH, Free T3, Free T4, TPO, thyroglobulin. Results in ~10 days. $199/year."
    ),
    "thyroid-symptoms": (
        "Thyroid Problems Hide in Plain Sight.",
        "100+ biomarkers in one blood draw. TSH, T3, T4, antibodies, metabolic panel. Results in ~10 days. $199/year."
    ),
    "thyroid-test-at-home": (
        "Test All 7 Thyroid Markers. At Home.",
        "100+ biomarkers. Licensed phlebotomist. TSH, T3, T4, antibodies. Results in ~10 days. $199/year."
    ),
    "triglycerides": (
        "High Triglycerides Come From Carbs.",
        "100+ biomarkers in one blood draw. Triglycerides, lipid panel, insulin, glucose. Results in ~10 days. $199/year."
    ),
    "triglycerides-causes": (
        "Triglycerides Come From Sugar, Not Fat.",
        "100+ biomarkers in one blood draw. Triglycerides, insulin, glucose, liver panel. Results in ~10 days. $199/year."
    ),
    "triglycerides-high": (
        "Triglycerides Over 150? Check Insulin.",
        "100+ biomarkers in one blood draw. Triglycerides, fasting insulin, glucose, lipids. Results in ~10 days. $199/year."
    ),
    "triglycerides-meaning": (
        "Triglycerides Reveal Metabolic Health.",
        "100+ biomarkers in one blood draw. Triglycerides, HDL ratio, insulin, glucose. Results in ~10 days. $199/year."
    ),
    "tsh-test": (
        "TSH Alone Misses 60% of Thyroid Issues.",
        "100+ biomarkers in one blood draw. TSH, Free T3, Free T4, thyroid antibodies. Results in ~10 days. $199/year."
    ),
    "uric-acid-test": (
        "That Joint Pain Might Be Gout.",
        "100+ biomarkers in one blood draw. Uric acid, kidney function, inflammation. Results in ~10 days. $199/year."
    ),
    "vitamin-d-deficiency": (
        "42% of Americans Are Vitamin D Deficient.",
        "100+ biomarkers in one blood draw. Vitamin D, calcium, PTH, metabolic panel. Results in ~10 days. $199/year."
    ),
    "vitamin-d-info": (
        "Vitamin D Affects Almost Everything.",
        "100+ biomarkers in one blood draw. Vitamin D, calcium, immune markers, hormones. Results in ~10 days. $199/year."
    ),
    "vitamin-d-sun": (
        "You Probably Don't Get Enough Sun.",
        "100+ biomarkers in one blood draw. Vitamin D, calcium, metabolic panel. Results in ~10 days. $199/year."
    ),
    "vitamin-d-test": (
        "Supplements Don't Always Fix Deficiency.",
        "100+ biomarkers in one blood draw. Vitamin D, calcium, PTH, metabolic panel. Results in ~10 days. $199/year."
    ),
    "vitamin-panel": (
        "Eating Healthy Doesn't Mean Absorbing It.",
        "100+ biomarkers in one blood draw. Vitamin D, B12, folate, iron, magnesium. Results in ~10 days. $199/year."
    ),
    "wellness-testing": (
        "Feeling Fine? Get the Data to Prove It.",
        "100+ biomarkers in one blood draw. Heart, metabolic, hormones, vitamins, inflammation. Results in ~10 days. $199/year."
    ),

    # Biomarker-test pages (53 pages)
    "addisons-disease-biomarker-test": (
        "Fatigue, Salt Cravings, Dark Skin?",
        "100+ biomarkers in one blood draw. Cortisol, DHEA, electrolytes, metabolic panel. Results in ~10 days. $199/year."
    ),
    "alcoholic-liver-disease-biomarker-test": (
        "Your Liver Keeps Score.",
        "100+ biomarkers in one blood draw. GGT, AST/ALT ratio, liver panel. Results in ~10 days. $199/year."
    ),
    "anemia-of-chronic-disease-biomarker-test": (
        "Iron Supplements Not Working?",
        "100+ biomarkers in one blood draw. Iron, ferritin, CBC, inflammation markers. Results in ~10 days. $199/year."
    ),
    "atherosclerosis-biomarker-test": (
        "Plaque Builds for 20 Years in Silence.",
        "100+ biomarkers in one blood draw. ApoB, Lp(a), hsCRP, lipid panel. Results in ~10 days. $199/year."
    ),
    "bph-biomarker-test": (
        "Up 3 Times a Night to Urinate?",
        "100+ biomarkers in one blood draw. PSA, testosterone, metabolic panel. Results in ~10 days. $199/year."
    ),
    "celiac-disease-biomarker-test": (
        "Bloating and Brain Fog After Eating?",
        "100+ biomarkers in one blood draw. tTG-IgA, iron, B12, vitamin D, folate. Results in ~10 days. $199/year."
    ),
    "cfs-me-biomarker-test": (
        "No CFS Test. But Tests for Mimics.",
        "100+ biomarkers in one blood draw. Thyroid, B12, iron, cortisol, inflammation. Results in ~10 days. $199/year."
    ),
    "cholestasis-biomarker-test": (
        "Itching, Dark Urine, Pale Stools?",
        "100+ biomarkers in one blood draw. ALP, bilirubin, GGT, liver panel. Results in ~10 days. $199/year."
    ),
    "chronic-infection-biomarker-test": (
        "Feeling Off for Months?",
        "100+ biomarkers in one blood draw. CBC, CRP, immune markers, metabolic panel. Results in ~10 days. $199/year."
    ),
    "chronic-kidney-disease-biomarker-test": (
        "37M Americans Have CKD. 90% Don't Know.",
        "100+ biomarkers in one blood draw. eGFR, creatinine, BUN, metabolic panel. Results in ~10 days. $199/year."
    ),
    "chronic-stress-biomarker-test": (
        "Stress Changes Your Blood Work.",
        "100+ biomarkers in one blood draw. Cortisol, DHEA, thyroid, inflammation. Results in ~10 days. $199/year."
    ),
    "cirrhosis-biomarker-test": (
        "Your Liver Scars Without Symptoms.",
        "100+ biomarkers in one blood draw. Albumin, liver enzymes, platelets. Results in ~10 days. $199/year."
    ),
    "coronary-artery-disease-biomarker-test": (
        "#1 Cause of Death. Catchable Early.",
        "100+ biomarkers in one blood draw. ApoB, Lp(a), hsCRP, lipid panel. Results in ~10 days. $199/year."
    ),
    "cushings-syndrome-biomarker-test": (
        "Weight Gain, Moon Face, Bruising?",
        "100+ biomarkers in one blood draw. Cortisol, DHEA, metabolic panel, glucose. Results in ~10 days. $199/year."
    ),
    "depression-biomarker-test": (
        "Depression Isn't Always In Your Head.",
        "100+ biomarkers in one blood draw. Thyroid, B12, vitamin D, hormones, iron. Results in ~10 days. $199/year."
    ),
    "diabetes-mellitus-type-2-biomarker-test": (
        "1 in 5 Diabetics Don't Know It.",
        "100+ biomarkers in one blood draw. A1C, glucose, insulin, kidney function. Results in ~10 days. $199/year."
    ),
    "dyslipidemia-biomarker-test": (
        "LDL Normal. ApoB Says Otherwise.",
        "100+ biomarkers in one blood draw. ApoB, Lp(a), lipid panel, inflammation. Results in ~10 days. $199/year."
    ),
    "female-hypogonadism-biomarker-test": (
        "It's Not 'Just Stress.'",
        "100+ biomarkers in one blood draw. Estradiol, FSH, testosterone, thyroid, cortisol. Results in ~10 days. $199/year."
    ),
    "female-infertility-biomarker-test": (
        "Blood Work Is the Essential First Step.",
        "100+ biomarkers in one blood draw. FSH, LH, estradiol, AMH, thyroid, prolactin. Results in ~10 days. $199/year."
    ),
    "folate-deficiency-biomarker-test": (
        "Low Energy, Mood Swings, Mouth Sores?",
        "100+ biomarkers in one blood draw. Folate, B12, homocysteine, CBC. Results in ~10 days. $199/year."
    ),
    "gout-biomarker-test": (
        "That Joint Pain Has an Answer.",
        "100+ biomarkers in one blood draw. Uric acid, kidney function, inflammation. Results in ~10 days. $199/year."
    ),
    "graves-disease-biomarker-test": (
        "Heart Racing, Losing Weight, Shaking?",
        "100+ biomarkers in one blood draw. TSH, T3, T4, thyroid antibodies. Results in ~10 days. $199/year."
    ),
    "hashimotos-biomarker-test": (
        "TSH Normal. Antibodies at 500+.",
        "100+ biomarkers in one blood draw. TSH, T3, T4, TPO and thyroglobulin antibodies. Results in ~10 days. $199/year."
    ),
    "heart-failure-biomarker-test": (
        "Heart Failure Starts With Risk Factors.",
        "100+ biomarkers in one blood draw. Lipids, hsCRP, metabolic panel, kidney function. Results in ~10 days. $199/year."
    ),
    "hepatitis-biomarker-test": (
        "Hepatitis Hides for Decades.",
        "100+ biomarkers in one blood draw. Liver enzymes, bilirubin, albumin. Results in ~10 days. $199/year."
    ),
    "hyperuricemia-biomarker-test": (
        "High Uric Acid Damages Silently.",
        "100+ biomarkers in one blood draw. Uric acid, kidney function, inflammation. Results in ~10 days. $199/year."
    ),
    "hyperprolactinemia-biomarker-test": (
        "Missed Periods? Low Libido?",
        "100+ biomarkers in one blood draw. Prolactin, thyroid, testosterone, estrogen. Results in ~10 days. $199/year."
    ),
    "hypertension-biomarker-test": (
        "High BP Has Root Causes.",
        "100+ biomarkers in one blood draw. Kidney function, thyroid, cortisol, metabolic. Results in ~10 days. $199/year."
    ),
    "hyperthyroidism-biomarker-test": (
        "Heart Pounding, Can't Sit Still?",
        "100+ biomarkers in one blood draw. TSH, Free T3, Free T4, thyroid antibodies. Results in ~10 days. $199/year."
    ),
    "hypothyroidism-biomarker-test": (
        "Doctors Test 1 Thyroid Marker. We Test 7.",
        "100+ biomarkers in one blood draw. TSH, Free T3, Free T4, TPO, thyroglobulin. Results in ~10 days. $199/year."
    ),
    "ibd-biomarker-test": (
        "Cramps and Bloody Stool for Months?",
        "100+ biomarkers in one blood draw. CRP, CBC, iron, B12, inflammation markers. Results in ~10 days. $199/year."
    ),
    "insulin-resistance-biomarker-test": (
        "Glucose Normal. Insulin Way Too High.",
        "100+ biomarkers in one blood draw. Fasting insulin, glucose, HbA1c, lipids. Results in ~10 days. $199/year."
    ),
    "iron-deficiency-anemia-biomarker-test": (
        "Hemoglobin Normal. Ferritin Is 8.",
        "100+ biomarkers in one blood draw. Ferritin, iron, TIBC, CBC, B12. Results in ~10 days. $199/year."
    ),
    "male-hypogonadism-biomarker-test": (
        "Total T Misses Half the Picture.",
        "100+ biomarkers in one blood draw. Total T, free T, SHBG, LH, FSH, estrogen. Results in ~10 days. $199/year."
    ),
    "male-infertility-biomarker-test": (
        "Male Factor Is 50% of Infertility.",
        "100+ biomarkers in one blood draw. Testosterone, FSH, LH, prolactin, thyroid. Results in ~10 days. $199/year."
    ),
    "menopause-biomarker-test": (
        "Is It Menopause or Thyroid?",
        "100+ biomarkers in one blood draw. FSH, estradiol, thyroid panel, cortisol. Results in ~10 days. $199/year."
    ),
    "metabolic-syndrome-biomarker-test": (
        "Belly Fat + High Triglycerides = Danger.",
        "100+ biomarkers in one blood draw. Glucose, insulin, lipids, inflammation. Results in ~10 days. $199/year."
    ),
    "nafld-biomarker-test": (
        "Elevated Liver Enzymes? Pay Attention.",
        "100+ biomarkers in one blood draw. ALT, AST, GGT, metabolic panel, lipids. Results in ~10 days. $199/year."
    ),
    "obesity-biomarker-test": (
        "Weight Shows. Biomarkers Show Impact.",
        "100+ biomarkers in one blood draw. Insulin, glucose, lipids, inflammation, liver. Results in ~10 days. $199/year."
    ),
    "osteomalacia-biomarker-test": (
        "Bone Pain and Muscle Weakness?",
        "100+ biomarkers in one blood draw. Vitamin D, calcium, phosphorus, PTH, ALP. Results in ~10 days. $199/year."
    ),
    "osteoporosis-biomarker-test": (
        "DEXA Shows Loss. Biomarkers Show Why.",
        "100+ biomarkers in one blood draw. Vitamin D, calcium, PTH, thyroid, inflammation. Results in ~10 days. $199/year."
    ),
    "pancreatitis-biomarker-test": (
        "Severe Pain After Eating?",
        "100+ biomarkers in one blood draw. Triglycerides, liver panel, metabolic markers. Results in ~10 days. $199/year."
    ),
    "pcos-biomarker-test": (
        "Blood Work Your Gynecologist Should Order.",
        "100+ biomarkers in one blood draw. Testosterone, insulin, DHEA, thyroid, LH/FSH. Results in ~10 days. $199/year."
    ),
    "peripheral-artery-disease-biomarker-test": (
        "Leg Pain When Walking?",
        "100+ biomarkers in one blood draw. Lipids, ApoB, hsCRP, metabolic panel. Results in ~10 days. $199/year."
    ),
    "prediabetes-biomarker-test": (
        "84% Don't Know They Have Prediabetes.",
        "100+ biomarkers in one blood draw. HbA1c, fasting glucose, fasting insulin. Results in ~10 days. $199/year."
    ),
    "prostate-cancer-biomarker-test": (
        "No Symptoms in Early Stages. PSA Catches It.",
        "100+ biomarkers in one blood draw. PSA, testosterone, inflammation markers. Results in ~10 days. $199/year."
    ),
    "rheumatoid-arthritis-biomarker-test": (
        "Morning Stiffness That Takes Hours?",
        "100+ biomarkers in one blood draw. ANA, CRP, ESR, RF, metabolic panel. Results in ~10 days. $199/year."
    ),
    "sleep-apnea-biomarker-test": (
        "Exhausted, Gaining Weight, BP Rising?",
        "100+ biomarkers in one blood draw. Glucose, insulin, hsCRP, thyroid, lipids. Results in ~10 days. $199/year."
    ),
    "subclinical-hyperthyroidism-biomarker-test": (
        "TSH Low But Doctor Says You're Fine?",
        "100+ biomarkers in one blood draw. TSH, Free T3, Free T4, thyroid antibodies. Results in ~10 days. $199/year."
    ),
    "subclinical-hypothyroidism-biomarker-test": (
        "TSH Borderline. Symptoms Aren't.",
        "100+ biomarkers in one blood draw. TSH, T3, T4, TPO, thyroglobulin antibodies. Results in ~10 days. $199/year."
    ),
    "systemic-lupus-erythematosus-biomarker-test": (
        "Lupus Takes 6 Years to Diagnose.",
        "100+ biomarkers in one blood draw. ANA, dsDNA, complement, CBC, CRP. Results in ~10 days. $199/year."
    ),
    "vitamin-b12-deficiency-biomarker-test": (
        "Tired, Foggy, Forgetful?",
        "100+ biomarkers in one blood draw. B12, MMA, homocysteine, folate, CBC. Results in ~10 days. $199/year."
    ),
    "vitamin-d-deficiency-biomarker-test": (
        "Supplements Alone Don't Fix Deficiency.",
        "100+ biomarkers in one blood draw. Vitamin D, calcium, PTH, metabolic panel. Results in ~10 days. $199/year."
    ),
}

def strip_html(text):
    return re.sub(r'<[^>]+>', '', text or '')

def main():
    # Fetch all items
    print("Fetching all items from Webflow...")
    all_items = []
    offset = 0
    while True:
        url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items?limit=100&offset={offset}"
        resp = requests.get(url, headers=headers)
        data = resp.json()
        items = data.get('items', [])
        if not items:
            break
        all_items.extend(items)
        offset += 100
        if len(items) < 100:
            break

    print(f"Fetched {len(all_items)} items")

    # Build slug -> item mapping
    slug_to_item = {}
    for item in all_items:
        slug = item.get('fieldData', {}).get('slug', '')
        if slug:
            slug_to_item[slug] = item

    # Track updates
    updates = []
    skipped = []
    not_found = []

    for slug, (new_headline, new_subheadline) in REWRITES.items():
        if slug not in slug_to_item:
            not_found.append(slug)
            continue

        item = slug_to_item[slug]
        item_id = item['id']
        current_headline = item.get('fieldData', {}).get('hero-headline', '') or ''
        current_subheadline = strip_html(item.get('fieldData', {}).get('hero-subheadline', '') or '')

        # Check if update needed
        if current_headline == new_headline and current_subheadline.startswith(new_subheadline[:50]):
            skipped.append(slug)
            continue

        # Validate lengths
        if len(new_headline) > 45:
            print(f"WARNING: {slug} headline too long ({len(new_headline)} chars): {new_headline}")
        if len(new_subheadline) > 120:
            print(f"WARNING: {slug} subheadline too long ({len(new_subheadline)} chars)")

        updates.append({
            'slug': slug,
            'item_id': item_id,
            'new_headline': new_headline,
            'new_subheadline': f"<p>{new_subheadline}</p>"
        })

    print(f"\nPages to update: {len(updates)}")
    print(f"Pages already correct: {len(skipped)}")
    print(f"Pages not found: {len(not_found)}")
    if not_found:
        print(f"  Not found: {not_found[:10]}...")

    if not updates:
        print("No updates needed!")
        return

    # Perform updates
    print(f"\nUpdating {len(updates)} pages...")
    success = []
    failed = []

    for i, update in enumerate(updates):
        slug = update['slug']
        item_id = update['item_id']

        patch_url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/{item_id}"
        payload = {
            "fieldData": {
                "hero-headline": update['new_headline'],
                "hero-subheadline": update['new_subheadline']
            }
        }

        resp = requests.patch(patch_url, headers=headers, json=payload)

        if resp.status_code == 200:
            success.append(slug)
            print(f"  [{i+1}/{len(updates)}] Updated: {slug}")
        else:
            failed.append({'slug': slug, 'error': resp.text})
            print(f"  [{i+1}/{len(updates)}] FAILED: {slug} - {resp.status_code}")

        time.sleep(0.3)  # Rate limiting

    print(f"\nUpdated: {len(success)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\nFailed updates:")
        for f in failed:
            print(f"  {f['slug']}: {f['error'][:100]}")

    # Publish all updated items
    if success:
        print(f"\nPublishing {len(success)} items...")

        # Get item IDs for successful updates
        item_ids = [u['item_id'] for u in updates if u['slug'] in success]

        # Publish in batches of 100
        for i in range(0, len(item_ids), 100):
            batch = item_ids[i:i+100]
            publish_url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/publish"
            resp = requests.post(publish_url, headers=headers, json={"itemIds": batch})

            if resp.status_code == 200:
                print(f"  Published batch {i//100 + 1}")
            else:
                print(f"  Failed to publish batch: {resp.text}")

            time.sleep(0.5)

    # Save results
    results = {
        'updated': success,
        'skipped': skipped,
        'failed': failed,
        'not_found': not_found
    }

    with open('/Users/jeffy/superpower-sem-gap/app/data/headline_fix_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to app/data/headline_fix_results.json")

if __name__ == "__main__":
    main()
EOF