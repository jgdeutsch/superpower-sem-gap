#!/usr/bin/env python3
"""
Create Responsive Search Ads (RSAs) for all 9 ad groups in the
Search_CareJourney_DUX_tCPA_US campaign.

Each ad group gets one RSA with:
- 15 headlines (max 30 chars each), headline 1 pinned to position 1
- 4 descriptions (max 90 chars each)
- Final URL specific to the ad group's landing page
- path1 and path2 for display URL
"""

import sys
import yaml
from google.ads.googleads.client import GoogleAdsClient

CONFIG_PATH = "/Users/jeffy/.config/google-ads-mcp/google-ads.yaml"
CUSTOMER_ID = "8618096874"
CAMPAIGN_ID = "23563151265"

# ── Ad group definitions ────────────────────────────────────────────────────

AD_GROUPS = [
    {
        "name": "Women's Hormone Health",
        "ad_group_id": "193544722699",
        "final_url": "https://www.superpower.com/welcome-cms/womens-hormone-test",
        "path1": "hormone-panel",
        "path2": "$388",
        "headlines": [
            ("Women's Hormone Panel - $388", True),   # pinned to pos 1
            ("Test All 12 Hormones at Once", False),
            ("129 Biomarkers. One Draw.", False),
            ("$32/Mo for Full Hormone Panel", False),
            ("FSA/HSA Eligible", False),
            ("24/7 Care Team", False),
            ("7 Thyroid Markers Included", False),
            ("Not Just Estradiol and TSH", False),
            ("Progesterone, DHEA-S & More", False),
            ("$100 Less Than InsideTracker", False),
            ("No Referral Needed", False),
            ("Results in ~10 Days", False),
            ("AI-Powered Analysis", False),
            ("Track Hormones Over Time", False),
            ("Stop Guessing. Start Testing.", False),
        ],
        "descriptions": [
            "Test all 12 hormones + 7 thyroid markers in one blood draw. Only $388/year. No referral.",
            "Most doctors test 2 hormones. We test 12 plus thyroid, metabolic & inflammation. $388/yr.",
            "129 biomarkers for $388/year. AI analysis, 24/7 care team & personalized action plan.",
            "Progesterone, DHEA-S, cortisol, estradiol & more. The complete hormone picture. $388.",
        ],
    },
    {
        "name": "Advanced Cholesterol & NMR",
        "ad_group_id": "194890338882",
        "final_url": "https://www.superpower.com/welcome-cms/cholesterol-test-advanced",
        "path1": "heart-panel",
        "path2": "$358",
        "headlines": [
            ("Advanced Heart Panel - $358", True),
            ("Full NMR + ApoB + Lp(a)", False),
            ("116 Biomarkers. One Draw.", False),
            ("$30/Mo. No Referral Needed.", False),
            ("FSA/HSA Eligible", False),
            ("24/7 Care Team", False),
            ("LDL Alone Misses Half the Risk", False),
            ("Next Closest Panel Is $529+", False),
            ("hs-CRP & Homocysteine Too", False),
            ("Particle Count Matters", False),
            ("Results in ~10 Days", False),
            ("AI-Powered Analysis", False),
            ("Track Heart Health Over Time", False),
            ("Know Your Real Heart Risk", False),
            ("Stop Guessing. Start Testing.", False),
        ],
        "descriptions": [
            "Full NMR lipoprofile, ApoB, Lp(a), hs-CRP & homocysteine. 116 biomarkers for $358/year.",
            "50% of heart attacks happen with normal LDL. Get the markers that actually predict risk.",
            "The only sub-$400 panel with full NMR particle counts plus ApoB and Lp(a). No referral.",
            "116 biomarkers, AI analysis, 24/7 care team & personalized plan. Just $30/month. $358/yr.",
        ],
    },
    {
        "name": "ApoB & Lp(a) Biohacker",
        "ad_group_id": "196898570561",
        "final_url": "https://www.superpower.com/welcome-cms/apob-lpa-test",
        "path1": "apob-lpa",
        "path2": "$358",
        "headlines": [
            ("ApoB + Lp(a) Panel - $358", True),
            ("Full NMR Lipoprofile Included", False),
            ("116 Biomarkers. One Draw.", False),
            ("$30/Mo. No Referral Needed.", False),
            ("FSA/HSA Eligible", False),
            ("24/7 Care Team", False),
            ("Next Closest Panel Is $595", False),
            ("Know Your Particle Count", False),
            ("hs-CRP & Homocysteine Too", False),
            ("1 in 5 Have High Lp(a)", False),
            ("Results in ~10 Days", False),
            ("AI-Powered Analysis", False),
            ("LDL-P vs LDL-C Matters", False),
            ("Most Doctors Never Test This", False),
            ("Stop Guessing. Start Testing.", False),
        ],
        "descriptions": [
            "ApoB, Lp(a) & full NMR particle counts plus 100+ biomarkers. Only $358/year. No referral.",
            "1 in 5 people have elevated Lp(a). Most doctors never test it. Find out for $30/month.",
            "The only sub-$400 panel with ApoB, Lp(a) & full NMR lipoprofile. Next closest is $595.",
            "116 biomarkers, AI analysis & 24/7 care team. The real heart risk panel. $358/year.",
        ],
    },
    {
        "name": "Heart Disease Family History",
        "ad_group_id": "194102562620",
        "final_url": "https://www.superpower.com/welcome-cms/heart-disease-risk-test",
        "path1": "heart-risk",
        "path2": "$358",
        "headlines": [
            ("Heart Risk Panel - $358/Year", True),
            ("Lp(a) + ApoB + Full NMR", False),
            ("116 Biomarkers. One Draw.", False),
            ("$30/Mo. No Referral Needed.", False),
            ("FSA/HSA Eligible", False),
            ("24/7 Care Team", False),
            ("Heart Disease Is Genetic", False),
            ("Is Your Lp(a) Elevated?", False),
            ("Know Your Inherited Risk", False),
            ("hs-CRP & Homocysteine Too", False),
            ("Results in ~10 Days", False),
            ("AI-Powered Analysis", False),
            ("#1 Killer in America", False),
            ("Don't Wait for Symptoms", False),
            ("Stop Guessing. Start Testing.", False),
        ],
        "descriptions": [
            "Lp(a), ApoB & full NMR particle counts. 116 biomarkers to know your real risk. $358/yr.",
            "Heart disease is the #1 killer. Lp(a) is genetic & most doctors never test it. $30/mo.",
            "The only sub-$400 panel testing Lp(a) genetic risk alongside ApoB & NMR. No referral.",
            "116 biomarkers, AI analysis & 24/7 care team. Know your inherited heart risk. $358/yr.",
        ],
    },
    {
        "name": "Advanced Insulin Resistance",
        "ad_group_id": "194890356442",
        "final_url": "https://www.superpower.com/welcome-cms/insulin-resistance-test-advanced",
        "path1": "insulin-test",
        "path2": "$328",
        "headlines": [
            ("Insulin Resistance Test $328", True),
            ("Adiponectin + Leptin + IR", False),
            ("111 Biomarkers. One Draw.", False),
            ("$27/Mo. No Referral Needed.", False),
            ("FSA/HSA Eligible", False),
            ("24/7 Care Team", False),
            ("Glucose Alone Misses It", False),
            ("Cardio IQ IR Score Included", False),
            ("Fructosamine Testing Too", False),
            ("Catch It Before Diabetes", False),
            ("Results in ~10 Days", False),
            ("AI-Powered Analysis", False),
            ("88M Americans Are Pre-Diabetic", False),
            ("Track Metabolic Health", False),
            ("Stop Guessing. Start Testing.", False),
        ],
        "descriptions": [
            "Adiponectin, leptin, fructosamine & Cardio IQ IR Score. 111 biomarkers for $328/year.",
            "Normal glucose can hide insulin resistance for years. We test what doctors don't. $27/mo.",
            "The only sub-$400 panel with all 4 advanced insulin markers. No referral needed. $328/yr.",
            "111 biomarkers, AI analysis & 24/7 care team. Catch insulin resistance early. $328/year.",
        ],
    },
    {
        "name": "Prediabetes Complete",
        "ad_group_id": "194102564300",
        "final_url": "https://www.superpower.com/welcome-cms/prediabetes-test-complete",
        "path1": "prediabetes",
        "path2": "$328",
        "headlines": [
            ("Prediabetes Panel - $328/Yr", True),
            ("More Than Just A1C & Glucose", False),
            ("111 Biomarkers. One Draw.", False),
            ("$27/Mo. No Referral Needed.", False),
            ("FSA/HSA Eligible", False),
            ("24/7 Care Team", False),
            ("84% Don't Know They Have It", False),
            ("IR Score + Adiponectin", False),
            ("Catch It Years Earlier", False),
            ("Fasting Insulin Included", False),
            ("Results in ~10 Days", False),
            ("AI-Powered Analysis", False),
            ("Reverse It Before Diabetes", False),
            ("Track Metabolic Progress", False),
            ("Stop Guessing. Start Testing.", False),
        ],
        "descriptions": [
            "A1C, fasting insulin, adiponectin, leptin & IR Score. 111 biomarkers for just $328/year.",
            "84% of people with prediabetes don't know it. Standard tests miss it for years. $27/mo.",
            "The only sub-$400 panel catching insulin resistance years before glucose moves. $328/yr.",
            "111 biomarkers, AI analysis & 24/7 care team. Find prediabetes early. Reverse it. $328.",
        ],
    },
    {
        "name": "Galleri Cancer Bundle",
        "ad_group_id": "193008925389",
        "final_url": "https://www.superpower.com/welcome-cms/galleri-test-bundle",
        "path1": "galleri",
        "path2": "$1048",
        "headlines": [
            ("Galleri + Blood Panel $1,048", True),
            ("Screen for 50+ Cancer Types", False),
            ("155+ Biomarkers. One Draw.", False),
            ("Galleri Alone Costs $949", False),
            ("FSA/HSA Eligible", False),
            ("24/7 Care Team", False),
            ("Add 100+ Biomarkers for $99", False),
            ("PSA & Thyroid Included", False),
            ("One Blood Draw. One Visit.", False),
            ("Multi-Cancer Detection", False),
            ("Results in ~10 Days", False),
            ("AI-Powered Analysis", False),
            ("No Referral Needed", False),
            ("Walk Into Quest. Get Both.", False),
            ("The Best Galleri Bundle.", False),
        ],
        "descriptions": [
            "Galleri screens 50+ cancers. We add 100+ biomarkers for $99 more. One draw. $1,048/year.",
            "Galleri standalone costs $949. Add full blood panel with PSA & thyroid for just $99 more.",
            "The only platform bundling Galleri with 100+ biomarkers in one blood draw. $1,048/year.",
            "155+ biomarkers, AI analysis & 24/7 care team. The most complete cancer screen. $1,048.",
        ],
    },
    {
        "name": "Multi-Cancer Screening",
        "ad_group_id": "194102566500",
        "final_url": "https://www.superpower.com/welcome-cms/multi-cancer-screening-test",
        "path1": "cancer-screen",
        "path2": "$1048",
        "headlines": [
            ("Cancer Screening - $1,048/Yr", True),
            ("Screen for 50+ Cancer Types", False),
            ("155+ Biomarkers. One Draw.", False),
            ("Pancreatic. Ovarian. Liver.", False),
            ("FSA/HSA Eligible", False),
            ("24/7 Care Team", False),
            ("No Standard Screening Exists", False),
            ("Cell-Free DNA Technology", False),
            ("100+ Health Markers Too", False),
            ("One Blood Draw Covers All", False),
            ("Results in ~10 Days", False),
            ("AI-Powered Analysis", False),
            ("No Referral Needed", False),
            ("71% of Cancer Deaths", False),
            ("Early Detection Saves Lives", False),
        ],
        "descriptions": [
            "Screen for 50+ cancer types plus 100+ health biomarkers in one blood draw. $1,048/year.",
            "71% of cancer deaths are from types with no standard screening. Get tested now. $1,048.",
            "Pancreatic, ovarian, liver & 47 more cancer types. Plus 100+ biomarkers. One blood draw.",
            "155+ biomarkers, AI analysis & 24/7 care team. The most complete cancer screen. $1,048.",
        ],
    },
    {
        "name": "Microbiome + Blood Panel",
        "ad_group_id": "194102567660",
        "final_url": "https://www.superpower.com/welcome-cms/microbiome-test-blood",
        "path1": "microbiome",
        "path2": "$438",
        "headlines": [
            ("Microbiome + Blood - $438", True),
            ("Gut + 100 Blood Biomarkers", False),
            ("199 Total Biomarkers", False),
            ("$37/Mo. No Referral Needed.", False),
            ("FSA/HSA Eligible", False),
            ("24/7 Care Team", False),
            ("Shotgun Metagenomics", False),
            ("Species-Level Gut Analysis", False),
            ("hs-CRP & Inflammation Too", False),
            ("Function Has No Gut Test", False),
            ("Results in ~10 Days", False),
            ("AI-Powered Analysis", False),
            ("70% of Immunity Is Gut", False),
            ("Beyond Basic Stool Tests", False),
            ("Stop Guessing. Start Testing.", False),
        ],
        "descriptions": [
            "Shotgun metagenomic gut analysis + 100 blood biomarkers in one membership. $438/year.",
            "The only membership combining clinical blood panel with species-level microbiome testing.",
            "199 biomarkers: gut species, inflammation, immune & metabolic markers. Just $37/month.",
            "199 biomarkers, AI analysis & 24/7 care team. Gut + blood in one membership. $438/year.",
        ],
    },
]


def validate_copy(ad_groups):
    """Validate all headlines <=30 chars and descriptions <=90 chars. Fail fast."""
    errors = []
    for ag in ad_groups:
        for i, (headline, _pinned) in enumerate(ag["headlines"]):
            if len(headline) > 30:
                errors.append(
                    f"  {ag['name']} headline {i+1}: '{headline}' = {len(headline)} chars (max 30)"
                )
        for i, desc in enumerate(ag["descriptions"]):
            if len(desc) > 90:
                errors.append(
                    f"  {ag['name']} desc {i+1}: '{desc}' = {len(desc)} chars (max 90)"
                )
        # Validate path1 <= 15 chars, path2 <= 15 chars
        if len(ag["path1"]) > 15:
            errors.append(
                f"  {ag['name']} path1: '{ag['path1']}' = {len(ag['path1'])} chars (max 15)"
            )
        if len(ag["path2"]) > 15:
            errors.append(
                f"  {ag['name']} path2: '{ag['path2']}' = {len(ag['path2'])} chars (max 15)"
            )
        # Validate exactly 15 headlines and 4 descriptions
        if len(ag["headlines"]) != 15:
            errors.append(
                f"  {ag['name']}: has {len(ag['headlines'])} headlines (need 15)"
            )
        if len(ag["descriptions"]) != 4:
            errors.append(
                f"  {ag['name']}: has {len(ag['descriptions'])} descriptions (need 4)"
            )
    return errors


def create_rsa_operations(client, customer_id, ad_groups):
    """Build AdGroupAdOperation list for all RSAs."""
    ad_group_ad_service = client.get_service("AdGroupAdService")
    operations = []

    for ag in ad_groups:
        operation = client.get_type("AdGroupAdOperation")
        ad_group_ad = operation.create

        # Set the ad group resource name
        ad_group_ad.ad_group = client.get_service("AdGroupService").ad_group_path(
            customer_id, ag["ad_group_id"]
        )

        # Set status to ENABLED
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

        # Set final URL
        ad_group_ad.ad.final_urls.append(ag["final_url"])

        # Set display URL paths
        ad_group_ad.ad.responsive_search_ad.path1 = ag["path1"]
        ad_group_ad.ad.responsive_search_ad.path2 = ag["path2"]

        # Add headlines
        for i, (headline_text, pinned) in enumerate(ag["headlines"]):
            headline = client.get_type("AdTextAsset")
            headline.text = headline_text
            if pinned:
                headline.pinned_field = (
                    client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
                )
            ad_group_ad.ad.responsive_search_ad.headlines.append(headline)

        # Add descriptions
        for desc_text in ag["descriptions"]:
            description = client.get_type("AdTextAsset")
            description.text = desc_text
            ad_group_ad.ad.responsive_search_ad.descriptions.append(description)

        operations.append(operation)

    return operations


def main():
    print("=" * 70)
    print("RSA Creator for Search_CareJourney_DUX_tCPA_US")
    print("=" * 70)

    # ── Step 1: Validate all copy ─────────────────────────────────────────
    print("\n[1/3] Validating ad copy character limits...")
    errors = validate_copy(AD_GROUPS)
    if errors:
        print("\nVALIDATION FAILED:")
        for err in errors:
            print(err)
        sys.exit(1)

    # Print validation summary
    for ag in AD_GROUPS:
        max_hl = max(len(h[0]) for h in ag["headlines"])
        max_desc = max(len(d) for d in ag["descriptions"])
        print(f"  OK: {ag['name']} (max headline: {max_hl}, max desc: {max_desc})")
    print("  All copy validated.")

    # ── Step 2: Build operations ──────────────────────────────────────────
    print("\n[2/3] Building RSA operations...")
    client = GoogleAdsClient.load_from_storage(CONFIG_PATH)
    operations = create_rsa_operations(client, CUSTOMER_ID, AD_GROUPS)
    print(f"  Built {len(operations)} RSA operations.")

    # ── Step 3: Mutate ────────────────────────────────────────────────────
    print("\n[3/3] Sending mutate request to Google Ads API...")
    ad_group_ad_service = client.get_service("AdGroupAdService")

    try:
        response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id=CUSTOMER_ID,
            operations=operations,
        )
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)

    print(f"\nSUCCESS: Created {len(response.results)} RSAs:")
    for i, result in enumerate(response.results):
        print(f"  {AD_GROUPS[i]['name']}: {result.resource_name}")

    print("\nDone.")


if __name__ == "__main__":
    main()
