#!/usr/bin/env python3
"""QA check for DSA - Labcorp Locations campaign."""

from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_storage("/Users/jeffy/.config/google-ads-mcp/google-ads.yaml")
ga = client.get_service("GoogleAdsService")
CID = "8618096874"
CAMPAIGN_ID = "23568629474"
ASSET_SET_ID = "9110366423"


def search(query):
    rows = []
    for batch in ga.search_stream(customer_id=CID, query=query):
        rows.extend(batch.results)
    return rows


# 1. Campaign
print("=== CAMPAIGN ===")
for row in search(f"""
    SELECT campaign.name, campaign.status, campaign.bidding_strategy_type,
           campaign.dynamic_search_ads_setting.domain_name,
           campaign.dynamic_search_ads_setting.language_code,
           campaign.network_settings.target_google_search,
           campaign.network_settings.target_search_network,
           campaign.network_settings.target_content_network
    FROM campaign WHERE campaign.id = {CAMPAIGN_ID}
"""):
    c = row.campaign
    print(f"  Name: {c.name}")
    print(f"  Status: {c.status.name}")
    print(f"  Bidding: {c.bidding_strategy_type.name}")
    print(f"  DSA domain: {c.dynamic_search_ads_setting.domain_name}")
    print(f"  DSA language: {c.dynamic_search_ads_setting.language_code}")
    print(f"  Google Search: {c.network_settings.target_google_search}")
    print(f"  Search partners: {c.network_settings.target_search_network}")
    print(f"  Display: {c.network_settings.target_content_network}")

# 2. Budget
print("\n=== BUDGET ===")
for row in search(f"""
    SELECT campaign_budget.amount_micros, campaign_budget.explicitly_shared
    FROM campaign WHERE campaign.id = {CAMPAIGN_ID}
"""):
    amt = row.campaign_budget.amount_micros / 1_000_000
    print(f"  Daily budget: ${amt:.0f}")
    print(f"  Shared: {row.campaign_budget.explicitly_shared}")

# 3. Ad group
print("\n=== AD GROUP ===")
for row in search(f"""
    SELECT ad_group.name, ad_group.type, ad_group.status
    FROM ad_group WHERE campaign.id = {CAMPAIGN_ID}
"""):
    print(f"  Name: {row.ad_group.name}")
    print(f"  Type: {row.ad_group.type_.name}")
    print(f"  Status: {row.ad_group.status.name}")

# 4. Ad
print("\n=== AD ===")
for row in search(f"""
    SELECT ad_group_ad.ad.expanded_dynamic_search_ad.description,
           ad_group_ad.ad.expanded_dynamic_search_ad.description2,
           ad_group_ad.status
    FROM ad_group_ad WHERE campaign.id = {CAMPAIGN_ID}
"""):
    dsa = row.ad_group_ad.ad.expanded_dynamic_search_ad
    print(f"  Status: {row.ad_group_ad.status.name}")
    print(f"  Desc 1: {dsa.description}")
    print(f"  Desc 2: {dsa.description2}")

# 5. Negative keywords
print("\n=== NEGATIVE KEYWORDS ===")
negs = search(f"""
    SELECT campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
    FROM campaign_criterion
    WHERE campaign.id = {CAMPAIGN_ID} AND campaign_criterion.negative = TRUE
""")
for row in negs:
    kw = row.campaign_criterion.keyword
    print(f"  [{kw.match_type.name}] {kw.text}")
print(f"  Total: {len(negs)}")

# 6. Page feed
print("\n=== PAGE FEED ===")
for row in search(f"""
    SELECT asset_set.name, asset_set.type
    FROM campaign_asset_set WHERE campaign.id = {CAMPAIGN_ID}
"""):
    print(f"  Asset set: {row.asset_set.name} ({row.asset_set.type_.name})")

assets = search(f"""
    SELECT asset_set_asset.asset, asset_set_asset.status
    FROM asset_set_asset WHERE asset_set.id = {ASSET_SET_ID}
""")
print(f"  URLs in feed: {len(assets)}")

# Spot-check 3 random URLs
import random
samples = random.sample(assets, min(3, len(assets)))
for row in samples:
    asset_id = row.asset_set_asset.asset.split("/")[-1]
    for a in search(f"""
        SELECT asset.page_feed_asset.page_url
        FROM asset WHERE asset.id = {asset_id}
    """):
        print(f"  Sample URL: {a.asset.page_feed_asset.page_url}")

# 7. Webpage criterion
print("\n=== TARGETING ===")
for row in search(f"""
    SELECT ad_group_criterion.webpage.criterion_name,
           ad_group_criterion.webpage.conditions
    FROM ad_group_criterion
    WHERE campaign.id = {CAMPAIGN_ID} AND ad_group_criterion.type = 'WEBPAGE'
"""):
    wp = row.ad_group_criterion.webpage
    print(f"  Criterion: {wp.criterion_name}")
    for c in wp.conditions:
        print(f"    {c.operand.name} = {c.argument}")

print("\n=== QA COMPLETE ===")
