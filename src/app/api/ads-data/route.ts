import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs/promises';
import * as path from 'path';

const execAsync = promisify(exec);

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const startDate = searchParams.get('start');
  const endDate = searchParams.get('end');

  if (!startDate || !endDate) {
    return NextResponse.json({ error: 'start and end dates required' }, { status: 400 });
  }

  // Validate date format
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
  if (!dateRegex.test(startDate) || !dateRegex.test(endDate)) {
    return NextResponse.json({ error: 'Invalid date format. Use YYYY-MM-DD' }, { status: 400 });
  }

  try {
    // Create a temporary Python script with the date range
    const scriptPath = '/tmp/fetch_ads_data.py';
    const outputPath = `/tmp/ads_data_${startDate}_${endDate}.json`;

    const pythonScript = `
import json
from google.ads.googleads.client import GoogleAdsClient
from datetime import datetime

client = GoogleAdsClient.load_from_storage('/Users/jeffy/.config/google-ads-mcp/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
customer_id = '8618096874'
manager_id = '3349101596'

start_date = '${startDate}'
end_date = '${endDate}'

# Calculate months between dates
start_dt = datetime.strptime(start_date, '%Y-%m-%d')
end_dt = datetime.strptime(end_date, '%Y-%m-%d')
months = max(1, (end_dt - start_dt).days / 30)

query = f"""
    SELECT
        campaign.id,
        campaign.name,
        campaign.advertising_channel_type,
        ad_group.id,
        ad_group.name,
        ad_group_ad.ad.final_urls,
        metrics.cost_micros,
        metrics.clicks,
        metrics.conversions,
        metrics.impressions
    FROM ad_group_ad
    WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY metrics.cost_micros DESC
"""

data_by_type = {
    'search': {
        'brand': {'campaigns': {}, 'ad_groups': {}, 'landing_pages': {}, 'totals': {'cost': 0, 'clicks': 0, 'conv': 0, 'impr': 0}},
        'non_brand': {'campaigns': {}, 'ad_groups': {}, 'landing_pages': {}, 'totals': {'cost': 0, 'clicks': 0, 'conv': 0, 'impr': 0}},
        'all': {'campaigns': {}, 'ad_groups': {}, 'landing_pages': {}, 'totals': {'cost': 0, 'clicks': 0, 'conv': 0, 'impr': 0}}
    },
    'demand_gen': {'campaigns': {}, 'ad_groups': {}, 'totals': {'cost': 0, 'clicks': 0, 'conv': 0, 'impr': 0}},
    'pmax': {'campaigns': {}, 'ad_groups': {}, 'totals': {'cost': 0, 'clicks': 0, 'conv': 0, 'impr': 0}},
    'shopping': {'campaigns': {}, 'ad_groups': {}, 'totals': {'cost': 0, 'clicks': 0, 'conv': 0, 'impr': 0}},
}

response = ga_service.search(customer_id=customer_id, query=query)

for row in response:
    channel_type = row.campaign.advertising_channel_type.name
    campaign_name = row.campaign.name
    campaign_id = row.campaign.id
    ag_name = row.ad_group.name
    ag_id = row.ad_group.id

    cost = row.metrics.cost_micros / 1_000_000
    clicks = row.metrics.clicks
    conv = row.metrics.conversions
    impr = row.metrics.impressions

    if channel_type == 'SEARCH':
        camp_type = 'search'
        is_brand = 'brand' in campaign_name.lower() or 'Brand' in campaign_name
        brand_key = 'brand' if is_brand else 'non_brand'
    elif channel_type == 'PERFORMANCE_MAX':
        camp_type = 'pmax'
        brand_key = None
    elif channel_type == 'SHOPPING':
        camp_type = 'shopping'
        brand_key = None
    elif channel_type in ['VIDEO', 'DEMAND_GEN'] or 'Demand' in campaign_name:
        camp_type = 'demand_gen'
        brand_key = None
    else:
        continue

    urls = list(row.ad_group_ad.ad.final_urls) if row.ad_group_ad.ad.final_urls else ['N/A']
    url = urls[0].replace('https://', '').replace('http://', '')

    if '/biomarkers/' in url or '/biomarker/' in url:
        lp_type = 'biomarker'
    elif url == 'superpower.com' or url == 'superpower.com/':
        lp_type = 'homepage'
    elif 'welcome' in url:
        lp_type = 'welcome'
    elif 'superpower-vs-' in url:
        lp_type = 'comparison'
    else:
        lp_type = 'other'

    ads_link = f"https://ads.google.com/aw/adgroups?ocid={manager_id}&uscid={customer_id}&__e={customer_id}&campaignId={campaign_id}&adGroupId={ag_id}"

    def add_to_bucket(bucket):
        bucket['totals']['cost'] += cost
        bucket['totals']['clicks'] += clicks
        bucket['totals']['conv'] += conv
        bucket['totals']['impr'] += impr

        if campaign_name not in bucket['campaigns']:
            bucket['campaigns'][campaign_name] = {'campaign_id': campaign_id, 'cost': 0, 'clicks': 0, 'conv': 0, 'impr': 0}
        bucket['campaigns'][campaign_name]['cost'] += cost
        bucket['campaigns'][campaign_name]['clicks'] += clicks
        bucket['campaigns'][campaign_name]['conv'] += conv

        ag_key = f"{campaign_name}|{ag_name}"
        if ag_key not in bucket['ad_groups']:
            bucket['ad_groups'][ag_key] = {
                'ad_group_name': ag_name, 'campaign_name': campaign_name,
                'campaign_id': campaign_id, 'ad_group_id': ag_id, 'ads_link': ads_link,
                'cost': 0, 'clicks': 0, 'conv': 0, 'impr': 0
            }
        bucket['ad_groups'][ag_key]['cost'] += cost
        bucket['ad_groups'][ag_key]['clicks'] += clicks
        bucket['ad_groups'][ag_key]['conv'] += conv

        if 'landing_pages' in bucket:
            if lp_type not in bucket['landing_pages']:
                bucket['landing_pages'][lp_type] = {'cost': 0, 'clicks': 0, 'conv': 0}
            bucket['landing_pages'][lp_type]['cost'] += cost
            bucket['landing_pages'][lp_type]['clicks'] += clicks
            bucket['landing_pages'][lp_type]['conv'] += conv

    if camp_type == 'search':
        add_to_bucket(data_by_type['search'][brand_key])
        add_to_bucket(data_by_type['search']['all'])
    else:
        add_to_bucket(data_by_type[camp_type])

def process_bucket(bucket, months):
    totals = bucket['totals']
    cvr = (totals['conv'] / totals['clicks'] * 100) if totals['clicks'] > 0 else 0
    cac = (totals['cost'] / totals['conv']) if totals['conv'] > 0 else 0

    result = {
        'totals': {
            'total_spend': totals['cost'], 'total_clicks': totals['clicks'],
            'total_conversions': totals['conv'], 'total_impressions': totals['impr'],
            'monthly_spend': totals['cost'] / months, 'monthly_clicks': totals['clicks'] / months,
            'monthly_conversions': totals['conv'] / months, 'cvr': cvr, 'cac': cac
        },
        'campaigns': [], 'ad_groups': []
    }

    for name, data in sorted(bucket['campaigns'].items(), key=lambda x: x[1]['cost'], reverse=True):
        cvr = (data['conv'] / data['clicks'] * 100) if data['clicks'] > 0 else 0
        cac = (data['cost'] / data['conv']) if data['conv'] > 0 else 0
        result['campaigns'].append({
            'name': name, 'campaign_id': data['campaign_id'],
            'total_spend': data['cost'], 'total_clicks': data['clicks'],
            'total_conversions': data['conv'], 'cvr': cvr, 'cac': cac,
            'ads_link': f"https://ads.google.com/aw/campaigns?ocid={manager_id}&uscid={customer_id}&__e={customer_id}&campaignId={data['campaign_id']}"
        })

    for key, data in sorted(bucket['ad_groups'].items(), key=lambda x: x[1]['cost'], reverse=True):
        cvr = (data['conv'] / data['clicks'] * 100) if data['clicks'] > 0 else 0
        cac = (data['cost'] / data['conv']) if data['conv'] > 0 else 0
        result['ad_groups'].append({
            'ad_group_name': data['ad_group_name'], 'campaign_name': data['campaign_name'],
            'campaign_id': data['campaign_id'], 'ad_group_id': data['ad_group_id'],
            'ads_link': data['ads_link'], 'total_spend': data['cost'],
            'total_clicks': data['clicks'], 'total_conversions': data['conv'], 'cvr': cvr, 'cac': cac
        })

    if 'landing_pages' in bucket:
        result['landing_pages'] = {}
        for lp_type, data in bucket['landing_pages'].items():
            cvr = (data['conv'] / data['clicks'] * 100) if data['clicks'] > 0 else 0
            cac = (data['cost'] / data['conv']) if data['conv'] > 0 else 0
            result['landing_pages'][lp_type] = {
                'total_spend': data['cost'], 'total_clicks': data['clicks'],
                'total_conversions': data['conv'], 'cvr': cvr, 'cac': cac
            }

    return result

output = {
    'date_range': {'start': start_date, 'end': end_date, 'months': months},
    'customer_id': customer_id, 'manager_id': manager_id,
    'search': {
        'all': process_bucket(data_by_type['search']['all'], months),
        'brand': process_bucket(data_by_type['search']['brand'], months),
        'non_brand': process_bucket(data_by_type['search']['non_brand'], months)
    },
    'demand_gen': process_bucket(data_by_type['demand_gen'], months),
    'pmax': process_bucket(data_by_type['pmax'], months),
    'shopping': process_bucket(data_by_type['shopping'], months)
}

with open('${outputPath}', 'w') as f:
    json.dump(output, f)
`;

    await fs.writeFile(scriptPath, pythonScript);

    // Execute the Python script
    const { stderr } = await execAsync(
      `/Users/jeffy/.local/bin/uvx --with google-ads python ${scriptPath}`,
      { timeout: 120000 }
    );

    if (stderr && !stderr.includes('zprofile')) {
      console.error('Python stderr:', stderr);
    }

    // Read the output
    const outputData = await fs.readFile(outputPath, 'utf-8');
    const jsonData = JSON.parse(outputData);

    return NextResponse.json(jsonData);
  } catch (error) {
    console.error('Error fetching ads data:', error);
    return NextResponse.json(
      { error: 'Failed to fetch ads data', details: String(error) },
      { status: 500 }
    );
  }
}
