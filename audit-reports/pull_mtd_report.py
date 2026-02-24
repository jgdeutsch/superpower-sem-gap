#!/usr/bin/env python3
"""Pull Google Ads MTD report for Feb 1-22, 2026 - Search + PMAX, non-brand."""

import yaml
from google.ads.googleads.client import GoogleAdsClient
from collections import defaultdict

# --- Config ---
CONFIG_PATH = "/Users/jeffy/.config/google-ads-mcp/google-ads.yaml"
CUSTOMER_ID = "8618096874"
MTD_START = "2026-02-01"
MTD_END = "2026-02-22"
RECENT_START = "2026-02-16"
RECENT_END = "2026-02-22"

EXPERIMENT_AD_GROUP_IDS = [
    188162566689, 188162568369, 188162568929, 188162569569, 188162566969
]

def get_client():
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)
    return GoogleAdsClient.load_from_dict(config)

def query(client, customer_id, gaql):
    service = client.get_service("GoogleAdsService")
    return service.search(customer_id=customer_id, query=gaql)

def fmt_money(micros):
    return micros / 1_000_000

def fmt_currency(val):
    return f"${val:,.2f}"

def safe_div(a, b):
    return a / b if b else float('inf')


def pull_spend(client, start, end):
    gaql = f"""
        SELECT
            campaign.name,
            campaign.advertising_channel_type,
            campaign.status,
            metrics.cost_micros,
            metrics.clicks
        FROM campaign
        WHERE campaign.advertising_channel_type IN ('SEARCH', 'PERFORMANCE_MAX')
          AND campaign.status != 'REMOVED'
          AND segments.date BETWEEN '{start}' AND '{end}'
    """
    data = {}
    for row in query(client, CUSTOMER_ID, gaql):
        name = row.campaign.name
        channel = row.campaign.advertising_channel_type.name
        if "brand" in name.lower():
            continue
        if name not in data:
            data[name] = {"channel": channel, "spend_micros": 0, "clicks": 0}
        data[name]["spend_micros"] += row.metrics.cost_micros
        data[name]["clicks"] += row.metrics.clicks
    return data


def pull_conversions(client, start, end, conversion_action_name):
    gaql = f"""
        SELECT
            campaign.name,
            campaign.advertising_channel_type,
            campaign.status,
            segments.conversion_action_name,
            metrics.all_conversions
        FROM campaign
        WHERE campaign.advertising_channel_type IN ('SEARCH', 'PERFORMANCE_MAX')
          AND campaign.status != 'REMOVED'
          AND segments.date BETWEEN '{start}' AND '{end}'
          AND segments.conversion_action_name = '{conversion_action_name}'
    """
    data = {}
    for row in query(client, CUSTOMER_ID, gaql):
        name = row.campaign.name
        if "brand" in name.lower():
            continue
        data[name] = data.get(name, 0) + row.metrics.all_conversions
    return data


def pull_experiment_ad_groups(client, start, end):
    id_list = ", ".join(str(i) for i in EXPERIMENT_AD_GROUP_IDS)
    gaql = f"""
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.status,
            campaign.name,
            campaign.advertising_channel_type,
            campaign.status,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions
        FROM ad_group
        WHERE ad_group.id IN ({id_list})
          AND segments.date BETWEEN '{start}' AND '{end}'
    """
    results = []
    try:
        for row in query(client, CUSTOMER_ID, gaql):
            results.append({
                "ag_id": row.ad_group.id,
                "ag_name": row.ad_group.name,
                "ag_status": row.ad_group.status.name,
                "campaign": row.campaign.name,
                "channel": row.campaign.advertising_channel_type.name,
                "spend_micros": row.metrics.cost_micros,
                "clicks": row.metrics.clicks,
                "impressions": row.metrics.impressions,
            })
    except Exception as e:
        print(f"  [Experiment ad groups query error: {e}]")
    return results


def pull_experiment_ag_conversions(client, start, end, conversion_action_name):
    id_list = ", ".join(str(i) for i in EXPERIMENT_AD_GROUP_IDS)
    gaql = f"""
        SELECT
            ad_group.id,
            ad_group.name,
            campaign.name,
            segments.conversion_action_name,
            metrics.all_conversions
        FROM ad_group
        WHERE ad_group.id IN ({id_list})
          AND segments.date BETWEEN '{start}' AND '{end}'
          AND segments.conversion_action_name = '{conversion_action_name}'
    """
    data = {}
    try:
        for row in query(client, CUSTOMER_ID, gaql):
            ag_id = row.ad_group.id
            data[ag_id] = data.get(ag_id, 0) + row.metrics.all_conversions
    except Exception:
        pass
    return data


def pull_enabled_search_ad_groups(client, start, end):
    gaql = f"""
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.status,
            campaign.name,
            campaign.advertising_channel_type,
            campaign.status,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions
        FROM ad_group
        WHERE campaign.advertising_channel_type = 'SEARCH'
          AND campaign.status != 'REMOVED'
          AND ad_group.status = 'ENABLED'
          AND segments.date BETWEEN '{start}' AND '{end}'
    """
    results = []
    for row in query(client, CUSTOMER_ID, gaql):
        if "brand" in row.campaign.name.lower():
            continue
        results.append({
            "ag_id": row.ad_group.id,
            "ag_name": row.ad_group.name,
            "campaign": row.campaign.name,
            "spend_micros": row.metrics.cost_micros,
            "clicks": row.metrics.clicks,
            "impressions": row.metrics.impressions,
        })
    return results


def pull_search_ag_conversions(client, start, end, conversion_action_name):
    gaql = f"""
        SELECT
            ad_group.id,
            ad_group.name,
            campaign.name,
            campaign.advertising_channel_type,
            campaign.status,
            ad_group.status,
            segments.conversion_action_name,
            metrics.all_conversions
        FROM ad_group
        WHERE campaign.advertising_channel_type = 'SEARCH'
          AND campaign.status != 'REMOVED'
          AND ad_group.status = 'ENABLED'
          AND segments.date BETWEEN '{start}' AND '{end}'
          AND segments.conversion_action_name = '{conversion_action_name}'
    """
    data = {}
    for row in query(client, CUSTOMER_ID, gaql):
        if "brand" in row.campaign.name.lower():
            continue
        ag_id = row.ad_group.id
        data[ag_id] = data.get(ag_id, 0) + row.metrics.all_conversions
    return data


def pull_enabled_pmax_asset_groups(client, start, end):
    gaql = f"""
        SELECT
            asset_group.id,
            asset_group.name,
            asset_group.status,
            campaign.name,
            campaign.advertising_channel_type,
            campaign.status,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions
        FROM asset_group
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
          AND campaign.status != 'REMOVED'
          AND asset_group.status = 'ENABLED'
          AND segments.date BETWEEN '{start}' AND '{end}'
    """
    results = []
    for row in query(client, CUSTOMER_ID, gaql):
        if "brand" in row.campaign.name.lower():
            continue
        results.append({
            "ag_id": row.asset_group.id,
            "ag_name": row.asset_group.name,
            "campaign": row.campaign.name,
            "spend_micros": row.metrics.cost_micros,
            "clicks": row.metrics.clicks,
            "impressions": row.metrics.impressions,
        })
    return results


def pull_pmax_ag_conversions(client, start, end, conversion_action_name):
    gaql = f"""
        SELECT
            asset_group.id,
            asset_group.name,
            campaign.name,
            campaign.advertising_channel_type,
            campaign.status,
            asset_group.status,
            segments.conversion_action_name,
            metrics.all_conversions
        FROM asset_group
        WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
          AND campaign.status != 'REMOVED'
          AND asset_group.status = 'ENABLED'
          AND segments.date BETWEEN '{start}' AND '{end}'
          AND segments.conversion_action_name = '{conversion_action_name}'
    """
    data = {}
    for row in query(client, CUSTOMER_ID, gaql):
        if "brand" in row.campaign.name.lower():
            continue
        ag_id = row.asset_group.id
        data[ag_id] = data.get(ag_id, 0) + row.metrics.all_conversions
    return data


# ============================================================
# Print helpers
# ============================================================
def print_campaign_table(spend_data, regs_data, subs_data, title):
    print(f"\n{'='*120}")
    print(f"  {title}")
    print(f"{'='*120}")
    header = f"{'Campaign':<55} {'Type':<12} {'Spend':>10} {'Clicks':>8} {'Regs':>6} {'Subs':>6} {'CPR':>10} {'CPS':>10}"
    print(header)
    print("-" * 120)

    totals = defaultdict(lambda: {"spend": 0, "clicks": 0, "regs": 0, "subs": 0})
    grand = {"spend": 0, "clicks": 0, "regs": 0, "subs": 0}

    # Only print campaigns with spend > 0
    active_campaigns = {k: v for k, v in spend_data.items() if v["spend_micros"] > 0}
    zero_campaigns = {k: v for k, v in spend_data.items() if v["spend_micros"] == 0}

    for name in sorted(active_campaigns.keys()):
        info = active_campaigns[name]
        channel = info["channel"]
        spend = fmt_money(info["spend_micros"])
        clicks = info["clicks"]
        regs = regs_data.get(name, 0)
        subs = subs_data.get(name, 0)
        cpr = safe_div(spend, regs)
        cps = safe_div(spend, subs)
        cpr_str = fmt_currency(cpr) if regs > 0 else "-"
        cps_str = fmt_currency(cps) if subs > 0 else "-"

        display_name = name[:54]
        print(f"{display_name:<55} {channel:<12} {fmt_currency(spend):>10} {clicks:>8} {regs:>6.1f} {subs:>6.1f} {cpr_str:>10} {cps_str:>10}")

        totals[channel]["spend"] += spend
        totals[channel]["clicks"] += clicks
        totals[channel]["regs"] += regs
        totals[channel]["subs"] += subs
        grand["spend"] += spend
        grand["clicks"] += clicks
        grand["regs"] += regs
        grand["subs"] += subs

    # Also count zero-spend campaigns into totals (they add nothing but let's be accurate)
    for name, info in zero_campaigns.items():
        pass  # zero spend, zero everything

    if zero_campaigns:
        print(f"  ... plus {len(zero_campaigns)} campaigns with $0 spend (paused/no impressions)")

    print("-" * 120)
    for ch in sorted(totals.keys()):
        t = totals[ch]
        cpr = safe_div(t["spend"], t["regs"])
        cps = safe_div(t["spend"], t["subs"])
        cpr_str = fmt_currency(cpr) if t["regs"] > 0 else "-"
        cps_str = fmt_currency(cps) if t["subs"] > 0 else "-"
        label = f"TOTAL {ch}"
        print(f"{label:<55} {'':12} {fmt_currency(t['spend']):>10} {t['clicks']:>8} {t['regs']:>6.1f} {t['subs']:>6.1f} {cpr_str:>10} {cps_str:>10}")

    g = grand
    cpr = safe_div(g["spend"], g["regs"])
    cps = safe_div(g["spend"], g["subs"])
    cpr_str = fmt_currency(cpr) if g["regs"] > 0 else "-"
    cps_str = fmt_currency(cps) if g["subs"] > 0 else "-"
    print(f"{'GRAND TOTAL':<55} {'':12} {fmt_currency(g['spend']):>10} {g['clicks']:>8} {g['regs']:>6.1f} {g['subs']:>6.1f} {cpr_str:>10} {cps_str:>10}")
    print("=" * 120)


def print_ag_table(ag_data, subs_data, title):
    """Generic ad group / asset group table. ag_data is a list of dicts with ag_id, ag_name, campaign, spend_micros, clicks, impressions."""
    print(f"\n{'='*130}")
    print(f"  {title}")
    print(f"{'='*130}")
    header = f"{'Ad Group / Asset Group':<50} {'Campaign':<35} {'Spend':>10} {'Clicks':>7} {'Impr':>7} {'Subs':>6} {'CPS':>10}"
    print(header)
    print("-" * 130)

    # Aggregate by ag_id
    agg = {}
    for row in ag_data:
        aid = row["ag_id"]
        if aid not in agg:
            agg[aid] = {
                "name": row["ag_name"],
                "campaign": row["campaign"],
                "spend_micros": 0,
                "clicks": 0,
                "impressions": 0,
            }
        agg[aid]["spend_micros"] += row["spend_micros"]
        agg[aid]["clicks"] += row["clicks"]
        agg[aid]["impressions"] += row["impressions"]

    total_spend = 0
    total_clicks = 0
    total_impr = 0
    total_subs = 0

    # Only show groups with spend > 0
    active = {k: v for k, v in agg.items() if v["spend_micros"] > 0}
    zero_count = len(agg) - len(active)

    for aid in sorted(active.keys(), key=lambda x: active[x]["spend_micros"], reverse=True):
        info = active[aid]
        spend = fmt_money(info["spend_micros"])
        clicks = info["clicks"]
        impr = info["impressions"]
        subs = subs_data.get(aid, 0)
        cps = safe_div(spend, subs)
        cps_str = fmt_currency(cps) if subs > 0 else "-"

        display_name = info["name"][:49]
        display_camp = info["campaign"][:34]
        print(f"{display_name:<50} {display_camp:<35} {fmt_currency(spend):>10} {clicks:>7} {impr:>7} {subs:>6.1f} {cps_str:>10}")

        total_spend += spend
        total_clicks += clicks
        total_impr += impr
        total_subs += subs

    if zero_count > 0:
        print(f"  ... plus {zero_count} groups with $0 spend")

    print("-" * 130)
    cps = safe_div(total_spend, total_subs)
    cps_str = fmt_currency(cps) if total_subs > 0 else "-"
    print(f"{'TOTAL':<50} {'':35} {fmt_currency(total_spend):>10} {total_clicks:>7} {total_impr:>7} {total_subs:>6.1f} {cps_str:>10}")
    print("=" * 130)


def main():
    print("Connecting to Google Ads API...")
    client = get_client()

    # ---- MTD Campaign Data ----
    print("Pulling MTD campaign spend (Feb 1-22)...")
    mtd_spend = pull_spend(client, MTD_START, MTD_END)
    active_count = sum(1 for v in mtd_spend.values() if v["spend_micros"] > 0)
    print(f"  Found {len(mtd_spend)} non-brand Search/PMAX campaigns ({active_count} with spend)")

    print("Pulling MTD registration conversions...")
    mtd_regs = pull_conversions(client, MTD_START, MTD_END, "ph_registration_started")
    print(f"  Found regs for {len(mtd_regs)} campaigns")

    print("Pulling MTD subscription conversions...")
    mtd_subs = pull_conversions(client, MTD_START, MTD_END, "ph_subscription_created")
    print(f"  Found subs for {len(mtd_subs)} campaigns")

    print_campaign_table(mtd_spend, mtd_regs, mtd_subs, "MTD CAMPAIGN REPORT (Feb 1-22, 2026) - Search + PMAX, Non-Brand")

    # ---- Recent 7 days ----
    print("\nPulling recent 7-day data (Feb 16-22)...")
    recent_spend = pull_spend(client, RECENT_START, RECENT_END)
    recent_regs = pull_conversions(client, RECENT_START, RECENT_END, "ph_registration_started")
    recent_subs = pull_conversions(client, RECENT_START, RECENT_END, "ph_subscription_created")

    print_campaign_table(recent_spend, recent_regs, recent_subs, "RECENT TREND (Feb 16-22, 2026) - Last 7 Days")

    # ---- Experiment Ad Groups ----
    print("\n\nPulling experiment ad group data...")
    exp_data = pull_experiment_ad_groups(client, MTD_START, MTD_END)
    exp_subs = pull_experiment_ag_conversions(client, MTD_START, MTD_END, "ph_subscription_created")

    if exp_data:
        print_ag_table(exp_data, exp_subs, "EXPERIMENT AD GROUPS (Homepage Test) - MTD")
    else:
        print(f"\n{'='*80}")
        print("  EXPERIMENT AD GROUPS (Homepage Test) - MTD")
        print(f"{'='*80}")
        print("  No data yet (expected - experiment just created Feb 23)")
        print("  Ad Group IDs checked: " + ", ".join(str(i) for i in EXPERIMENT_AD_GROUP_IDS))
        print(f"{'='*80}")

    # ---- All ENABLED Search Ad Groups (non-brand) ----
    print("\n\nPulling all ENABLED Search ad groups (non-brand)...")
    search_ags = pull_enabled_search_ad_groups(client, MTD_START, MTD_END)
    print(f"  Found {len(search_ags)} enabled Search ad group rows")
    search_ag_subs = pull_search_ag_conversions(client, MTD_START, MTD_END, "ph_subscription_created")

    if search_ags:
        print_ag_table(search_ags, search_ag_subs, "ALL ENABLED SEARCH AD GROUPS (Non-Brand) - MTD Spend + Subs")

    # ---- All ENABLED PMAX Asset Groups (non-brand) ----
    print("\nPulling all ENABLED PMAX asset groups (non-brand)...")
    pmax_ags = pull_enabled_pmax_asset_groups(client, MTD_START, MTD_END)
    print(f"  Found {len(pmax_ags)} enabled PMAX asset group rows")
    pmax_ag_subs = pull_pmax_ag_conversions(client, MTD_START, MTD_END, "ph_subscription_created")

    if pmax_ags:
        print_ag_table(pmax_ags, pmax_ag_subs, "ALL ENABLED PMAX ASSET GROUPS (Non-Brand) - MTD Spend + Subs")

    print("\n\nDone.")


if __name__ == "__main__":
    main()
