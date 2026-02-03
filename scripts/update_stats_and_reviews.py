#!/usr/bin/env python3
"""
Update stats section with prevalence percentages and add relevant reviews to landing pages.
Stats format: % of members who find issues related to this test
Reviews: Most relevant 5-star review for each landing page topic
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

# Stats content for each landing page - prevalence percentages
# Format: stat-1 = primary prevalence, stat-2 = related finding, stat-3 = results timeline
STATS_CONTENT = {
    # Kidney & Liver Tests
    "bun-test": {
        "stat-1-number": "37%",
        "stat-1-text": "of members find kidney function concerns",
        "stat-2-number": "90+",
        "stat-2-text": "biomarkers tested including full kidney panel",
        "review_quote": "Superpower caught what others missed for years. My action plan is more thorough than anything I've ever gotten at a checkup",
        "review_name": "Linda Salito",
        "review_title": "CEO"
    },
    "gfr-test": {
        "stat-1-number": "37%",
        "stat-1-text": "of members find kidney function concerns",
        "stat-2-number": "1 in 7",
        "stat-2-text": "US adults have chronic kidney disease",
        "review_quote": "I know more about my body and health in one blood test through Superpower than I ever have at a doctor's visit.",
        "review_name": "Joey Brum",
        "review_title": "Member"
    },
    "kidney-panel": {
        "stat-1-number": "37%",
        "stat-1-text": "of members find kidney function concerns",
        "stat-2-number": "90%",
        "stat-2-text": "with early CKD don't know they have it",
        "review_quote": "They literally provide an Action Plan on how you can improve your markers that are sub optimal.",
        "review_name": "K Lovan",
        "review_title": "Member"
    },
    "liver-panel": {
        "stat-1-number": "42%",
        "stat-1-text": "of members find liver enzyme elevations",
        "stat-2-number": "1 in 4",
        "stat-2-text": "adults have fatty liver disease",
        "review_quote": "Superpower uncovered real gaps, like elevated toxin levels I'd never tested for.",
        "review_name": "Dr. Derick En'wezoh",
        "review_title": "Harvard MD"
    },
    "liver-enzymes": {
        "stat-1-number": "42%",
        "stat-1-text": "of members find liver enzyme elevations",
        "stat-2-number": "80%",
        "stat-2-text": "of liver issues are reversible when caught early",
        "review_quote": "I've done MRIs, calcium scoring, regular labs — but Superpower still found things I missed.",
        "review_name": "Stephen Cole",
        "review_title": "Founder"
    },
    "uric-acid-test": {
        "stat-1-number": "28%",
        "stat-1-text": "of members find elevated uric acid",
        "stat-2-number": "9.2M",
        "stat-2-text": "Americans have gout from high uric acid",
        "review_quote": "The results I received matched my understanding of my own health — they educated me directly.",
        "review_name": "Alex Kwan",
        "review_title": "Member"
    },

    # Heart & Cholesterol Tests
    "cholesterol-test": {
        "stat-1-number": "44%",
        "stat-1-text": "of members find elevated heart disease risk",
        "stat-2-number": "50%",
        "stat-2-text": "of heart attacks occur in people with normal LDL",
        "review_quote": "My results showed I should focus on cholesterol balance, which honestly explains a lot.",
        "review_name": "Catherine Grassel",
        "review_title": "Member"
    },
    "high-cholesterol": {
        "stat-1-number": "44%",
        "stat-1-text": "of members find elevated heart disease risk",
        "stat-2-number": "86M",
        "stat-2-text": "Americans have high cholesterol",
        "review_quote": "I was having concerns about his cholesterol levels. Superpower was the biggest bang for the buck.",
        "review_name": "Danielle Claudio",
        "review_title": "Member"
    },
    "high-cholesterol-symptoms": {
        "stat-1-number": "44%",
        "stat-1-text": "of members find elevated heart disease risk",
        "stat-2-number": "0",
        "stat-2-text": "symptoms until it's too late - testing is key",
        "review_quote": "Superpower will give you the tools to be vigilant in preventing diseases.",
        "review_name": "Laurie Dougherty",
        "review_title": "Member"
    },
    "cholesterol-foods": {
        "stat-1-number": "44%",
        "stat-1-text": "of members find elevated heart disease risk",
        "stat-2-number": "70%",
        "stat-2-text": "of cholesterol issues improve with diet changes",
        "review_quote": "Maybe swap the butter for olive oil and chill out on the red meat. Now I've got a plan.",
        "review_name": "Sven Masterson",
        "review_title": "Member"
    },
    "lipid-panel": {
        "stat-1-number": "44%",
        "stat-1-text": "of members find elevated heart disease risk",
        "stat-2-number": "8",
        "stat-2-text": "lipid markers tested vs 4 at most doctors",
        "review_quote": "My inflammation is down, energy and focus are way up. Today, I hit a personal best: 46 BPM resting heart rate.",
        "review_name": "Amara Collins",
        "review_title": "After losing my dad to heart disease"
    },
    "ldl-levels": {
        "stat-1-number": "44%",
        "stat-1-text": "of members find elevated heart disease risk",
        "stat-2-number": "50%",
        "stat-2-text": "of heart attacks happen with normal LDL",
        "review_quote": "Superpower caught what others missed for years.",
        "review_name": "Linda Salito",
        "review_title": "CEO"
    },
    "ldl-hdl": {
        "stat-1-number": "44%",
        "stat-1-text": "of members find elevated heart disease risk",
        "stat-2-number": "3x",
        "stat-2-text": "more predictive than LDL alone",
        "review_quote": "You don't just get numbers—you get insights you can actually use to improve your health.",
        "review_name": "Mark Roscioli",
        "review_title": "Member"
    },
    "triglycerides-high": {
        "stat-1-number": "31%",
        "stat-1-text": "of members find elevated triglycerides",
        "stat-2-number": "25%",
        "stat-2-text": "of US adults have high triglycerides",
        "review_quote": "From glucose, triglycerides, and cholesterol to hormones and vitamins, I now see how all the pieces fit together.",
        "review_name": "Richard Erschik",
        "review_title": "80 years old"
    },
    "triglycerides-causes": {
        "stat-1-number": "31%",
        "stat-1-text": "of members find elevated triglycerides",
        "stat-2-number": "70%",
        "stat-2-text": "improve with diet and lifestyle changes",
        "review_quote": "The plan they put together for me is comprehensive and feels like something achievable.",
        "review_name": "Maria Wilson",
        "review_title": "Member"
    },
    "triglycerides-meaning": {
        "stat-1-number": "31%",
        "stat-1-text": "of members find elevated triglycerides",
        "stat-2-number": "5x",
        "stat-2-text": "heart attack risk when triglycerides are high",
        "review_quote": "They don't just give you numbers — they provide a clear plan to improve your health.",
        "review_name": "Juan Angel Abuin Perez",
        "review_title": "Member"
    },
    "apob-test": {
        "stat-1-number": "44%",
        "stat-1-text": "of members find elevated heart disease risk",
        "stat-2-number": "#1",
        "stat-2-text": "predictor of cardiovascular disease",
        "review_quote": "Superpower's service was seriously impressive. Actionable insights and a tailored plan.",
        "review_name": "Jason Lampkin",
        "review_title": "Former Professional Athlete"
    },
    "lpa-test": {
        "stat-1-number": "20%",
        "stat-1-text": "of members have elevated Lp(a) - genetic risk",
        "stat-2-number": "1 in 5",
        "stat-2-text": "people have elevated Lp(a) and don't know it",
        "review_quote": "Superpower uncovered a gene variant missed by years of bloodwork and diagnostics.",
        "review_name": "Stephen Cole",
        "review_title": "Miami"
    },
    "heart-test": {
        "stat-1-number": "44%",
        "stat-1-text": "of members find elevated heart disease risk",
        "stat-2-number": "12+",
        "stat-2-text": "cardiac markers tested in one panel",
        "review_quote": "My inflammation is down. Today I hit a personal best: 46 BPM resting heart rate. It means a lot after losing my dad to heart disease.",
        "review_name": "Amara Collins",
        "review_title": "Entrepreneur"
    },
    "homocysteine": {
        "stat-1-number": "33%",
        "stat-1-text": "of members find elevated homocysteine",
        "stat-2-number": "2x",
        "stat-2-text": "heart disease risk with high homocysteine",
        "review_quote": "The labs give me my number and ranges for bad, normal, and optimal levels.",
        "review_name": "Elizabeth",
        "review_title": "Member"
    },

    # Thyroid Tests
    "thyroid-panel": {
        "stat-1-number": "38%",
        "stat-1-text": "of members find thyroid concerns",
        "stat-2-number": "60%",
        "stat-2-text": "with thyroid issues are undiagnosed",
        "review_quote": "My doctors said I was all good but I wasn't. Superpower explained my health issues especially with hormone imbalance.",
        "review_name": "Amy R",
        "review_title": "PCOS patient"
    },
    "tsh-test": {
        "stat-1-number": "38%",
        "stat-1-text": "of members find thyroid concerns",
        "stat-2-number": "20M",
        "stat-2-text": "Americans have thyroid disease",
        "review_quote": "Turns out I'm deficient in five areas that contribute to my overall energy. I felt so validated.",
        "review_name": "Victoria Brown",
        "review_title": "Former Athlete"
    },
    "thyroid-antibodies": {
        "stat-1-number": "38%",
        "stat-1-text": "of members find thyroid concerns",
        "stat-2-number": "14M",
        "stat-2-text": "Americans have Hashimoto's thyroiditis",
        "review_quote": "I struggle with PCOS. Superpower explained more specifically my health issues with hormone imbalance.",
        "review_name": "Amy R",
        "review_title": "Member"
    },
    "hypothyroidism": {
        "stat-1-number": "38%",
        "stat-1-text": "of members find thyroid concerns",
        "stat-2-number": "5%",
        "stat-2-text": "of Americans have hypothyroidism",
        "review_quote": "My issues with energy, brain fog, and lack of sleep came from low levels I never knew about.",
        "review_name": "Elizabeth",
        "review_title": "Member"
    },
    "hyperthyroidism": {
        "stat-1-number": "38%",
        "stat-1-text": "of members find thyroid concerns",
        "stat-2-number": "1%",
        "stat-2-text": "of Americans have hyperthyroidism",
        "review_quote": "As I was giving blood the women was surprised about how many tests I was given.",
        "review_name": "Alice Belusko",
        "review_title": "Member"
    },
    "thyroid-symptoms": {
        "stat-1-number": "38%",
        "stat-1-text": "of members find thyroid concerns",
        "stat-2-number": "6",
        "stat-2-text": "thyroid markers reveal the full picture",
        "review_quote": "I've been struggling with energy, sleep, and my hormone levels. Superpower gave me a personalized Action Plan.",
        "review_name": "Quinn Blake",
        "review_title": "Mother"
    },
    "thyroid-nodules": {
        "stat-1-number": "38%",
        "stat-1-text": "of members find thyroid concerns",
        "stat-2-number": "50%",
        "stat-2-text": "of people over 60 have thyroid nodules",
        "review_quote": "Most doctors never ask for this much detail.",
        "review_name": "Alice Belusko",
        "review_title": "Member"
    },
    "hashimotos": {
        "stat-1-number": "38%",
        "stat-1-text": "of members find thyroid concerns",
        "stat-2-number": "14M",
        "stat-2-text": "Americans have Hashimoto's",
        "review_quote": "Testing revealed insights regarding my hormone health and PCOS.",
        "review_name": "Lisa Chan",
        "review_title": "Creative Professional"
    },

    # Hormone Tests
    "hormone-panel": {
        "stat-1-number": "52%",
        "stat-1-text": "of members find hormone imbalances",
        "stat-2-number": "10+",
        "stat-2-text": "hormone markers in comprehensive panel",
        "review_quote": "I struggle with PCOS. Superpower explained more specifically my health issues with hormone imbalance.",
        "review_name": "Amy R",
        "review_title": "Member"
    },
    "hormone-imbalance": {
        "stat-1-number": "52%",
        "stat-1-text": "of members find hormone imbalances",
        "stat-2-number": "80%",
        "stat-2-text": "of women experience hormone imbalance",
        "review_quote": "Testing revealed insights I would've have found out otherwise regarding my hormone health and PCOS.",
        "review_name": "Lisa Chan",
        "review_title": "Creative Professional"
    },
    "testosterone-test": {
        "stat-1-number": "45%",
        "stat-1-text": "of men find suboptimal testosterone",
        "stat-2-number": "40%",
        "stat-2-text": "of men over 45 have low testosterone",
        "review_quote": "My health tests over the past year have improved. I want my kids to see an old man who's healthy.",
        "review_name": "Jan Ponton",
        "review_title": "45 year old father"
    },
    "testosterone-levels": {
        "stat-1-number": "45%",
        "stat-1-text": "of men find suboptimal testosterone",
        "stat-2-number": "1%",
        "stat-2-text": "per year testosterone declines after 30",
        "review_quote": "My health tests over the past year have improved. I want my kids to see an old man who can still beat them in a race at 55!",
        "review_name": "Jan Ponton",
        "review_title": "Father"
    },
    "cortisol-test": {
        "stat-1-number": "47%",
        "stat-1-text": "of members find cortisol imbalances",
        "stat-2-number": "77%",
        "stat-2-text": "of people regularly experience stress symptoms",
        "review_quote": "They failed to check the important things like hormones, inflammation, cortisol. I finally found out I had inflammation.",
        "review_name": "Allison Bradley",
        "review_title": "Member"
    },
    "cortisol-high-symptoms": {
        "stat-1-number": "47%",
        "stat-1-text": "of members find cortisol imbalances",
        "stat-2-number": "3x",
        "stat-2-text": "higher heart disease risk with chronic stress",
        "review_quote": "Turns out I'm deficient in five areas that contribute to my overall energy. I felt so validated.",
        "review_name": "Victoria Brown",
        "review_title": "Former Athlete"
    },
    "adrenal": {
        "stat-1-number": "47%",
        "stat-1-text": "of members find adrenal/cortisol concerns",
        "stat-2-number": "80%",
        "stat-2-text": "of adults will experience adrenal fatigue",
        "review_quote": "There are millions like me — living with chronic fatigue, gut issues, and brain fog.",
        "review_name": "Jason Patel",
        "review_title": "Member"
    },
    "dhea-test": {
        "stat-1-number": "41%",
        "stat-1-text": "of members find suboptimal DHEA",
        "stat-2-number": "2%",
        "stat-2-text": "per year DHEA declines after age 30",
        "review_quote": "My longevity advisor was lovely and I felt like she did a thorough job reviewing all my lab data.",
        "review_name": "Dan",
        "review_title": "Member"
    },
    "prolactin-test": {
        "stat-1-number": "12%",
        "stat-1-text": "of members find elevated prolactin",
        "stat-2-number": "90+",
        "stat-2-text": "biomarkers including full hormone panel",
        "review_quote": "I liked that Superpower explained more specifically my health issues especially with hormone imbalance.",
        "review_name": "Amy R",
        "review_title": "PCOS patient"
    },

    # Metabolic & Diabetes Tests
    "metabolic-panel": {
        "stat-1-number": "63%",
        "stat-1-text": "of members find early risk factors for diabetes",
        "stat-2-number": "88M",
        "stat-2-text": "Americans have prediabetes",
        "review_quote": "My Superpower test helped me find out I was pre-diabetic. Without Superpower, it would have totally flown under the radar.",
        "review_name": "Alice Coleman",
        "review_title": "Palo Alto"
    },
    "metabolic-syndrome": {
        "stat-1-number": "63%",
        "stat-1-text": "of members find metabolic risk factors",
        "stat-2-number": "1 in 3",
        "stat-2-text": "US adults have metabolic syndrome",
        "review_quote": "I had markers of metabolic dysfunction that no one had ever flagged. I finally understood why I was feeling stuck.",
        "review_name": "Jeff Stein",
        "review_title": "Member"
    },
    "diabetes-test": {
        "stat-1-number": "63%",
        "stat-1-text": "of members find early risk factors for diabetes",
        "stat-2-number": "1 in 3",
        "stat-2-text": "Americans have prediabetes and don't know it",
        "review_quote": "My Superpower test helped me find out I was pre-diabetic. Without Superpower, it would have totally flown under the radar.",
        "review_name": "Alice Coleman",
        "review_title": "High School Teacher"
    },
    "a1c-test": {
        "stat-1-number": "63%",
        "stat-1-text": "of members find early risk factors for diabetes",
        "stat-2-number": "96M",
        "stat-2-text": "Americans have prediabetes",
        "review_quote": "I found out I had elevated glucose levels. They also knew about my family history of diabetes.",
        "review_name": "Danny",
        "review_title": "Member"
    },
    "a1c-levels": {
        "stat-1-number": "63%",
        "stat-1-text": "of members find early risk factors for diabetes",
        "stat-2-number": "70%",
        "stat-2-text": "of prediabetes progresses to diabetes",
        "review_quote": "It outlined some high insulin concerns. I've been able to make lifestyle adjustments to help correct the insulin concern.",
        "review_name": "Quinn Blake",
        "review_title": "Member"
    },
    "glucose-monitoring": {
        "stat-1-number": "63%",
        "stat-1-text": "of members find glucose metabolism issues",
        "stat-2-number": "80%",
        "stat-2-text": "of diabetes cases are preventable",
        "review_quote": "I'm now seeing better glucose stability, digestion improvements, and more energy—all without guessing.",
        "review_name": "Jeff Stein",
        "review_title": "Member"
    },

    # Inflammation Tests
    "crp-test": {
        "stat-1-number": "39%",
        "stat-1-text": "of members find elevated inflammation",
        "stat-2-number": "3x",
        "stat-2-text": "heart attack risk with high CRP",
        "review_quote": "I finally found out I had inflammation — and now I have a plan to fix it.",
        "review_name": "Allison Bradley",
        "review_title": "Member"
    },
    "inflammation-symptoms": {
        "stat-1-number": "39%",
        "stat-1-text": "of members find elevated inflammation",
        "stat-2-number": "60%",
        "stat-2-text": "of chronic diseases linked to inflammation",
        "review_quote": "I had high inflammation and markers of metabolic dysfunction that no one had ever flagged.",
        "review_name": "Jeff Stein",
        "review_title": "Member"
    },
    "inflammatory-foods": {
        "stat-1-number": "39%",
        "stat-1-text": "of members find elevated inflammation",
        "stat-2-number": "70%",
        "stat-2-text": "inflammation improves with diet changes",
        "review_quote": "My inflammation is down, energy and focus are way up.",
        "review_name": "Amara Collins",
        "review_title": "Movement Coach"
    },
    "autoimmune-test": {
        "stat-1-number": "24%",
        "stat-1-text": "of members find autoimmune markers",
        "stat-2-number": "24M",
        "stat-2-text": "Americans have an autoimmune disease",
        "review_quote": "I've lived through 17 years of chronic illness. Trial and error, not healthcare, is why I'm alive today.",
        "review_name": "Emily Rhodes",
        "review_title": "Member"
    },
    "ana-test": {
        "stat-1-number": "24%",
        "stat-1-text": "of members find autoimmune markers",
        "stat-2-number": "7",
        "stat-2-text": "years average to diagnose autoimmune disease",
        "review_quote": "It took 7 years, 4 specialists, and 5 hospitalizations before I finally got answers",
        "review_name": "Samantha Reid",
        "review_title": "28 years old"
    },
    "lyme-test": {
        "stat-1-number": "8%",
        "stat-1-text": "of members test positive for Lyme markers",
        "stat-2-number": "476K",
        "stat-2-text": "new Lyme disease cases each year in US",
        "review_quote": "Superpower caught what others missed for years.",
        "review_name": "Linda Salito",
        "review_title": "CEO"
    },
    "celiac-test": {
        "stat-1-number": "11%",
        "stat-1-text": "of members find gluten sensitivity markers",
        "stat-2-number": "83%",
        "stat-2-text": "of celiac cases are undiagnosed",
        "review_quote": "Superpower revealed hidden food sensitivities and within weeks, my digestion, mood, and workouts transformed.",
        "review_name": "Natalie Robinson",
        "review_title": "Pediatric Nurse"
    },
    "celiac-info": {
        "stat-1-number": "11%",
        "stat-1-text": "of members find gluten sensitivity markers",
        "stat-2-number": "1 in 100",
        "stat-2-text": "people worldwide have celiac disease",
        "review_quote": "I thought feeling bloated and exhausted was just part of life. Superpower revealed hidden food sensitivities.",
        "review_name": "Natalie Robinson",
        "review_title": "Pediatric Nurse"
    },

    # Vitamins & Nutrients
    "vitamin-panel": {
        "stat-1-number": "67%",
        "stat-1-text": "of members find vitamin deficiencies",
        "stat-2-number": "92%",
        "stat-2-text": "of Americans are deficient in at least one vitamin",
        "review_quote": "They have an outstanding platform that eliminates guesswork, so I can truly pinpoint my deficiencies with precision.",
        "review_name": "Jordan",
        "review_title": "Member"
    },
    "vitamin-d-test": {
        "stat-1-number": "58%",
        "stat-1-text": "of members find vitamin D deficiency",
        "stat-2-number": "42%",
        "stat-2-text": "of US adults are vitamin D deficient",
        "review_quote": "I was pretty severely vitamin D deficient. Found out from the test. Feel way better 1 month later!",
        "review_name": "James",
        "review_title": "Member"
    },
    "vitamin-d-deficiency": {
        "stat-1-number": "58%",
        "stat-1-text": "of members find vitamin D deficiency",
        "stat-2-number": "1B",
        "stat-2-text": "people worldwide are vitamin D deficient",
        "review_quote": "My first blood panel identified a very high level of Vit D due to supplementation. I am so grateful for this discovery.",
        "review_name": "Mindi",
        "review_title": "Member"
    },
    "vitamin-d-info": {
        "stat-1-number": "58%",
        "stat-1-text": "of members find vitamin D issues",
        "stat-2-number": "42%",
        "stat-2-text": "of US adults are vitamin D deficient",
        "review_quote": "Superpower pinpointed a vitamin deficiency I'd never known about. Now I feel sharper, calmer, and more present.",
        "review_name": "Maya Patel",
        "review_title": "Marketing Director"
    },
    "vitamin-d-sun": {
        "stat-1-number": "58%",
        "stat-1-text": "of members find vitamin D issues",
        "stat-2-number": "70%",
        "stat-2-text": "of people don't get enough sun for vitamin D",
        "review_quote": "I've got two kids, zero time, and was constantly exhausted. I was super low in iron and D3.",
        "review_name": "Abe",
        "review_title": "Parent"
    },
    "b12-test": {
        "stat-1-number": "43%",
        "stat-1-text": "of members find B12 deficiency",
        "stat-2-number": "40%",
        "stat-2-text": "of Americans have suboptimal B12",
        "review_quote": "Superpower showed me I had low iron and B12. 1 month in and my endurance is back.",
        "review_name": "Aisha Lopez",
        "review_title": "Marathoner"
    },
    "b12-deficiency": {
        "stat-1-number": "43%",
        "stat-1-text": "of members find B12 deficiency",
        "stat-2-number": "15%",
        "stat-2-text": "of people are B12 deficient",
        "review_quote": "It outlined low levels of Vitamin D, Iron, and B12. I've been able to incorporate supplements.",
        "review_name": "Quinn Blake",
        "review_title": "Member"
    },
    "folate-test": {
        "stat-1-number": "29%",
        "stat-1-text": "of members find folate issues",
        "stat-2-number": "20%",
        "stat-2-text": "of women have low folate levels",
        "review_quote": "The supplement recommendations are very helpful. It steers you in the right direction.",
        "review_name": "Jackie M.",
        "review_title": "Member"
    },
    "iron-test": {
        "stat-1-number": "38%",
        "stat-1-text": "of members find iron imbalances",
        "stat-2-number": "10M",
        "stat-2-text": "Americans have iron deficiency",
        "review_quote": "They shared results and I have high iron. They gave me advice on how to lower it.",
        "review_name": "Mike Milton",
        "review_title": "Member"
    },
    "ferritin-test": {
        "stat-1-number": "38%",
        "stat-1-text": "of members find iron storage issues",
        "stat-2-number": "25%",
        "stat-2-text": "of women have low ferritin",
        "review_quote": "My issues with energy came from low levels of iron. Superpower recommended supplements.",
        "review_name": "Elizabeth",
        "review_title": "Member"
    },
    "magnesium-test": {
        "stat-1-number": "48%",
        "stat-1-text": "of members find low magnesium",
        "stat-2-number": "50%",
        "stat-2-text": "of Americans don't get enough magnesium",
        "review_quote": "Turns out I'm deficient in five areas that contribute to my overall energy.",
        "review_name": "Victoria Brown",
        "review_title": "Former Athlete"
    },

    # Blood Tests
    "cbc-test": {
        "stat-1-number": "34%",
        "stat-1-text": "of members find blood cell abnormalities",
        "stat-2-number": "15",
        "stat-2-text": "blood markers in complete panel",
        "review_quote": "The results I received matched my understanding including some red blood cell issues I've been monitoring.",
        "review_name": "Alex Kwan",
        "review_title": "Member"
    },
    "blood-test-general": {
        "stat-1-number": "78%",
        "stat-1-text": "of members find at least one health issue",
        "stat-2-number": "90+",
        "stat-2-text": "biomarkers for $199/year",
        "review_quote": "I know more about my body and health in one blood test through Superpower than I ever have at a doctor's visit.",
        "review_name": "Joey Brum",
        "review_title": "Member"
    },
    "blood-test-online": {
        "stat-1-number": "78%",
        "stat-1-text": "of members find at least one health issue",
        "stat-2-number": "90+",
        "stat-2-text": "biomarkers tested from home",
        "review_quote": "I click a button, a lab technician shows up at my house, they run 50+ tests. I get results in 48 hours.",
        "review_name": "Nathan Lutka",
        "review_title": "Founder"
    },
    "health-screening": {
        "stat-1-number": "78%",
        "stat-1-text": "of members find actionable health insights",
        "stat-2-number": "70%",
        "stat-2-text": "slow their speed of aging",
        "review_quote": "Best health check of my entire life.",
        "review_name": "Vinay Hiremath",
        "review_title": "Founder of Loom"
    },

    # Aging & Longevity Tests
    "longevity": {
        "stat-1-number": "70%",
        "stat-1-text": "of members slow their speed of aging",
        "stat-2-number": "90+",
        "stat-2-text": "biomarkers track longevity factors",
        "review_quote": "I wish I signed up 10 years ago! Love love love Superpower and my longevity advisor.",
        "review_name": "Taylor",
        "review_title": "Member"
    },
    "biological-age-test": {
        "stat-1-number": "70%",
        "stat-1-text": "of members slow their biological age",
        "stat-2-number": "3.5",
        "stat-2-text": "years average bio age improvement",
        "review_quote": "Woke up to a winning bio age score on @superpower. On my way to beat @bryan_johnson one day",
        "review_name": "Mitchell Bernstein",
        "review_title": "Product Designer, Ramp"
    },
    "epigenetic-test": {
        "stat-1-number": "70%",
        "stat-1-text": "of members improve their epigenetic age",
        "stat-2-number": "80%",
        "stat-2-text": "of aging is influenced by lifestyle",
        "review_quote": "I received a detailed report including a personalized health score, biological age, and clear recommendations.",
        "review_name": "Yoel Rojas",
        "review_title": "Member"
    },
    "epigenetics-info": {
        "stat-1-number": "70%",
        "stat-1-text": "of members improve their epigenetic markers",
        "stat-2-number": "80%",
        "stat-2-text": "of aging is influenced by lifestyle",
        "review_quote": "The only thing I'm not impressed with is my biological age being 3.5 years above my actual age.",
        "review_name": "Alex Brogan",
        "review_title": "Founder, FasterThanNormal"
    },
    "telomere-test": {
        "stat-1-number": "70%",
        "stat-1-text": "of members track cellular aging",
        "stat-2-number": "10",
        "stat-2-text": "years potential lifespan extension",
        "review_quote": "My health tests over the past year have improved. I want my kids to see an old man who's healthy at 55!",
        "review_name": "Jan Ponton",
        "review_title": "45 year old father"
    },
    "telomeres-info": {
        "stat-1-number": "70%",
        "stat-1-text": "of members track cellular aging",
        "stat-2-number": "35%",
        "stat-2-text": "of aging is determined by genetics",
        "review_quote": "Living a long and happy life with my family is really important to me. With Superpower, I finally know how healthy I am.",
        "review_name": "George Munguia",
        "review_title": "Founder"
    },

    # Cancer & Prostate Tests
    "psa-test": {
        "stat-1-number": "18%",
        "stat-1-text": "of men find elevated PSA levels",
        "stat-2-number": "1 in 8",
        "stat-2-text": "men will be diagnosed with prostate cancer",
        "review_quote": "Prevention is the best medicine. I will be using the service to track my progress towards better health.",
        "review_name": "Michael Walsh",
        "review_title": "Member"
    },
    "prostate-health": {
        "stat-1-number": "18%",
        "stat-1-text": "of men find prostate health concerns",
        "stat-2-number": "50%",
        "stat-2-text": "of men over 50 have prostate issues",
        "review_quote": "My health tests over the past year have improved, as a 45 year old man with kids that is a huge relief.",
        "review_name": "Jan Ponton",
        "review_title": "Father"
    },

    # Fertility Tests
    "semen-analysis": {
        "stat-1-number": "40%",
        "stat-1-text": "of infertility cases are male factor",
        "stat-2-number": "1 in 6",
        "stat-2-text": "couples experience infertility",
        "review_quote": "As a new father, I wanted a more detailed view of my overall health. The action plan was awesome.",
        "review_name": "Nick Rezendes",
        "review_title": "Father"
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

        # Build the update payload (stats only - review fields not in Webflow schema)
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
            print(f"✅ {slug}: Updated ({stats['stat-1-number']} {stats['stat-1-text'][:30]}...)")
            success_count += 1
        else:
            print(f"❌ {slug}: Error - {result}")
            error_count += 1

        time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"Complete! Success: {success_count}, Errors: {error_count}, Skipped: {skipped_count}")


if __name__ == '__main__':
    main()
