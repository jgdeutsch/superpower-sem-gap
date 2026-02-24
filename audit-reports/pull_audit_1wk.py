#!/usr/bin/env python3
"""Pull comprehensive Google Ads performance data for 1-week audit (Feb 16 - Feb 22, 2026)."""

import csv
import sys
import yaml
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Config
CONFIG_PATH = "/Users/jeffy/.config/google-ads-mcp/google-ads.yaml"
CUSTOMER_ID = "8618096874"

# Fixed date range: 1 week (Feb 16 - Feb 22, 2026)
DATE_FROM = "2026-02-16"
DATE_TO = "2026-02-22"

print(f"Date range: {DATE_FROM} to {DATE_TO} (1 week)")
print(f"Customer ID: {CUSTOMER_ID}")
print()

# Load config and create client
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

client = GoogleAdsClient.load_from_dict(config, version="v23")
ga_service = client.get_service("GoogleAdsService")


def run_query(query, description):
    """Run a GAQL query and return rows as list."""
    print(f"Running: {description}...")
    rows = []
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                rows.append(row)
        print(f"  -> {len(rows)} rows returned")
    except GoogleAdsException as ex:
        print(f"  -> ERROR:")
        for error in ex.failure.errors:
            print(f"     {error.message}")
        return None
    return rows


def write_csv(filepath, headers, data_rows):
    """Write list of list to CSV."""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data_rows)
    print(f"  -> Wrote {len(data_rows)} rows to {filepath}")


# --- QUERY 1: Search campaign ad groups (daily) ---
q1 = f"""
SELECT
  campaign.name,
  campaign.advertising_channel_type,
  ad_group.name,
  ad_group.status,
  metrics.cost_micros,
  metrics.clicks,
  metrics.impressions,
  metrics.conversions,
  segments.date
FROM ad_group
WHERE campaign.advertising_channel_type = 'SEARCH'
  AND campaign.status = 'ENABLED'
  AND segments.date BETWEEN '{DATE_FROM}' AND '{DATE_TO}'
ORDER BY segments.date DESC
"""

rows1 = run_query(q1, "Query 1: Search ad groups daily performance")
if rows1 is not None:
    data = []
    for r in rows1:
        data.append([
            r.campaign.name,
            r.ad_group.name,
            r.ad_group.status.name,
            r.segments.date,
            round(r.metrics.cost_micros / 1_000_000, 2),
            r.metrics.clicks,
            r.metrics.impressions,
            round(r.metrics.conversions, 2),
        ])
    write_csv("/tmp/audit_search_adgroups_daily_1wk.csv",
              ["campaign", "ad_group", "status", "date", "cost", "clicks", "impressions", "conversions"],
              data)

# --- QUERY 2: Search ad group conversions by action ---
q2 = f"""
SELECT
  campaign.name,
  campaign.advertising_channel_type,
  ad_group.name,
  segments.conversion_action_name,
  metrics.all_conversions,
  segments.date
FROM ad_group
WHERE campaign.advertising_channel_type = 'SEARCH'
  AND campaign.status = 'ENABLED'
  AND segments.date BETWEEN '{DATE_FROM}' AND '{DATE_TO}'
ORDER BY segments.date DESC
"""

rows2 = run_query(q2, "Query 2: Search ad group conversions by action")
if rows2 is not None:
    data = []
    for r in rows2:
        data.append([
            r.campaign.name,
            r.ad_group.name,
            r.segments.date,
            r.segments.conversion_action_name,
            round(r.metrics.all_conversions, 2),
        ])
    write_csv("/tmp/audit_search_conversions_by_action_1wk.csv",
              ["campaign", "ad_group", "date", "conversion_action", "all_conversions"],
              data)

# --- QUERY 3: PMAX asset groups (daily) ---
q3 = f"""
SELECT
  campaign.name,
  campaign.advertising_channel_type,
  asset_group.name,
  asset_group.status,
  metrics.cost_micros,
  metrics.clicks,
  metrics.impressions,
  metrics.conversions,
  segments.date
FROM asset_group
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
  AND campaign.status = 'ENABLED'
  AND segments.date BETWEEN '{DATE_FROM}' AND '{DATE_TO}'
ORDER BY segments.date DESC
"""

rows3 = run_query(q3, "Query 3: PMAX asset groups daily performance")
if rows3 is not None:
    data = []
    for r in rows3:
        data.append([
            r.campaign.name,
            r.asset_group.name,
            r.asset_group.status.name,
            r.segments.date,
            round(r.metrics.cost_micros / 1_000_000, 2),
            r.metrics.clicks,
            r.metrics.impressions,
            round(r.metrics.conversions, 2),
        ])
    write_csv("/tmp/audit_pmax_assetgroups_daily_1wk.csv",
              ["campaign", "asset_group", "status", "date", "cost", "clicks", "impressions", "conversions"],
              data)

# --- QUERY 4: PMAX asset group conversions by action ---
q4 = f"""
SELECT
  campaign.name,
  campaign.advertising_channel_type,
  asset_group.name,
  segments.conversion_action_name,
  metrics.all_conversions,
  segments.date
FROM asset_group
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
  AND campaign.status = 'ENABLED'
  AND segments.date BETWEEN '{DATE_FROM}' AND '{DATE_TO}'
ORDER BY segments.date DESC
"""

rows4 = run_query(q4, "Query 4: PMAX asset group conversions by action")
if rows4 is not None:
    data = []
    for r in rows4:
        data.append([
            r.campaign.name,
            r.asset_group.name,
            r.segments.date,
            r.segments.conversion_action_name,
            round(r.metrics.all_conversions, 2),
        ])
    write_csv("/tmp/audit_pmax_conversions_by_action_1wk.csv",
              ["campaign", "asset_group", "date", "conversion_action", "all_conversions"],
              data)

# --- QUERY 5: Search terms ---
q5 = f"""
SELECT
  campaign.name,
  campaign.advertising_channel_type,
  ad_group.name,
  search_term_view.search_term,
  metrics.cost_micros,
  metrics.clicks,
  metrics.impressions,
  metrics.conversions,
  segments.date
FROM search_term_view
WHERE campaign.advertising_channel_type = 'SEARCH'
  AND campaign.status = 'ENABLED'
  AND segments.date BETWEEN '{DATE_FROM}' AND '{DATE_TO}'
ORDER BY metrics.cost_micros DESC
"""

rows5 = run_query(q5, "Query 5: Search terms for search campaigns")
if rows5 is not None:
    data = []
    for r in rows5:
        data.append([
            r.campaign.name,
            r.ad_group.name,
            r.search_term_view.search_term,
            r.segments.date,
            round(r.metrics.cost_micros / 1_000_000, 2),
            r.metrics.clicks,
            r.metrics.impressions,
            round(r.metrics.conversions, 2),
        ])
    write_csv("/tmp/audit_search_terms_1wk.csv",
              ["campaign", "ad_group", "search_term", "date", "cost", "clicks", "impressions", "conversions"],
              data)

# --- QUERY 6: Landing pages for search campaigns ---
q6 = f"""
SELECT
  campaign.name,
  campaign.advertising_channel_type,
  landing_page_view.unexpanded_final_url,
  metrics.cost_micros,
  metrics.clicks,
  metrics.impressions,
  metrics.conversions,
  segments.date
FROM landing_page_view
WHERE campaign.advertising_channel_type = 'SEARCH'
  AND campaign.status = 'ENABLED'
  AND segments.date BETWEEN '{DATE_FROM}' AND '{DATE_TO}'
ORDER BY metrics.cost_micros DESC
"""

rows6 = run_query(q6, "Query 6: Landing pages for search campaigns")
if rows6 is not None:
    data = []
    for r in rows6:
        data.append([
            r.campaign.name,
            r.landing_page_view.unexpanded_final_url,
            r.segments.date,
            round(r.metrics.cost_micros / 1_000_000, 2),
            r.metrics.clicks,
            r.metrics.impressions,
            round(r.metrics.conversions, 2),
        ])
    write_csv("/tmp/audit_landing_pages_1wk.csv",
              ["campaign", "landing_page_url", "date", "cost", "clicks", "impressions", "conversions"],
              data)

print()
print("=" * 60)
print("DONE. All CSV files written to /tmp/audit_*_1wk.csv")
print("=" * 60)
