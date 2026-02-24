"""
LP EXPERIMENT: Add second RSA with homepage URL to 5 Diagnostic-Discovery ad groups.
Google rotates ads within ad groups, so this gives ~50/50 split between CMS and homepage.

Experiment groups (non-BAD, decent volume):
1. Biomarker - $2,248/wk, $321 CPS (GOOD)
2. Gene test - $593/wk, $297 CPS (GOOD)
3. igf 1 test - $496/wk, $496 CPS (MIDDLE)
4. Medical test - $391/wk, $195 CPS (GOOD)
5. Body composition - $372/wk, $372 CPS (MIDDLE)

Each new ad copies the existing headlines/descriptions but changes final_url to homepage.
After 2-3 weeks, compare CPS by ad to see if homepage or CMS wins.
"""
import yaml
from google.ads.googleads.client import GoogleAdsClient

config_path = "/Users/jeffy/.config/google-ads-mcp/google-ads.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

client = GoogleAdsClient.load_from_dict(config)
service = client.get_service("GoogleAdsService")
ad_service = client.get_service("AdGroupAdService")
customer_id = "8618096874"
campaign_id = 23020350152  # Search_Generic_Diagnostic-Discovery_tCPA_US

HOMEPAGE_URL = "https://superpower.com/"

experiment_groups = [
    {
        'ag_id': 188162566689,
        'name': 'Biomarker',
        'headlines': [
            ("Your Doctor Tests 5 Biomarkers", "HEADLINE_1"),
            ("100+ Biomarkers Tested", None),
            ("One Draw. Full Picture.", None),
            ("Deep Biomarker Analysis", None),
            ("Every Biomarker Counts", None),
            ("Harvard-Backed Science", None),
            ("HSA/FSA Eligible", None),
            ("No Doctor Visit Required", None),
            ("Results in About 10 Days", None),
            ("$199/Yr - Not $365", None),
            ("At-Home Blood Draw", None),
            ("100+ Biomarkers. One Draw.", None),
            ("Would Cost $2,000+ Elsewhere", None),
            ("No Referral Needed", None),
            ("Personalized Insights", None),
        ],
        'descriptions': [
            ("Heart, hormones, thyroid, metabolic, vitamins - one blood draw. $199/yr.", "DESCRIPTION_1"),
            ("100+ biomarkers for $199/yr. At-home blood draw. HSA/FSA eligible.", None),
            ("Harvard-backed testing at home. A phlebotomist draws your blood. Results in about 10 days.", None),
            ("Same tests that would cost $2,000+ at a doctor. HSA/FSA eligible. $199/yr.", None),
        ],
    },
    {
        'ag_id': 188162568369,
        'name': 'Gene test',
        'headlines': [
            ("40% Carry the MTHFR Variant", "HEADLINE_1"),
            ("Test MTHFR-Related Markers", None),
            ("Homocysteine + B12 + Folate", None),
            ("Only $199/Year", None),
            ("100+ Biomarkers Tested", None),
            ("Results in About 10 Days", None),
            ("Harvard-Backed Science", None),
            ("Beyond Just the Gene", None),
            ("See If Methylation Works", None),
            ("HSA/FSA Eligible", None),
            ("CLIA-Certified Labs", None),
            ("No Prescription Needed", None),
            ("$199/Yr Membership", None),
            ("40% Carry MTHFR Variants", None),
            ("Full Methylation Panel", None),
        ],
        'descriptions': [
            ("40% of people carry MTHFR variants. Test the biomarkers it affects. $199/year.", None),
            ("Homocysteine, folate, B12, and inflammation markers show if methylation is working.", None),
            ("MTHFR status matters less than its impact. Test 100+ biomarkers in one blood draw.", None),
            ("Monitor your methylation-related biomarkers. Results in about 10 days. HSA/FSA eligible.", None),
        ],
    },
    {
        'ag_id': 188162568929,
        'name': 'igf 1 test',
        'headlines': [
            ("IGF-1 Alone Is Half the Story", "HEADLINE_1"),
            ("Full Growth Hormone Panel", None),
            ("IGF-1 Alone Is Half", None),
            ("100+ Biomarkers - $199/Yr", None),
            ("Liver, Insulin, Thyroid", None),
            ("At-Home Blood Draw", None),
            ("Harvard-Backed Science", None),
            ("Results in About 10 Days", None),
            ("HSA/FSA Eligible", None),
            ("Optimize With Full Data", None),
        ],
        'descriptions': [
            ("IGF-1 plus everything that affects it. Liver, insulin, thyroid and 100+ biomarkers.", "DESCRIPTION_1"),
            ("IGF-1 from 112 to 185 by fixing root causes found in 100+ biomarkers. $199/yr.", None),
            ("A standalone IGF-1 test is half the story. Get the full picture for $199/yr.", None),
            ("Screen for growth hormone issues and 1,000+ conditions. At-home draw. About 10 days.", None),
        ],
    },
    {
        'ag_id': 188162569569,
        'name': 'Medical test',
        'headlines': [
            ("Your Physical Checks 5 Things", "HEADLINE_1"),
            ("Screen 40+ Conditions", None),
            ("Comprehensive Lab Testing", None),
            ("Full Medical Blood Test", None),
            ("All Key Systems Tested", None),
            ("Harvard-Backed Science", None),
            ("HSA/FSA Eligible", None),
            ("No Doctor Visit Required", None),
            ("Results in About 10 Days", None),
            ("$199/Yr - Not $365", None),
            ("At-Home Blood Draw", None),
            ("100+ Biomarkers. One Draw.", None),
            ("Would Cost $2,000+ Elsewhere", None),
            ("No Referral Needed", None),
            ("Personalized Insights", None),
        ],
        'descriptions': [
            ("Screen for 40+ conditions. Heart, thyroid, hormones, vitamins. $199/yr.", "DESCRIPTION_1"),
            ("100+ biomarkers for $199/yr. At-home blood draw. HSA/FSA eligible.", None),
            ("Harvard-backed testing at home. A phlebotomist draws your blood. Results in about 10 days.", None),
            ("Same tests that would cost $2,000+ at a doctor. HSA/FSA eligible. $199/yr.", None),
        ],
    },
    {
        'ag_id': 188162566969,
        'name': 'Body composition',
        'headlines': [
            ("A DEXA Shows What. Not Why.", "HEADLINE_1"),
            ("The Why Behind the Weight", None),
            ("Insulin, Thyroid, Hormones", None),
            ("100+ Biomarkers - $199/Yr", None),
            ("Beyond a DEXA Scan", None),
            ("At-Home Blood Draw", None),
            ("Harvard-Backed Science", None),
            ("Results in About 10 Days", None),
            ("HSA/FSA Eligible", None),
            ("Metabolic Root Causes", None),
        ],
        'descriptions': [
            ("A DEXA shows what. Blood shows why. Test insulin, thyroid, hormones and 100+ biomarkers.", "DESCRIPTION_1"),
            ("Insulin resistant, low T3, low testosterone. Fixed the hormones, lost 22 pounds.", None),
            ("Body comp is the result. Blood markers reveal the metabolic cause. $199/yr. At-home draw.", None),
            ("Screen for metabolic issues and 1,000+ conditions. One blood draw. About 10 days.", None),
        ],
    },
]

PIN_MAP = {
    "HEADLINE_1": 2,
    "HEADLINE_2": 3,
    "HEADLINE_3": 4,
    "DESCRIPTION_1": 5,
    "DESCRIPTION_2": 6,
}

print("=" * 80)
print("  CREATING HOMEPAGE EXPERIMENT ADS")
print("=" * 80)

operations = []
for group in experiment_groups:
    op = client.get_type("AdGroupAdOperation")
    ad_group_ad = op.create
    ad_group_ad.ad_group = f"customers/{customer_id}/adGroups/{group['ag_id']}"
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad = ad_group_ad.ad
    ad.final_urls.append(HOMEPAGE_URL)

    rsa = ad.responsive_search_ad
    for text, pin in group['headlines']:
        headline = client.get_type("AdTextAsset")
        headline.text = text
        if pin and pin in PIN_MAP:
            headline.pinned_field = PIN_MAP[pin]
        rsa.headlines.append(headline)

    for text, pin in group['descriptions']:
        desc = client.get_type("AdTextAsset")
        desc.text = text
        if pin and pin in PIN_MAP:
            desc.pinned_field = PIN_MAP[pin]
        rsa.descriptions.append(desc)

    operations.append(op)
    print(f"  [+] {group['name']} (AG={group['ag_id']}) -> {HOMEPAGE_URL}")

print(f"\n  Sending {len(operations)} ad creation operations...")
try:
    response = ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=operations)
    print(f"  SUCCESS: {len(response.results)} experiment ads created")
    for result in response.results:
        print(f"    - {result.resource_name}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "=" * 80)
print("  EXPERIMENT SETUP COMPLETE")
print("  Each ad group now has 2 RSAs: 1x CMS page + 1x homepage")
print("  Google will auto-rotate ~50/50")
print("  Review after 2-3 weeks by comparing ad-level CPS")
print("=" * 80)

