#!/usr/bin/env python3
"""
Comprehensive Google Ads Audit Analysis v3
4-week data: Jan 26 - Feb 22, 2026
BRAND EXCLUDED: Filters out all brand campaigns and brand-themed ad/asset groups.
With CPR (Cost per Registration) and CPS (Cost per Subscription) as explicit columns.
"""

import pandas as pd
import numpy as np
import sys
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 300)

# ─────────────────────────────────────────────────────────────────────
# Redirect all output to report file
# ─────────────────────────────────────────────────────────────────────
output_file = '/tmp/audit_report_v3.txt'
original_stdout = sys.stdout
sys.stdout = open(output_file, 'w')

# ─────────────────────────────────────────────────────────────────────
# UTILITY: Box-drawing table printer
# ─────────────────────────────────────────────────────────────────────

def is_blank(val):
    """Check if value is blank/empty/NaN"""
    if val is None:
        return True
    if isinstance(val, str) and val.strip() == '':
        return True
    if isinstance(val, float) and np.isnan(val):
        return True
    return False

def fmt_money(val):
    if is_blank(val):
        return "-"
    try:
        val = float(val)
    except (ValueError, TypeError):
        return str(val)
    if np.isnan(val):
        return "-"
    if abs(val) >= 10:
        return f"${val:,.0f}"
    else:
        return f"${val:,.2f}"

def fmt_pct(val):
    if is_blank(val):
        return "-"
    try:
        val = float(val)
    except (ValueError, TypeError):
        return str(val)
    if np.isnan(val):
        return "-"
    return f"{val:.1f}%"

def fmt_num(val, decimals=0):
    if is_blank(val):
        return "-"
    try:
        val = float(val)
    except (ValueError, TypeError):
        return str(val)
    if np.isnan(val):
        return "-"
    if decimals == 0:
        return f"{val:,.0f}"
    return f"{val:,.{decimals}f}"

def fmt_val(val, fmt_type):
    if isinstance(val, str) and val.strip() == '':
        return ""
    if fmt_type == 'money':
        return fmt_money(val)
    elif fmt_type == 'pct':
        return fmt_pct(val)
    elif fmt_type == 'num':
        return fmt_num(val, 0)
    elif fmt_type == 'num1':
        return fmt_num(val, 1)
    elif fmt_type == 'num2':
        return fmt_num(val, 2)
    elif fmt_type == 'str':
        return str(val) if val is not None else "-"
    return str(val)

def print_box_table(headers, rows, col_formats, col_aligns=None, title=None, total_row=None):
    if col_aligns is None:
        col_aligns = ['l' if f == 'str' else 'r' for f in col_formats]

    formatted_rows = []
    for row in rows:
        formatted = []
        for i, val in enumerate(row):
            formatted.append(fmt_val(val, col_formats[i]))
        formatted_rows.append(formatted)

    formatted_total = None
    if total_row:
        formatted_total = []
        for i, val in enumerate(total_row):
            formatted_total.append(fmt_val(val, col_formats[i]))

    all_rows_for_width = [headers] + formatted_rows
    if formatted_total:
        all_rows_for_width.append(formatted_total)

    col_widths = []
    for i in range(len(headers)):
        max_w = len(str(headers[i]))
        for row in all_rows_for_width:
            if i < len(row):
                max_w = max(max_w, len(str(row[i])))
        col_widths.append(max_w)

    def make_line(left, mid, right, fill):
        parts = [fill * (w + 2) for w in col_widths]
        return left + mid.join(parts) + right

    def make_row(cells, aligns):
        parts = []
        for i, cell in enumerate(cells):
            s = str(cell)
            w = col_widths[i]
            if aligns[i] == 'r':
                parts.append(' ' + s.rjust(w) + ' ')
            else:
                parts.append(' ' + s.ljust(w) + ' ')
        return '│' + '│'.join(parts) + '│'

    top_line = make_line('┌', '┬', '┐', '─')
    header_sep = make_line('├', '┼', '┤', '─')
    double_sep = make_line('╠', '╬', '╣', '═')
    bottom_line = make_line('└', '┴', '┘', '─')

    if title:
        print(f"\n{'=' * 80}")
        print(f"  {title}")
        print(f"{'=' * 80}")

    print(top_line)
    print(make_row(headers, ['l'] * len(headers)))
    print(header_sep)

    for row in formatted_rows:
        print(make_row(row, col_aligns))

    if formatted_total:
        print(double_sep)
        print(make_row(formatted_total, col_aligns))

    print(bottom_line)
    print(f"  ({len(rows)} rows)")


def safe_div(num, denom):
    if denom == 0 or pd.isna(denom):
        return np.nan
    return num / denom


# ─────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────

print("\n" + "=" * 80)
print("  LOADING DATA... (BRAND EXCLUDED VERSION)")
print("=" * 80)

search_daily = pd.read_csv('/tmp/audit_search_adgroups_daily_4wk.csv')
search_conv = pd.read_csv('/tmp/audit_search_conversions_by_action_4wk.csv')
pmax_daily = pd.read_csv('/tmp/audit_pmax_assetgroups_daily_4wk.csv')
pmax_conv = pd.read_csv('/tmp/audit_pmax_conversions_by_action_4wk.csv')
search_terms = pd.read_csv('/tmp/audit_search_terms_4wk.csv')
landing_pages = pd.read_csv('/tmp/audit_landing_pages_4wk.csv')

print(f"  BEFORE brand filter:")
print(f"  Search daily rows:    {len(search_daily):,}")
print(f"  Search conv rows:     {len(search_conv):,}")
print(f"  PMAX daily rows:      {len(pmax_daily):,}")
print(f"  PMAX conv rows:       {len(pmax_conv):,}")
print(f"  Search terms rows:    {len(search_terms):,}")
print(f"  Landing pages rows:   {len(landing_pages):,}")

# ─────────────────────────────────────────────────────────────────────
# FILTER OUT BRAND CAMPAIGNS (case-insensitive)
# ─────────────────────────────────────────────────────────────────────

print(f"\n  FILTERING: Excluding campaigns where campaign_name contains 'Brand' (case-insensitive)")

# Filter each dataframe - remove rows where campaign contains "brand"
search_daily = search_daily[~search_daily['campaign'].str.contains('brand', case=False, na=False)]
search_conv = search_conv[~search_conv['campaign'].str.contains('brand', case=False, na=False)]
pmax_daily = pmax_daily[~pmax_daily['campaign'].str.contains('brand', case=False, na=False)]
pmax_conv = pmax_conv[~pmax_conv['campaign'].str.contains('brand', case=False, na=False)]
search_terms = search_terms[~search_terms['campaign'].str.contains('brand', case=False, na=False)]
landing_pages = landing_pages[~landing_pages['campaign'].str.contains('brand', case=False, na=False)]

# Also filter out brand-themed ad groups from search data
search_daily = search_daily[~search_daily['ad_group'].str.contains('brand', case=False, na=False)]
search_conv = search_conv[~search_conv['ad_group'].str.contains('brand', case=False, na=False)]
search_terms = search_terms[~search_terms['ad_group'].str.contains('brand', case=False, na=False)]

# Also filter out brand-themed asset groups from PMAX data
pmax_daily = pmax_daily[~pmax_daily['asset_group'].str.contains('brand', case=False, na=False)]
pmax_conv = pmax_conv[~pmax_conv['asset_group'].str.contains('brand', case=False, na=False)]

print(f"\n  AFTER brand filter:")
print(f"  Search daily rows:    {len(search_daily):,}")
print(f"  Search conv rows:     {len(search_conv):,}")
print(f"  PMAX daily rows:      {len(pmax_daily):,}")
print(f"  PMAX conv rows:       {len(pmax_conv):,}")
print(f"  Search terms rows:    {len(search_terms):,}")
print(f"  Landing pages rows:   {len(landing_pages):,}")

# ─────────────────────────────────────────────────────────────────────
# AGGREGATE: Search ad groups
# ─────────────────────────────────────────────────────────────────────

search_agg = search_daily.groupby(['campaign', 'ad_group', 'status']).agg(
    spend=('cost', 'sum'),
    clicks=('clicks', 'sum'),
    impressions=('impressions', 'sum'),
    conversions=('conversions', 'sum')
).reset_index()

search_regs = search_conv[search_conv['conversion_action'] == 'ph_registration_started'].groupby(
    ['campaign', 'ad_group']
)['all_conversions'].sum().reset_index().rename(columns={'all_conversions': 'regs'})

search_subs = search_conv[search_conv['conversion_action'] == 'ph_subscription_created'].groupby(
    ['campaign', 'ad_group']
)['all_conversions'].sum().reset_index().rename(columns={'all_conversions': 'subs'})

search_agg = search_agg.merge(search_regs, on=['campaign', 'ad_group'], how='left')
search_agg = search_agg.merge(search_subs, on=['campaign', 'ad_group'], how='left')
search_agg['regs'] = search_agg['regs'].fillna(0)
search_agg['subs'] = search_agg['subs'].fillna(0)

def get_search_type(campaign):
    if 'DSA' in campaign:
        return 'DSA'
    return 'Search'

search_agg['type'] = search_agg['campaign'].apply(get_search_type)
search_agg = search_agg.rename(columns={'ad_group': 'group_name', 'campaign': 'campaign_name', 'status': 'group_status'})

# ─────────────────────────────────────────────────────────────────────
# AGGREGATE: PMAX asset groups
# ─────────────────────────────────────────────────────────────────────

pmax_agg = pmax_daily.groupby(['campaign', 'asset_group', 'status']).agg(
    spend=('cost', 'sum'),
    clicks=('clicks', 'sum'),
    impressions=('impressions', 'sum'),
    conversions=('conversions', 'sum')
).reset_index()

pmax_regs = pmax_conv[pmax_conv['conversion_action'] == 'ph_registration_started'].groupby(
    ['campaign', 'asset_group']
)['all_conversions'].sum().reset_index().rename(columns={'all_conversions': 'regs'})

pmax_subs = pmax_conv[pmax_conv['conversion_action'] == 'ph_subscription_created'].groupby(
    ['campaign', 'asset_group']
)['all_conversions'].sum().reset_index().rename(columns={'all_conversions': 'subs'})

pmax_agg = pmax_agg.merge(pmax_regs, on=['campaign', 'asset_group'], how='left')
pmax_agg = pmax_agg.merge(pmax_subs, on=['campaign', 'asset_group'], how='left')
pmax_agg['regs'] = pmax_agg['regs'].fillna(0)
pmax_agg['subs'] = pmax_agg['subs'].fillna(0)
pmax_agg['type'] = 'PMAX'
pmax_agg = pmax_agg.rename(columns={'asset_group': 'group_name', 'campaign': 'campaign_name', 'status': 'group_status'})

# ─────────────────────────────────────────────────────────────────────
# COMBINE into master table
# ─────────────────────────────────────────────────────────────────────

cols = ['group_name', 'campaign_name', 'type', 'group_status', 'spend', 'clicks', 'impressions', 'conversions', 'regs', 'subs']
master = pd.concat([search_agg[cols], pmax_agg[cols]], ignore_index=True)

master['ctr'] = master.apply(lambda r: safe_div(r['clicks'], r['impressions']) * 100, axis=1)
master['cpc'] = master.apply(lambda r: safe_div(r['spend'], r['clicks']), axis=1)
master['cpr'] = master.apply(lambda r: safe_div(r['spend'], r['regs']), axis=1)
master['cps'] = master.apply(lambda r: safe_div(r['spend'], r['subs']), axis=1)
master['reg_sub_pct'] = master.apply(lambda r: safe_div(r['subs'], r['regs']) * 100, axis=1)

def classify(row):
    if row['subs'] > 0 and row['cps'] < 350:
        return 'GOOD'
    elif row['subs'] > 0 and row['cps'] <= 500:
        return 'MIDDLE'
    elif row['subs'] == 0 and row['spend'] >= 500:
        return 'BAD'
    elif row['subs'] > 0 and row['cps'] > 500:
        return 'BAD'
    else:
        return 'LOW-SPEND'

master['classification'] = master.apply(classify, axis=1)

# ─────────────────────────────────────────────────────────────────────
# ADDITIONAL FILTER: Remove brand-themed groups from master table
# ─────────────────────────────────────────────────────────────────────

def get_theme(group_name):
    g = group_name.lower()
    if 'brand' in g:
        return 'brand'
    gen_health_names = ['blood tests general', 'blood work', 'lab test', 'lab tests online', 'medical test',
             'test', 'health testing', 'health check', 'health and wellness test', 'health assessment',
             'blood test - general', 'blood test', 'blood test (compliant)', 'at-home blood test',
             'best blood test service', 'comprehensive panel', 'specialty tests',
             'blood test - top converting search interests (female & unknown)',
             'blood test - top converting search interests (male & unknown)']
    if g in gen_health_names:
        return 'general_health'
    if any(x in g for x in ['hormone', 'testosterone', 'estrogen', 'menopause', 't blood tests']):
        return 'hormone'
    if any(x in g for x in ['vitamin', 'nutrient', 'mineral', 'iron', 'ferritin', 'b12']):
        return 'vitamin_nutrient'
    if any(x in g for x in ['heart', 'cholesterol', 'cardiovascular', 'lipid', 'ldl', 'apob', 'lp(a)']):
        return 'heart_cholesterol'
    if any(x in g for x in ['diabetes', 'glucose', 'insulin', 'metabolic', 'prediabetes', 'cgm',
                              'continuous glucose']):
        return 'diabetes_metabolic'
    if any(x in g for x in ['inflammat', 'autoimmune', 'crp', 'lupus', 'rheumatoid', 'worst inflammatory']):
        return 'inflammation'
    if any(x in g for x in ['cancer', 'galleri', 'prostate']):
        return 'cancer'
    if any(x in g for x in ['kidney', 'liver', 'hepat', 'alt ', 'ast ', 'alk', 'alp', 'alt alkaline',
                              'alanine', 'hepatic', 'urea']):
        return 'kidney_liver'
    if any(x in g for x in ['thyroid', 'tsh', 'hashimoto', 'hyperthyroid', 'overactive thyroid']):
        return 'thyroid'
    if any(x in g for x in ['longevity', 'aging', 'age blood', 'biological age', 'epigenetic',
                              'igf']):
        return 'longevity'
    if any(x in g for x in ['gut', 'celiac', 'gluten']):
        return 'gut'
    if any(x in g for x in ['dyslipidemia', 'gout', 'disease screening', 'adrenal', 'stress',
                              'immune', 'energy', 'body composition', 'body fat', 'gene test',
                              'cbc', 'cmp', 'bmp', 'biomarker', 'creatine kinase']):
        return 'specific_condition'
    if any(x in g for x in ['function health', 'competitor']):
        return 'competitor'
    return 'other'

master['theme'] = master['group_name'].apply(get_theme)

# Count brand-themed groups being removed
brand_themed_count = len(master[master['theme'] == 'brand'])
brand_themed_spend = master[master['theme'] == 'brand']['spend'].sum()
print(f"\n  Brand-themed groups removed from master: {brand_themed_count} (${brand_themed_spend:,.0f} spend)")

# Remove brand-themed groups
master = master[master['theme'] != 'brand'].reset_index(drop=True)

master = master.sort_values('cps', ascending=True, na_position='last').reset_index(drop=True)

print(f"\n  Master table (brand excluded): {len(master)} groups")
print(f"  Total spend: ${master['spend'].sum():,.2f}")
print(f"  Total regs:  {master['regs'].sum():,.1f}")
print(f"  Total subs:  {master['subs'].sum():,.1f}")

# ─────────────────────────────────────────────────────────────────────
# SECTION 1: MASTER TABLE
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 1: MASTER TABLE - All Non-Brand Groups Sorted by CPS Ascending   ║")
print("╚" + "═" * 78 + "╝")

headers = ['#', 'Group Name', 'Campaign', 'Type', 'Status', 'Spend', 'Clicks', 'Impr',
           'CTR', 'CPC', 'Regs', 'CPR', 'Subs', 'CPS', 'Reg>Sub%', 'Class']
col_formats = ['str', 'str', 'str', 'str', 'str', 'money', 'num', 'num',
               'pct', 'money', 'num1', 'money', 'num1', 'money', 'pct', 'str']
col_aligns = ['r', 'l', 'l', 'l', 'l', 'r', 'r', 'r',
              'r', 'r', 'r', 'r', 'r', 'r', 'r', 'l']

rows = []
for i, r in master.iterrows():
    gname = str(r['group_name'])[:45]
    cname = str(r['campaign_name'])[:40]
    rows.append([
        str(i + 1), gname, cname, r['type'], r['group_status'],
        r['spend'], r['clicks'], r['impressions'],
        r['ctr'], r['cpc'], r['regs'], r['cpr'],
        r['subs'], r['cps'], r['reg_sub_pct'], r['classification']
    ])

total_spend = master['spend'].sum()
total_clicks = master['clicks'].sum()
total_impr = master['impressions'].sum()
total_regs = master['regs'].sum()
total_subs = master['subs'].sum()
total_row = [
    '', 'TOTAL', '', '', '',
    total_spend, total_clicks, total_impr,
    safe_div(total_clicks, total_impr) * 100,
    safe_div(total_spend, total_clicks),
    total_regs,
    safe_div(total_spend, total_regs),
    total_subs,
    safe_div(total_spend, total_subs),
    safe_div(total_subs, total_regs) * 100,
    ''
]

print_box_table(headers, rows, col_formats, col_aligns, total_row=total_row)

# ─────────────────────────────────────────────────────────────────────
# SECTION 2: CLASSIFICATION SUMMARY
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 2: CLASSIFICATION SUMMARY (Brand Excluded)" + " " * 25 + "║")
print("╚" + "═" * 78 + "╝")

class_order = ['GOOD', 'MIDDLE', 'BAD', 'LOW-SPEND']
class_rows = []
for cls in class_order:
    subset = master[master['classification'] == cls]
    if len(subset) == 0:
        continue
    cnt = len(subset)
    sp = subset['spend'].sum()
    sp_pct = safe_div(sp, total_spend) * 100
    rg = subset['regs'].sum()
    sb = subset['subs'].sum()
    sb_pct = safe_div(sb, total_subs) * 100 if total_subs > 0 else np.nan
    bl_cpr = safe_div(sp, rg)
    bl_cps = safe_div(sp, sb)
    avg_rs = subset['reg_sub_pct'].mean()
    med_ctr = subset['ctr'].median()
    med_cpc = subset['cpc'].median()
    med_cpr = subset['cpr'].median()
    med_cps = subset['cps'].median()
    class_rows.append([cls, cnt, sp, sp_pct, rg, sb, sb_pct, bl_cpr, bl_cps, avg_rs, med_ctr, med_cpc, med_cpr, med_cps])

cls_headers = ['Class', 'Count', 'Spend', '% Spend', 'Regs', 'Subs', '% Subs',
               'Blend CPR', 'Blend CPS', 'Avg R>S%', 'Med CTR', 'Med CPC', 'Med CPR', 'Med CPS']
cls_formats = ['str', 'num', 'money', 'pct', 'num1', 'num1', 'pct',
               'money', 'money', 'pct', 'pct', 'money', 'money', 'money']
cls_aligns = ['l', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']

cls_total = ['TOTAL', len(master), total_spend, 100.0, total_regs, total_subs, 100.0,
             safe_div(total_spend, total_regs), safe_div(total_spend, total_subs),
             master['reg_sub_pct'].mean(),
             master['ctr'].median(), master['cpc'].median(), master['cpr'].median(), master['cps'].median()]

print_box_table(cls_headers, class_rows, cls_formats, cls_aligns, total_row=cls_total)

# ─────────────────────────────────────────────────────────────────────
# SECTION 3: CAMPAIGN-LEVEL ROLLUP
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 3: CAMPAIGN-LEVEL ROLLUP (Brand Excluded)" + " " * 26 + "║")
print("╚" + "═" * 78 + "╝")

camp_agg = master.groupby('campaign_name').agg(
    spend=('spend', 'sum'),
    clicks=('clicks', 'sum'),
    impressions=('impressions', 'sum'),
    regs=('regs', 'sum'),
    subs=('subs', 'sum')
).reset_index()

camp_agg['ctr'] = camp_agg.apply(lambda r: safe_div(r['clicks'], r['impressions']) * 100, axis=1)
camp_agg['cpc'] = camp_agg.apply(lambda r: safe_div(r['spend'], r['clicks']), axis=1)
camp_agg['cpr'] = camp_agg.apply(lambda r: safe_div(r['spend'], r['regs']), axis=1)
camp_agg['cps'] = camp_agg.apply(lambda r: safe_div(r['spend'], r['subs']), axis=1)
camp_agg['reg_sub_pct'] = camp_agg.apply(lambda r: safe_div(r['subs'], r['regs']) * 100, axis=1)
camp_agg = camp_agg.sort_values('spend', ascending=False)

camp_headers = ['Campaign', 'Spend', 'Clicks', 'CTR', 'CPC', 'Regs', 'CPR', 'Subs', 'CPS', 'Reg>Sub%']
camp_formats = ['str', 'money', 'num', 'pct', 'money', 'num1', 'money', 'num1', 'money', 'pct']
camp_aligns = ['l', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']

camp_rows = []
for _, r in camp_agg.iterrows():
    camp_rows.append([
        str(r['campaign_name'])[:55],
        r['spend'], r['clicks'], r['ctr'], r['cpc'],
        r['regs'], r['cpr'], r['subs'], r['cps'], r['reg_sub_pct']
    ])

camp_total = ['TOTAL', total_spend, total_clicks,
              safe_div(total_clicks, total_impr) * 100,
              safe_div(total_spend, total_clicks),
              total_regs, safe_div(total_spend, total_regs),
              total_subs, safe_div(total_spend, total_subs),
              safe_div(total_subs, total_regs) * 100]

print_box_table(camp_headers, camp_rows, camp_formats, camp_aligns, total_row=camp_total)

# ─────────────────────────────────────────────────────────────────────
# SECTION 4: STRATEGY-LEVEL ROLLUP
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 4: STRATEGY-LEVEL ROLLUP (Brand Excluded)" + " " * 26 + "║")
print("╚" + "═" * 78 + "╝")

def get_strategy(campaign):
    c = campaign.lower()
    if 'brand' in c:
        return 'Brand'
    elif 'sem-gap' in c or 'sem_gap' in c:
        return 'SEM-Gap'
    elif 'diagnostic-discovery' in c or 'diagnostic_discovery' in c or 'generic' in c:
        return 'Generic/Diag-Discovery'
    elif 'pmax' in c or 'prospecting' in c:
        return 'Prospecting/PMAX'
    elif 'dsa' in c:
        return 'DSA'
    elif 'competitor' in c:
        return 'Competitors'
    elif 'rx' in c or 'rxfrontdoor' in c:
        return 'RxFrontDoor'
    else:
        return 'Other'

master['strategy'] = master['campaign_name'].apply(get_strategy)

strat_rows = []
# Note: 'Brand' strategy should be empty after filtering, but we include it in the loop for completeness
for strat in ['Brand', 'SEM-Gap', 'Generic/Diag-Discovery', 'Prospecting/PMAX', 'DSA', 'Competitors', 'RxFrontDoor', 'Other']:
    subset = master[master['strategy'] == strat]
    if len(subset) == 0:
        continue
    sp = subset['spend'].sum()
    rg = subset['regs'].sum()
    sb = subset['subs'].sum()
    g_cnt = len(subset[subset['classification'] == 'GOOD'])
    m_cnt = len(subset[subset['classification'] == 'MIDDLE'])
    b_cnt = len(subset[subset['classification'] == 'BAD'])
    ls_cnt = len(subset[subset['classification'] == 'LOW-SPEND'])
    strat_rows.append([
        strat, sp, rg, safe_div(sp, rg), sb, safe_div(sp, sb),
        safe_div(sb, rg) * 100 if rg > 0 else np.nan,
        g_cnt, m_cnt, b_cnt, ls_cnt
    ])

strat_headers = ['Strategy', 'Spend', 'Regs', 'CPR', 'Subs', 'CPS', 'Reg>Sub%', 'GOOD', 'MID', 'BAD', 'LOW$']
strat_formats = ['str', 'money', 'num1', 'money', 'num1', 'money', 'pct', 'num', 'num', 'num', 'num']
strat_aligns = ['l', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']

print_box_table(strat_headers, strat_rows, strat_formats, strat_aligns)

# ─────────────────────────────────────────────────────────────────────
# SECTION 5: THEME PERFORMANCE
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 5: THEME PERFORMANCE (Brand Excluded)" + " " * 30 + "║")
print("╚" + "═" * 78 + "╝")

# Theme already assigned above; brand theme already filtered out

theme_rows = []
for theme in sorted(master['theme'].unique()):
    subset = master[master['theme'] == theme]
    cnt = len(subset)
    sp = subset['spend'].sum()
    rg = subset['regs'].sum()
    sb = subset['subs'].sum()
    cl = subset['clicks'].sum()
    imp = subset['impressions'].sum()
    g_cnt = len(subset[subset['classification'] == 'GOOD'])
    m_cnt = len(subset[subset['classification'] == 'MIDDLE'])
    b_cnt = len(subset[subset['classification'] == 'BAD'])
    theme_rows.append([
        theme, cnt, sp, rg, safe_div(sp, rg), sb, safe_div(sp, sb),
        safe_div(cl, imp) * 100 if imp > 0 else np.nan,
        safe_div(sb, rg) * 100 if rg > 0 else np.nan,
        f"{g_cnt}/{m_cnt}/{b_cnt}"
    ])

theme_rows.sort(key=lambda x: x[2], reverse=True)

theme_headers = ['Theme', 'Grps', 'Spend', 'Regs', 'CPR', 'Subs', 'CPS', 'CTR', 'Reg>Sub%', 'G/M/B']
theme_formats = ['str', 'num', 'money', 'num1', 'money', 'num1', 'money', 'pct', 'pct', 'str']
theme_aligns = ['l', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']

print_box_table(theme_headers, theme_rows, theme_formats, theme_aligns)

# ─────────────────────────────────────────────────────────────────────
# SECTION 6: SEARCH TERM ANALYSIS
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 6: SEARCH TERM ANALYSIS BY CLASSIFICATION (Brand Excluded)       ║")
print("╚" + "═" * 78 + "╝")

class_map = dict(zip(
    zip(master['campaign_name'], master['group_name']),
    master['classification']
))

search_terms['classification'] = search_terms.apply(
    lambda r: class_map.get((r['campaign'], r['ad_group']), 'UNKNOWN'), axis=1
)

st_agg = search_terms.groupby(['classification', 'search_term']).agg(
    spend=('cost', 'sum'),
    clicks=('clicks', 'sum'),
    impressions=('impressions', 'sum'),
    conversions=('conversions', 'sum')
).reset_index()

st_agg['ctr'] = st_agg.apply(lambda r: safe_div(r['clicks'], r['impressions']) * 100, axis=1)
st_agg['cpc'] = st_agg.apply(lambda r: safe_div(r['spend'], r['clicks']), axis=1)
st_agg['conv_rate'] = st_agg.apply(lambda r: safe_div(r['conversions'], r['clicks']) * 100, axis=1)

st_headers = ['Search Term', 'Spend', 'Clicks', 'CTR', 'CPC', 'Conv', 'Conv%']
st_formats = ['str', 'money', 'num', 'pct', 'money', 'num1', 'pct']
st_aligns = ['l', 'r', 'r', 'r', 'r', 'r', 'r']

for cls in ['GOOD', 'MIDDLE', 'BAD', 'LOW-SPEND']:
    subset = st_agg[st_agg['classification'] == cls].sort_values('spend', ascending=False).head(15)
    if len(subset) == 0:
        continue
    full_subset = st_agg[st_agg['classification'] == cls]
    unique_terms = len(full_subset)
    top_spend_val = full_subset.sort_values('spend', ascending=False).head(1)['spend'].values[0] if len(full_subset) > 0 else 0
    total_st_spend = full_subset['spend'].sum()
    top_conc = safe_div(top_spend_val, total_st_spend) * 100

    print(f"\n  --- {cls} Groups: Top 15 Search Terms by Spend ---")
    print(f"  Unique terms: {unique_terms:,} | Top-term concentration: {fmt_pct(top_conc)} | Total spend: ${total_st_spend:,.0f}")

    st_rows = []
    for _, r in subset.iterrows():
        st_rows.append([
            str(r['search_term'])[:55],
            r['spend'], r['clicks'], r['ctr'], r['cpc'], r['conversions'], r['conv_rate']
        ])
    print_box_table(st_headers, st_rows, st_formats, st_aligns)

# ─────────────────────────────────────────────────────────────────────
# SECTION 7: LANDING PAGE PERFORMANCE
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 7: LANDING PAGE PERFORMANCE ($200+ Spend, Brand Excluded)        ║")
print("╚" + "═" * 78 + "╝")

lp_agg = landing_pages.groupby('landing_page_url').agg(
    spend=('cost', 'sum'),
    clicks=('clicks', 'sum'),
    impressions=('impressions', 'sum'),
    conversions=('conversions', 'sum')
).reset_index()

lp_agg['ctr'] = lp_agg.apply(lambda r: safe_div(r['clicks'], r['impressions']) * 100, axis=1)
lp_agg['cpc'] = lp_agg.apply(lambda r: safe_div(r['spend'], r['clicks']), axis=1)
lp_agg['conv_rate'] = lp_agg.apply(lambda r: safe_div(r['conversions'], r['clicks']) * 100, axis=1)

lp_filtered = lp_agg[lp_agg['spend'] >= 200].sort_values('conv_rate', ascending=False)

lp_headers = ['Landing Page', 'Spend', 'Clicks', 'CTR', 'CPC', 'Conv', 'Conv%']
lp_formats = ['str', 'money', 'num', 'pct', 'money', 'num1', 'pct']
lp_aligns = ['l', 'r', 'r', 'r', 'r', 'r', 'r']

lp_rows = []
for _, r in lp_filtered.iterrows():
    url = str(r['landing_page_url'])
    url = url.replace('https://superpower.com', 'sp.com').replace('https://www.superpower.com', 'sp.com')
    url = url[:50]
    lp_rows.append([url, r['spend'], r['clicks'], r['ctr'], r['cpc'], r['conversions'], r['conv_rate']])

print_box_table(lp_headers, lp_rows, lp_formats, lp_aligns)

# ─────────────────────────────────────────────────────────────────────
# SECTION 8: CPR vs CPS DISTRIBUTION ANALYSIS
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 8: CPR vs CPS DISTRIBUTION ANALYSIS (Brand Excluded)             ║")
print("╚" + "═" * 78 + "╝")

has_both = master[(master['regs'] > 0) & (master['subs'] > 0)].copy()

print(f"\n  Groups with both regs AND subs: {len(has_both)}")
print(f"  Groups with regs but NO subs:  {len(master[(master['regs'] > 0) & (master['subs'] == 0)])}")
print(f"  Groups with NO regs:           {len(master[master['regs'] == 0])}")

print("\n  --- CPR vs CPS Side-by-Side (groups with both regs & subs) ---")
cpr_cps_headers = ['Group Name', 'Spend', 'Regs', 'CPR', 'Subs', 'CPS', 'Reg>Sub%', 'Class']
cpr_cps_formats = ['str', 'money', 'num1', 'money', 'num1', 'money', 'pct', 'str']
cpr_cps_aligns = ['l', 'r', 'r', 'r', 'r', 'r', 'r', 'l']

cpr_cps_rows = []
for _, r in has_both.sort_values('cps').iterrows():
    cpr_cps_rows.append([
        str(r['group_name'])[:45], r['spend'], r['regs'], r['cpr'],
        r['subs'], r['cps'], r['reg_sub_pct'], r['classification']
    ])
print_box_table(cpr_cps_headers, cpr_cps_rows, cpr_cps_formats, cpr_cps_aligns)

if len(has_both) >= 3:
    corr = has_both['cpr'].corr(has_both['cps'])
    print(f"\n  Pearson correlation between CPR and CPS: {corr:.3f}")
    rank_corr = has_both['cpr'].corr(has_both['cps'], method='spearman')
    print(f"  Spearman rank correlation:               {rank_corr:.3f}")
else:
    print("\n  Not enough data for correlation analysis.")

print("\n  --- CPR Buckets: Average CPS by CPR Range ---")
cpr_thresh_headers = ['CPR Bucket', 'Groups', 'Avg CPR', 'Avg CPS', 'Med CPS', 'Avg Reg>Sub%', 'GOOD', 'MID', 'BAD']
cpr_thresh_formats = ['str', 'num', 'money', 'money', 'money', 'pct', 'num', 'num', 'num']
cpr_thresh_aligns = ['l', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']

cpr_buckets = [
    ('< $10', 0, 10),
    ('$10 - $20', 10, 20),
    ('$20 - $30', 20, 30),
    ('$30 - $50', 30, 50),
    ('$50 - $100', 50, 100),
    ('$100+', 100, 99999)
]

cpr_rows = []
for label, lo, hi in cpr_buckets:
    subset = has_both[(has_both['cpr'] >= lo) & (has_both['cpr'] < hi)]
    if len(subset) == 0:
        cpr_rows.append([label, 0, np.nan, np.nan, np.nan, np.nan, 0, 0, 0])
        continue
    g_cnt = len(subset[subset['classification'] == 'GOOD'])
    m_cnt = len(subset[subset['classification'] == 'MIDDLE'])
    b_cnt = len(subset[subset['classification'] == 'BAD'])
    cpr_rows.append([
        label, len(subset), subset['cpr'].mean(), subset['cps'].mean(),
        subset['cps'].median(), subset['reg_sub_pct'].mean(),
        g_cnt, m_cnt, b_cnt
    ])

print_box_table(cpr_thresh_headers, cpr_rows, cpr_thresh_formats, cpr_thresh_aligns)

# Anomaly: Low CPR but high CPS
print("\n  --- Anomaly: Low CPR (< $30) but High CPS (> $500) ---")
print("  (Cheap regs that don't convert to subscriptions)")
anomaly1 = has_both[(has_both['cpr'] < 30) & (has_both['cps'] > 500)]
if len(anomaly1) > 0:
    anom_rows = []
    for _, r in anomaly1.sort_values('cps', ascending=False).iterrows():
        anom_rows.append([
            str(r['group_name'])[:45], r['spend'], r['regs'], r['cpr'],
            r['subs'], r['cps'], r['reg_sub_pct']
        ])
    anom_headers = ['Group Name', 'Spend', 'Regs', 'CPR', 'Subs', 'CPS', 'Reg>Sub%']
    anom_formats = ['str', 'money', 'num1', 'money', 'num1', 'money', 'pct']
    anom_aligns = ['l', 'r', 'r', 'r', 'r', 'r', 'r']
    print_box_table(anom_headers, anom_rows, anom_formats, anom_aligns)
else:
    print("  None found.")

# Anomaly: High CPR but low CPS
print("\n  --- Anomaly: High CPR (> $50) but Low CPS (< $350) ---")
print("  (Expensive regs that DO convert to subscriptions)")
anomaly2 = has_both[(has_both['cpr'] > 50) & (has_both['cps'] < 350)]
if len(anomaly2) > 0:
    anom_rows = []
    for _, r in anomaly2.sort_values('cps').iterrows():
        anom_rows.append([
            str(r['group_name'])[:45], r['spend'], r['regs'], r['cpr'],
            r['subs'], r['cps'], r['reg_sub_pct']
        ])
    anom_headers = ['Group Name', 'Spend', 'Regs', 'CPR', 'Subs', 'CPS', 'Reg>Sub%']
    anom_formats = ['str', 'money', 'num1', 'money', 'num1', 'money', 'pct']
    anom_aligns = ['l', 'r', 'r', 'r', 'r', 'r', 'r']
    print_box_table(anom_headers, anom_rows, anom_formats, anom_aligns)
else:
    print("  None found.")

# CPR Sweet Spot
print("\n  --- CPR Sweet Spot Analysis ---")
if len(has_both) >= 5:
    good_groups = has_both[has_both['classification'] == 'GOOD']
    if len(good_groups) > 0:
        print(f"  GOOD groups CPR range:  ${good_groups['cpr'].min():.2f} - ${good_groups['cpr'].max():.2f}")
        print(f"  GOOD groups CPR median: ${good_groups['cpr'].median():.2f}")
        print(f"  GOOD groups CPR P25:    ${good_groups['cpr'].quantile(0.25):.2f}")
        print(f"  GOOD groups CPR P75:    ${good_groups['cpr'].quantile(0.75):.2f}")
    bad_groups_cpr = has_both[has_both['classification'] == 'BAD']
    if len(bad_groups_cpr) > 0:
        print(f"\n  BAD groups CPR range:   ${bad_groups_cpr['cpr'].min():.2f} - ${bad_groups_cpr['cpr'].max():.2f}")
        print(f"  BAD groups CPR median:  ${bad_groups_cpr['cpr'].median():.2f}")
        print(f"  BAD groups CPR P25:     ${bad_groups_cpr['cpr'].quantile(0.25):.2f}")
        print(f"  BAD groups CPR P75:     ${bad_groups_cpr['cpr'].quantile(0.75):.2f}")

# Groups with regs but NO subs
print("\n  --- Groups with Regs but ZERO Subs (Infinite CPS) ---")
regs_no_subs = master[(master['regs'] > 0) & (master['subs'] == 0)].sort_values('spend', ascending=False)
if len(regs_no_subs) > 0:
    rns_headers = ['Group Name', 'Campaign', 'Spend', 'Regs', 'CPR', 'Subs', 'Class']
    rns_formats = ['str', 'str', 'money', 'num1', 'money', 'num', 'str']
    rns_aligns = ['l', 'l', 'r', 'r', 'r', 'r', 'l']
    rns_rows = []
    for _, r in regs_no_subs.iterrows():
        rns_rows.append([
            str(r['group_name'])[:45], str(r['campaign_name'])[:40],
            r['spend'], r['regs'], r['cpr'], int(r['subs']), r['classification']
        ])
    print_box_table(rns_headers, rns_rows, rns_formats, rns_aligns)
else:
    print("  None found.")

# ─────────────────────────────────────────────────────────────────────
# SECTION 9: PATTERN ANALYSIS SUMMARY
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 9: PATTERN ANALYSIS - GOOD vs BAD (Brand Excluded)" + " " * 17 + "║")
print("╚" + "═" * 78 + "╝")

for cls in ['GOOD', 'BAD']:
    subset = master[master['classification'] == cls]
    if len(subset) == 0:
        continue
    print(f"\n  === {cls} Classification ({len(subset)} groups) ===")
    print(f"  Total spend: ${subset['spend'].sum():,.0f}")

    for metric, col in [('CTR', 'ctr'), ('CPC', 'cpc'), ('CPR', 'cpr'), ('CPS', 'cps'), ('Reg>Sub%', 'reg_sub_pct')]:
        vals = subset[col].dropna()
        if len(vals) == 0:
            print(f"  {metric}: no data")
            continue
        if metric in ['CTR', 'Reg>Sub%']:
            def fmt_fn(v, _m=metric):
                return f"{v:.1f}%"
        else:
            def fmt_fn(v, _m=metric):
                return f"${v:.2f}"
        print(f"  {metric:10s}  P25={fmt_fn(vals.quantile(0.25)):>10s}  Median={fmt_fn(vals.median()):>10s}  P75={fmt_fn(vals.quantile(0.75)):>10s}  Range=[{fmt_fn(vals.min()):>10s} - {fmt_fn(vals.max()):>10s}]")

    # Theme distribution
    themes = subset['theme'].value_counts()
    parts = [f"{t}({c})" for t, c in themes.items()]
    print(f"  Themes: {', '.join(parts)}")

    # Search term diversity
    st_cls = st_agg[st_agg['classification'] == cls]
    if len(st_cls) > 0:
        top_st_spend = st_cls.sort_values('spend', ascending=False).head(1)['spend'].values[0]
        st_total = st_cls['spend'].sum()
        print(f"  Search terms: {len(st_cls):,} unique | Top-term spend%: {safe_div(top_st_spend, st_total) * 100:.1f}%")

    # LP distribution
    cls_campaigns = subset['campaign_name'].unique()
    lp_cls = landing_pages[landing_pages['campaign'].isin(cls_campaigns)]
    if len(lp_cls) > 0:
        lp_cls_agg = lp_cls.groupby('landing_page_url')['cost'].sum().sort_values(ascending=False)
        top_lps = lp_cls_agg.head(3)
        lp_parts = []
        for url, sp in top_lps.items():
            short = url.replace('https://superpower.com', 'sp.com')[:40]
            lp_parts.append(f"{short} (${sp:,.0f})")
        print(f"  Top LPs: {', '.join(lp_parts)}")

# ─────────────────────────────────────────────────────────────────────
# SECTION 10: PMAX DEEP DIVE
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 10: PMAX DEEP DIVE (Brand Excluded)" + " " * 32 + "║")
print("╚" + "═" * 78 + "╝")

pmax_subset = master[master['type'] == 'PMAX'].sort_values('spend', ascending=False)

pmax_headers = ['Campaign', 'Asset Group', 'Status', 'Spend', 'Clicks', 'CTR', 'CPC',
                'Regs', 'CPR', 'Subs', 'CPS', 'Reg>Sub%', 'Class']
pmax_formats = ['str', 'str', 'str', 'money', 'num', 'pct', 'money',
                'num1', 'money', 'num1', 'money', 'pct', 'str']
pmax_aligns = ['l', 'l', 'l', 'r', 'r', 'r', 'r',
               'r', 'r', 'r', 'r', 'r', 'l']

pmax_rows = []
for _, r in pmax_subset.iterrows():
    pmax_rows.append([
        str(r['campaign_name'])[:40], str(r['group_name'])[:45], r['group_status'],
        r['spend'], r['clicks'], r['ctr'], r['cpc'],
        r['regs'], r['cpr'], r['subs'], r['cps'], r['reg_sub_pct'], r['classification']
    ])

pmax_total_sp = pmax_subset['spend'].sum()
pmax_total_cl = pmax_subset['clicks'].sum()
pmax_total_im = pmax_subset['impressions'].sum()
pmax_total_rg = pmax_subset['regs'].sum()
pmax_total_sb = pmax_subset['subs'].sum()

pmax_total = [
    'TOTAL', '', '', pmax_total_sp, pmax_total_cl,
    safe_div(pmax_total_cl, pmax_total_im) * 100,
    safe_div(pmax_total_sp, pmax_total_cl),
    pmax_total_rg, safe_div(pmax_total_sp, pmax_total_rg),
    pmax_total_sb, safe_div(pmax_total_sp, pmax_total_sb),
    safe_div(pmax_total_sb, pmax_total_rg) * 100, ''
]

print_box_table(pmax_headers, pmax_rows, pmax_formats, pmax_aligns, total_row=pmax_total)

# ─────────────────────────────────────────────────────────────────────
# SECTION 11: BIGGEST WASTE
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 11: BIGGEST WASTE - Top 15 BAD Groups by Spend (Brand Excluded)  ║")
print("╚" + "═" * 78 + "╝")

bad_groups = master[master['classification'] == 'BAD'].sort_values('spend', ascending=False).head(15)

waste_headers = ['#', 'Group Name', 'Campaign', 'Type', 'Spend', 'Clicks', 'CTR', 'CPC',
                 'Regs', 'CPR', 'Subs', 'CPS', 'Reg>Sub%']
waste_formats = ['str', 'str', 'str', 'str', 'money', 'num', 'pct', 'money',
                 'num1', 'money', 'num1', 'money', 'pct']
waste_aligns = ['r', 'l', 'l', 'l', 'r', 'r', 'r', 'r',
                'r', 'r', 'r', 'r', 'r']

waste_rows = []
for idx, (_, r) in enumerate(bad_groups.iterrows()):
    waste_rows.append([
        str(idx + 1), str(r['group_name'])[:45], str(r['campaign_name'])[:40], r['type'],
        r['spend'], r['clicks'], r['ctr'], r['cpc'],
        r['regs'], r['cpr'], r['subs'], r['cps'], r['reg_sub_pct']
    ])

waste_total_sp = bad_groups['spend'].sum()
bg_regs = bad_groups['regs'].sum()
bg_subs = bad_groups['subs'].sum()
waste_total = ['', 'TOTAL (Top 15 BAD)', '', '', waste_total_sp,
               bad_groups['clicks'].sum(),
               safe_div(bad_groups['clicks'].sum(), bad_groups['impressions'].sum()) * 100,
               safe_div(waste_total_sp, bad_groups['clicks'].sum()),
               bg_regs, safe_div(waste_total_sp, bg_regs),
               bg_subs, safe_div(waste_total_sp, bg_subs),
               safe_div(bg_subs, bg_regs) * 100 if bg_regs > 0 else np.nan]

print_box_table(waste_headers, waste_rows, waste_formats, waste_aligns, total_row=waste_total)

total_bad_spend = master[master['classification'] == 'BAD']['spend'].sum()
print(f"\n  Total BAD spend (all BAD groups): ${total_bad_spend:,.0f} ({safe_div(total_bad_spend, total_spend) * 100:.1f}% of total)")

# ─────────────────────────────────────────────────────────────────────
# SECTION 12: EFFICIENCY FRONTIER
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  SECTION 12: EFFICIENCY FRONTIER - Top 15 by Reg>Sub% (min 5 regs)       ║")
print("╚" + "═" * 78 + "╝")

eff_groups = master[master['regs'] >= 5].sort_values('reg_sub_pct', ascending=False).head(15)

eff_headers = ['#', 'Group Name', 'Campaign', 'Type', 'Spend', 'Regs', 'CPR', 'Subs', 'CPS', 'Reg>Sub%', 'Class']
eff_formats = ['str', 'str', 'str', 'str', 'money', 'num1', 'money', 'num1', 'money', 'pct', 'str']
eff_aligns = ['r', 'l', 'l', 'l', 'r', 'r', 'r', 'r', 'r', 'r', 'l']

eff_rows = []
for idx, (_, r) in enumerate(eff_groups.iterrows()):
    eff_rows.append([
        str(idx + 1), str(r['group_name'])[:45], str(r['campaign_name'])[:40], r['type'],
        r['spend'], r['regs'], r['cpr'], r['subs'], r['cps'], r['reg_sub_pct'], r['classification']
    ])

print_box_table(eff_headers, eff_rows, eff_formats, eff_aligns)

# ─────────────────────────────────────────────────────────────────────
# EXECUTIVE SUMMARY
# ─────────────────────────────────────────────────────────────────────

print("\n")
print("╔" + "═" * 78 + "╗")
print("║  EXECUTIVE SUMMARY (BRAND EXCLUDED)" + " " * 42 + "║")
print("╠" + "═" * 78 + "╣")

good_spend = master[master['classification'] == 'GOOD']['spend'].sum()
good_subs = master[master['classification'] == 'GOOD']['subs'].sum()
good_regs = master[master['classification'] == 'GOOD']['regs'].sum()
mid_spend = master[master['classification'] == 'MIDDLE']['spend'].sum()
mid_subs = master[master['classification'] == 'MIDDLE']['subs'].sum()
bad_spend = master[master['classification'] == 'BAD']['spend'].sum()
bad_subs = master[master['classification'] == 'BAD']['subs'].sum()

blended_cpr = safe_div(total_spend, total_regs)
blended_cps = safe_div(total_spend, total_subs)

def print_summary_line(text):
    padding = 79 - len(text)
    if padding < 1:
        padding = 1
    print(f"║ {text}" + " " * padding + "║")

print_summary_line(f"Period: Jan 26 - Feb 22, 2026 (4 weeks) -- BRAND CAMPAIGNS EXCLUDED")
print_summary_line(f"Total Spend: ${total_spend:>10,.0f}")
print_summary_line(f"Total Regs:  {total_regs:>10,.1f}   Blended CPR: ${blended_cpr:>8,.2f}")
print_summary_line(f"Total Subs:  {total_subs:>10,.1f}   Blended CPS: ${blended_cps:>8,.2f}")
print_summary_line(f"Reg>Sub Rate: {safe_div(total_subs, total_regs) * 100:>5.1f}%")
print_summary_line(f"")
print_summary_line(f"GOOD  (<$350 CPS): ${good_spend:>8,.0f} spend | {good_subs:>6,.1f} subs | CPS ${safe_div(good_spend, good_subs):>7,.0f}")
print_summary_line(f"MIDDLE ($350-500): ${mid_spend:>8,.0f} spend | {mid_subs:>6,.1f} subs | CPS ${safe_div(mid_spend, mid_subs):>7,.0f}")
if bad_subs > 0:
    print_summary_line(f"BAD   (>$500/no$): ${bad_spend:>8,.0f} spend | {bad_subs:>6,.1f} subs | CPS ${safe_div(bad_spend, bad_subs):>7,.0f}")
else:
    print_summary_line(f"BAD   (>$500/no$): ${bad_spend:>8,.0f} spend | {bad_subs:>6,.1f} subs | CPS       -")

print("╚" + "═" * 78 + "╝")

print(f"\n  Analysis complete. All 12 sections generated.")
print(f"  Total groups analyzed: {len(master)} (brand excluded)")
print(f"  Script: /tmp/analyze_audit_v3.py")
print(f"  Report: /tmp/audit_report_v3.txt")
print()

# Close file and restore stdout
sys.stdout.close()
sys.stdout = original_stdout
print(f"Report saved to {output_file}")
