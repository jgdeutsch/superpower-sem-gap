#!/usr/bin/env python3
"""
Create a Dynamic Search Ads (DSA) campaign for Labcorp location pages.

Targets 1,138 Labcorp location pages at superpower.com/labcorp/{slug} with DSA,
so Google auto-matches searchers looking for "labcorp near me", "labcorp [city]",
"blood test near me" etc. to the correct location page.

Creates (all PAUSED so you can review before enabling):
1. Campaign budget ($30/day)
2. Campaign (Search, DSA, Maximize Conversions)
3. Page feed asset set with all 1,138 URLs
4. Ad group (SEARCH_DYNAMIC_ADS)
5. Webpage criterion targeting URLs from page feed
6. Expanded Dynamic Search Ad (2 descriptions)
7. Negative keywords to block irrelevant traffic

Run:
  /Users/jeffy/.local/bin/uvx --with 'google-ads>=25.1.0' --with pyyaml \
    python3 /Users/jeffy/superpower-sem-gap/app/scripts/create_labcorp_dsa_campaign.py
"""

import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

CONFIG_PATH = "/Users/jeffy/.config/google-ads-mcp/google-ads.yaml"
CUSTOMER_ID = "8618096874"
SLUGS_FILE = os.path.join(os.path.dirname(__file__), "labcorp_slugs.txt")

CAMPAIGN_NAME = "DSA - Labcorp Locations"
BUDGET_AMOUNT_MICROS = 30_000_000  # $30/day

AD_DESCRIPTION_1 = "100+ blood tests in one draw. $199/year. HSA/FSA eligible. Results in 10 days."
AD_DESCRIPTION_2 = "Your doctor orders 20 tests. We run 100+. Heart, thyroid, hormones, vitamins & more."

NEGATIVE_KEYWORDS = [
    ("labcorp jobs", "EXACT"),
    ("labcorp careers", "EXACT"),
    ("labcorp login", "EXACT"),
    ("labcorp results", "EXACT"),
    ("labcorp portal", "EXACT"),
    ("labcorp stock", "EXACT"),
    ("labcorp employee", "EXACT"),
    ("labcorp jobs", "PHRASE"),
    ("labcorp careers", "PHRASE"),
    ("labcorp employee", "PHRASE"),
]


def load_slugs():
    """Load Labcorp page slugs from file."""
    with open(SLUGS_FILE, "r") as f:
        slugs = [line.strip() for line in f if line.strip()]
    print(f"  Loaded {len(slugs)} slugs from {SLUGS_FILE}")
    return slugs


def create_budget(client):
    """Step 1: Create campaign budget ($30/day)."""
    print("\n[1/7] Creating campaign budget ($30/day)...")

    budget_op = client.get_type("CampaignBudgetOperation")
    budget = budget_op.create
    budget.name = f"{CAMPAIGN_NAME} Budget"
    budget.amount_micros = BUDGET_AMOUNT_MICROS
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    budget.explicitly_shared = False

    budget_service = client.get_service("CampaignBudgetService")
    response = budget_service.mutate_campaign_budgets(
        customer_id=CUSTOMER_ID, operations=[budget_op]
    )
    budget_resource = response.results[0].resource_name
    print(f"  Created: {budget_resource}")
    return budget_resource


def create_campaign(client, budget_resource):
    """Step 2: Create DSA campaign (Search, Maximize Conversions, PAUSED)."""
    print("\n[2/7] Creating DSA campaign...")

    campaign_op = client.get_type("CampaignOperation")
    campaign = campaign_op.create
    campaign.name = CAMPAIGN_NAME
    campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    campaign.campaign_budget = budget_resource

    # Maximize Conversions bidding (no target CPA - pure maximize)
    # Access the proto wrapper to trigger the oneof without setting sub-fields
    campaign._pb.maximize_conversions.SetInParent()

    # DSA settings
    campaign.dynamic_search_ads_setting.domain_name = "www.superpower.com"
    campaign.dynamic_search_ads_setting.language_code = "en"

    # Search network only (no display)
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = False
    campaign.network_settings.target_content_network = False

    # Required EU political advertising disclosure
    campaign.contains_eu_political_advertising = (
        client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    )

    campaign_service = client.get_service("CampaignService")
    response = campaign_service.mutate_campaigns(
        customer_id=CUSTOMER_ID, operations=[campaign_op]
    )
    campaign_resource = response.results[0].resource_name
    campaign_id = campaign_resource.split("/")[-1]
    print(f"  Created: {campaign_resource}")
    return campaign_resource, campaign_id


def create_page_feed(client, campaign_resource, campaign_id, slugs):
    """Step 3: Create page feed asset set with all Labcorp URLs."""
    print(f"\n[3/7] Creating page feed with {len(slugs)} URLs...")

    # 3a: Create AssetSet
    print("  3a: Creating PAGE_FEED asset set...")
    asset_set_op = client.get_type("AssetSetOperation")
    asset_set = asset_set_op.create
    asset_set.name = f"{CAMPAIGN_NAME} - Page Feed"
    asset_set.type_ = client.enums.AssetSetTypeEnum.PAGE_FEED

    asset_set_service = client.get_service("AssetSetService")
    response = asset_set_service.mutate_asset_sets(
        customer_id=CUSTOMER_ID, operations=[asset_set_op]
    )
    asset_set_resource = response.results[0].resource_name
    print(f"      Created: {asset_set_resource}")

    # 3b: Create Asset for each URL (batch in groups of 1000)
    print(f"  3b: Creating {len(slugs)} page feed assets...")
    asset_service = client.get_service("AssetService")
    all_asset_resources = []
    batch_size = 1000

    for i in range(0, len(slugs), batch_size):
        batch_slugs = slugs[i : i + batch_size]
        operations = []
        for slug in batch_slugs:
            op = client.get_type("AssetOperation")
            asset = op.create
            asset.page_feed_asset.page_url = f"https://www.superpower.com/labcorp/{slug}"
            asset.page_feed_asset.labels.append("labcorp-locations")
            operations.append(op)

        response = asset_service.mutate_assets(
            customer_id=CUSTOMER_ID, operations=operations
        )
        batch_resources = [r.resource_name for r in response.results]
        all_asset_resources.extend(batch_resources)
        print(f"      Batch {i // batch_size + 1}: created {len(batch_resources)} assets")

    print(f"      Total assets created: {len(all_asset_resources)}")

    # 3c: Link assets to asset set
    print(f"  3c: Linking assets to asset set...")
    asset_set_asset_service = client.get_service("AssetSetAssetService")

    for i in range(0, len(all_asset_resources), batch_size):
        batch_resources = all_asset_resources[i : i + batch_size]
        operations = []
        for asset_resource in batch_resources:
            op = client.get_type("AssetSetAssetOperation")
            link = op.create
            link.asset = asset_resource
            link.asset_set = asset_set_resource
            operations.append(op)

        response = asset_set_asset_service.mutate_asset_set_assets(
            customer_id=CUSTOMER_ID, operations=operations
        )
        print(f"      Batch {i // batch_size + 1}: linked {len(response.results)} assets")

    # 3d: Link asset set to campaign
    print("  3d: Linking asset set to campaign...")
    campaign_asset_set_service = client.get_service("CampaignAssetSetService")
    cas_op = client.get_type("CampaignAssetSetOperation")
    cas = cas_op.create
    cas.campaign = campaign_resource
    cas.asset_set = asset_set_resource

    response = campaign_asset_set_service.mutate_campaign_asset_sets(
        customer_id=CUSTOMER_ID, operations=[cas_op]
    )
    print(f"      Linked: {response.results[0].resource_name}")

    return asset_set_resource


def create_ad_group(client, campaign_resource):
    """Step 4: Create SEARCH_DYNAMIC_ADS ad group."""
    print("\n[4/7] Creating ad group...")

    ag_op = client.get_type("AdGroupOperation")
    ag = ag_op.create
    ag.name = "All Labcorp Locations"
    ag.campaign = campaign_resource
    ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS
    ag.status = client.enums.AdGroupStatusEnum.ENABLED

    ad_group_service = client.get_service("AdGroupService")
    response = ad_group_service.mutate_ad_groups(
        customer_id=CUSTOMER_ID, operations=[ag_op]
    )
    ag_resource = response.results[0].resource_name
    print(f"  Created: {ag_resource}")
    return ag_resource


def create_webpage_criterion(client, ad_group_resource):
    """Step 5: Create webpage criterion to target page feed URLs."""
    print("\n[5/7] Creating webpage targeting criterion...")

    criterion_op = client.get_type("AdGroupCriterionOperation")
    criterion = criterion_op.create
    criterion.ad_group = ad_group_resource
    criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED

    criterion.webpage.criterion_name = "Labcorp Location Pages"

    # Target using CUSTOM_LABEL that matches the label we set on assets
    condition = client.get_type("WebpageConditionInfo")
    condition.operand = client.enums.WebpageConditionOperandEnum.CUSTOM_LABEL
    condition.argument = "labcorp-locations"
    criterion.webpage.conditions.append(condition)

    ag_criterion_service = client.get_service("AdGroupCriterionService")
    response = ag_criterion_service.mutate_ad_group_criteria(
        customer_id=CUSTOMER_ID, operations=[criterion_op]
    )
    print(f"  Created: {response.results[0].resource_name}")


def create_dynamic_search_ad(client, ad_group_resource):
    """Step 6: Create Expanded Dynamic Search Ad."""
    print("\n[6/7] Creating dynamic search ad...")

    ad_op = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_op.create
    ad_group_ad.ad_group = ad_group_resource
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad_group_ad.ad.expanded_dynamic_search_ad.description = AD_DESCRIPTION_1
    ad_group_ad.ad.expanded_dynamic_search_ad.description2 = AD_DESCRIPTION_2

    ad_service = client.get_service("AdGroupAdService")

    try:
        response = ad_service.mutate_ad_group_ads(
            customer_id=CUSTOMER_ID, operations=[ad_op]
        )
        print(f"  Created: {response.results[0].resource_name}")
    except GoogleAdsException as ex:
        # Handle health-in-personalized-ads policy violation
        exempt_keys = []
        for error in ex.failure.errors:
            if error.details and error.details.policy_violation_details:
                key = error.details.policy_violation_details.key
                if key:
                    exempt_keys.append(
                        {
                            "policy_name": key.policy_name,
                            "violating_text": key.violating_text,
                        }
                    )

        if exempt_keys:
            print(f"  Policy violation ({len(exempt_keys)} keys), retrying with exemptions...")
            ad_op2 = client.get_type("AdGroupAdOperation")
            ad_op2.CopyFrom(ad_op)
            for ek in exempt_keys:
                pvk = client.get_type("PolicyViolationKey")
                pvk.policy_name = ek["policy_name"]
                pvk.violating_text = ek["violating_text"]
                ad_op2.policy_violation_keys.append(pvk)

            response = ad_service.mutate_ad_group_ads(
                customer_id=CUSTOMER_ID, operations=[ad_op2]
            )
            print(f"  Created (with exemption): {response.results[0].resource_name}")
        else:
            raise


def add_negative_keywords(client, campaign_resource):
    """Step 7: Add negative keywords to block irrelevant traffic."""
    print("\n[7/7] Adding negative keywords...")

    operations = []
    for keyword_text, match_type_str in NEGATIVE_KEYWORDS:
        op = client.get_type("CampaignCriterionOperation")
        criterion = op.create
        criterion.campaign = campaign_resource
        criterion.negative = True
        criterion.keyword.text = keyword_text
        if match_type_str == "EXACT":
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
        elif match_type_str == "PHRASE":
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        operations.append(op)

    campaign_criterion_service = client.get_service("CampaignCriterionService")
    response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=CUSTOMER_ID, operations=operations
    )
    print(f"  Added {len(response.results)} negative keywords:")
    for kw_text, match_type in NEGATIVE_KEYWORDS:
        print(f"    [{match_type}] {kw_text}")


def main():
    print("=" * 70)
    print("DSA Campaign Creator for Labcorp Location Pages")
    print("=" * 70)

    # Load slugs
    print("\nLoading Labcorp page slugs...")
    slugs = load_slugs()

    # Validate descriptions
    if len(AD_DESCRIPTION_1) > 90:
        print(f"ERROR: Description 1 is {len(AD_DESCRIPTION_1)} chars (max 90)")
        sys.exit(1)
    if len(AD_DESCRIPTION_2) > 90:
        print(f"ERROR: Description 2 is {len(AD_DESCRIPTION_2)} chars (max 90)")
        sys.exit(1)
    print(f"  Description 1: {len(AD_DESCRIPTION_1)} chars")
    print(f"  Description 2: {len(AD_DESCRIPTION_2)} chars")

    # Initialize client
    client = GoogleAdsClient.load_from_storage(CONFIG_PATH)

    try:
        # Step 1: Budget
        budget_resource = create_budget(client)

        # Step 2: Campaign
        campaign_resource, campaign_id = create_campaign(client, budget_resource)

        # Step 3: Page feed
        create_page_feed(client, campaign_resource, campaign_id, slugs)

        # Step 4: Ad group
        ag_resource = create_ad_group(client, campaign_resource)

        # Step 5: Webpage criterion
        create_webpage_criterion(client, ag_resource)

        # Step 6: Dynamic search ad
        create_dynamic_search_ad(client, ag_resource)

        # Step 7: Negative keywords
        add_negative_keywords(client, campaign_resource)

    except GoogleAdsException as ex:
        print(f"\nGOOGLE ADS API ERROR:")
        for error in ex.failure.errors:
            print(f"  {error.error_code}: {error.message}")
        sys.exit(1)
    except Exception as ex:
        print(f"\nERROR: {ex}")
        sys.exit(1)

    print("\n" + "=" * 70)
    print("SUCCESS! Campaign created in PAUSED state.")
    print("=" * 70)
    print(f"\nCampaign: {CAMPAIGN_NAME}")
    print(f"Budget: $30/day")
    print(f"Page feed: {len(slugs)} URLs")
    print(f"Status: PAUSED (enable in Google Ads UI when ready)")
    print(f"\nNext steps:")
    print(f"  1. Open Google Ads > Campaigns > '{CAMPAIGN_NAME}'")
    print(f"  2. Verify page feed is attached")
    print(f"  3. Verify negative keywords")
    print(f"  4. Enable when ready")


if __name__ == "__main__":
    main()
