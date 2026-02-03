#!/usr/bin/env python3
"""
Rewrite "How It Works" section copy in David Ogilvy style.
- Specific, not vague
- Benefits, not features
- Concrete numbers and conditions
- Creates urgency through specificity
- Tells them exactly what they're getting
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

# Ogilvy-style copy for each landing page
# Format: slug -> {how_it_works_1, how_it_works_2, how_it_works_3, how_it_works_4}
OGILVY_COPY = {
    # ============================================
    # BLOOD TESTS
    # ============================================
    "blood-test-general": {
        "how-it-works-1-subheading": "One test screens for diabetes, heart disease, thyroid disorders, anemia, liver disease, kidney dysfunction, and 50+ other conditions—for $199/year.",
        "how-it-works-2-subheading": "Your results show exactly which of your 100+ biomarkers fall outside optimal range—and what that means for your risk of stroke, cancer, and metabolic disease.",
        "how-it-works-3-subheading": "Your physician-reviewed report includes specific supplement dosages, dietary changes, and lifestyle interventions proven to move your numbers.",
        "how-it-works-4-subheading": "Text our clinical team at 2am when you're worried about your cholesterol. They'll explain your results in plain English.",
    },
    "cbc-test": {
        "how-it-works-1-subheading": "Your CBC is part of a 100+ biomarker panel that also screens for thyroid disease, diabetes, heart risk, vitamin deficiencies, and inflammation—all for $199/year.",
        "how-it-works-2-subheading": "See if your white blood cells signal hidden infection, if your red blood cells explain your fatigue, or if your platelets put you at clotting risk.",
        "how-it-works-3-subheading": "If your CBC reveals iron-deficiency anemia, you'll get the exact iron dosage, timing, and vitamin C pairing to fix it in 90 days.",
        "how-it-works-4-subheading": "Confused about what 'low MCV' means? Our clinical team explains it in plain English—available 24/7 by text.",
    },
    "blood-test-online": {
        "how-it-works-1-subheading": "Skip the doctor's office. Screen for heart disease, diabetes, thyroid dysfunction, liver damage, and 50+ conditions—from your couch, for $199/year.",
        "how-it-works-2-subheading": "Your dashboard flags every biomarker outside optimal range, ranks them by urgency, and shows you exactly what each one means for your healthspan.",
        "how-it-works-3-subheading": "High LDL? You'll get the specific statin alternatives, fiber targets, and exercise protocols that lower it without drugs.",
        "how-it-works-4-subheading": "Our physicians review every result. Questions about your numbers? Text us anytime—yes, even Sunday night.",
    },

    # ============================================
    # THYROID
    # ============================================
    "hashimotos": {
        "how-it-works-1-subheading": "We test TPO antibodies, thyroglobulin antibodies, TSH, Free T3, Free T4, and Reverse T3—the full picture most doctors miss. Plus 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "Antibodies elevated but TSH 'normal'? We'll catch the Hashimoto's your doctor missed and show you exactly how aggressive the autoimmune attack is.",
        "how-it-works-3-subheading": "Your plan includes the specific selenium dose, gluten elimination protocol, and stress interventions proven to lower thyroid antibodies.",
        "how-it-works-4-subheading": "Worried your medication isn't working? Text our clinical team your symptoms—they'll help you advocate for proper treatment.",
    },
    "thyroid-symptoms": {
        "how-it-works-1-subheading": "We test all 7 thyroid markers—not just TSH. Plus hormones, vitamins, and inflammation markers that mimic thyroid symptoms. $199/year for everything.",
        "how-it-works-2-subheading": "Finally find out if your fatigue is thyroid, iron deficiency, B12 depletion, or cortisol dysfunction. No more guessing.",
        "how-it-works-3-subheading": "If it's thyroid, you'll get the exact medication conversation to have with your doctor. If it's not, you'll know exactly what it is.",
        "how-it-works-4-subheading": "Doctors dismissing your symptoms? Our team helps you interpret your results and prepare for your next appointment.",
    },
    "hyperthyroidism": {
        "how-it-works-1-subheading": "We test TSH, Free T3, Free T4, and thyroid antibodies to detect Graves' disease and other causes of overactive thyroid—plus 90+ other markers for $199/year.",
        "how-it-works-2-subheading": "See exactly how elevated your thyroid hormones are, whether it's autoimmune, and what that means for your heart and bone health.",
        "how-it-works-3-subheading": "Your report explains treatment options—medication, radioactive iodine, surgery—so you can have an informed conversation with your endocrinologist.",
        "how-it-works-4-subheading": "Heart racing at 3am? Text our team. They'll tell you if it's your thyroid or anxiety—and what to do next.",
    },
    "tsh-test": {
        "how-it-works-1-subheading": "TSH alone misses 60% of thyroid problems. We test Free T3, Free T4, Reverse T3, and antibodies too—plus 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "Your TSH might be 'normal' while your Free T3 is tanked. We show you the full picture that explains why you still feel terrible.",
        "how-it-works-3-subheading": "If your pattern suggests underconversion, you'll get the specific zinc, selenium, and lifestyle changes that improve T4-to-T3 conversion.",
        "how-it-works-4-subheading": "Doctor says your TSH is fine but you feel awful? Our team helps you understand why—and what to ask for next.",
    },
    "thyroid-panel": {
        "how-it-works-1-subheading": "7 thyroid markers: TSH, Free T4, Free T3, Reverse T3, TPO antibodies, thyroglobulin antibodies, and more. Plus 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "We catch Hashimoto's years before your TSH goes abnormal, identify conversion problems, and spot patterns that single-marker tests miss.",
        "how-it-works-3-subheading": "High Reverse T3? You'll get the specific protocol for reducing inflammation and stress that's blocking your active thyroid hormone.",
        "how-it-works-4-subheading": "Bring your results to your next doctor's appointment. Our team helps you prepare the right questions.",
    },
    "hypothyroidism": {
        "how-it-works-1-subheading": "We test TSH, Free T4, Free T3, and thyroid antibodies to catch underactive thyroid and identify Hashimoto's as the cause. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "See exactly how underactive your thyroid is—and whether antibodies explain the weight gain, fatigue, and brain fog you've been dismissing.",
        "how-it-works-3-subheading": "Already on medication but still symptomatic? Your plan shows if you need a dosage change, T3 addition, or lifestyle intervention.",
        "how-it-works-4-subheading": "Struggling to get your doctor to adjust your dose? Our team helps you advocate with evidence.",
    },
    "thyroid-nodules": {
        "how-it-works-1-subheading": "We track thyroid function alongside your nodule monitoring. Plus test for thyroid cancer markers and 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "See if your nodules are affecting hormone production, and catch any changes between your ultrasound appointments.",
        "how-it-works-3-subheading": "Your results help your endocrinologist decide between watchful waiting and intervention—with objective data, not just imaging.",
        "how-it-works-4-subheading": "Anxious about your nodules? Our team explains what your blood work means for your cancer risk.",
    },
    "thyroid-test-at-home": {
        "how-it-works-1-subheading": "Complete thyroid panel shipped to your door: TSH, Free T4, Free T3, Reverse T3, TPO and thyroglobulin antibodies. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "More comprehensive than most endocrinologist panels—without the appointment, the wait, or the co-pay.",
        "how-it-works-3-subheading": "Your results come with specific intervention recommendations, not just a list of numbers and 'normal' ranges.",
        "how-it-works-4-subheading": "Add a licensed phlebotomist to your home for $99 if you prefer a professional draw. Results in 10 days either way.",
    },
    "thyroid-antibodies": {
        "how-it-works-1-subheading": "We test TPO and thyroglobulin antibodies—the markers that reveal autoimmune thyroid disease years before TSH changes. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Antibodies at 500? 50? The number matters. We show you exactly how active the autoimmune attack is and what that means for progression.",
        "how-it-works-3-subheading": "Elevated antibodies get a specific protocol: selenium dosing, gluten elimination, stress reduction—interventions proven to lower them.",
        "how-it-works-4-subheading": "Positive antibodies can feel scary. Our team explains what it means and what you can actually do about it.",
    },

    # ============================================
    # HORMONES - CORTISOL
    # ============================================
    "cortisol-test": {
        "how-it-works-1-subheading": "We test cortisol and DHEA-S to assess your stress response, plus thyroid, sex hormones, and 90+ other markers that explain fatigue and weight gain. $199/year.",
        "how-it-works-2-subheading": "See if your cortisol is spiked (burning out), crashed (burned out), or dysregulated—and how that's affecting your sleep, weight, and energy.",
        "how-it-works-3-subheading": "High cortisol? You'll get specific adaptogen protocols, sleep hygiene interventions, and stress management techniques proven to lower it.",
        "how-it-works-4-subheading": "Wired but tired at midnight? Text our team. They'll explain what your cortisol pattern means and how to fix it.",
    },
    "cortisol-high-symptoms": {
        "how-it-works-1-subheading": "We test cortisol, DHEA-S, fasting insulin, and thyroid—the full picture of why you're gaining belly fat and can't sleep. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Find out if your cortisol is actually high or if insulin resistance, thyroid dysfunction, or sex hormone imbalance explains your symptoms.",
        "how-it-works-3-subheading": "Your plan includes the specific ashwagandha dose, sleep protocol, and carb timing that brings cortisol back to normal.",
        "how-it-works-4-subheading": "Doctor said 'just reduce stress'? Our team gives you the specific, actionable interventions that actually lower cortisol.",
    },
    "cortisol-test-at-home": {
        "how-it-works-1-subheading": "Test your morning cortisol from home—the most important measurement for adrenal function. Plus DHEA-S and 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "See exactly where your stress hormones stand without the stress of a doctor's appointment—which would spike your cortisol anyway.",
        "how-it-works-3-subheading": "Your results come with a specific protocol based on your cortisol/DHEA ratio: adaptogens, lifestyle changes, and supplement timing.",
        "how-it-works-4-subheading": "Add a licensed phlebotomist for $99 if you want a professional draw at home. Results in 10 days.",
    },
    "cortisol-causes": {
        "how-it-works-1-subheading": "We test cortisol alongside sleep markers, thyroid, blood sugar, and inflammation—to identify what's actually driving your cortisol up. $199/year for 100+ markers.",
        "how-it-works-2-subheading": "Is it chronic stress? Sleep deprivation? Blood sugar swings? Hidden inflammation? Your results reveal the root cause.",
        "how-it-works-3-subheading": "Cortisol high from poor sleep? You'll get specific sleep hygiene protocols. From blood sugar? Specific meal timing and macros.",
        "how-it-works-4-subheading": "Our team helps you identify your specific cortisol triggers and build a plan that addresses them.",
    },

    # ============================================
    # HORMONES - TESTOSTERONE
    # ============================================
    "testosterone-test": {
        "how-it-works-1-subheading": "We test total and free testosterone, SHBG, estradiol, and LH—the full picture of male hormonal health. Plus 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "See if your testosterone is truly low or just poorly converted. Know if the problem is production, conversion, or excess estrogen.",
        "how-it-works-3-subheading": "Low T? You'll get the specific interventions to try before TRT: sleep optimization, body composition targets, and micronutrient protocols.",
        "how-it-works-4-subheading": "Considering testosterone therapy? Our team helps you understand if you're a good candidate and what questions to ask.",
    },
    "testosterone-levels": {
        "how-it-works-1-subheading": "We show you where your testosterone falls for your age—not just if it's in the 'normal' range for all men 18-80. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "A 45-year-old with testosterone of 350 isn't 'normal'—it's bottom quartile. We show you where you actually stand.",
        "how-it-works-3-subheading": "Your plan targets the specific lifestyle factors dragging your T down: sleep debt, body fat, zinc deficiency, or overtraining.",
        "how-it-works-4-subheading": "Our team explains what your testosterone level means for energy, muscle, mood, and libido—in plain English.",
    },
    "testosterone-test-at-home": {
        "how-it-works-1-subheading": "Morning testosterone draw from home—the only accurate way to test. Plus free T, SHBG, estradiol, and 90+ other markers for $199/year.",
        "how-it-works-2-subheading": "Lab accuracy without the awkward clinic visit. Collect your sample before 10am when testosterone peaks.",
        "how-it-works-3-subheading": "Your results show not just your levels but your conversion patterns, estrogen balance, and what's actually actionable.",
        "how-it-works-4-subheading": "Add a licensed phlebotomist for $99 if you want a professional draw at home. Results in 10 days.",
    },

    # ============================================
    # HORMONES - GENERAL
    # ============================================
    "hormone-panel": {
        "how-it-works-1-subheading": "We test thyroid, cortisol, DHEA, testosterone, estradiol, and insulin—every hormone that affects energy, weight, and mood. Plus 80+ more markers for $199/year.",
        "how-it-works-2-subheading": "Hormones work as a system. We show you which are out of balance, how they're affecting each other, and what's driving the dysfunction.",
        "how-it-works-3-subheading": "Your plan addresses the root cause: thyroid support, cortisol management, or insulin sensitivity—not just symptom masking.",
        "how-it-works-4-subheading": "Confused about how your hormones interact? Our team explains the cascade and what to prioritize.",
    },
    "hormone-imbalance": {
        "how-it-works-1-subheading": "We test 15+ hormones to identify exactly which are out of balance—thyroid, cortisol, sex hormones, and insulin. Plus 80+ other markers for $199/year.",
        "how-it-works-2-subheading": "Stop guessing. See exactly which hormones are high, low, or dysregulated—and how they explain your fatigue, weight gain, and mood changes.",
        "how-it-works-3-subheading": "Your plan prioritizes interventions: fix cortisol before thyroid, fix insulin before sex hormones—the order matters.",
        "how-it-works-4-subheading": "Our team helps you understand the hierarchy of hormonal health and what to address first.",
    },
    "dhea-test": {
        "how-it-works-1-subheading": "We test DHEA-S alongside cortisol, testosterone, and estradiol—the full adrenal and sex hormone picture. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "See if low DHEA explains your fatigue, low libido, and inability to build muscle—and how it relates to your cortisol status.",
        "how-it-works-3-subheading": "Low DHEA with high cortisol? Different protocol than low DHEA with low cortisol. We tell you exactly what to do.",
        "how-it-works-4-subheading": "Considering DHEA supplementation? Our team explains the right dose based on your actual levels.",
    },
    "prolactin-test": {
        "how-it-works-1-subheading": "We test prolactin alongside thyroid, testosterone, and estradiol—because high prolactin often signals something bigger. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Elevated prolactin tanks testosterone, disrupts cycles, and can signal pituitary issues. We help you understand what your level means.",
        "how-it-works-3-subheading": "Your results include next steps: when to get imaging, when to repeat testing, and what interventions help.",
        "how-it-works-4-subheading": "Worried about what high prolactin means? Our team explains the possibilities and helps you prepare for follow-up.",
    },

    # ============================================
    # HEART & CHOLESTEROL
    # ============================================
    "triglycerides-high": {
        "how-it-works-1-subheading": "We test triglycerides with full lipid panel, ApoB, fasting insulin, and liver enzymes—the complete metabolic picture. Plus 80+ markers for $199/year.",
        "how-it-works-2-subheading": "High triglycerides usually mean insulin resistance. We show you if that's the case—and how bad the metabolic dysfunction is.",
        "how-it-works-3-subheading": "Your plan targets the real cause: sugar and refined carb limits, omega-3 dosing, and the exercise type that actually lowers triglycerides.",
        "how-it-works-4-subheading": "Triglycerides over 500? Our team explains the pancreatitis risk and what to do urgently.",
    },
    "high-cholesterol": {
        "how-it-works-1-subheading": "We test LDL particle count and ApoB—not just LDL-C. These predict heart attacks better than the test your doctor runs. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Your LDL-C might be 'borderline' while your particle count screams danger. We show you your actual cardiovascular risk.",
        "how-it-works-3-subheading": "Your plan includes specific dietary changes that lower LDL 20-30%: fiber targets, saturated fat limits, and plant sterol sources.",
        "how-it-works-4-subheading": "Doctor pushing statins but you want to try lifestyle first? Our team helps you build a 90-day protocol with retest milestones.",
    },
    "cholesterol-test": {
        "how-it-works-1-subheading": "We test LDL, HDL, triglycerides, ApoB, Lp(a), and particle counts—the advanced cardiac panel that predicts heart attacks. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Your doctor's basic lipid panel misses Lp(a)—a genetic risk factor that affects 20% of people and triples heart attack risk.",
        "how-it-works-3-subheading": "High Lp(a)? Your plan focuses on the modifiable risks you can control: aggressive LDL lowering, inflammation reduction, blood pressure.",
        "how-it-works-4-subheading": "Our team explains which of your lipid markers matter most—and which your doctor might be over- or under-emphasizing.",
    },
    "cholesterol-foods": {
        "how-it-works-1-subheading": "We test before and after dietary changes to show you exactly how your body responds. Full lipid panel plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "See if cutting saturated fat actually dropped your LDL, or if you're a 'hyper-responder' who needs a different approach.",
        "how-it-works-3-subheading": "Your plan includes the specific foods proven to lower cholesterol: soluble fiber sources, omega-3 targets, and plant sterol options.",
        "how-it-works-4-subheading": "Tried everything but cholesterol won't budge? Our team helps identify if genetics are the issue and what options remain.",
    },
    "apob-test": {
        "how-it-works-1-subheading": "ApoB counts every particle that causes atherosclerosis—LDL, VLDL, Lp(a), all of them. The single best predictor of heart attack. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Your LDL-C can be 'optimal' while your ApoB is dangerously high. We show you the number that actually matters.",
        "how-it-works-3-subheading": "ApoB over 90? Your plan includes the specific interventions—diet, exercise, and if needed, medication—to get it under 80.",
        "how-it-works-4-subheading": "Cardiologists are moving to ApoB as the primary target. Our team explains why—and what your number means.",
    },
    "lipid-panel": {
        "how-it-works-1-subheading": "Advanced lipid panel: LDL, HDL, triglycerides, ApoB, Lp(a), particle counts, and ratios. The full cardiac picture. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "We test what actually predicts heart attacks—not the outdated markers from 1980s guidelines.",
        "how-it-works-3-subheading": "Your plan targets the specific lipid abnormalities you have: small dense LDL? Different intervention than high triglycerides.",
        "how-it-works-4-subheading": "Confused by all the numbers? Our team ranks your lipid priorities and explains what to address first.",
    },
    "ldl-hdl": {
        "how-it-works-1-subheading": "We test LDL, HDL, their ratios, particle sizes, and ApoB—because the balance matters as much as the individual numbers. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "High LDL with high HDL? Different risk than high LDL with low HDL. We show you what your specific pattern means.",
        "how-it-works-3-subheading": "Your plan includes the specific exercise type that raises HDL (hint: it's not steady-state cardio) and dietary changes that shift the ratio.",
        "how-it-works-4-subheading": "Our team explains the ratio targets that actually predict cardiovascular events—not just arbitrary cutoffs.",
    },
    "homocysteine": {
        "how-it-works-1-subheading": "We test homocysteine with B12, folate, and B6—the vitamins that control it. High homocysteine triples stroke risk. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "See if your homocysteine is elevated and which B vitamin deficiency is causing it. The fix is usually simple.",
        "how-it-works-3-subheading": "Homocysteine over 10? You'll get the specific methylfolate and B12 protocol—including doses for MTHFR variants.",
        "how-it-works-4-subheading": "Have the MTHFR mutation? Our team explains what it means for your homocysteine and what form of folate you need.",
    },
    "heart-test": {
        "how-it-works-1-subheading": "Complete cardiac risk panel: lipids, ApoB, Lp(a), hsCRP, homocysteine, HbA1c, and fasting insulin. Every marker that predicts heart attacks. $199/year.",
        "how-it-works-2-subheading": "We calculate your true 10-year cardiovascular risk using modern markers—not the outdated Framingham score from 1998.",
        "how-it-works-3-subheading": "Your plan prioritizes by impact: which interventions will reduce your specific risk the most, in what order.",
        "how-it-works-4-subheading": "Family history of heart attacks? Our team explains which markers to watch and how aggressive to be.",
    },
    "high-cholesterol-symptoms": {
        "how-it-works-1-subheading": "High cholesterol has no symptoms—that's what makes it dangerous. The only way to know is testing. Full lipid panel plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "By the time you feel chest pain, you already have significant atherosclerosis. We catch the problem decades earlier.",
        "how-it-works-3-subheading": "Your results show exactly how much plaque-building potential is circulating in your blood—and what to do about it.",
        "how-it-works-4-subheading": "Our team explains why waiting for symptoms is the worst possible cholesterol strategy.",
    },
    "triglycerides-meaning": {
        "how-it-works-1-subheading": "Triglycerides are the blood fats that reflect your carb and sugar intake. We test them with insulin and liver markers to show the full metabolic picture. $199/year.",
        "how-it-works-2-subheading": "High triglycerides usually mean insulin resistance is brewing—even if your blood sugar looks fine. We catch it early.",
        "how-it-works-3-subheading": "Your plan shows you exactly how cutting sugar and refined carbs will drop your triglycerides—typically 30-50% in 8 weeks.",
        "how-it-works-4-subheading": "Confused about what triglycerides actually are? Our team explains the science in plain English.",
    },
    "triglycerides-causes": {
        "how-it-works-1-subheading": "We test triglycerides alongside fasting insulin, liver enzymes, and thyroid—to identify what's actually driving them up. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Is it sugar? Alcohol? Undiagnosed diabetes? Fatty liver? Your results reveal the root cause of your elevated triglycerides.",
        "how-it-works-3-subheading": "Your plan targets your specific cause: alcohol-driven gets a different protocol than insulin resistance-driven.",
        "how-it-works-4-subheading": "Triglycerides stubbornly high despite diet changes? Our team helps identify what you might be missing.",
    },
    "ldl-levels": {
        "how-it-works-1-subheading": "We test LDL-C, LDL particle count, and ApoB—because the concentration and number of particles both matter. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "LDL of 130 could mean 1,000 particles or 2,000 particles—very different risks. We tell you which you have.",
        "how-it-works-3-subheading": "Your plan includes the specific dietary changes that lower LDL: soluble fiber grams per day, saturated fat limits, and exercise protocols.",
        "how-it-works-4-subheading": "Should your LDL be under 100? Under 70? Our team explains what target makes sense for your risk profile.",
    },

    # ============================================
    # METABOLIC / DIABETES
    # ============================================
    "metabolic-panel": {
        "how-it-works-1-subheading": "Complete metabolic panel: glucose, insulin, HbA1c, liver enzymes, kidney markers, and electrolytes. We catch diabetes and organ dysfunction early. $199/year.",
        "how-it-works-2-subheading": "Your fasting glucose can be 'normal' while your insulin is 5x higher than optimal—prediabetes hiding in plain sight. We find it.",
        "how-it-works-3-subheading": "Elevated liver enzymes? Your plan includes the specific dietary and lifestyle changes that reverse fatty liver in 90 days.",
        "how-it-works-4-subheading": "Our team explains what each metabolic marker means for your risk of diabetes, fatty liver, and kidney disease.",
    },
    "glucose-monitoring": {
        "how-it-works-1-subheading": "We test fasting glucose, fasting insulin, HbA1c, and calculate HOMA-IR—the complete picture of blood sugar control. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "See if you're insulin resistant, how severe it is, and what that means for your diabetes risk and weight loss ability.",
        "how-it-works-3-subheading": "Your plan includes specific carb targets, meal timing, and exercise protocols proven to restore insulin sensitivity.",
        "how-it-works-4-subheading": "Considering a CGM? Our team helps you understand what your baseline blood work means for that decision.",
    },
    "a1c-test": {
        "how-it-works-1-subheading": "We test HbA1c with fasting glucose and fasting insulin—the three markers that reveal true diabetes risk. Plus 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "A1c of 5.8% means your average blood sugar has been 120 for 3 months. We show you exactly what that means for your organs.",
        "how-it-works-3-subheading": "Prediabetic A1c? Your plan includes the specific diet, exercise, and supplement protocol that reverses it in 90 days.",
        "how-it-works-4-subheading": "Doctor said 'watch your diet'? Our team gives you the specific carb limits and meal strategies that actually lower A1c.",
    },
    "a1c-levels": {
        "how-it-works-1-subheading": "We show you exactly what your A1c means: 5.7% = prediabetes. 6.5% = diabetes. 7.0% = elevated complication risk. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Your A1c reflects 3 months of blood sugar. We track it over time to show if your interventions are actually working.",
        "how-it-works-3-subheading": "A1c of 6.2%? Your plan targets a 0.5% reduction in 90 days through specific dietary and exercise interventions.",
        "how-it-works-4-subheading": "Our team explains the difference between 'diabetic range' and 'optimal'—and what A1c you should actually target.",
    },
    "diabetes-test": {
        "how-it-works-1-subheading": "Complete diabetes screening: fasting glucose, HbA1c, fasting insulin, and HOMA-IR. We catch it 10 years before your doctor would. $199/year.",
        "how-it-works-2-subheading": "37 million Americans have diabetes. 96 million have prediabetes. Most don't know. Your results show exactly where you stand.",
        "how-it-works-3-subheading": "Prediabetic? Your plan includes the specific interventions proven to reverse it: carb limits, meal timing, exercise protocols, and metformin alternatives.",
        "how-it-works-4-subheading": "Family history of diabetes? Our team explains your genetic risk and what you can do to avoid the same fate.",
    },
    "metabolic-syndrome": {
        "how-it-works-1-subheading": "We test all 5 metabolic syndrome markers: waist-driven (you measure), plus glucose, triglycerides, HDL, and blood pressure context. $199/year for 100+ markers.",
        "how-it-works-2-subheading": "3 of 5 abnormal = metabolic syndrome = 5x higher heart attack risk. We tell you exactly how many markers you have.",
        "how-it-works-3-subheading": "Your plan targets the most impactful marker first—usually triglycerides and glucose respond fastest to intervention.",
        "how-it-works-4-subheading": "Metabolic syndrome is reversible. Our team shows you the order of operations to dismantle it marker by marker.",
    },

    # ============================================
    # INFLAMMATION
    # ============================================
    "inflammatory-foods": {
        "how-it-works-1-subheading": "We test hsCRP, ESR, and ferritin—the markers that reveal if your diet is causing chronic inflammation. Plus 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "See if your inflammation is diet-driven, gut-driven, or autoimmune. The treatment is completely different for each.",
        "how-it-works-3-subheading": "Your plan includes the specific elimination protocol to identify your inflammatory triggers—and the anti-inflammatory foods proven to lower CRP.",
        "how-it-works-4-subheading": "Tried 'anti-inflammatory diets' but CRP still high? Our team helps identify what you might be missing.",
    },
    "ana-test": {
        "how-it-works-1-subheading": "We test ANA with pattern and titer, plus inflammatory markers and thyroid antibodies—the full autoimmune screening. Plus 80+ markers for $199/year.",
        "how-it-works-2-subheading": "Positive ANA could mean lupus, Sjögren's, or nothing at all. The pattern and titer tell the story. We explain what yours means.",
        "how-it-works-3-subheading": "Your results include guidance on next steps: when to see rheumatology, what additional tests to request, and what symptoms to watch for.",
        "how-it-works-4-subheading": "Scared about a positive ANA? Our team explains that 15% of healthy people are positive—context matters.",
    },
    "crp-test": {
        "how-it-works-1-subheading": "We test high-sensitivity CRP—the marker that predicts heart attacks independent of cholesterol. Plus 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "CRP over 3 doubles your cardiovascular risk even with perfect cholesterol. We show you where you stand on the inflammation spectrum.",
        "how-it-works-3-subheading": "Your plan includes the specific interventions proven to lower CRP: omega-3 doses, exercise protocols, and weight loss targets.",
        "how-it-works-4-subheading": "CRP spiked since last test? Our team helps identify what changed—infection, stress, diet, or something else.",
    },
    "autoimmune-test": {
        "how-it-works-1-subheading": "Complete autoimmune screening: ANA, thyroid antibodies, rheumatoid factor, CCP antibodies, plus inflammatory markers. $199/year for 100+ markers.",
        "how-it-works-2-subheading": "80+ autoimmune diseases exist. We screen for the most common patterns and help you understand what your antibodies mean.",
        "how-it-works-3-subheading": "Your results include specific next steps based on which antibodies are positive—and which specialists to see.",
        "how-it-works-4-subheading": "Unexplained symptoms for years? Our team helps you connect the dots between your symptoms and your immune markers.",
    },
    "inflammation-symptoms": {
        "how-it-works-1-subheading": "We test hsCRP, ESR, ferritin, and CBC—the markers that prove the inflammation you feel but doctors dismiss. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Finally get objective evidence that something is wrong—numbers that validate your fatigue, pain, and brain fog.",
        "how-it-works-3-subheading": "Your plan addresses the root cause: gut dysfunction, food sensitivities, chronic infection, or autoimmune activation.",
        "how-it-works-4-subheading": "Doctors say your labs are 'normal' but you feel terrible? Our team explains what standard labs miss.",
    },

    # ============================================
    # KIDNEY & LIVER
    # ============================================
    "adrenal": {
        "how-it-works-1-subheading": "We test cortisol, DHEA-S, and their ratio—the markers that reveal adrenal dysfunction. Plus thyroid, sex hormones, and 90+ markers for $199/year.",
        "how-it-works-2-subheading": "See if your adrenals are overproducing (anxiety, insomnia), underproducing (exhaustion, crashes), or dysregulated (both).",
        "how-it-works-3-subheading": "Your plan includes specific adaptogen protocols based on your pattern: different herbs for high cortisol vs. low cortisol.",
        "how-it-works-4-subheading": "Our team explains why 'adrenal fatigue' isn't a real diagnosis—but HPA axis dysfunction absolutely is.",
    },
    "liver-panel": {
        "how-it-works-1-subheading": "Complete liver panel: ALT, AST, ALP, GGT, bilirubin, albumin—the markers that catch fatty liver, hepatitis, and obstruction. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "25% of Americans have fatty liver and don't know it. We catch it before it progresses to cirrhosis.",
        "how-it-works-3-subheading": "Elevated liver enzymes? Your plan includes the specific dietary changes, alcohol limits, and supplements that reverse fatty liver.",
        "how-it-works-4-subheading": "ALT creeping up year over year? Our team explains what's causing it and how aggressively to intervene.",
    },
    "liver-enzymes": {
        "how-it-works-1-subheading": "We test ALT, AST, GGT, and ALP—with ratios that distinguish fatty liver from alcohol damage from obstruction. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "AST/ALT ratio tells us what's causing the damage. GGT elevation pattern tells us if alcohol is involved. We interpret the full picture.",
        "how-it-works-3-subheading": "Your plan targets your specific pattern: weight loss for fatty liver, alcohol reduction for alcohol-related, imaging for obstruction patterns.",
        "how-it-works-4-subheading": "Taking medications that affect liver? Our team monitors for drug-induced elevation and knows when to be concerned.",
    },
    "kidney-panel": {
        "how-it-works-1-subheading": "Complete kidney panel: creatinine, BUN, eGFR, cystatin C, and electrolytes. We catch kidney disease at stage 1—not stage 4. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "37 million Americans have kidney disease. 90% don't know. By the time symptoms appear, you've lost 70% of function. We catch it early.",
        "how-it-works-3-subheading": "GFR declining? Your plan includes blood pressure targets, protein limits, and medication reviews that slow progression.",
        "how-it-works-4-subheading": "Diabetic or hypertensive? Our team explains why annual kidney screening is non-negotiable for you.",
    },
    "gfr-test": {
        "how-it-works-1-subheading": "We calculate eGFR from creatinine and cystatin C—more accurate than creatinine alone, especially if you're muscular. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "GFR of 60 means you've lost 40% of kidney function. GFR of 45 means you're approaching the need for specialist care. We track it precisely.",
        "how-it-works-3-subheading": "Your plan includes the specific interventions that protect remaining kidney function: BP targets, SGLT2 inhibitor candidates, protein guidelines.",
        "how-it-works-4-subheading": "GFR dropped since last year? Our team explains how fast it's declining and what to do about it.",
    },
    "bun-test": {
        "how-it-works-1-subheading": "We test BUN with creatinine, eGFR, and electrolytes—because BUN alone doesn't tell the full kidney story. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "BUN/creatinine ratio distinguishes dehydration from true kidney disease from GI bleeding. We interpret the pattern, not just the number.",
        "how-it-works-3-subheading": "Elevated BUN from dehydration? Your plan includes specific hydration targets. From kidney dysfunction? Different protocol entirely.",
        "how-it-works-4-subheading": "High BUN can mean 5 different things. Our team explains which one applies to you.",
    },

    # ============================================
    # VITAMINS & NUTRIENTS
    # ============================================
    "ferritin-test": {
        "how-it-works-1-subheading": "We test ferritin with complete iron studies and CBC—the full picture of your iron status. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Ferritin of 20 is 'normal' on the lab range but causes fatigue, hair loss, and restless legs. We flag anything under 50.",
        "how-it-works-3-subheading": "Low ferritin? Your plan includes specific iron forms, doses, timing, and vitamin C pairing to raise levels without GI distress.",
        "how-it-works-4-subheading": "Our team explains why your doctor might say your iron is 'fine' when you feel terrible—and what optimal actually looks like.",
    },
    "vitamin-d-test": {
        "how-it-works-1-subheading": "We test 25-hydroxy vitamin D—the true measure of your status. 42% of Americans are deficient. Plus 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "Vitamin D of 20 is 'normal' but suboptimal. We show you where you fall on the spectrum from deficient to optimal to potentially toxic.",
        "how-it-works-3-subheading": "Your plan includes the specific D3 dose for your current level, K2 pairing recommendations, and retest timeline.",
        "how-it-works-4-subheading": "Taking vitamin D but levels won't budge? Our team helps identify absorption issues and dosing problems.",
    },
    "vitamin-panel": {
        "how-it-works-1-subheading": "We test D, B12, folate, iron studies, and magnesium—the deficiencies that cause 80% of unexplained fatigue. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Finally find out if your fatigue is B12, iron, D deficiency—or something else entirely. No more random supplement stacking.",
        "how-it-works-3-subheading": "Your plan includes specific doses based on your actual levels—not generic RDA recommendations.",
        "how-it-works-4-subheading": "Our team explains which deficiencies to prioritize and in what order to address them.",
    },
    "magnesium-test": {
        "how-it-works-1-subheading": "We test serum magnesium—though we'll explain why it's imperfect. Plus 90+ other biomarkers including the electrolytes that interact with magnesium. $199/year.",
        "how-it-works-2-subheading": "Serum magnesium only shows 1% of your body's stores. We interpret it alongside symptoms and other electrolytes for the full picture.",
        "how-it-works-3-subheading": "Symptoms of deficiency with 'normal' serum levels? Your plan includes a therapeutic trial protocol with specific forms and doses.",
        "how-it-works-4-subheading": "Glycinate vs citrate vs threonate? Our team explains which magnesium form matches your symptoms.",
    },
    "b12-test": {
        "how-it-works-1-subheading": "We test B12 with MMA and homocysteine—the functional markers that catch deficiency even when B12 looks normal. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "B12 of 300 is 'normal' but MMA elevated? That's functional deficiency causing neurological damage. We catch what standard tests miss.",
        "how-it-works-3-subheading": "Your plan includes the specific form (methylcobalamin vs cyanocobalamin), dose, and route (oral vs sublingual vs injection) for your situation.",
        "how-it-works-4-subheading": "Vegan, over 60, or on metformin? Our team explains why you're at higher deficiency risk and how often to retest.",
    },
    "b12-deficiency": {
        "how-it-works-1-subheading": "We test B12 with MMA—the marker that catches deficiency before permanent nerve damage. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "B12 deficiency causes irreversible neuropathy if caught late. We catch it early when it's completely fixable.",
        "how-it-works-3-subheading": "Deficiency confirmed? Your plan includes the loading protocol to replete stores quickly, then maintenance dosing.",
        "how-it-works-4-subheading": "Neurological symptoms already present? Our team explains the expected timeline for improvement with treatment.",
    },
    "vitamin-d-deficiency": {
        "how-it-works-1-subheading": "42% of Americans are vitamin D deficient. We test your actual level and show you exactly how deficient you are. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Severe deficiency (under 20) needs different treatment than insufficiency (20-30). We guide the appropriate repletion protocol.",
        "how-it-works-3-subheading": "Your plan includes the specific D3 dose to get you from deficient to optimal in 8-12 weeks, with K2 pairing.",
        "how-it-works-4-subheading": "Dark skin, limited sun, or obesity? Our team explains why you're at higher deficiency risk.",
    },
    "vitamin-d-info": {
        "how-it-works-1-subheading": "Vitamin D affects 1,000+ genes—immunity, mood, bones, and cancer risk. We test your level to optimize all of them. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "See exactly where you fall: severely deficient, deficient, insufficient, optimal, or potentially toxic.",
        "how-it-works-3-subheading": "Your plan includes specific D3 dosing based on your current level and your target—plus K2 and cofactors.",
        "how-it-works-4-subheading": "Our team explains the research on optimal vitamin D levels—and why the 'normal' range is probably too low.",
    },
    "vitamin-d-sun": {
        "how-it-works-1-subheading": "Think you get enough D from sun? We test to find out. Spoiler: most people don't, even in sunny climates. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Your level proves whether your sun exposure is sufficient or if you need supplementation. No more guessing.",
        "how-it-works-3-subheading": "If sun isn't enough, your plan includes specific D3 dosing to close the gap between your level and optimal.",
        "how-it-works-4-subheading": "Sunscreen, darker skin, or northern latitude? Our team explains why sun exposure math doesn't work for you.",
    },
    "folate-test": {
        "how-it-works-1-subheading": "We test serum and RBC folate—because serum can be normal while tissue stores are depleted. Plus B12 and 90+ markers for $199/year.",
        "how-it-works-2-subheading": "RBC folate shows 3 months of tissue status. Serum folate can be misleading. We test both.",
        "how-it-works-3-subheading": "Have MTHFR? Your plan specifies methylfolate vs folic acid and the correct dose for your variant.",
        "how-it-works-4-subheading": "Planning pregnancy? Our team explains why folate optimization pre-conception is critical—and what level you need.",
    },
    "iron-test": {
        "how-it-works-1-subheading": "Complete iron panel: serum iron, ferritin, TIBC, and transferrin saturation. The full picture, not just one number. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Low ferritin with normal hemoglobin? That's iron depletion before anemia—and it's already causing symptoms.",
        "how-it-works-3-subheading": "Your plan includes specific iron form, dose, timing (away from coffee and calcium), and vitamin C pairing for maximum absorption.",
        "how-it-works-4-subheading": "Heavy periods, vegetarian, or endurance athlete? Our team explains your specific depletion risk factors.",
    },

    # ============================================
    # AGING & LONGEVITY
    # ============================================
    "telomeres-info": {
        "how-it-works-1-subheading": "We test the biomarkers that correlate with biological aging: inflammation, metabolic health, insulin, and hormones. 100+ markers for $199/year.",
        "how-it-works-2-subheading": "Telomere length tests have limitations. We test the modifiable markers that actually predict healthspan—and that you can improve.",
        "how-it-works-3-subheading": "Your plan targets the biggest aging accelerators in your results: inflammation, insulin resistance, oxidative stress, or hormonal decline.",
        "how-it-works-4-subheading": "Our team explains which longevity markers matter most—and which are more hype than science.",
    },
    "telomere-test": {
        "how-it-works-1-subheading": "We test 100+ biomarkers that reflect biological aging: metabolic health, inflammation, hormones, and organ function. All for $199/year.",
        "how-it-works-2-subheading": "Your biological age might be 10 years older—or younger—than your calendar age. These markers show you which.",
        "how-it-works-3-subheading": "Your plan targets the specific accelerated aging patterns in your results: metabolic, inflammatory, or hormonal.",
        "how-it-works-4-subheading": "Want to slow aging? Our team explains which interventions have the most evidence—and which are just expensive hope.",
    },
    "biological-age-test": {
        "how-it-works-1-subheading": "We test 100+ biomarkers across every body system—the data that determines if you're aging faster or slower than your years. $199/year.",
        "how-it-works-2-subheading": "Biological age is calculated from metabolic health, inflammation, organ function, and hormones. We show you exactly where you're accelerated.",
        "how-it-works-3-subheading": "Your plan targets the systems aging fastest: if it's metabolic, different intervention than if it's inflammatory or hormonal.",
        "how-it-works-4-subheading": "Our team explains how to interpret biological age—and what realistic improvement looks like with intervention.",
    },
    "epigenetics-info": {
        "how-it-works-1-subheading": "Epigenetic clocks measure DNA methylation patterns. We test the upstream biomarkers that drive those patterns. 100+ markers for $199/year.",
        "how-it-works-2-subheading": "Your blood biomarkers predict epigenetic age—and unlike methylation tests, they show you exactly what to fix.",
        "how-it-works-3-subheading": "Your plan addresses the metabolic, inflammatory, and hormonal factors that accelerate epigenetic aging.",
        "how-it-works-4-subheading": "Our team explains the science of epigenetic aging—what's proven, what's promising, and what's premature.",
    },
    "epigenetic-test": {
        "how-it-works-1-subheading": "We test the biomarkers that drive epigenetic aging: metabolic dysfunction, chronic inflammation, and hormonal decline. 100+ markers for $199/year.",
        "how-it-works-2-subheading": "Your results show which aging pathways are accelerated—and exactly what's modifiable through lifestyle intervention.",
        "how-it-works-3-subheading": "Your plan prioritizes interventions by impact: which changes will slow your specific aging trajectory the most.",
        "how-it-works-4-subheading": "Our team explains how your biomarkers connect to epigenetic age—and what realistic reversal looks like.",
    },
    "longevity": {
        "how-it-works-1-subheading": "We test every biomarker linked to healthspan: metabolic health, cardiovascular risk, inflammation, hormones, and nutrient status. 100+ markers for $199/year.",
        "how-it-works-2-subheading": "Your results reveal which aging pathways are accelerated—insulin resistance, chronic inflammation, or hormonal decline.",
        "how-it-works-3-subheading": "Your plan includes the specific interventions proven to extend healthspan: metabolic optimization, inflammation reduction, and hormonal support.",
        "how-it-works-4-subheading": "Our team separates longevity science from longevity hype—evidence-based interventions only.",
    },

    # ============================================
    # CANCER SCREENING
    # ============================================
    "psa-test": {
        "how-it-works-1-subheading": "We test PSA as part of a comprehensive panel that includes inflammatory markers, metabolic health, and hormones. 100+ markers for $199/year.",
        "how-it-works-2-subheading": "PSA context matters: velocity, density, and free PSA ratio. We help you interpret your number beyond just 'high' or 'low'.",
        "how-it-works-3-subheading": "PSA elevated? Your results include guidance on next steps: when to repeat, when to image, when to biopsy.",
        "how-it-works-4-subheading": "Our team explains PSA nuances—why a rising PSA at 4.0 is more concerning than a stable PSA at 5.0.",
    },
    "prostate-health": {
        "how-it-works-1-subheading": "We test PSA alongside testosterone, estradiol, and inflammatory markers—the full picture of prostate health. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "Track PSA over time to calculate velocity. A number means nothing without context—we provide the context.",
        "how-it-works-3-subheading": "Your results include prostate-specific recommendations: when to consider 5-alpha reductase inhibitors, when to see urology.",
        "how-it-works-4-subheading": "Family history of prostate cancer? Our team explains your screening timeline and what to watch for.",
    },

    # ============================================
    # OTHER HEALTH TESTS
    # ============================================
    "health-screening": {
        "how-it-works-1-subheading": "100+ biomarkers screen for heart disease, diabetes, thyroid dysfunction, liver disease, kidney disease, anemia, vitamin deficiencies, and hormone imbalances. $199/year.",
        "how-it-works-2-subheading": "63% of our members discover health issues they didn't know they had. Most are caught early enough to reverse.",
        "how-it-works-3-subheading": "Your results are prioritized by urgency: what needs attention now, what to watch, and what's optimized.",
        "how-it-works-4-subheading": "Our team reviews every panel. Concerning results get flagged immediately—not buried in a patient portal.",
    },
    "celiac-info": {
        "how-it-works-1-subheading": "We test tTG-IgA and total IgA—the gold standard celiac screening. Plus 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "83% of celiacs are undiagnosed, suffering for years with 'IBS' or 'just sensitive stomach.' We find them.",
        "how-it-works-3-subheading": "Your results include specific next steps: when to biopsy, how to prepare, and what a gluten-free life looks like.",
        "how-it-works-4-subheading": "Already gluten-free? Our team explains why you need to eat gluten before testing—and for how long.",
    },
    "celiac-test": {
        "how-it-works-1-subheading": "We test tTG-IgA with total IgA (to rule out IgA deficiency that causes false negatives). Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "tTG-IgA is 98% sensitive for active celiac disease. A negative test effectively rules it out.",
        "how-it-works-3-subheading": "Positive screening? Your results include guidance on the endoscopy and biopsy process that confirms diagnosis.",
        "how-it-works-4-subheading": "Negative but still symptomatic? Our team explains non-celiac gluten sensitivity and other possibilities.",
    },
    "semen-analysis": {
        "how-it-works-1-subheading": "Complete semen analysis: count, concentration, motility, and morphology—every WHO parameter. Plus hormone testing for $199/year.",
        "how-it-works-2-subheading": "Male factor contributes to 50% of infertility cases. We show you exactly where you stand on each fertility parameter.",
        "how-it-works-3-subheading": "Suboptimal results? Your plan includes the specific interventions proven to improve sperm: heat avoidance, supplements, lifestyle changes.",
        "how-it-works-4-subheading": "Our team explains what each parameter means for your fertility—and what's actually modifiable.",
    },
    "lpa-test": {
        "how-it-works-1-subheading": "Lp(a) is genetic and affects 20% of people. It triples heart attack risk—and most doctors never test it. We do. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "One test tells you your lifetime Lp(a) level—it doesn't change. If it's high, you know to be aggressive about everything else.",
        "how-it-works-3-subheading": "High Lp(a)? Your plan focuses on the modifiable risks: aggressive LDL lowering, inflammation control, and blood pressure optimization.",
        "how-it-works-4-subheading": "Family history of early heart attacks? Our team explains why Lp(a) might be the hidden culprit.",
    },
    "uric-acid-test": {
        "how-it-works-1-subheading": "We test uric acid with kidney function, inflammatory markers, and metabolic panel—the full gout and metabolic picture. Plus 90+ markers for $199/year.",
        "how-it-works-2-subheading": "High uric acid predicts gout, kidney stones, and cardiovascular disease. We catch it before the first painful flare.",
        "how-it-works-3-subheading": "Your plan includes specific dietary changes (it's not just purines), alcohol limits, and hydration targets to lower uric acid naturally.",
        "how-it-works-4-subheading": "Already had a gout attack? Our team explains prevention strategies and when medication makes sense.",
    },
    "lyme-test": {
        "how-it-works-1-subheading": "We test Lyme antibodies (IgM and IgG) alongside inflammatory markers and CBC. Plus 90+ other biomarkers for $199/year.",
        "how-it-works-2-subheading": "Lyme testing is imperfect—false negatives are common early on. We help you interpret results in context of symptoms and exposure.",
        "how-it-works-3-subheading": "Your results include guidance on when to retest, when to treat empirically, and what additional testing might help.",
        "how-it-works-4-subheading": "Tick bite with bull's-eye rash? Our team explains why you should treat immediately—without waiting for test results.",
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
    print("Rewriting all 'How It Works' content in Ogilvy style...\n")

    success_count = 0
    error_count = 0
    skipped_count = 0

    for item in items:
        slug = item.get('fieldData', {}).get('slug', '') or ''
        item_id = item.get('id', '')

        if slug not in OGILVY_COPY:
            print(f"⚠️  No Ogilvy copy for: {slug}")
            skipped_count += 1
            continue

        updates = OGILVY_COPY[slug]

        # Update the landing page
        status, result = update_landing_page(item_id, updates)

        if status == 200:
            print(f"✅ {slug}: Rewritten")
            success_count += 1
        else:
            print(f"❌ {slug}: Error - {result}")
            error_count += 1

        time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"Complete! Success: {success_count}, Errors: {error_count}, Skipped: {skipped_count}")
    print(f"\nAll copy now written in Ogilvy style:")
    print("- Specific conditions and diseases named")
    print("- Concrete numbers and percentages")
    print("- Benefits over features")
    print("- Urgency through specificity")
    print("- Plain English explanations")


if __name__ == '__main__':
    main()
