#!/usr/bin/env python3
"""
Create RSA ads for static product pages in existing Care Journey ad groups.
This enables 50/50 traffic split testing: bundle LP vs static product page.

Creates:
  1. RSA in "Microbiome + Blood Panel" AG -> superpower.com/gut-microbiome ($399)
  2. RSA in "Galleri Cancer Bundle" AG -> superpower.com/galleri ($999)
  3. RSA in "Multi-Cancer Screening" AG -> superpower.com/galleri ($999)

Also sets ad rotation to ROTATE_INDEFINITELY for even split.
"""
import yaml
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CUSTOMER_ID = "8618096874"

# Ad group IDs and their new static page ads
AD_CONFIGS = [
    {
        "ag_id": 194102567660,
        "ag_name": "Microbiome + Blood Panel",
        "final_url": "https://www.superpower.com/gut-microbiome",
        "headlines": [
            {"text": "Gut Microbiome Test - $399/Yr", "pinned": "HEADLINE_1"},
            {"text": "Species-Level Gut Analysis"},
            {"text": "Shotgun Metagenomics"},
            {"text": "$33/Mo. No Referral Needed."},
            {"text": "FSA/HSA Eligible"},
            {"text": "24/7 Care Team"},
            {"text": "Go Beyond Basic Stool Tests"},
            {"text": "See What Lives In Your Gut"},
            {"text": "hs-CRP & Inflammation"},
            {"text": "Results in ~10 Days"},
            {"text": "AI-Powered Analysis"},
            {"text": "No Referral Needed"},
            {"text": "70% of Immunity Is Gut"},
            {"text": "Comprehensive Gut Testing"},
            {"text": "Stop Guessing. Start Testing."},
        ],
        "descriptions": [
            "Shotgun metagenomics reveals gut species. AI analysis & care team. $399/yr.",
            "Go beyond basic stool tests. See species-level gut composition. $399/year.",
            "Species-level gut microbiome testing with AI analysis. No referral. $33/mo.",
            "The most comprehensive gut test. No referral needed. AI included. $399/yr.",
        ],
    },
    {
        "ag_id": 193008925389,
        "ag_name": "Galleri Cancer Bundle",
        "final_url": "https://www.superpower.com/galleri",
        "headlines": [
            {"text": "Galleri Cancer Test - $999/Yr", "pinned": "HEADLINE_1"},
            {"text": "Screen for 50+ Cancer Types"},
            {"text": "Cell-Free DNA Technology"},
            {"text": "$83/Mo. No Referral Needed."},
            {"text": "FSA/HSA Eligible"},
            {"text": "24/7 Care Team"},
            {"text": "Pancreatic. Ovarian. Liver."},
            {"text": "No Standard Screening Exists"},
            {"text": "One Blood Draw. Done."},
            {"text": "Results in ~10 Days"},
            {"text": "AI-Powered Analysis"},
            {"text": "Multi-Cancer Detection"},
            {"text": "Early Detection Saves Lives"},
            {"text": "Walk Into Quest. Get Tested."},
            {"text": "71% of Cancer Deaths"},
        ],
        "descriptions": [
            "Screen for 50+ cancer types with one blood draw. Cell-free DNA tech. $999/yr.",
            "Pancreatic, ovarian, liver & 47 more. No standard screening exists. $999/yr.",
            "71% of cancer deaths have no standard screening. Get tested. $999/year.",
            "Galleri multi-cancer screening with AI analysis & care team. $83/month.",
        ],
    },
    {
        "ag_id": 194102566500,
        "ag_name": "Multi-Cancer Screening",
        "final_url": "https://www.superpower.com/galleri",
        "headlines": [
            {"text": "Cancer Screening - $999/Year", "pinned": "HEADLINE_1"},
            {"text": "Screen for 50+ Cancer Types"},
            {"text": "Cell-Free DNA Technology"},
            {"text": "$83/Mo. No Referral Needed."},
            {"text": "FSA/HSA Eligible"},
            {"text": "24/7 Care Team"},
            {"text": "Pancreatic. Ovarian. Liver."},
            {"text": "No Standard Screening Exists"},
            {"text": "Cancers With No Other Test"},
            {"text": "Results in ~10 Days"},
            {"text": "AI-Powered Analysis"},
            {"text": "Multi-Cancer Detection"},
            {"text": "Early Detection Saves Lives"},
            {"text": "One Blood Draw. Done."},
            {"text": "71% of Cancer Deaths"},
        ],
        "descriptions": [
            "Screen for 50+ cancer types with one blood draw. Cell-free DNA tech. $999/yr.",
            "71% of cancer deaths have no standard screening. Get tested now. $999/year.",
            "Pancreatic, ovarian, liver & 47 more. One blood draw. AI included. $999.",
            "Galleri multi-cancer screening with AI analysis & care team. $83/month.",
        ],
    },
]


def main():
    config = yaml.safe_load(open("/Users/jeffy/.config/google-ads-mcp/google-ads.yaml"))
    client = GoogleAdsClient.load_from_dict(config)

    print("=== Creating Static Page RSA Ads ===\n")

    for cfg in AD_CONFIGS:
        ag_id = cfg["ag_id"]
        ag_name = cfg["ag_name"]
        final_url = cfg["final_url"]

        print(f"--- {ag_name} (AG {ag_id}) ---")
        print(f"  Final URL: {final_url}")

        # 1. Set ad rotation to ROTATE_INDEFINITELY
        print("  Setting ad rotation to ROTATE_INDEFINITELY...")
        ag_service = client.get_service("AdGroupService")
        ag_operation = client.get_type("AdGroupOperation")
        ag = ag_operation.update
        ag.resource_name = ag_service.ad_group_path(CUSTOMER_ID, ag_id)
        ag.ad_rotation_mode = client.enums.AdGroupAdRotationModeEnum.ROTATE_FOREVER
        ag_operation.update_mask.paths.append("ad_rotation_mode")

        try:
            ag_response = ag_service.mutate_ad_groups(
                customer_id=CUSTOMER_ID, operations=[ag_operation]
            )
            print(f"  Ad rotation updated: {ag_response.results[0].resource_name}")
        except GoogleAdsException as e:
            print(f"  ERROR setting rotation: {e.failure.errors[0].message}")

        # 2. Create the RSA ad
        print("  Creating RSA ad...")
        ad_service = client.get_service("AdGroupAdService")
        ad_operation = client.get_type("AdGroupAdOperation")
        ad_group_ad = ad_operation.create
        ad_group_ad.ad_group = ag_service.ad_group_path(CUSTOMER_ID, ag_id)
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

        ad = ad_group_ad.ad
        ad.final_urls.append(final_url)

        # Add headlines
        for h in cfg["headlines"]:
            headline = client.get_type("AdTextAsset")
            headline.text = h["text"]
            if h.get("pinned") == "HEADLINE_1":
                headline.pinned_field = (
                    client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
                )
            ad.responsive_search_ad.headlines.append(headline)

        # Add descriptions
        for d_text in cfg["descriptions"]:
            desc = client.get_type("AdTextAsset")
            desc.text = d_text
            ad.responsive_search_ad.descriptions.append(desc)

        try:
            ad_response = ad_service.mutate_ad_group_ads(
                customer_id=CUSTOMER_ID, operations=[ad_operation]
            )
            print(f"  Created ad: {ad_response.results[0].resource_name}")
        except GoogleAdsException as e:
            for error in e.failure.errors:
                print(f"  ERROR: {error.message}")
                if error.location:
                    for fe in error.location.field_path_elements:
                        print(f"    Field: {fe.field_name} [{fe.index}]")

        print()

    print("=== Done! ===")
    print("\nEach ad group now has 2 RSAs with ROTATE_INDEFINITELY:")
    print("  - Original bundle LP ad")
    print("  - New static product page ad")
    print("\nTraffic should split ~50/50 between bundle and static pages.")


if __name__ == "__main__":
    main()
