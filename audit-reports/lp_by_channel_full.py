"""LP type split by Search vs PMAX with CPR/CPS - 1wk."""
import yaml
from google.ads.googleads.client import GoogleAdsClient
from collections import defaultdict

config_path = "/Users/jeffy/.config/google-ads-mcp/google-ads.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

client = GoogleAdsClient.load_from_dict(config)
service = client.get_service("GoogleAdsService")
customer_id = "8618096874"

date_range = "segments.date BETWEEN '2026-02-16' AND '2026-02-22'"

def categorize(url):
    if '/welcome-cms/' in url:
        return '/welcome-cms/*'
    elif '/welcome' in url:
        return '/welcome*'
    elif url.rstrip('/') == 'https://superpower.com' or url == 'https://superpower.com/':
        return 'Homepage (/)'
    elif '/checkout/' in url:
        return '/checkout/*'
    elif '/how-it-works' in url:
        return '/how-it-works'
    elif '/biomarkers' in url:
        return '/biomarkers'
    elif '/pricing' in url:
        return '/pricing'
    else:
        return 'Other'

def get_channel(row):
    ch_type = str(row.campaign.advertising_channel_type)
    return 'PMAX' if '10' in ch_type or 'PERFORMANCE_MAX' in ch_type else 'Search'

# channel -> url -> {cost, clicks, regs, subs}
raw = defaultdict(lambda: defaultdict(lambda: {'cost': 0, 'clicks': 0, 'regs': 0.0, 'subs': 0.0}))

# Cost
print("Pulling cost...")
query_cost = f"""
    SELECT
        landing_page_view.unexpanded_final_url,
        campaign.name, campaign.status, campaign.advertising_channel_type,
        metrics.cost_micros, metrics.clicks
    FROM landing_page_view
    WHERE {date_range}
        AND campaign.status != 'REMOVED'
        AND campaign.advertising_channel_type IN ('SEARCH', 'PERFORMANCE_MAX')
"""
response = service.search(customer_id=customer_id, query=query_cost)
for row in response:
    if 'brand' in row.campaign.name.lower():
        continue
    ch = get_channel(row)
    url = row.landing_page_view.unexpanded_final_url
    raw[ch][url]['cost'] += row.metrics.cost_micros / 1_000_000
    raw[ch][url]['clicks'] += row.metrics.clicks

# Regs
print("Pulling regs...")
query_reg = f"""
    SELECT
        landing_page_view.unexpanded_final_url,
        campaign.name, campaign.status, campaign.advertising_channel_type,
        segments.conversion_action_name, metrics.all_conversions
    FROM landing_page_view
    WHERE {date_range}
        AND segments.conversion_action_name = 'ph_registration_started'
        AND campaign.status != 'REMOVED'
        AND campaign.advertising_channel_type IN ('SEARCH', 'PERFORMANCE_MAX')
"""
response = service.search(customer_id=customer_id, query=query_reg)
for row in response:
    if 'brand' in row.campaign.name.lower():
        continue
    ch = get_channel(row)
    url = row.landing_page_view.unexpanded_final_url
    raw[ch][url]['regs'] += row.metrics.all_conversions

# Subs
print("Pulling subs...")
query_sub = f"""
    SELECT
        landing_page_view.unexpanded_final_url,
        campaign.name, campaign.status, campaign.advertising_channel_type,
        segments.conversion_action_name, metrics.all_conversions
    FROM landing_page_view
    WHERE {date_range}
        AND segments.conversion_action_name = 'ph_subscription_created'
        AND campaign.status != 'REMOVED'
        AND campaign.advertising_channel_type IN ('SEARCH', 'PERFORMANCE_MAX')
"""
response = service.search(customer_id=customer_id, query=query_sub)
for row in response:
    if 'brand' in row.campaign.name.lower():
        continue
    ch = get_channel(row)
    url = row.landing_page_view.unexpanded_final_url
    raw[ch][url]['subs'] += row.metrics.all_conversions

# Aggregate by category and print
for channel in ['Search', 'PMAX']:
    cats = defaultdict(lambda: {'cost': 0, 'clicks': 0, 'regs': 0.0, 'subs': 0.0})
    for url, d in raw[channel].items():
        cat = categorize(url)
        for k in ['cost', 'clicks', 'regs', 'subs']:
            cats[cat][k] += d[k]
    
    total_cost = sum(d['cost'] for d in cats.values())
    total_clicks = sum(d['clicks'] for d in cats.values())
    total_regs = sum(d['regs'] for d in cats.values())
    total_subs = sum(d['subs'] for d in cats.values())
    
    print(f"\n{'='*120}")
    print(f"  {channel} — 1WK (Feb 16-22) | Brand Excluded")
    print(f"  Total: ${total_cost:,.0f} spend | {total_clicks:,} clicks | {total_regs:.0f} regs | {total_subs:.0f} subs")
    print(f"{'='*120}")
    print(f"{'Category':<20} {'Clicks':>8} {'%Spend':>7} {'Spend':>10} {'Regs':>7} {'CPR':>8} {'Subs':>7} {'CPS':>8} {'R>S%':>7}")
    print('-'*120)
    
    sorted_cats = sorted(cats.items(), key=lambda x: x[1]['cost'], reverse=True)
    for cat, d in sorted_cats:
        if d['cost'] < 5:
            continue
        pct_spend = d['cost']/total_cost*100 if total_cost else 0
        cpr = f"${d['cost']/d['regs']:,.0f}" if d['regs'] > 0 else '-'
        cps = f"${d['cost']/d['subs']:,.0f}" if d['subs'] > 0 else '-'
        r2s = f"{d['subs']/d['regs']*100:.1f}%" if d['regs'] > 0 else '-'
        print(f"{cat:<20} {d['clicks']:>8,} {pct_spend:>6.1f}% ${d['cost']:>9,.0f} {d['regs']:>7.1f} {cpr:>8} {d['subs']:>7.1f} {cps:>8} {r2s:>7}")
    
    print('-'*120)
    total_cpr = f"${total_cost/total_regs:,.0f}" if total_regs else '-'
    total_cps = f"${total_cost/total_subs:,.0f}" if total_subs else '-'
    total_r2s = f"{total_subs/total_regs*100:.1f}%" if total_regs else '-'
    print(f"{'TOTAL':<20} {total_clicks:>8,} {'100%':>7} ${total_cost:>9,.0f} {total_regs:>7.1f} {total_cpr:>8} {total_subs:>7.1f} {total_cps:>8} {total_r2s:>7}")

