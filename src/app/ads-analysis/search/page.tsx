'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAdsData } from '@/context/AdsDataContext';
import DateRangePicker from '@/components/DateRangePicker';

interface LandingPageData {
  url: string;
  total_spend: number;
  total_clicks: number;
  total_conversions: number;
  cvr: number;
  cac: number;
}

type FilterMode = 'all' | 'brand' | 'non_brand';

export default function SearchAnalysis() {
  const { data, isLoading, startDate, endDate, setDateRange } = useAdsData();
  const [filterMode, setFilterMode] = useState<FilterMode>('all');
  const [expandedAdGroup, setExpandedAdGroup] = useState<string | null>(null);

  if (!data) {
    return (
      <main className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <div className="text-gray-400">Loading...</div>
        </div>
      </main>
    );
  }

  // Select data based on toggle
  const activeData = filterMode === 'all'
    ? data.search.all
    : filterMode === 'brand'
      ? data.search.brand
      : data.search.non_brand;
  const brandData = data.search.brand;
  const nonBrandData = data.search.non_brand;

  const filterLabel = filterMode === 'all' ? 'All Search' : filterMode === 'brand' ? 'Brand Only' : 'Non-Brand Only';

  const getCvrClass = (cvr: number) => {
    if (cvr >= 3.5) return 'text-green-400';
    if (cvr >= 2.0) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getCacClass = (cac: number) => {
    if (cac === 0) return 'text-gray-500';
    if (cac <= 100) return 'text-green-400';
    if (cac <= 200) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getRowBgClass = (cvr: number) => {
    if (cvr >= 3.5) return 'bg-green-900/20';
    if (cvr >= 2.0) return 'bg-yellow-900/20';
    return 'bg-red-900/20';
  };

  const landingPageOrder = ['welcome', 'homepage', 'comparison', 'biomarker', 'other'];
  const lpLabels: Record<string, string> = {
    welcome: 'Welcome Page',
    homepage: 'Homepage',
    comparison: 'Comparison Pages',
    biomarker: 'Biomarker Pages',
    other: 'Other'
  };

  // Calculate days in range
  const startDt = new Date(data.date_range.start);
  const endDt = new Date(data.date_range.end);
  const daysInRange = Math.round((endDt.getTime() - startDt.getTime()) / (1000 * 60 * 60 * 24));

  return (
    <main className="min-h-screen bg-gray-950 text-white">
      <div className="bg-gray-900 border-b border-gray-800 px-6 py-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/ads-analysis" className="text-gray-400 hover:text-white text-sm">&larr; All Campaigns</Link>
              <h1 className="text-2xl font-bold flex items-center gap-2">
                <span>🔍</span> Search Campaign Analysis
              </h1>
            </div>
            <DateRangePicker
              startDate={startDate}
              endDate={endDate}
              onDateChange={setDateRange}
              isLoading={isLoading}
            />
          </div>
          {/* Navigation Links */}
          <div className="flex items-center gap-2 mt-3">
            <span className="text-gray-500 text-sm mr-2">Jump to:</span>
            <Link
              href="/"
              className="px-3 py-1 bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm rounded-lg transition-colors"
            >
              Gap Analysis
            </Link>
            <Link
              href="/ads-analysis"
              className="px-3 py-1 bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm rounded-lg transition-colors"
            >
              Ads Overview
            </Link>
            <Link
              href="/ads-analysis/search"
              className="px-3 py-1 bg-blue-600 text-white text-sm rounded-lg"
            >
              🔍 Search
            </Link>
            <Link
              href="/ads-analysis/pmax"
              className="px-3 py-1 bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm rounded-lg transition-colors"
            >
              ⚡ PMax
            </Link>
          </div>
          <p className="text-gray-400 text-sm mt-2">
            {daysInRange} days of data
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6 space-y-8">
        {/* Brand Toggle */}
        <section className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">Search Performance</h2>
            <p className="text-gray-400 text-sm">Filter by brand/non-brand to analyze performance in isolation</p>
          </div>
          <div className="flex items-center gap-1 bg-gray-900 rounded-lg p-1 border border-gray-800">
            <button
              onClick={() => setFilterMode('all')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                filterMode === 'all'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              All Search
            </button>
            <button
              onClick={() => setFilterMode('brand')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                filterMode === 'brand'
                  ? 'bg-green-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Brand Only
            </button>
            <button
              onClick={() => setFilterMode('non_brand')}
              className={`px-4 py-2 rounded-lg transition-colors ${
                filterMode === 'non_brand'
                  ? 'bg-red-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Non-Brand Only
            </button>
          </div>
        </section>

        {/* Summary Cards */}
        <section>
          <div className="grid grid-cols-5 gap-4">
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-blue-400">${Math.round(activeData.totals.total_spend / 1000)}K</div>
              <div className="text-sm text-gray-400">Total Spend</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-blue-400">{Math.round(activeData.totals.total_clicks).toLocaleString()}</div>
              <div className="text-sm text-gray-400">Total Clicks</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-green-400">{Math.round(activeData.totals.total_conversions).toLocaleString()}</div>
              <div className="text-sm text-gray-400">Subscriptions</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className={`text-3xl font-bold ${getCvrClass(activeData.totals.cvr)}`}>{activeData.totals.cvr.toFixed(2)}%</div>
              <div className="text-sm text-gray-400">CVR</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className={`text-3xl font-bold ${getCacClass(activeData.totals.cac)}`}>${Math.round(activeData.totals.cac)}</div>
              <div className="text-sm text-gray-400">CAC</div>
            </div>
          </div>
        </section>

        {/* Brand vs Non-Brand Comparison */}
        <section>
          <h2 className="text-xl font-semibold mb-4">Brand vs Non-Brand Comparison</h2>
          <div className="bg-gray-900 rounded-xl overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-800">
                <tr>
                  <th className="text-left px-4 py-3">Segment</th>
                  <th className="text-right px-4 py-3">Spend</th>
                  <th className="text-right px-4 py-3">Clicks</th>
                  <th className="text-right px-4 py-3">Subs</th>
                  <th className="text-right px-4 py-3">CVR</th>
                  <th className="text-right px-4 py-3">CAC</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                <tr className={`${filterMode !== 'non_brand' ? 'bg-green-900/20' : 'bg-gray-800/30 opacity-50'}`}>
                  <td className="px-4 py-3 font-medium">
                    Brand Search
                    {filterMode === 'non_brand' && <span className="ml-2 text-xs text-gray-500">(excluded)</span>}
                  </td>
                  <td className="px-4 py-3 text-right">${Math.round(brandData.totals.total_spend).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right">{Math.round(brandData.totals.total_clicks).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right font-bold text-green-400">{Math.round(brandData.totals.total_conversions).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right text-green-400">{brandData.totals.cvr.toFixed(2)}%</td>
                  <td className="px-4 py-3 text-right text-green-400">${Math.round(brandData.totals.cac)}</td>
                </tr>
                <tr className={`${filterMode !== 'brand' ? 'bg-red-900/20' : 'bg-gray-800/30 opacity-50'}`}>
                  <td className="px-4 py-3 font-medium">
                    Non-Brand Search
                    {filterMode === 'brand' && <span className="ml-2 text-xs text-gray-500">(excluded)</span>}
                  </td>
                  <td className="px-4 py-3 text-right">${Math.round(nonBrandData.totals.total_spend).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right">{Math.round(nonBrandData.totals.total_clicks).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right font-bold text-red-400">{Math.round(nonBrandData.totals.total_conversions).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right text-red-400">{nonBrandData.totals.cvr.toFixed(2)}%</td>
                  <td className="px-4 py-3 text-right text-red-400">${Math.round(nonBrandData.totals.cac)}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="mt-4 p-4 bg-yellow-900/20 border border-yellow-800/50 rounded-xl">
            <div className="font-semibold text-yellow-300 mb-2">Key Insight: Non-Brand is {Math.round(nonBrandData.totals.cac / brandData.totals.cac)}x More Expensive</div>
            <p className="text-sm text-gray-400">
              Brand: <strong className="text-green-400">${Math.round(brandData.totals.cac)} CAC</strong> | Non-Brand: <strong className="text-red-400">${Math.round(nonBrandData.totals.cac)} CAC</strong><br/>
              Non-Brand gets {Math.round(nonBrandData.totals.total_spend / data.search.all.totals.total_spend * 100)}% of spend but only {Math.round(nonBrandData.totals.total_conversions / data.search.all.totals.total_conversions * 100)}% of subscriptions.
            </p>
          </div>
        </section>

        {/* Landing Page Performance (for selected segment) */}
        {activeData.landing_pages && (
          <section>
            <h2 className="text-xl font-semibold mb-4">
              Landing Page Performance
              <span className="text-sm font-normal text-gray-400 ml-2">
                ({filterLabel})
              </span>
            </h2>
            <div className="bg-gray-900 rounded-xl overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-800">
                  <tr>
                    <th className="text-left px-4 py-3">Landing Page</th>
                    <th className="text-right px-4 py-3">Spend</th>
                    <th className="text-right px-4 py-3">Clicks</th>
                    <th className="text-right px-4 py-3">Subs</th>
                    <th className="text-right px-4 py-3">CVR</th>
                    <th className="text-right px-4 py-3">CAC</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-800">
                  {landingPageOrder.map((key) => {
                    const lp = activeData.landing_pages?.[key];
                    if (!lp) return null;
                    return (
                      <tr key={key} className={getRowBgClass(lp.cvr)}>
                        <td className="px-4 py-3 font-medium">{lpLabels[key]}</td>
                        <td className="px-4 py-3 text-right">${Math.round(lp.total_spend).toLocaleString()}</td>
                        <td className="px-4 py-3 text-right">{Math.round(lp.total_clicks).toLocaleString()}</td>
                        <td className="px-4 py-3 text-right font-bold">
                          <span className={getCvrClass(lp.cvr)}>{Math.round(lp.total_conversions)}</span>
                        </td>
                        <td className="px-4 py-3 text-right">
                          <span className={getCvrClass(lp.cvr)}>{lp.cvr.toFixed(2)}%</span>
                        </td>
                        <td className="px-4 py-3 text-right">
                          <span className={getCacClass(lp.cac)}>
                            {lp.cac === 0 ? 'N/A' : `$${Math.round(lp.cac)}`}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </section>
        )}

        {/* Campaigns */}
        <section>
          <h2 className="text-xl font-semibold mb-4">
            Campaigns
            <span className="text-sm font-normal text-gray-400 ml-2">
              ({filterLabel})
            </span>
          </h2>
          <div className="bg-gray-900 rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-800">
                <tr>
                  <th className="text-left px-4 py-3">Campaign</th>
                  <th className="text-right px-4 py-3">Spend</th>
                  <th className="text-right px-4 py-3">Subs</th>
                  <th className="text-right px-4 py-3">CVR</th>
                  <th className="text-right px-4 py-3">CAC</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {activeData.campaigns.slice(0, 15).map((campaign, idx) => (
                  <tr key={idx} className={getRowBgClass(campaign.cvr)}>
                    <td className="px-4 py-3 font-medium">{campaign.name}</td>
                    <td className="px-4 py-3 text-right">${Math.round(campaign.total_spend).toLocaleString()}</td>
                    <td className="px-4 py-3 text-right font-bold">
                      <span className={getCvrClass(campaign.cvr)}>{campaign.total_conversions.toFixed(1)}</span>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <span className={getCvrClass(campaign.cvr)}>{campaign.cvr.toFixed(2)}%</span>
                    </td>
                    <td className="px-4 py-3 text-right">
                      <span className={getCacClass(campaign.cac)}>
                        {campaign.cac === 0 ? 'N/A' : `$${Math.round(campaign.cac)}`}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* Ad Groups */}
        <section>
          <h2 className="text-xl font-semibold mb-4">
            Top Ad Groups by Spend
            <span className="text-sm font-normal text-gray-400 ml-2">
              ({filterLabel})
            </span>
          </h2>
          <p className="text-gray-400 text-sm mb-4">Click an ad group to see landing page breakdown</p>
          <div className="bg-gray-900 rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-800">
                <tr>
                  <th className="text-left px-4 py-3">Ad Group</th>
                  <th className="text-left px-4 py-3">Campaign</th>
                  <th className="text-right px-4 py-3">Spend</th>
                  <th className="text-right px-4 py-3">Subs</th>
                  <th className="text-right px-4 py-3">CVR</th>
                  <th className="text-right px-4 py-3">CAC</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {activeData.ad_groups.slice(0, 20).map((ag, idx) => {
                  const agKey = `${ag.campaign_name}|${ag.ad_group_name}`;
                  const isExpanded = expandedAdGroup === agKey;
                  const landingPages = (ag as { landing_pages?: Record<string, LandingPageData> }).landing_pages || {};
                  const hasMultipleLPs = Object.keys(landingPages).length > 1;

                  return (
                    <tr key={idx} className="contents">
                      <td colSpan={6} className="p-0">
                        <div
                          className={`${getRowBgClass(ag.cvr)} ${hasMultipleLPs ? 'cursor-pointer hover:bg-gray-800/50' : ''} grid grid-cols-[1fr_180px_100px_80px_80px_80px] items-center`}
                          onClick={() => hasMultipleLPs && setExpandedAdGroup(isExpanded ? null : agKey)}
                        >
                          <div className="px-4 py-3 font-medium">
                            <span className="flex items-center gap-2">
                              {hasMultipleLPs && (
                                <span className={`text-gray-500 transition-transform text-xs ${isExpanded ? 'rotate-90' : ''}`}>▶</span>
                              )}
                              {!hasMultipleLPs && <span className="w-3" />}
                              {ag.ad_group_name}
                              {hasMultipleLPs && (
                                <span className="text-xs text-gray-500 ml-1">({Object.keys(landingPages).length} LPs)</span>
                              )}
                            </span>
                          </div>
                          <div className="px-4 py-3 text-gray-400 text-xs truncate" title={ag.campaign_name}>
                            {ag.campaign_name}
                          </div>
                          <div className="px-4 py-3 text-right">${Math.round(ag.total_spend).toLocaleString()}</div>
                          <div className="px-4 py-3 text-right font-bold">
                            <span className={getCvrClass(ag.cvr)}>{ag.total_conversions.toFixed(1)}</span>
                          </div>
                          <div className="px-4 py-3 text-right">
                            <span className={getCvrClass(ag.cvr)}>{ag.cvr.toFixed(2)}%</span>
                          </div>
                          <div className="px-4 py-3 text-right">
                            <span className={getCacClass(ag.cac)}>
                              {ag.cac === 0 ? 'N/A' : `$${Math.round(ag.cac)}`}
                            </span>
                          </div>
                        </div>
                        {isExpanded && hasMultipleLPs && (
                          <div className="bg-gray-800/40 border-t border-gray-700">
                            <div className="px-8 py-3">
                              <div className="text-xs text-gray-500 uppercase tracking-wide mb-2">Landing Page Breakdown</div>
                              <table className="w-full text-xs">
                                <thead>
                                  <tr className="text-gray-500">
                                    <th className="text-left py-1 font-medium">Landing Page</th>
                                    <th className="text-right py-1 font-medium">Spend</th>
                                    <th className="text-right py-1 font-medium">Clicks</th>
                                    <th className="text-right py-1 font-medium">Subs</th>
                                    <th className="text-right py-1 font-medium">CVR</th>
                                    <th className="text-right py-1 font-medium">CAC</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {landingPageOrder.map((lpKey) => {
                                    const lp = landingPages[lpKey];
                                    if (!lp) return null;
                                    return (
                                      <tr key={lpKey} className="border-t border-gray-700/50">
                                        <td className="py-2 text-gray-300">
                                          {lpLabels[lpKey] || lpKey}
                                          <span className="text-gray-600 ml-2 text-[10px] truncate max-w-[200px] inline-block align-bottom">
                                            {lp.url?.replace('https://', '').substring(0, 40)}
                                          </span>
                                        </td>
                                        <td className="py-2 text-right text-gray-300">${Math.round(lp.total_spend).toLocaleString()}</td>
                                        <td className="py-2 text-right text-gray-300">{Math.round(lp.total_clicks).toLocaleString()}</td>
                                        <td className="py-2 text-right font-medium">
                                          <span className={getCvrClass(lp.cvr)}>{lp.total_conversions.toFixed(1)}</span>
                                        </td>
                                        <td className="py-2 text-right">
                                          <span className={getCvrClass(lp.cvr)}>{lp.cvr.toFixed(2)}%</span>
                                        </td>
                                        <td className="py-2 text-right">
                                          <span className={getCacClass(lp.cac)}>
                                            {lp.cac === 0 ? 'N/A' : `$${Math.round(lp.cac)}`}
                                          </span>
                                        </td>
                                      </tr>
                                    );
                                  })}
                                </tbody>
                              </table>
                            </div>
                          </div>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>

      </div>
    </main>
  );
}
