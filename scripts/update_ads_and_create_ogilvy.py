#!/usr/bin/env python3
"""
Two operations:
1. Update all existing bundle LP RSA ads: replace sticker prices with discounted prices
2. Create one Ogilvy-style RSA ad per ad group (21 total)

Price mapping (sticker -> discounted):
  Metabolic:   $328 -> $298, $27/mo -> $25/mo
  Thyroid:     $388 -> $348, $32/mo -> $29/mo
  Autoimmune:  $338 -> $298, $28/mo -> $25/mo
  Heart:       $358 -> $328, $30/mo -> $27/mo
  Nutrients:   $358 -> $328, $30/mo -> $27/mo
  Methylation: $368 -> $338, $31/mo -> $28/mo
  Gut:         $438 -> $398, $37/mo -> $33/mo
  Galleri:     $1,048 -> $998, $87/mo -> $83/mo
  Longevity:   $686 -> $636, $57/mo -> $53/mo
"""
import yaml
import json
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = "8618096874"
CAMPAIGN_ID = 23563151265

# Price replacements: old text -> new text
# Applied as substring replacements across all headlines and descriptions
PRICE_REPLACEMENTS = {
    # Metabolic ($328 -> $298)
    "$328/year": "$298/year",
    "$328/yr": "$298/yr",
    "$328.": "$298.",
    "$328": "$298",
    "$27/mo": "$25/mo",
    "$27/month": "$25/month",
    "for $328": "for $298",
    # Thyroid ($388 -> $348) - already correct in ads
    "$388/year": "$348/year",
    "$388/yr": "$348/yr",
    "$388": "$348",
    "$32/mo": "$29/mo",
    "$32/month": "$29/month",
    # Autoimmune ($338 -> $298)
    "$338/year": "$298/year",
    "$338/yr": "$298/yr",
    "$338.": "$298.",
    "$338": "$298",
    "$28/mo": "$25/mo",
    "$28/month": "$25/month",
    # Heart ($358 -> $328)
    "$358/year": "$328/year",
    "$358/yr": "$328/yr",
    "$358.": "$328.",
    "$358": "$328",
    "$30/mo": "$27/mo",
    "$30/month": "$27/month",
    # Nutrients - same as Heart prices
    # Methylation ($368 -> $338)
    "$368/year": "$338/year",
    "$368/yr": "$338/yr",
    "$368.": "$338.",
    "$368": "$338",
    "$31/mo": "$28/mo",
    "$31/month": "$28/month",
    # Gut ($438 -> $398)
    "$438/year": "$398/year",
    "$438/yr": "$398/yr",
    "$438.": "$398.",
    "$438": "$398",
    "$37/mo": "$33/mo",
    "$37/month": "$33/month",
    # Galleri ($1,048 -> $998)
    "$1,048/year": "$998/year",
    "$1,048/yr": "$998/yr",
    "$1,048.": "$998.",
    "$1,048": "$998",
    "$87/mo": "$83/mo",
    # Longevity ($686 -> $636)
    "$686/year": "$636/year",
    "$686": "$636",
    "$57/mo": "$53/mo",
    # Fix sub-$X claims
    "Sub-$400": "Sub-$350",
    "sub-$400": "sub-$350",
}

# Also fix the "Next Closest Panel" comparisons and "$99 more" for Galleri
GALLERI_REPLACEMENTS = {
    "$99 more": "$49 more",
    "for $99 more": "for $49 more",
    "extra $99": "extra $49",
}


def apply_replacements(text, ag_name):
    """Apply price replacements to a text string."""
    result = text
    for old, new in PRICE_REPLACEMENTS.items():
        result = result.replace(old, new)
    # Galleri-specific replacements
    if "Galleri" in ag_name or "Cancer" in ag_name:
        for old, new in GALLERI_REPLACEMENTS.items():
            result = result.replace(old, new)
    return result


# Ogilvy-style RSA ads for each ad group
# Style: provocative, fact-based, agitate-the-problem headlines
# Max 30 chars headline, max 90 chars description
OGILVY_ADS = {
    # AG Name -> {url, headlines, descriptions}
    "ANA & Autoimmune Screening": {
        "url": "https://www.superpower.com/welcome-cms/ana-test-autoimmune",
        "headlines": [
            {"text": "A Positive ANA Means Nothing.", "pin": "HEADLINE_1"},
            {"text": "Without These 5 Other Tests."},
            {"text": "Your Doctor Tested 1 Marker."},
            {"text": "We Test 114."},
            {"text": "24M Americans. Undiagnosed."},
            {"text": "ANA Is Just the Beginning."},
            {"text": "The Average Diagnosis: 4 Yrs"},
            {"text": "No Referral. $298/Year."},
            {"text": "One Blood Draw. 114 Answers."},
            {"text": "hs-CRP Tells the Real Story."},
            {"text": "Inflammation Hides in Plain"},
            {"text": "ESR + CRP + ANA. One Draw."},
            {"text": "Why Wait for a Flare?"},
            {"text": "Most Doctors Skip ESR."},
            {"text": "AI Reads What Doctors Miss."},
        ],
        "descriptions": [
            "A positive ANA without hs-CRP, ESR & metabolic context is a guess. 114 markers. $298/yr.",
            "Autoimmune disease takes 4 years and 4 doctors to diagnose. One blood draw changes that.",
            "ANA, hs-CRP, ESR, tTG-IgA & 110 more biomarkers. AI analysis & care team. $298/yr.",
            "Your doctor tested ANA. We test the 113 markers that tell you what ANA alone cannot.",
        ],
    },
    "Advanced Cholesterol & NMR": {
        "url": "https://www.superpower.com/welcome-cms/cholesterol-test-advanced",
        "headlines": [
            {"text": "LDL 'Normal.' ApoB Was Not.", "pin": "HEADLINE_1"},
            {"text": "Half of Heart Attacks Are."},
            {"text": "Your Doctor Tests 4 Lipids."},
            {"text": "We Test 116 Biomarkers."},
            {"text": "NMR Counts Every Particle."},
            {"text": "LDL-C Misses Half the Risk."},
            {"text": "ApoB + Lp(a) + Full NMR."},
            {"text": "No Referral. $328/Year."},
            {"text": "The Panel Cardiologists Want."},
            {"text": "Standard Panels Miss This."},
            {"text": "50% of Heart Attacks."},
            {"text": "One Blood Draw. $27/Month."},
            {"text": "Particle Count > Cholesterol"},
            {"text": "hs-CRP + Homocysteine Too."},
            {"text": "AI Flags Hidden Risk."},
        ],
        "descriptions": [
            "50% of heart attacks strike people with 'normal' LDL. ApoB & NMR tell the truth. $328/yr.",
            "Full NMR particle counts, ApoB, Lp(a), hs-CRP & homocysteine. 116 biomarkers. $328/year.",
            "Your doctor tests LDL-C. We test LDL particle count, size, ApoB & Lp(a). Big difference.",
            "The cholesterol test cardiologists wish everyone got. 116 biomarkers, AI analysis. $27/mo.",
        ],
    },
    "Advanced Insulin Resistance": {
        "url": "https://www.superpower.com/welcome-cms/insulin-resistance-test-advanced",
        "headlines": [
            {"text": "Glucose Was 94. 'Normal.'", "pin": "HEADLINE_1"},
            {"text": "Insulin Was 18. Not Normal."},
            {"text": "84% Have No Idea."},
            {"text": "Fasting Glucose Lies."},
            {"text": "Adiponectin Tells the Truth."},
            {"text": "IR Score. Leptin. Insulin."},
            {"text": "No Referral. $298/Year."},
            {"text": "111 Biomarkers. One Draw."},
            {"text": "The Test Before Diabetes."},
            {"text": "Your Doctor Checks Glucose."},
            {"text": "We Check 111 Markers."},
            {"text": "88M Americans. Prediabetic."},
            {"text": "Catch It 10 Years Earlier."},
            {"text": "AI Connects the Pattern."},
            {"text": "Stop Checking Glucose Alone."},
        ],
        "descriptions": [
            "Fasting glucose was 94 -- 'normal.' Fasting insulin was 18. Adiponectin tanked. $298/year.",
            "88M Americans have prediabetes. 84% don't know. Glucose alone won't tell you. $298/yr.",
            "Adiponectin, leptin, fructosamine & IR Score. The 4 markers glucose tests miss. $25/month.",
            "Your doctor tests glucose. We test 111 markers that catch insulin resistance early.",
        ],
    },
    "ApoB & Lp(a) Biohacker": {
        "url": "https://www.superpower.com/welcome-cms/apob-lpa-test",
        "headlines": [
            {"text": "LDL Was 118. ApoB Was 142.", "pin": "HEADLINE_1"},
            {"text": "Classic Discordance. Missed."},
            {"text": "1 in 5 Have High Lp(a)."},
            {"text": "Most Doctors Never Test It."},
            {"text": "ApoB + Lp(a) + Full NMR."},
            {"text": "No Referral. $328/Year."},
            {"text": "116 Biomarkers. One Draw."},
            {"text": "The Real Heart Risk Panel."},
            {"text": "Particle Count Matters More."},
            {"text": "Lp(a) Is 100% Genetic."},
            {"text": "You Can't Fix What You Miss."},
            {"text": "Small Dense LDL Is the Risk."},
            {"text": "AI Spots Discordance."},
            {"text": "Beyond Standard Lipid Panels."},
            {"text": "$27/Month. No Referral."},
        ],
        "descriptions": [
            "LDL-C was 118. ApoB was 142. Classic discordance -- high risk behind a 'normal' number.",
            "1 in 5 have elevated Lp(a). It's 100% genetic. Most doctors never test it. $328/yr.",
            "ApoB, Lp(a), full NMR particle counts, hs-CRP & homocysteine. 116 biomarkers. $27/month.",
            "The panel biohackers and cardiologists agree on. ApoB + Lp(a) + NMR. No referral. $328/yr.",
        ],
    },
    "Biological Age Test": {
        "url": "https://www.superpower.com/welcome-cms/biological-age-test-blood",
        "headlines": [
            {"text": "Bio Age Said 5 Years Younger.", "pin": "HEADLINE_1"},
            {"text": "ApoB Said Otherwise."},
            {"text": "A Score Without Data Is Hype."},
            {"text": "We Show You the Biomarkers."},
            {"text": "116 Markers Behind Your Score."},
            {"text": "No Referral. $636/Year."},
            {"text": "Age Is a Number. ApoB Isn't."},
            {"text": "80% of Aging Is Modifiable."},
            {"text": "Which Organs Are Aging Fast?"},
            {"text": "Insulin. hs-CRP. DHEA-S."},
            {"text": "AI Prioritizes What to Fix."},
            {"text": "Pace of Aging + Blood Panel."},
            {"text": "One Draw. Your Real Age."},
            {"text": "Stop Guessing. Measure It."},
            {"text": "$53/Month. 116 Biomarkers."},
        ],
        "descriptions": [
            "Bio-age without ApoB, insulin & hs-CRP is flattery, not data. 116 markers. $636/yr.",
            "80% of aging is modifiable. Know which biomarkers are aging you fastest. $53/mo.",
            "Bio age, pace of aging & 116 clinical biomarkers. AI tells you what to fix first. $636/yr.",
            "Another test said 5 years younger. ApoB was 138. Insulin 16. CRP 2.9. $636/yr.",
        ],
    },
    "Celiac & Gluten Sensitivity": {
        "url": "https://www.superpower.com/welcome-cms/celiac-test-panel",
        "headlines": [
            {"text": "83% of Celiac Is Undiagnosed.", "pin": "HEADLINE_1"},
            {"text": "One Negative Test Means Zero."},
            {"text": "Antibodies Fluctuate. Test."},
            {"text": "tTG-IgA + ANA + hs-CRP."},
            {"text": "114 Biomarkers. One Draw."},
            {"text": "No Referral. $298/Year."},
            {"text": "3 Years of Bloating. 1 Test."},
            {"text": "Iron, B12 & Vitamin D Too."},
            {"text": "Gluten Damage Isn't Obvious."},
            {"text": "AI Connects the Pattern."},
            {"text": "Your Doctor Tested Once."},
            {"text": "We Test Everything."},
            {"text": "$25/Month. Full Panel."},
            {"text": "Celiac + Autoimmune Screen."},
            {"text": "Stop Wondering. Start Testing."},
        ],
        "descriptions": [
            "83% of celiac is undiagnosed. Antibodies fluctuate. One negative test means zero. $298/yr.",
            "tTG-IgA, ANA, hs-CRP, ESR & 110 more biomarkers. The celiac panel doctors should order.",
            "3 years of bloating and brain fog. Doctor tested once -- negative. tTG-IgA was elevated.",
            "Celiac screening plus iron, B12, vitamin D & autoimmune context. 114 biomarkers. $25/mo.",
        ],
    },
    "Galleri Cancer Bundle": {
        "url": "https://www.superpower.com/welcome-cms/galleri-test-bundle",
        "headlines": [
            {"text": "Galleri Alone Is $949.", "pin": "HEADLINE_1"},
            {"text": "We Add 100 Biomarkers for $49."},  # 30
            {"text": "Screen 50+ Cancers. One Draw."},
            {"text": "PSA & Thyroid Included."},
            {"text": "71% of Cancer Deaths."},
            {"text": "Have No Standard Screening."},
            {"text": "No Referral. $998/Year."},
            {"text": "Pancreatic. Ovarian. Liver."},
            {"text": "Cancers That Hide."},
            {"text": "Your Annual Physical Misses."},
            {"text": "Cell-Free DNA Technology."},
            {"text": "One Draw. 155+ Biomarkers."},
            {"text": "AI Connects All Results."},
            {"text": "Walk Into Quest. Get Both."},
            {"text": "The Smartest $49 You'll Spend."},
        ],
        "descriptions": [
            "Galleri alone is $949. Add PSA, thyroid & 100+ biomarkers for just $49 more. $998/yr.",
            "71% of cancer deaths have no standard screening. Galleri changes that. $998.",
            "Screen for 50+ cancer types and get 100+ blood biomarkers in one blood draw. No referral.",
            "Smartest $49 you'll spend: turn a $949 cancer screen into a 155+ biomarker panel.",
        ],
    },
    "Hashimoto's & Thyroid Autoimmune": {
        "url": "https://www.superpower.com/welcome-cms/hashimotos-test-panel",
        "headlines": [
            {"text": "TSH Was 'Normal' for 5 Years.", "pin": "HEADLINE_1"},
            {"text": "TPO Was 412. Nobody Tested."},
            {"text": "60% of Thyroid Disease."},
            {"text": "Is Undiagnosed Right Now."},
            {"text": "TSH Alone Misses Hashimoto's."},
            {"text": "TPO + Thyroglobulin + ANA."},
            {"text": "No Referral. $298/Year."},
            {"text": "114 Biomarkers. One Draw."},
            {"text": "Weight Gain? Hair Loss? Test."},
            {"text": "Your Doctor Tests TSH."},
            {"text": "We Test 114 Markers."},
            {"text": "AI Spots the Pattern."},
            {"text": "$25/Month. Full Panel."},
            {"text": "Stop Wondering. Start Testing."},
            {"text": "Antibodies Tell the Story."},
        ],
        "descriptions": [
            "TSH 'normal' for 5 years. She gained 40 lbs, lost her hair. TPO was 412. Nobody tested.",
            "60% of people with thyroid disease are undiagnosed. TSH alone misses Hashimoto's. $298/yr.",
            "TPO antibodies, thyroglobulin antibodies, ANA, hs-CRP & 110 more biomarkers. $25/month.",
            "Your doctor tests TSH. We test the 114 markers that find Hashimoto's before it's advanced.",
        ],
    },
    "Heart Disease Family History": {
        "url": "https://www.superpower.com/welcome-cms/heart-disease-risk-test",
        "headlines": [
            {"text": "His Dad Died at 58.", "pin": "HEADLINE_1"},
            {"text": "Cholesterol Was Always 'Fine.'"},
            {"text": "Lp(a) Was 212. Nobody Tested."},
            {"text": "Heart Disease Is #1 Killer."},
            {"text": "659K Americans. Every Year."},
            {"text": "Lp(a) Is Genetic."},
            {"text": "No Referral. $328/Year."},
            {"text": "ApoB + Lp(a) + NMR."},
            {"text": "116 Biomarkers. One Draw."},
            {"text": "Know Your Inherited Risk."},
            {"text": "Your Doctor Tests LDL."},
            {"text": "We Test 116 Markers."},
            {"text": "AI Flags Genetic Risk."},
            {"text": "$27/Month. No Referral."},
            {"text": "Family History Demands Data."},
        ],
        "descriptions": [
            "His dad died at 58. Heart attack. Cholesterol was 'fine.' Lp(a) was 212. Never tested.",
            "Heart disease kills 659K Americans yearly. Lp(a) is genetic. Most doctors never test it.",
            "Lp(a), ApoB, full NMR particle counts, hs-CRP & homocysteine. 116 markers. $328/yr.",
            "Heart disease in your family? A standard lipid panel is not enough. Test 116 markers.",
        ],
    },
    "Homocysteine & B12 Complete": {
        "url": "https://www.superpower.com/welcome-cms/homocysteine-test-complete",
        "headlines": [
            {"text": "Homocysteine Was 15.2.", "pin": "HEADLINE_1"},
            {"text": "Doctor Said 'Take B12.'"},
            {"text": "3 Root Causes. Not 1."},
            {"text": "MMA + Folate + B6 = Why."},
            {"text": "No Referral. $338/Year."},
            {"text": "118 Biomarkers. One Draw."},
            {"text": "A Standalone Test Finds Zero."},
            {"text": "Causes of High Homocysteine."},
            {"text": "AI Identifies the Pathway."},
            {"text": "Dropped to 7.8. Targeted Fix."},
            {"text": "$28/Month. Full Panel."},
            {"text": "RBC Folate. Not Serum."},
            {"text": "B12, MMA, B6, RBC Folate."},
            {"text": "Context Changes Everything."},
            {"text": "Stop Guessing. Start Testing."},
        ],
        "descriptions": [
            "Homocysteine was 15.2. Doctor said take B12. We found 3 root causes. Down to 7.8.",
            "Elevated homocysteine has 6 causes. A standalone test finds none. We test all 5 markers.",
            "Homocysteine, MMA, B12, RBC folate & B6 plus 113 more biomarkers. AI analysis. $338/year.",
            "Your doctor tests homocysteine. We test why it's elevated. 118 biomarkers. $28/month.",
        ],
    },
    "Longevity Blood Panel": {
        "url": "https://www.superpower.com/welcome-cms/longevity-blood-panel",
        "headlines": [
            {"text": "$200/Mo on Supplements.", "pin": "HEADLINE_1"},
            {"text": "Zero Data Behind Any of It."},
            {"text": "ApoB Was 127. CRP Was 2.4."},
            {"text": "Vitamin D Was Already Fine."},
            {"text": "116 Longevity Biomarkers."},
            {"text": "No Referral. $636/Year."},
            {"text": "DHEA-S. Insulin. HbA1c."},
            {"text": "The Stack Without the Data."},
            {"text": "Fix What Matters. Skip Rest."},
            {"text": "AI Prioritizes Your Stack."},
            {"text": "$53/Month. 116 Markers."},
            {"text": "Bio Age + Blood Panel."},
            {"text": "One Draw. Your Longevity Map."},
            {"text": "Stop Supplementing Blind."},
            {"text": "Test. Don't Guess."},
        ],
        "descriptions": [
            "He spent $200/mo on supplements with zero data. ApoB was 127, CRP 2.4. Vitamin D was fine.",
            "ApoB, hs-CRP, HbA1c, fasting insulin, DHEA-S & 111 more longevity biomarkers. $636/year.",
            "Every biomarker the longevity community tracks. One draw. AI says what to fix. $53/mo.",
            "Stop spending on supplements you don't need. Test 116 longevity biomarkers. $636/year.",
        ],
    },
    "MTHFR Functional Impact": {
        "url": "https://www.superpower.com/welcome-cms/mthfr-test-functional",
        "headlines": [
            {"text": "MTHFR Homozygous. So What?", "pin": "HEADLINE_1"},
            {"text": "Homocysteine Was 18.4."},
            {"text": "That's What."},
            {"text": "40% Carry the Variant."},
            {"text": "Most Have Zero Impact."},
            {"text": "Does Yours Matter? Test It."},
            {"text": "No Referral. $338/Year."},
            {"text": "MMA + B12 + RBC Folate."},
            {"text": "118 Biomarkers. One Draw."},
            {"text": "AI Reads the Pattern."},
            {"text": "Down to 8.2 in 4 Months."},
            {"text": "$28/Month. Full Panel."},
            {"text": "Methylfolate Fixed It."},
            {"text": "Function > Genotype."},
            {"text": "5 Markers Tell the Truth."},
        ],
        "descriptions": [
            "MTHFR homozygous for years. Nobody tested functional markers. Homocysteine: 18.4. $338/yr.",
            "40% carry an MTHFR variant. Most have no functional impact. 5 markers tell the truth.",
            "MMA, homocysteine, B12, RBC folate & B6. Know if your MTHFR variant matters. $28/mo.",
            "Homocysteine from 18.4 to 8.2 in 4 months. The test told her exactly what to take.",
        ],
    },
    "Magnesium & Mineral Test": {
        "url": "https://www.superpower.com/welcome-cms/magnesium-test-panel",
        "headlines": [
            {"text": "Serum Mg Was 2.1. 'Normal.'", "pin": "HEADLINE_1"},
            {"text": "RBC Mg Was 3.8. Deficient."},
            {"text": "80% of Deficiencies. Missed."},
            {"text": "Serum Hides the Truth."},
            {"text": "RBC Magnesium Matters."},
            {"text": "No Referral. $328/Year."},
            {"text": "Selenium + Zinc + 110 More."},
            {"text": "113 Biomarkers. One Draw."},
            {"text": "Cramps? Sleep Issues? Test."},
            {"text": "AI Flags What's Actually Low."},
            {"text": "$27/Month. Full Panel."},
            {"text": "Wrong Mg Form? We'll Know."},
            {"text": "3 Weeks to Feel Better."},
            {"text": "The Real Mineral Panel."},
            {"text": "Stop Guessing. Start Testing."},
        ],
        "descriptions": [
            "Serum Mg was 2.1 -- 'normal.' RBC Mg was 3.8 -- deficient. 80% of cases missed.",
            "RBC magnesium, selenium, zinc & 110 more biomarkers. The mineral panel that works. $328.",
            "Switched to Mg glycinate after testing. Cramps and sleep issues gone in 3 weeks. $27/mo.",
            "Your doctor orders serum Mg. It stays normal until you're severely depleted. We test RBC.",
        ],
    },
    "Methylation Panel Complete": {
        "url": "https://www.superpower.com/welcome-cms/methylation-panel-complete",
        "headlines": [
            {"text": "Previous Panel: 2 of 5.", "pin": "HEADLINE_1"},
            {"text": "We Test All 5."},
            {"text": "Partial Testing. False Hope."},
            {"text": "MMA, B12, Folate, B6, HCY."},
            {"text": "118 Biomarkers. One Draw."},
            {"text": "No Referral. $338/Year."},
            {"text": "3 Methylation Issues Found."},
            {"text": "That Partial Panels Missed."},
            {"text": "AI Connects the Pathway."},
            {"text": "$28/Month. Full Panel."},
            {"text": "5 Markers. No Blind Spots."},
            {"text": "Complete > Partial."},
            {"text": "The Gold Standard Panel."},
            {"text": "Context Changes Everything."},
            {"text": "Stop Guessing. Start Testing."},
        ],
        "descriptions": [
            "Previous panel tested homocysteine and B12. That's 2 of 5. MMA, folate & B6 were all off.",
            "All 5 gold-standard methylation markers plus 113 biomarkers. Full context. $338/yr.",
            "Partial methylation testing gave false confidence. Complete testing gave answers. $28/mo.",
            "MMA, homocysteine, B12, RBC folate & B6. The complete methylation picture. 118 biomarkers.",
        ],
    },
    "Microbiome + Blood Panel": {
        "url": "https://www.superpower.com/welcome-cms/microbiome-test-blood",
        "headlines": [
            {"text": "Viome Said 'Mostly Healthy.'", "pin": "HEADLINE_1"},
            {"text": "hs-CRP Was 4.2. Not Healthy."},
            {"text": "Zero Bifidobacterium Found."},
            {"text": "Gut + Blood in One Draw."},
            {"text": "199 Biomarkers. $398/Year."},
            {"text": "No Referral. $33/Month."},
            {"text": "70% of Immunity Is Gut."},
            {"text": "Shotgun Metagenomics."},
            {"text": "Species-Level Gut Data."},
            {"text": "hs-CRP Dropped to 0.8."},
            {"text": "AI Connects Gut to Blood."},
            {"text": "Beyond Basic Stool Tests."},
            {"text": "IgA + ESR + Celiac Markers."},
            {"text": "The Most Complete Gut Test."},
            {"text": "Stop Guessing. Start Testing."},
        ],
        "descriptions": [
            "Viome said 'mostly healthy.' hs-CRP was 4.2, IgA elevated, zero Bifido. $398/year.",
            "Shotgun metagenomics + hs-CRP, ESR, celiac & 90+ blood biomarkers. 199 total. $33/mo.",
            "70% of your immune system lives in your gut. We test gut species AND blood markers. $398.",
            "The only test combining species-level gut analysis with 100+ blood markers. No referral.",
        ],
    },
    "Micronutrient Test Complete": {
        "url": "https://www.superpower.com/welcome-cms/micronutrient-test-blood",
        "headlines": [
            {"text": "B6 Was Too High.", "pin": "HEADLINE_1"},
            {"text": "Vitamin K Was Deficient."},
            {"text": "RBC Mg Was Low."},
            {"text": "All While Supplementing."},
            {"text": "13 Nutrient Markers. $328."},
            {"text": "No Referral. $27/Month."},
            {"text": "92% Are Deficient in 1+."},
            {"text": "A, B2, B6, C, D, E, K."},
            {"text": "Selenium + RBC Magnesium."},
            {"text": "113 Biomarkers. One Draw."},
            {"text": "AI Flags the Real Gaps."},
            {"text": "Stop Supplementing Blind."},
            {"text": "Wrong Dose? Wrong Form?"},
            {"text": "Data > Guesswork."},
            {"text": "Test. Then Supplement."},
        ],
        "descriptions": [
            "Supplementing for years. B6 too high, vitamin K deficient, RBC Mg low. Data changes it.",
            "Vitamins A, B2, B6, C, D, E, K plus RBC magnesium & selenium. 113 biomarkers. $328/year.",
            "92% of Americans are deficient in at least one nutrient. Stop guessing which. $27/month.",
            "Switched supplement forms and doses based on data. 13 nutrient markers + 100 more. $328.",
        ],
    },
    "Multi-Cancer Screening": {
        "url": "https://www.superpower.com/welcome-cms/multi-cancer-screening-test",
        "headlines": [
            {"text": "Her Mom. Pancreatic. Stage 4.", "pin": "HEADLINE_1"},
            {"text": "No Screening. Until Now."},
            {"text": "50+ Cancer Types. One Draw."},
            {"text": "Cell-Free DNA Technology."},
            {"text": "71% of Cancer Deaths."},
            {"text": "Have No Standard Screening."},
            {"text": "No Referral. $998/Year."},
            {"text": "Pancreatic. Ovarian. Liver."},
            {"text": "155+ Biomarkers Total."},
            {"text": "No Cancer Signal Detected."},
            {"text": "Plus 3 Health Issues Found."},
            {"text": "AI Connects All Results."},
            {"text": "$83/Month. Peace of Mind."},
            {"text": "One Blood Draw. Done."},
            {"text": "Early Detection Saves Lives."},
        ],
        "descriptions": [
            "Her mother had pancreatic cancer. Stage 4. No screening existed. Now it does. $998/year.",
            "No cancer signal detected. But TSH was off, vitamin D was 18, insulin creeping up. $998.",
            "71% of cancer deaths are from types with no standard screening. One draw changes that.",
            "Screen for 50+ cancer types plus 100+ health biomarkers. One draw. AI analysis. $83/month.",
        ],
    },
    "Organ Age Test": {
        "url": "https://www.superpower.com/welcome-cms/organ-age-test",
        "headlines": [
            {"text": "Bio Age: 3 Years Younger.", "pin": "HEADLINE_1"},
            {"text": "Liver Age: 8 Years Older."},
            {"text": "ALT Was 42. GGT Was 58."},
            {"text": "Organs Age at Diff Speeds."},
            {"text": "The Fast Ones Need Help."},
            {"text": "No Referral. $636/Year."},
            {"text": "Heart. Liver. Kidney. More."},
            {"text": "116 Biomarkers Behind Scores."},
            {"text": "Cut Alcohol. Lost 12 Lbs."},
            {"text": "Liver Age Dropped 5 Years."},
            {"text": "AI Shows What to Fix First."},
            {"text": "$53/Month. 116 Markers."},
            {"text": "One Draw. Every Organ."},
            {"text": "Average =/= Healthy."},
            {"text": "Which Organ Is Aging You?"},
        ],
        "descriptions": [
            "Bio age was 3 years younger. Liver age was 8 years older. ALT 42, GGT 58. $636/year.",
            "Heart age, liver age, kidney age & more. Plus 116 biomarkers behind each score. $53/month.",
            "Cut alcohol, lost 12 lbs. Retested 6 months later. Liver age dropped 5 years. That's data.",
            "Your organs age at different speeds. The fast ones need help first. 116 markers. $636/yr.",
        ],
    },
    "Prediabetes Complete": {
        "url": "https://www.superpower.com/welcome-cms/prediabetes-test-complete",
        "headlines": [
            {"text": "A1c Was 5.8. 'Watch Your Diet'", "pin": "HEADLINE_1"},
            {"text": "Insulin Was 22. Nobody Tested."},
            {"text": "84% Don't Know They Have It."},
            {"text": "IR Score Flagged Severe."},
            {"text": "Glucose Alone Is Not Enough."},
            {"text": "No Referral. $298/Year."},
            {"text": "111 Biomarkers. One Draw."},
            {"text": "Adiponectin + Leptin + IR."},
            {"text": "From 22 to 7 in 5 Months."},
            {"text": "AI Catches It Early."},
            {"text": "$25/Month. Full Panel."},
            {"text": "The Test Before Diabetes."},
            {"text": "Invisible on Standard Labs."},
            {"text": "88M Americans. Prediabetic."},
            {"text": "Stop Watching. Start Testing."},
        ],
        "descriptions": [
            "A1c was 5.8. Doctor said 'watch your diet.' Fasting insulin was 22. IR Score: severe.",
            "84% with prediabetes don't know. Fasting insulin went from 22 to 7 in 5 months. $298.",
            "Adiponectin, leptin, fructosamine & IR Score. The 4 markers glucose can't see. $25/month.",
            "Your doctor tests glucose. We test 111 markers that catch prediabetes early. $298/yr.",
        ],
    },
    "Vitamin Deficiency Fatigue": {
        "url": "https://www.superpower.com/welcome-cms/vitamin-deficiency-fatigue-test",
        "headlines": [
            {"text": "CBC + Thyroid. Both 'Normal.'", "pin": "HEADLINE_1"},
            {"text": "Still Exhausted Every Day."},
            {"text": "Vitamin D Was 14."},
            {"text": "B6 Below Range. Mg Depleted."},
            {"text": "4 Causes Found. Doctor: Zero."},
            {"text": "No Referral. $328/Year."},
            {"text": "113 Biomarkers. One Draw."},
            {"text": "13 Nutrient Markers."},
            {"text": "AI Finds the Pattern."},
            {"text": "$27/Month. Full Panel."},
            {"text": "40% of Fatigue = Nutrients."},
            {"text": "Your Doctor Tests 8 Markers."},
            {"text": "We Test 113."},
            {"text": "Stop Living Tired."},
            {"text": "The Test Your Doctor Skipped."},
        ],
        "descriptions": [
            "CBC and thyroid 'normal.' Vitamin D was 14, B6 below range, Mg depleted, insulin 19. $328.",
            "40% of fatigue has a nutritional cause. Your doctor tests 8 markers. We test 113.",
            "13 nutrient markers plus thyroid, metabolic & inflammation panels. AI finds gaps. $27/mo.",
            "4 causes of fatigue her doctor never tested. 113 biomarkers in one blood draw. $328/year.",
        ],
    },
    "Women's Hormone Health": {
        "url": "https://www.superpower.com/welcome-cms/womens-hormone-test",
        "headlines": [
            {"text": "Estradiol + TSH. Both 'Fine.'", "pin": "HEADLINE_1"},
            {"text": "3 Hormone Issues Hiding."},
            {"text": "Progesterone. Barely There."},
            {"text": "DHEA-S Tanked. TPO at 340."},
            {"text": "12 Hormones + 7 Thyroid."},
            {"text": "No Referral. $348/Year."},
            {"text": "129 Biomarkers. One Draw."},
            {"text": "AI Connects the Pattern."},
            {"text": "$29/Month. Full Panel."},
            {"text": "80% Told 'Labs Are Normal.'"},
            {"text": "Track Across Cycles & Years."},
            {"text": "Your Doctor Tests 2 Hormones."},
            {"text": "We Test 129 Biomarkers."},
            {"text": "Stop Being Dismissed."},
            {"text": "Data Demands Attention."},
        ],
        "descriptions": [
            "Doctor tested estradiol and TSH. Both 'fine.' Progesterone barely there, TPO 340. $348/yr.",
            "80% of women with hormone imbalance are told labs are 'normal.' 129 biomarkers. $29/mo.",
            "12 hormones, 7 thyroid markers & 110 more biomarkers. Track across cycles. $348/yr.",
            "Your doctor tests 2 hormones. We test 129. AI connects the pattern. No referral.",
        ],
    },
}


def main():
    config = yaml.safe_load(
        open("/Users/jeffy/.config/google-ads-mcp/google-ads.yaml")
    )
    client = GoogleAdsClient.load_from_dict(config)
    service = client.get_service("GoogleAdsService")
    ad_service = client.get_service("AdService")
    ad_group_ad_service = client.get_service("AdGroupAdService")
    campaign_service = client.get_service("CampaignService")

    # 1. Get all existing RSA ads
    print("=== Step 1: Fetching existing ads ===")
    query = """
    SELECT
      ad_group.id,
      ad_group.name,
      ad_group_ad.ad.id,
      ad_group_ad.ad.responsive_search_ad.headlines,
      ad_group_ad.ad.responsive_search_ad.descriptions,
      ad_group_ad.ad.final_urls
    FROM ad_group_ad
    WHERE campaign.id = 23563151265
      AND ad_group_ad.ad.type = RESPONSIVE_SEARCH_AD
    ORDER BY ad_group.name
    """

    response = service.search(customer_id=CUSTOMER_ID, query=query)
    existing_ads = []
    for row in response:
        ag = row.ad_group
        ad = row.ad_group_ad.ad
        rsa = ad.responsive_search_ad
        urls = list(ad.final_urls)
        existing_ads.append(
            {
                "ag_id": ag.id,
                "ag_name": ag.name,
                "ad_id": ad.id,
                "url": urls[0] if urls else "",
                "headlines": [
                    {
                        "text": h.text,
                        "pin": (
                            h.pinned_field.name
                            if h.pinned_field and h.pinned_field != 0
                            else None
                        ),
                    }
                    for h in rsa.headlines
                ],
                "descriptions": [
                    {
                        "text": d.text,
                        "pin": (
                            d.pinned_field.name
                            if d.pinned_field and d.pinned_field != 0
                            else None
                        ),
                    }
                    for d in rsa.descriptions
                ],
            }
        )
    print(f"  Found {len(existing_ads)} existing ads\n")

    # 2. Update existing ads with discounted prices
    print("=== Step 2: Updating prices on existing bundle LP ads ===")
    update_count = 0
    update_errors = 0

    for ad_data in existing_ads:
        # Skip static page ads (they already have correct prices)
        if "/welcome-cms/" not in ad_data["url"]:
            print(f"  SKIP (static page): {ad_data['ag_name']} Ad {ad_data['ad_id']}")
            continue

        # Check if any prices need updating
        needs_update = False
        new_headlines = []
        for h in ad_data["headlines"]:
            new_text = apply_replacements(h["text"], ad_data["ag_name"])
            if new_text != h["text"]:
                needs_update = True
            new_headlines.append({"text": new_text, "pin": h["pin"]})

        new_descriptions = []
        for d in ad_data["descriptions"]:
            new_text = apply_replacements(d["text"], ad_data["ag_name"])
            if new_text != d["text"]:
                needs_update = True
            new_descriptions.append({"text": new_text, "pin": d["pin"]})

        if not needs_update:
            print(
                f"  SKIP (no price changes): {ad_data['ag_name']} Ad {ad_data['ad_id']}"
            )
            continue

        # Build update operation
        ad_op = client.get_type("AdOperation")
        updated_ad = ad_op.update
        updated_ad.resource_name = ad_service.ad_path(CUSTOMER_ID, ad_data["ad_id"])

        for h in new_headlines:
            new_h = client.get_type("AdTextAsset")
            new_h.text = h["text"]
            if h["pin"]:
                new_h.pinned_field = client.enums.ServedAssetFieldTypeEnum[h["pin"]]
            updated_ad.responsive_search_ad.headlines.append(new_h)

        for d in new_descriptions:
            new_d = client.get_type("AdTextAsset")
            new_d.text = d["text"]
            if d["pin"]:
                new_d.pinned_field = client.enums.ServedAssetFieldTypeEnum[d["pin"]]
            updated_ad.responsive_search_ad.descriptions.append(new_d)

        ad_op.update_mask.paths.append("responsive_search_ad.headlines")
        ad_op.update_mask.paths.append("responsive_search_ad.descriptions")

        try:
            result = ad_service.mutate_ads(
                customer_id=CUSTOMER_ID, operations=[ad_op]
            )
            # Log what changed
            changes = []
            for old_h, new_h in zip(ad_data["headlines"], new_headlines):
                if old_h["text"] != new_h["text"]:
                    changes.append(f'    H: "{old_h["text"]}" -> "{new_h["text"]}"')
            for old_d, new_d in zip(ad_data["descriptions"], new_descriptions):
                if old_d["text"] != new_d["text"]:
                    changes.append(f'    D: "{old_d["text"]}" -> "{new_d["text"]}"')
            print(f"  UPDATED: {ad_data['ag_name']} Ad {ad_data['ad_id']}")
            for c in changes:
                print(c)
            update_count += 1
        except GoogleAdsException as e:
            print(f"  ERROR: {ad_data['ag_name']} Ad {ad_data['ad_id']}")
            for error in e.failure.errors:
                print(f"    {error.message}")
                if error.details and hasattr(error.details, 'policy_finding_details'):
                    pfd = error.details.policy_finding_details
                    for pte in pfd.policy_topic_entries:
                        print(f"    Policy: {pte.topic} ({pte.type_.name})")
                        for ev in pte.evidences:
                            if ev.text_list:
                                print(f"    Evidence: {ev.text_list.texts}")
            update_errors += 1

    print(f"\n  Updated: {update_count}, Errors: {update_errors}\n")

    # 3. Create Ogilvy-style ads
    print("=== Step 3: Creating Ogilvy-style RSA ads ===")

    # Get ad group IDs by name
    ag_query = """
    SELECT ad_group.id, ad_group.name
    FROM ad_group
    WHERE campaign.id = 23563151265
    """
    ag_response = service.search(customer_id=CUSTOMER_ID, query=ag_query)
    ag_map = {}
    for row in ag_response:
        ag_map[row.ad_group.name] = row.ad_group.id

    create_count = 0
    create_errors = 0

    for ag_name, ad_config in OGILVY_ADS.items():
        ag_id = ag_map.get(ag_name)
        if not ag_id:
            print(f"  SKIP (AG not found): {ag_name}")
            continue

        ad_op = client.get_type("AdGroupAdOperation")
        ad_group_ad = ad_op.create
        ad_group_ad.ad_group = client.get_service("AdGroupService").ad_group_path(
            CUSTOMER_ID, ag_id
        )
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

        ad = ad_group_ad.ad
        ad.final_urls.append(ad_config["url"])

        for h in ad_config["headlines"]:
            headline = client.get_type("AdTextAsset")
            headline.text = h["text"]
            if h.get("pin") == "HEADLINE_1":
                headline.pinned_field = (
                    client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
                )
            ad.responsive_search_ad.headlines.append(headline)

        for d_text in ad_config["descriptions"]:
            desc = client.get_type("AdTextAsset")
            desc.text = d_text
            ad.responsive_search_ad.descriptions.append(desc)

        try:
            result = ad_group_ad_service.mutate_ad_group_ads(
                customer_id=CUSTOMER_ID, operations=[ad_op]
            )
            print(f"  CREATED: {ag_name} -> {result.results[0].resource_name}")
            create_count += 1
        except GoogleAdsException as e:
            print(f"  ERROR: {ag_name}")
            for error in e.failure.errors:
                print(f"    {error.message}")
                if error.location:
                    for fe in error.location.field_path_elements:
                        print(f"    Field: {fe.field_name} [{fe.index}]")
                if error.details and hasattr(error.details, 'policy_finding_details'):
                    pfd = error.details.policy_finding_details
                    for pte in pfd.policy_topic_entries:
                        print(f"    Policy: {pte.topic} ({pte.type_.name})")
                        for ev in pte.evidences:
                            if ev.text_list:
                                print(f"    Evidence: {ev.text_list.texts}")
            create_errors += 1

    print(f"\n  Created: {create_count}, Errors: {create_errors}\n")

    # 4. Set ad rotation to ROTATE_INDEFINITELY on all ad groups
    print("=== Step 4: Setting ROTATE_INDEFINITELY on all ad groups ===")
    ag_service = client.get_service("AdGroupService")
    rotation_ops = []
    for ag_name, ag_id in ag_map.items():
        ag_op = client.get_type("AdGroupOperation")
        ag = ag_op.update
        ag.resource_name = ag_service.ad_group_path(CUSTOMER_ID, ag_id)
        ag.ad_rotation_mode = client.enums.AdGroupAdRotationModeEnum.ROTATE_FOREVER
        ag_op.update_mask.paths.append("ad_rotation_mode")
        rotation_ops.append(ag_op)

    try:
        result = ag_service.mutate_ad_groups(
            customer_id=CUSTOMER_ID, operations=rotation_ops
        )
        print(f"  Set ROTATE_INDEFINITELY on {len(result.results)} ad groups\n")
    except GoogleAdsException as e:
        print(f"  ERROR: {e.failure.errors[0].message}\n")

    print("=== DONE ===")
    print(f"  Prices updated: {update_count}")
    print(f"  Ogilvy ads created: {create_count}")
    print(f"  Total errors: {update_errors + create_errors}")


if __name__ == "__main__":
    main()
