#!/usr/bin/env python3
"""Verify the RSAs just created in the CareJourney campaign."""

import yaml
from google.ads.googleads.client import GoogleAdsClient

CONFIG_PATH = "/Users/jeffy/.config/google-ads-mcp/google-ads.yaml"
CUSTOMER_ID = "8618096874"
CAMPAIGN_ID = "23563151265"

client = GoogleAdsClient.load_from_storage(CONFIG_PATH)
ga_service = client.get_service("GoogleAdsService")

query = f"""
    SELECT
        ad_group.name,
        ad_group_ad.ad.id,
        ad_group_ad.ad.responsive_search_ad.headlines,
        ad_group_ad.ad.responsive_search_ad.descriptions,
        ad_group_ad.ad.responsive_search_ad.path1,
        ad_group_ad.ad.responsive_search_ad.path2,
        ad_group_ad.ad.final_urls,
        ad_group_ad.status,
        ad_group_ad.ad.type
    FROM ad_group_ad
    WHERE campaign.id = {CAMPAIGN_ID}
    ORDER BY ad_group.name
"""

response = ga_service.search(customer_id=CUSTOMER_ID, query=query)

for row in response:
    ad = row.ad_group_ad.ad
    rsa = ad.responsive_search_ad
    print(f"\n{'='*70}")
    print(f"Ad Group: {row.ad_group.name}")
    print(f"Ad ID: {ad.id} | Status: {row.ad_group_ad.status.name} | Type: {ad.type.name}")
    print(f"Final URL: {ad.final_urls[0] if ad.final_urls else 'N/A'}")
    print(f"Path: /{rsa.path1}/{rsa.path2}")
    print(f"\nHeadlines ({len(rsa.headlines)}):")
    for i, hl in enumerate(rsa.headlines):
        pin = ""
        if hl.pinned_field:
            pin = f" [PINNED: {hl.pinned_field.name}]"
        print(f"  {i+1}. ({len(hl.text):2d} chars) {hl.text}{pin}")
    print(f"\nDescriptions ({len(rsa.descriptions)}):")
    for i, desc in enumerate(rsa.descriptions):
        print(f"  {i+1}. ({len(desc.text):2d} chars) {desc.text}")

print(f"\n{'='*70}")
print("Verification complete.")
