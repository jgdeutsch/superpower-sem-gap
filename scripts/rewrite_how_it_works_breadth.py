#!/usr/bin/env python3
"""
Rewrite How It Works copy to emphasize the BREADTH of Superpower testing.
Each test they searched for is just ONE of 100+ biomarkers they get.

Key messaging:
1. Yes, we test [what you searched for]
2. But you ALSO get heart, metabolic, hormones, inflammation, liver, kidney, blood cells
3. $199/year for everything
4. Results in ~10 days
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

# Copy that emphasizes breadth - grouped by test category
# Format: step 1 = their test + breadth, step 2 = pattern/insight, step 3 = action, step 4 = support

BREADTH_COPY = {
    # ===================
    # KIDNEY TESTS
    # ===================
    "bun-test": {
        "how-it-works-1-subheading": "Yes, we test BUN. But you also get ApoB, testosterone, thyroid, inflammation markers, liver enzymes, and 100+ other biomarkers. One draw. $199/year.",
        "how-it-works-2-subheading": "Your BUN tells part of the kidney story. Combined with your cholesterol, hormones, and metabolic markers, we see the full picture of what's driving your health.",
        "how-it-works-3-subheading": "High BUN plus high inflammation? Different plan than high BUN alone. We connect the dots across all 100+ markers to find the real cause.",
        "how-it-works-4-subheading": "Questions about your BUN -or any of your other 100+ results? Our clinical team is here. Results in ~10 days.",
    },
    "gfr-test": {
        "how-it-works-1-subheading": "GFR is included -along with heart markers, hormones, thyroid, inflammation, liver function, and 100+ other biomarkers. One blood draw. $199/year.",
        "how-it-works-2-subheading": "Kidney function doesn't exist in isolation. Your GFR combined with metabolic, inflammatory, and cardiovascular markers reveals what's actually happening.",
        "how-it-works-3-subheading": "Low GFR with normal inflammation? Different approach than low GFR with high hs-CRP. Your plan addresses your specific pattern.",
        "how-it-works-4-subheading": "Get answers about your GFR and all 100+ biomarkers from our clinical team. Results in ~10 days.",
    },
    "kidney-panel": {
        "how-it-works-1-subheading": "Full kidney panel included: BUN, creatinine, eGFR, electrolytes. Plus heart, hormones, thyroid, liver, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Kidney health connects to everything -blood pressure, inflammation, metabolic function. We test it all so you see the complete picture.",
        "how-it-works-3-subheading": "Kidney stress from inflammation looks different than kidney stress from metabolic issues. Your plan targets what's actually driving the numbers.",
        "how-it-works-4-subheading": "Our team explains your kidney results in context of your full health picture. Results in ~10 days.",
    },

    # ===================
    # LIVER TESTS
    # ===================
    "liver-panel": {
        "how-it-works-1-subheading": "Complete liver panel: ALT, AST, bilirubin, albumin, ALP. Plus heart, hormones, kidney, thyroid, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Liver enzymes tell you there's a problem. Your metabolic, inflammatory, and hormonal markers tell you why. We test everything.",
        "how-it-works-3-subheading": "Elevated liver enzymes from fatty liver? Different protocol than medication-induced. Your full panel reveals the cause.",
        "how-it-works-4-subheading": "Understand your liver results alongside your complete health picture. Our team is here. Results in ~10 days.",
    },
    "liver-enzymes": {
        "how-it-works-1-subheading": "ALT, AST, and full liver function included -plus cholesterol, hormones, thyroid, kidney, inflammation, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Elevated enzymes are a signal. Your metabolic markers, inflammation levels, and hormones reveal what's causing them.",
        "how-it-works-3-subheading": "Liver stress with high triglycerides? Different plan than liver stress with normal lipids. We address your specific pattern.",
        "how-it-works-4-subheading": "Get clarity on your liver enzymes and all 100+ results from our clinical team. Results in ~10 days.",
    },
    "uric-acid-test": {
        "how-it-works-1-subheading": "Uric acid included -along with kidney function, metabolic markers, inflammation, hormones, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "High uric acid connects to metabolic health, kidney function, and inflammation. We test all of it to find the root cause.",
        "how-it-works-3-subheading": "Uric acid from diet looks different than uric acid from kidney clearance issues. Your full panel reveals which one.",
        "how-it-works-4-subheading": "Our team explains your uric acid in context of your complete metabolic picture. Results in ~10 days.",
    },

    # ===================
    # CHOLESTEROL/HEART TESTS
    # ===================
    "cholesterol-test": {
        "how-it-works-1-subheading": "Full lipid panel with ApoB -plus hormones, thyroid, inflammation, liver, kidney, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Cholesterol numbers alone miss half the story. Your inflammation, metabolic, and hormonal markers show your true cardiovascular risk.",
        "how-it-works-3-subheading": "High LDL with low inflammation? Different risk than high LDL with high hs-CRP. Your plan matches your actual risk profile.",
        "how-it-works-4-subheading": "Understand your cholesterol alongside your complete health picture. Our team is here. Results in ~10 days.",
    },
    "high-cholesterol": {
        "how-it-works-1-subheading": "Advanced lipid testing with ApoB -plus metabolic markers, hormones, inflammation, thyroid, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "High cholesterol is a symptom. Your thyroid, metabolic, and inflammatory markers reveal what's driving it.",
        "how-it-works-3-subheading": "Cholesterol from thyroid dysfunction? Different approach than dietary cholesterol. We find the actual cause.",
        "how-it-works-4-subheading": "Get the full picture of your cardiovascular health across 100+ markers. Results in ~10 days.",
    },
    "high-cholesterol-symptoms": {
        "how-it-works-1-subheading": "Complete cardiovascular panel: ApoB, LDL, HDL, triglycerides -plus hormones, inflammation, metabolic markers, and 100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Cholesterol doesn't cause symptoms until it's serious. Your inflammatory and metabolic markers catch risk years earlier.",
        "how-it-works-3-subheading": "Silent high cholesterol with high inflammation? Urgent action needed. With normal inflammation? Different timeline. Your plan reflects your risk.",
        "how-it-works-4-subheading": "Our team explains what your results mean for your heart health. Results in ~10 days.",
    },
    "cholesterol-foods": {
        "how-it-works-1-subheading": "See how diet affects your lipids -ApoB, LDL, triglycerides -plus metabolic, inflammatory, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "Diet impacts more than cholesterol. Your glucose, inflammation, and liver markers show the full metabolic picture.",
        "how-it-works-3-subheading": "High triglycerides from sugar? Different fix than high LDL from saturated fat. Your markers guide specific dietary changes.",
        "how-it-works-4-subheading": "Understand how your diet affects all 100+ health markers. Our team is here. Results in ~10 days.",
    },
    "lipid-panel": {
        "how-it-works-1-subheading": "Advanced lipid panel: ApoB, LDL, HDL, triglycerides, ratios -plus hormones, inflammation, thyroid, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Lipids interact with everything -thyroid, hormones, inflammation, liver function. We test it all for the complete cardiovascular picture.",
        "how-it-works-3-subheading": "Lipid dysfunction from hypothyroidism? Different treatment than dietary. Your full panel identifies the driver.",
        "how-it-works-4-subheading": "Get expert interpretation of your lipids alongside all 100+ markers. Results in ~10 days.",
    },
    "ldl-levels": {
        "how-it-works-1-subheading": "LDL plus ApoB (the better predictor) -along with inflammation, metabolic, hormones, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "LDL alone misses context. Combined with ApoB, hs-CRP, and metabolic markers, you see true cardiovascular risk.",
        "how-it-works-3-subheading": "High LDL with optimal ApoB? Less concerning than you think. Your full panel reveals actual risk level.",
        "how-it-works-4-subheading": "Our team puts your LDL in context of your complete health picture. Results in ~10 days.",
    },
    "ldl-hdl": {
        "how-it-works-1-subheading": "LDL/HDL ratio plus ApoB, triglycerides, inflammation markers, hormones, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Ratios matter more than individual numbers. Your metabolic and inflammatory context determines what they mean.",
        "how-it-works-3-subheading": "Poor ratio from low HDL? Different fix than poor ratio from high LDL. Your markers guide the specific intervention.",
        "how-it-works-4-subheading": "Understand your lipid ratios in full context. Our clinical team is here. Results in ~10 days.",
    },
    "triglycerides-high": {
        "how-it-works-1-subheading": "Triglycerides plus glucose, HbA1c, liver enzymes, hormones, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "High triglycerides signal metabolic stress. Your insulin, liver, and inflammatory markers reveal why.",
        "how-it-works-3-subheading": "Triglycerides from insulin resistance? Different approach than triglycerides from alcohol. Your full panel identifies the cause.",
        "how-it-works-4-subheading": "Get clarity on your triglycerides and complete metabolic health. Results in ~10 days.",
    },
    "triglycerides-causes": {
        "how-it-works-1-subheading": "Find the cause: triglycerides plus metabolic markers, liver function, inflammation, hormones, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Triglycerides rise for many reasons -diet, insulin resistance, thyroid, medications. Your full panel reveals which one.",
        "how-it-works-3-subheading": "Cause identified = targeted solution. Generic advice doesn't work. Your specific pattern drives your specific plan.",
        "how-it-works-4-subheading": "Our team connects the dots across all 100+ markers to find your cause. Results in ~10 days.",
    },
    "triglycerides-meaning": {
        "how-it-works-1-subheading": "Understand triglycerides in context -with metabolic, cardiovascular, liver, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "A triglyceride number means nothing alone. Combined with glucose, insulin markers, and inflammation, it tells a story.",
        "how-it-works-3-subheading": "High triglycerides + high glucose = metabolic syndrome risk. High triglycerides + normal glucose = different issue. Context is everything.",
        "how-it-works-4-subheading": "Get expert interpretation of what your numbers actually mean. Results in ~10 days.",
    },
    "apob-test": {
        "how-it-works-1-subheading": "ApoB (the gold standard for heart risk) -plus full lipids, inflammation, hormones, metabolic markers, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "ApoB counts actual atherogenic particles. Combined with hs-CRP and metabolic markers, you see true cardiovascular risk.",
        "how-it-works-3-subheading": "High ApoB with low inflammation? Different risk than high ApoB with high hs-CRP. Your plan matches your specific profile.",
        "how-it-works-4-subheading": "Our team explains your ApoB alongside your complete cardiovascular picture. Results in ~10 days.",
    },
    "lpa-test": {
        "how-it-works-1-subheading": "Lp(a) genetic risk marker -plus ApoB, full lipids, inflammation, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "Lp(a) is inherited and doesn't respond to lifestyle. But your other markers show what you CAN control.",
        "how-it-works-3-subheading": "High Lp(a) means aggressive management of controllable factors -ApoB, inflammation, metabolic health. Your plan prioritizes what moves the needle.",
        "how-it-works-4-subheading": "Understand your genetic risk in context of your full health picture. Results in ~10 days.",
    },
    "heart-test": {
        "how-it-works-1-subheading": "Complete cardiac panel: ApoB, lipids, hs-CRP, homocysteine -plus hormones, metabolic, thyroid, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Heart health depends on lipids, inflammation, metabolic function, and hormones. We test everything that matters.",
        "how-it-works-3-subheading": "Cardiac risk from inflammation looks different than risk from lipids alone. Your full panel reveals your specific risk drivers.",
        "how-it-works-4-subheading": "Get the complete picture of your cardiovascular health across 100+ markers. Results in ~10 days.",
    },
    "homocysteine": {
        "how-it-works-1-subheading": "Homocysteine plus B vitamins, cardiovascular markers, inflammation, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "High homocysteine often signals B vitamin deficiency. Your nutrient panel and inflammatory markers confirm the cause.",
        "how-it-works-3-subheading": "Homocysteine from low B12? Simple fix. From genetic factors? Different approach. Your full panel guides the right intervention.",
        "how-it-works-4-subheading": "Our team connects homocysteine to your complete health picture. Results in ~10 days.",
    },

    # ===================
    # THYROID TESTS
    # ===================
    "thyroid-panel": {
        "how-it-works-1-subheading": "Complete thyroid: TSH, Free T4, Free T3, antibodies -plus hormones, metabolic, cardiovascular, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Thyroid affects energy, weight, mood, cholesterol, and more. We test thyroid alongside everything it impacts.",
        "how-it-works-3-subheading": "Thyroid dysfunction driving your high cholesterol? Your plan addresses the root cause, not just the symptom.",
        "how-it-works-4-subheading": "Understand your thyroid in context of your complete metabolic picture. Results in ~10 days.",
    },
    "tsh-test": {
        "how-it-works-1-subheading": "TSH plus Free T4, Free T3, thyroid antibodies -and cardiovascular, metabolic, hormone, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "TSH alone misses conversion issues and early autoimmunity. Your full thyroid panel plus related markers catches what TSH-only testing misses.",
        "how-it-works-3-subheading": "Normal TSH but still exhausted? Your T3, iron, and adrenal markers may reveal why. We test the full picture.",
        "how-it-works-4-subheading": "Get complete thyroid answers, not just one number. Our team is here. Results in ~10 days.",
    },
    "thyroid-antibodies": {
        "how-it-works-1-subheading": "TPO and thyroglobulin antibodies -plus full thyroid function, inflammation, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "Antibodies appear years before TSH goes abnormal. Combined with inflammatory markers, we catch autoimmune thyroid early.",
        "how-it-works-3-subheading": "Positive antibodies with normal TSH? Time for proactive management. Your inflammation and immune markers guide the approach.",
        "how-it-works-4-subheading": "Understand your autoimmune risk across your complete health picture. Results in ~10 days.",
    },
    "hypothyroidism": {
        "how-it-works-1-subheading": "Full hypothyroid workup: TSH, T4, T3, antibodies -plus cholesterol, metabolic, energy markers, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Hypothyroidism causes weight gain, fatigue, high cholesterol, brain fog. We test thyroid plus everything it affects.",
        "how-it-works-3-subheading": "Hypothyroid symptoms but normal TSH? Your T3, iron, cortisol, and B12 may explain why. We find the answer.",
        "how-it-works-4-subheading": "Get clarity on your thyroid and energy levels. Our team is here. Results in ~10 days.",
    },
    "hyperthyroidism": {
        "how-it-works-1-subheading": "Complete hyperthyroid panel: TSH, T4, T3, antibodies -plus heart markers, metabolic function, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Hyperthyroidism stresses your heart, bones, and metabolism. We test thyroid alongside everything at risk.",
        "how-it-works-3-subheading": "Overactive thyroid affecting your heart rhythm? Your cardiovascular markers show the impact. Your plan protects what matters.",
        "how-it-works-4-subheading": "Understand hyperthyroid effects across your whole body. Results in ~10 days.",
    },
    "thyroid-symptoms": {
        "how-it-works-1-subheading": "Fatigue? Weight changes? We test full thyroid plus hormones, iron, B12, metabolic markers -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Thyroid symptoms overlap with iron deficiency, hormone imbalance, and adrenal issues. We test everything to find the real cause.",
        "how-it-works-3-subheading": "Symptoms from thyroid? From low iron? From cortisol? Your full panel reveals which one -so your plan actually works.",
        "how-it-works-4-subheading": "Stop guessing. Get answers across 100+ markers. Results in ~10 days.",
    },
    "thyroid-nodules": {
        "how-it-works-1-subheading": "Thyroid function panel: TSH, T4, T3, antibodies -plus inflammation, metabolic, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "Nodules need monitoring. Your thyroid function, antibodies, and inflammatory markers track what matters.",
        "how-it-works-3-subheading": "Nodules with autoimmune thyroiditis? Different monitoring than nodules with normal antibodies. Your full panel guides surveillance.",
        "how-it-works-4-subheading": "Stay on top of thyroid health with complete testing. Results in ~10 days.",
    },
    "hashimotos": {
        "how-it-works-1-subheading": "Hashimoto's panel: TPO antibodies, thyroglobulin, full thyroid -plus inflammation, nutrients, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Hashimoto's connects to inflammation, nutrient deficiencies, and gut health. We test beyond just thyroid.",
        "how-it-works-3-subheading": "Flaring antibodies with high inflammation? Different approach than stable antibodies. Your markers guide your specific protocol.",
        "how-it-works-4-subheading": "Manage Hashimoto's with complete health visibility. Results in ~10 days.",
    },

    # ===================
    # HORMONE TESTS
    # ===================
    "hormone-panel": {
        "how-it-works-1-subheading": "Complete hormones: testosterone, DHEA, cortisol, thyroid -plus metabolic, cardiovascular, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Hormones don't exist in isolation. Your metabolic, inflammatory, and nutrient status affects hormone function. We test it all.",
        "how-it-works-3-subheading": "Low testosterone from inflammation? From poor sleep? From metabolic dysfunction? Your full panel finds the root cause.",
        "how-it-works-4-subheading": "Get the complete hormone picture across 100+ markers. Results in ~10 days.",
    },
    "hormone-imbalance": {
        "how-it-works-1-subheading": "Find the imbalance: full hormone panel plus thyroid, metabolic, inflammation, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Hormone symptoms can come from thyroid, adrenals, sex hormones, or metabolic dysfunction. We test everything.",
        "how-it-works-3-subheading": "Fatigue from low testosterone? Low cortisol? Thyroid? Iron? Your full panel identifies which system needs attention.",
        "how-it-works-4-subheading": "Stop guessing which hormone is off. Get answers. Results in ~10 days.",
    },
    "testosterone-test": {
        "how-it-works-1-subheading": "Total and free testosterone plus SHBG, DHEA, thyroid, metabolic markers -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Testosterone depends on sleep, stress, weight, and thyroid function. We test T alongside everything that affects it.",
        "how-it-works-3-subheading": "Low T from high SHBG? Different fix than low T from inflammation. Your full panel reveals the actual driver.",
        "how-it-works-4-subheading": "Understand your testosterone in complete metabolic context. Results in ~10 days.",
    },
    "testosterone-levels": {
        "how-it-works-1-subheading": "Testosterone (total, free, bioavailable) plus hormones, thyroid, metabolic -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "A testosterone number without context is meaningless. Your SHBG, thyroid, and metabolic markers determine what it means for you.",
        "how-it-works-3-subheading": "Optimize testosterone by fixing what's suppressing it -inflammation, poor sleep, metabolic dysfunction. Your markers show where to focus.",
        "how-it-works-4-subheading": "Get actionable testosterone insights, not just a number. Results in ~10 days.",
    },
    "cortisol-test": {
        "how-it-works-1-subheading": "Cortisol plus DHEA, thyroid, blood sugar, inflammation -100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Cortisol affects blood sugar, immune function, sleep, and energy. We test cortisol alongside everything it impacts.",
        "how-it-works-3-subheading": "High cortisol crashing your testosterone? Spiking your glucose? Your full panel shows the downstream effects.",
        "how-it-works-4-subheading": "Understand stress impact across your whole body. Results in ~10 days.",
    },
    "cortisol-high-symptoms": {
        "how-it-works-1-subheading": "Cortisol plus metabolic markers, hormones, inflammation, thyroid -100+ biomarkers reveal stress impact. $199/year.",
        "how-it-works-2-subheading": "Chronic stress damages more than mood. Your glucose, testosterone, thyroid, and inflammation show the toll.",
        "how-it-works-3-subheading": "High cortisol driving weight gain? Killing testosterone? Raising blood sugar? Your markers reveal what to prioritize.",
        "how-it-works-4-subheading": "See the full impact of stress on your health. Results in ~10 days.",
    },
    "adrenal": {
        "how-it-works-1-subheading": "Adrenal markers: cortisol, DHEA -plus thyroid, metabolic, inflammation, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Adrenal fatigue symptoms overlap with thyroid, iron, and hormone issues. We test everything to find the real cause.",
        "how-it-works-3-subheading": "Burnt out adrenals? Or thyroid dysfunction? Or both? Your full panel differentiates -so your recovery plan actually works.",
        "how-it-works-4-subheading": "Get complete answers about your energy and stress response. Results in ~10 days.",
    },
    "dhea-test": {
        "how-it-works-1-subheading": "DHEA-S plus cortisol, testosterone, thyroid, metabolic markers -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "DHEA is the 'mother hormone.' Your other hormones, stress markers, and metabolic health determine how well you use it.",
        "how-it-works-3-subheading": "Low DHEA with high cortisol? Adrenal burnout pattern. Low DHEA with low cortisol? Different story. Context is everything.",
        "how-it-works-4-subheading": "Understand DHEA in your complete hormonal context. Results in ~10 days.",
    },
    "prolactin-test": {
        "how-it-works-1-subheading": "Prolactin plus full hormone panel, thyroid, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "High prolactin can suppress testosterone, affect thyroid, and cause symptoms. We test everything it impacts.",
        "how-it-works-3-subheading": "Elevated prolactin from stress? Medication? Thyroid? Your full panel helps identify the cause.",
        "how-it-works-4-subheading": "Get complete hormone clarity across 100+ markers. Results in ~10 days.",
    },

    # ===================
    # DIABETES/METABOLIC TESTS
    # ===================
    "metabolic-panel": {
        "how-it-works-1-subheading": "Complete metabolic: glucose, HbA1c, lipids, liver, kidney -plus hormones, inflammation, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Metabolic health connects to heart disease, hormone function, energy, and aging. We test the complete picture.",
        "how-it-works-3-subheading": "Prediabetic? Your inflammation, liver, and hormone markers show severity and guide how aggressively to intervene.",
        "how-it-works-4-subheading": "Understand your complete metabolic health. Our team is here. Results in ~10 days.",
    },
    "metabolic-syndrome": {
        "how-it-works-1-subheading": "All 5 metabolic syndrome markers -plus hormones, inflammation, liver function, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Metabolic syndrome accelerates aging and disease. Your inflammatory and hormonal markers show how far it's progressed.",
        "how-it-works-3-subheading": "Catching metabolic syndrome early? Reversible. Catching it late? Manageable. Your markers determine the approach.",
        "how-it-works-4-subheading": "Get ahead of metabolic disease. Complete testing. Results in ~10 days.",
    },
    "diabetes-test": {
        "how-it-works-1-subheading": "Glucose, HbA1c, fasting insulin -plus lipids, inflammation, kidney function, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Diabetes affects everything -heart, kidneys, nerves, eyes. We test glucose alongside all the organs at risk.",
        "how-it-works-3-subheading": "Prediabetic with high inflammation? Aggressive intervention needed. Prediabetic with normal inflammation? Different timeline.",
        "how-it-works-4-subheading": "Understand your diabetes risk across your complete health picture. Results in ~10 days.",
    },
    "a1c-test": {
        "how-it-works-1-subheading": "HbA1c plus fasting glucose, metabolic markers, cardiovascular panel, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "A1c shows 3-month average glucose. Combined with lipids, inflammation, and kidney markers, you see the full metabolic picture.",
        "how-it-works-3-subheading": "Elevated A1c with normal lipids? Different risk than elevated A1c with high triglycerides. Your full panel guides the plan.",
        "how-it-works-4-subheading": "Get complete metabolic clarity, not just one number. Results in ~10 days.",
    },
    "a1c-levels": {
        "how-it-works-1-subheading": "Understand your A1c in context -with lipids, inflammation, kidney, liver, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "An A1c of 5.8% means different things depending on your other markers. Full context determines your actual risk.",
        "how-it-works-3-subheading": "Borderline A1c? Your inflammatory and metabolic markers reveal whether you're trending toward diabetes or away from it.",
        "how-it-works-4-subheading": "Our team puts your A1c in complete context. Results in ~10 days.",
    },
    "glucose-monitoring": {
        "how-it-works-1-subheading": "Fasting glucose and HbA1c -plus metabolic, cardiovascular, hormone, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "Glucose metabolism depends on hormones, stress, liver function, and more. We test glucose alongside everything that affects it.",
        "how-it-works-3-subheading": "High glucose from cortisol? From insulin resistance? From thyroid? Your full panel identifies the driver.",
        "how-it-works-4-subheading": "Understand what's driving your blood sugar. Results in ~10 days.",
    },

    # ===================
    # INFLAMMATION TESTS
    # ===================
    "crp-test": {
        "how-it-works-1-subheading": "hs-CRP plus inflammatory ratios, metabolic markers, cardiovascular panel, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Inflammation connects to heart disease, diabetes, autoimmunity, and aging. We test CRP alongside everything inflammation affects.",
        "how-it-works-3-subheading": "High CRP from metabolic dysfunction? Infection? Autoimmunity? Your full panel helps identify the source.",
        "how-it-works-4-subheading": "Find and address inflammation with complete testing. Results in ~10 days.",
    },
    "inflammation-symptoms": {
        "how-it-works-1-subheading": "Full inflammation panel plus autoimmune markers, metabolic health, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Chronic inflammation causes fatigue, pain, brain fog, and accelerates disease. We test inflammation plus what's driving it.",
        "how-it-works-3-subheading": "Inflammation from diet? Gut issues? Autoimmunity? Metabolic dysfunction? Your markers narrow down the cause.",
        "how-it-works-4-subheading": "Stop living with inflammation. Get answers. Results in ~10 days.",
    },
    "inflammatory-foods": {
        "how-it-works-1-subheading": "See diet's impact: hs-CRP, metabolic markers, lipids, liver -100+ biomarkers reveal what's working. $199/year.",
        "how-it-works-2-subheading": "Food affects inflammation, glucose, lipids, and liver function. We test everything diet influences.",
        "how-it-works-3-subheading": "Inflammation down but triglycerides up? Your markers show exactly which dietary changes are helping and which aren't.",
        "how-it-works-4-subheading": "Make diet changes that actually work. Track with 100+ markers. Results in ~10 days.",
    },
    "autoimmune-test": {
        "how-it-works-1-subheading": "Autoimmune screen: ANA, inflammation markers, thyroid antibodies -plus metabolic and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Autoimmune disease affects the whole body. We test immune markers alongside everything that might be under attack.",
        "how-it-works-3-subheading": "Positive ANA with thyroid antibodies? Different concern than positive ANA alone. Your pattern guides the next steps.",
        "how-it-works-4-subheading": "Get autoimmune answers across your complete health picture. Results in ~10 days.",
    },
    "ana-test": {
        "how-it-works-1-subheading": "ANA screening plus inflammation, thyroid antibodies, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "ANA can be positive for many reasons. Your inflammation, thyroid, and metabolic markers help determine what it means.",
        "how-it-works-3-subheading": "Positive ANA with symptoms? Time for deeper investigation. Positive ANA without symptoms? Different approach. Context matters.",
        "how-it-works-4-subheading": "Understand what your ANA means in full context. Results in ~10 days.",
    },
    "lyme-test": {
        "how-it-works-1-subheading": "Lyme screening plus inflammation, immune markers, and 100+ other biomarkers. $199/year.",
        "how-it-works-2-subheading": "Lyme symptoms overlap with many conditions. Your inflammatory, autoimmune, and metabolic markers help differentiate.",
        "how-it-works-3-subheading": "Chronic fatigue from Lyme? From thyroid? From another cause? Your full panel narrows down the possibilities.",
        "how-it-works-4-subheading": "Get answers about persistent symptoms. Results in ~10 days.",
    },
    "celiac-test": {
        "how-it-works-1-subheading": "Celiac antibodies plus inflammation, nutrient levels, liver, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Celiac causes nutrient deficiencies, inflammation, and liver stress. We test for celiac plus everything it affects.",
        "how-it-works-3-subheading": "Positive celiac markers? Your nutrient panel shows the damage already done and what needs replenishing.",
        "how-it-works-4-subheading": "Complete celiac and nutrient assessment. Results in ~10 days.",
    },
    "celiac-info": {
        "how-it-works-1-subheading": "Celiac screen plus iron, B12, vitamin D, liver function -100+ biomarkers show the full impact. $199/year.",
        "how-it-works-2-subheading": "Undiagnosed celiac causes years of silent damage. We test for celiac plus the nutrient deficiencies it causes.",
        "how-it-works-3-subheading": "Celiac damage shows up in iron, B12, vitamin D, and liver markers long before obvious symptoms. We catch it early.",
        "how-it-works-4-subheading": "Get complete answers about gluten and your health. Results in ~10 days.",
    },

    # ===================
    # VITAMIN/NUTRIENT TESTS
    # ===================
    "vitamin-panel": {
        "how-it-works-1-subheading": "Key vitamins: D, B12, folate, iron -plus hormones, thyroid, metabolic, and 100+ total biomarkers. $199/year.",
        "how-it-works-2-subheading": "Nutrient status affects energy, immunity, hormones, and brain function. We test vitamins alongside everything they impact.",
        "how-it-works-3-subheading": "Low B12 causing your fatigue? Or is it thyroid? Iron? Your full panel identifies the real deficiency.",
        "how-it-works-4-subheading": "Stop guessing which supplements you need. Test and know. Results in ~10 days.",
    },
    "vitamin-d-test": {
        "how-it-works-1-subheading": "Vitamin D plus calcium, thyroid, inflammation, hormones -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Vitamin D affects bones, immunity, mood, and hormones. We test D alongside everything it influences.",
        "how-it-works-3-subheading": "Low D with normal calcium? Different than low D with low calcium. Your full panel guides appropriate supplementation.",
        "how-it-works-4-subheading": "Optimize vitamin D with complete context. Results in ~10 days.",
    },
    "vitamin-d-deficiency": {
        "how-it-works-1-subheading": "Vitamin D plus thyroid, hormones, inflammation, metabolic markers -100+ biomarkers reveal what low D affects. $199/year.",
        "how-it-works-2-subheading": "Vitamin D deficiency contributes to fatigue, depression, weak immunity, and hormone issues. We test everything affected.",
        "how-it-works-3-subheading": "Low D causing your symptoms? Or is it thyroid? Hormones? Your full panel identifies the primary driver.",
        "how-it-works-4-subheading": "Find out what low vitamin D is really doing to you. Results in ~10 days.",
    },
    "vitamin-d-info": {
        "how-it-works-1-subheading": "Complete vitamin D assessment plus related markers: calcium, thyroid, hormones -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Understanding vitamin D requires context. Your thyroid, parathyroid, and inflammatory markers determine what your level means.",
        "how-it-works-3-subheading": "Vitamin D of 28 ng/mL? Could be fine or could be a problem -depends on your other markers. We provide full context.",
        "how-it-works-4-subheading": "Get the complete picture of your vitamin D status. Results in ~10 days.",
    },
    "vitamin-d-sun": {
        "how-it-works-1-subheading": "Check if you're getting enough: vitamin D plus thyroid, hormones, inflammation -100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Sun exposure, skin tone, latitude, and age all affect vitamin D. Your test reveals your actual status regardless of lifestyle.",
        "how-it-works-3-subheading": "Think you get enough sun? Your level might surprise you. Plus see how D connects to your hormones, thyroid, and immunity.",
        "how-it-works-4-subheading": "Stop guessing. Know your vitamin D level and more. Results in ~10 days.",
    },
    "b12-test": {
        "how-it-works-1-subheading": "B12 plus folate, iron, thyroid, metabolic markers -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Low B12 causes fatigue, brain fog, and nerve issues. We test B12 alongside thyroid and iron -the other common causes of these symptoms.",
        "how-it-works-3-subheading": "Fatigue from B12 deficiency? Thyroid? Anemia? Your full panel identifies which one -so supplementation actually works.",
        "how-it-works-4-subheading": "Find the real cause of your low energy. Results in ~10 days.",
    },
    "b12-deficiency": {
        "how-it-works-1-subheading": "B12 status plus folate, iron, thyroid, neurological markers -100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "B12 deficiency mimics thyroid problems, anemia, and neurological conditions. We test everything to confirm the real issue.",
        "how-it-works-3-subheading": "True B12 deficiency needs aggressive treatment. Borderline B12 with normal MCV? Different approach. Your full panel guides the response.",
        "how-it-works-4-subheading": "Get clear answers about your B12 status. Results in ~10 days.",
    },
    "folate-test": {
        "how-it-works-1-subheading": "Folate plus B12, homocysteine, metabolic markers -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Folate works with B12. Deficiency in one masks the other. We test both plus homocysteine to see the complete picture.",
        "how-it-works-3-subheading": "Low folate with high homocysteine? Cardiovascular risk. Low folate with normal homocysteine? Different concern. Context matters.",
        "how-it-works-4-subheading": "Understand your B vitamin status completely. Results in ~10 days.",
    },
    "iron-test": {
        "how-it-works-1-subheading": "Complete iron panel: ferritin, serum iron, TIBC, saturation -plus thyroid, hormones, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Iron affects energy, thyroid function, and hormone production. We test iron alongside everything it impacts.",
        "how-it-works-3-subheading": "Low ferritin causing fatigue? Or low thyroid? Or both? Your full panel identifies all the factors at play.",
        "how-it-works-4-subheading": "Get complete answers about your iron and energy. Results in ~10 days.",
    },
    "ferritin-test": {
        "how-it-works-1-subheading": "Ferritin plus full iron panel, inflammation, thyroid -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Ferritin shows iron stores, but inflammation falsely elevates it. We test ferritin with hs-CRP to get the true picture.",
        "how-it-works-3-subheading": "Normal ferritin with high inflammation? You might still be iron deficient. Your full panel reveals the truth.",
        "how-it-works-4-subheading": "Understand your true iron status. Our team is here. Results in ~10 days.",
    },
    "magnesium-test": {
        "how-it-works-1-subheading": "Magnesium plus metabolic markers, thyroid, hormones -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Magnesium affects heart rhythm, blood pressure, sleep, and stress. We test it alongside cardiovascular and metabolic markers.",
        "how-it-works-3-subheading": "Low magnesium contributing to your high blood pressure? Insomnia? Anxiety? Your full panel connects the dots.",
        "how-it-works-4-subheading": "See how magnesium fits into your complete health picture. Results in ~10 days.",
    },

    # ===================
    # BLOOD TESTS
    # ===================
    "cbc-test": {
        "how-it-works-1-subheading": "Complete CBC with differentials -plus iron, B12, thyroid, metabolic markers, and 100+ biomarkers. $199/year.",
        "how-it-works-2-subheading": "Blood cells reflect bone marrow health, nutrition, and immune function. We test CBC alongside everything that affects it.",
        "how-it-works-3-subheading": "Low hemoglobin from iron deficiency? B12? Chronic disease? Your nutrient and inflammatory markers identify the cause.",
        "how-it-works-4-subheading": "Understand your blood cells in complete context. Results in ~10 days.",
    },
    "blood-test-general": {
        "how-it-works-1-subheading": "100+ biomarkers: heart, metabolic, hormones, thyroid, liver, kidney, blood cells, inflammation -all for $199/year.",
        "how-it-works-2-subheading": "Most doctors test 10-20 markers. We test 100+ in one draw because health problems don't happen in isolation.",
        "how-it-works-3-subheading": "Your heart, hormones, metabolism, and immune system all connect. We test everything so your plan addresses root causes.",
        "how-it-works-4-subheading": "The most comprehensive blood test available. One draw. $199/year. Results in ~10 days.",
    },
    "blood-test-online": {
        "how-it-works-1-subheading": "Order online, draw at 2,000+ labs -100+ biomarkers including heart, hormones, metabolic, and more. $199/year.",
        "how-it-works-2-subheading": "No doctor visit required. Same CLIA-certified labs as hospitals. But we test 5x more markers than your annual physical.",
        "how-it-works-3-subheading": "Online convenience with clinical rigor. 100+ markers in one draw, interpreted by our clinical team, delivered to your dashboard.",
        "how-it-works-4-subheading": "Complete health testing on your schedule. Results in ~10 days.",
    },
    "health-screening": {
        "how-it-works-1-subheading": "Comprehensive screening: 100+ biomarkers covering heart, metabolic, hormones, inflammation, and more. $199/year.",
        "how-it-works-2-subheading": "Annual physicals catch problems late. Our 100+ marker panel catches early warning signs years before symptoms appear.",
        "how-it-works-3-subheading": "63% of our members find something actionable they didn't know about. What will your screening reveal?",
        "how-it-works-4-subheading": "The health screening your doctor should do but doesn't. Results in ~10 days.",
    },

    # ===================
    # LONGEVITY/AGING TESTS
    # ===================
    "longevity": {
        "how-it-works-1-subheading": "Longevity markers: inflammation, metabolic health, hormones, cardiovascular -100+ biomarkers that affect how you age. $199/year.",
        "how-it-works-2-subheading": "Aging isn't just birthday candles. It's inflammation, metabolic dysfunction, and hormone decline. We test everything that matters.",
        "how-it-works-3-subheading": "70% of our members slow their biological age by addressing what their markers reveal. Your results guide your longevity protocol.",
        "how-it-works-4-subheading": "Age smarter. Test everything. Our team is here. Results in ~10 days.",
    },
    "biological-age-test": {
        "how-it-works-1-subheading": "Calculate biological age with 100+ biomarkers: inflammation, metabolic, cardiovascular, hormones, and more. $199/year.",
        "how-it-works-2-subheading": "Biological age reflects how your body is actually aging -not calendar years. Your markers show which systems are aging fastest.",
        "how-it-works-3-subheading": "Older biological age from inflammation? Metabolic dysfunction? Hormone decline? Your specific pattern determines your protocol.",
        "how-it-works-4-subheading": "Know your biological age and how to improve it. Results in ~10 days.",
    },
    "epigenetic-test": {
        "how-it-works-1-subheading": "Epigenetic insights through 100+ biomarkers: inflammation, metabolic, hormones, cardiovascular health. $199/year.",
        "how-it-works-2-subheading": "Your lifestyle choices show up in your biomarkers. We test the measurable effects of sleep, diet, stress, and exercise.",
        "how-it-works-3-subheading": "See how your choices affect your biology. High inflammation from stress? Metabolic issues from diet? Your markers reveal the impact.",
        "how-it-works-4-subheading": "Understand how your lifestyle affects your biology. Results in ~10 days.",
    },
    "epigenetics-info": {
        "how-it-works-1-subheading": "Track lifestyle impact: 100+ biomarkers reveal how diet, sleep, and stress affect your health. $199/year.",
        "how-it-works-2-subheading": "Epigenetics means your genes aren't your destiny. Your choices matter -and your biomarkers prove it.",
        "how-it-works-3-subheading": "Making healthy changes? Your inflammation, metabolic, and hormone markers will show the results. We track what matters.",
        "how-it-works-4-subheading": "See the biological impact of your lifestyle choices. Results in ~10 days.",
    },
    "telomere-test": {
        "how-it-works-1-subheading": "Cellular aging markers plus inflammation, metabolic, cardiovascular -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Telomere length reflects cellular aging. But inflammation, oxidative stress, and metabolic health determine the rate. We test it all.",
        "how-it-works-3-subheading": "Accelerated cellular aging from chronic inflammation? Metabolic stress? Your markers identify what's speeding up the clock.",
        "how-it-works-4-subheading": "Understand cellular aging in complete context. Results in ~10 days.",
    },
    "telomeres-info": {
        "how-it-works-1-subheading": "Understand aging: 100+ biomarkers including inflammation, metabolic, and cardiovascular health. $199/year.",
        "how-it-works-2-subheading": "Telomeres shorten with age, but lifestyle accelerates or slows the process. Your markers show which factors are affecting you.",
        "how-it-works-3-subheading": "Protect your telomeres by addressing what's damaging them -inflammation, oxidative stress, metabolic dysfunction. Your results guide the strategy.",
        "how-it-works-4-subheading": "Get the complete picture of how you're aging. Results in ~10 days.",
    },

    # ===================
    # MEN'S HEALTH
    # ===================
    "psa-test": {
        "how-it-works-1-subheading": "PSA screening plus full hormone panel, inflammation, metabolic markers -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "PSA alone doesn't tell the whole story. Your inflammation, testosterone, and metabolic markers provide essential context.",
        "how-it-works-3-subheading": "Elevated PSA with high inflammation? Different concern than elevated PSA with normal inflammation. Context determines next steps.",
        "how-it-works-4-subheading": "Understand your prostate health in complete context. Results in ~10 days.",
    },
    "prostate-health": {
        "how-it-works-1-subheading": "Prostate markers plus testosterone, inflammation, metabolic health -100+ biomarkers total. $199/year.",
        "how-it-works-2-subheading": "Prostate health connects to hormone balance, inflammation, and metabolic function. We test the complete picture.",
        "how-it-works-3-subheading": "Prostate concerns with low testosterone? High inflammation? Your markers reveal contributing factors and guide the approach.",
        "how-it-works-4-subheading": "Complete men's health testing. Our team is here. Results in ~10 days.",
    },
    "semen-analysis": {
        "how-it-works-1-subheading": "Fertility markers plus hormones, thyroid, metabolic health -100+ biomarkers affect reproductive function. $199/year.",
        "how-it-works-2-subheading": "Male fertility depends on hormone balance, metabolic health, and oxidative stress. We test everything that affects it.",
        "how-it-works-3-subheading": "Low testosterone affecting fertility? Thyroid issues? Inflammation? Your full panel identifies which factors need attention.",
        "how-it-works-4-subheading": "Understand your reproductive health completely. Results in ~10 days.",
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

    print("Rewriting 'How It Works' with BREADTH messaging...\n")

    success_count = 0
    error_count = 0
    skipped_count = 0

    for item in items:
        slug = item.get('fieldData', {}).get('slug', '') or ''
        item_id = item.get('id', '')

        if slug not in BREADTH_COPY:
            print(f"⏭️  {slug}: No copy defined")
            skipped_count += 1
            continue

        copy = BREADTH_COPY[slug]

        updates = {
            "how-it-works-1-subheading": copy["how-it-works-1-subheading"],
            "how-it-works-2-subheading": copy["how-it-works-2-subheading"],
            "how-it-works-3-subheading": copy["how-it-works-3-subheading"],
            "how-it-works-4-subheading": copy["how-it-works-4-subheading"],
        }

        status, result = update_landing_page(item_id, updates)

        if status == 200:
            print(f"✅ {slug}: Rewritten with breadth messaging")
            success_count += 1
        else:
            print(f"❌ {slug}: Error - {result}")
            error_count += 1

        time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"Complete!")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Skipped: {skipped_count}")
    print(f"\nKey messaging in all copy:")
    print("- Their specific test IS included")
    print("- PLUS heart, metabolic, hormones, thyroid, liver, kidney, inflammation")
    print("- 100+ biomarkers total")
    print("- $199/year")
    print("- Results in ~10 days")


if __name__ == '__main__':
    main()
