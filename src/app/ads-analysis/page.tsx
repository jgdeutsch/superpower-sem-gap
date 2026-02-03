'use client';

import Link from 'next/link';
import { useAdsData } from '@/context/AdsDataContext';
import DateRangePicker from '@/components/DateRangePicker';

export default function AdsAnalysisOverview() {
  const { data, isLoading, error, startDate, endDate, setDateRange } = useAdsData();

  if (isLoading && !data) {
    return (
      <main className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <div className="text-gray-400">Loading Google Ads data...</div>
        </div>
      </main>
    );
  }

  if (!data) {
    return (
      <main className="min-h-screen bg-gray-950 text-white flex items-center justify-center">
        <div className="text-red-400">Failed to load data: {error}</div>
      </main>
    );
  }

  // Note: Demand Gen excluded (tracks registration_started not subscription_created)
  // Note: Shopping excluded (minimal spend, no conversions)
  const campaignTypes = [
    {
      key: 'search',
      name: 'Search',
      icon: '🔍',
      color: 'blue',
      data: data.search.all.totals,
      href: '/ads-analysis/search',
      description: 'Brand + Non-Brand keyword targeting'
    },
    {
      key: 'pmax',
      name: 'Performance Max',
      icon: '⚡',
      color: 'green',
      data: data.pmax.totals,
      href: '/ads-analysis/pmax',
      description: 'Cross-channel automated campaigns'
    },
  ];

  const totalSpend = campaignTypes.reduce((sum, t) => sum + t.data.total_spend, 0);
  const totalConv = campaignTypes.reduce((sum, t) => sum + t.data.total_conversions, 0);
  const totalClicks = campaignTypes.reduce((sum, t) => sum + t.data.total_clicks, 0);
  const overallCvr = totalClicks > 0 ? (totalConv / totalClicks * 100) : 0;
  const overallCac = totalConv > 0 ? (totalSpend / totalConv) : 0;

  const getCacColor = (cac: number) => {
    if (cac === 0) return 'text-gray-500';
    if (cac <= 50) return 'text-green-400';
    if (cac <= 150) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getCvrColor = (cvr: number) => {
    if (cvr >= 4) return 'text-green-400';
    if (cvr >= 2) return 'text-yellow-400';
    return 'text-red-400';
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
              <a href="/" className="text-gray-400 hover:text-white text-sm">&larr; Gap Analysis</a>
              <h1 className="text-2xl font-bold">Google Ads Performance Analysis</h1>
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
              className="px-3 py-1 bg-blue-600 text-white text-sm rounded-lg"
            >
              Ads Overview
            </Link>
            <Link
              href="/ads-analysis/search"
              className="px-3 py-1 bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm rounded-lg transition-colors"
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
          <div className="flex items-center gap-4 mt-2">
            <p className="text-gray-400 text-sm">
              Customer ID: {data.customer_id}
            </p>
            {error && (
              <span className="px-2 py-1 bg-yellow-900/30 border border-yellow-700/50 rounded text-yellow-400 text-xs">
                {error}
              </span>
            )}
            {isLoading && (
              <span className="px-2 py-1 bg-blue-900/30 border border-blue-700/50 rounded text-blue-400 text-xs flex items-center gap-2">
                <svg className="animate-spin h-3 w-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Updating...
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6 space-y-8">
        {/* Overall Metrics */}
        <section>
          <h2 className="text-xl font-semibold mb-4">Overall Account Performance ({daysInRange} days)</h2>
          <div className="grid grid-cols-5 gap-4">
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-blue-400">${Math.round(totalSpend / 1000)}K</div>
              <div className="text-sm text-gray-400">Total Spend</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-blue-400">{Math.round(totalClicks).toLocaleString()}</div>
              <div className="text-sm text-gray-400">Total Clicks</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-green-400">{Math.round(totalConv).toLocaleString()}</div>
              <div className="text-sm text-gray-400">Total Subscriptions</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-green-400">{overallCvr.toFixed(2)}%</div>
              <div className="text-sm text-gray-400">Overall CVR</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-yellow-400">${Math.round(overallCac)}</div>
              <div className="text-sm text-gray-400">Overall CAC</div>
            </div>
          </div>
        </section>

        {/* Campaign Type Cards */}
        <section>
          <h2 className="text-xl font-semibold mb-4">Performance by Campaign Type</h2>
          <div className="grid grid-cols-2 gap-6">
            {campaignTypes.map((type) => {
              const pctSpend = totalSpend > 0 ? (type.data.total_spend / totalSpend * 100) : 0;
              const pctConv = totalConv > 0 ? (type.data.total_conversions / totalConv * 100) : 0;

              return (
                <Link
                  key={type.key}
                  href={type.href}
                  className="bg-gray-900 rounded-xl p-6 border border-gray-800 hover:border-blue-500/50 transition-colors group"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <span className="text-3xl">{type.icon}</span>
                      <div>
                        <h3 className="text-xl font-bold group-hover:text-blue-400 transition-colors">{type.name}</h3>
                        <p className="text-sm text-gray-500">{type.description}</p>
                      </div>
                    </div>
                    <span className="text-gray-500 group-hover:text-blue-400 transition-colors">→</span>
                  </div>

                  <div className="grid grid-cols-4 gap-4 text-center">
                    <div>
                      <div className="text-lg font-bold">${Math.round(type.data.total_spend / 1000)}K</div>
                      <div className="text-xs text-gray-500">Spend ({pctSpend.toFixed(0)}%)</div>
                    </div>
                    <div>
                      <div className="text-lg font-bold">{Math.round(type.data.total_conversions).toLocaleString()}</div>
                      <div className="text-xs text-gray-500">Subs ({pctConv.toFixed(0)}%)</div>
                    </div>
                    <div>
                      <div className={`text-lg font-bold ${getCvrColor(type.data.cvr)}`}>{type.data.cvr.toFixed(2)}%</div>
                      <div className="text-xs text-gray-500">CVR</div>
                    </div>
                    <div>
                      <div className={`text-lg font-bold ${getCacColor(type.data.cac)}`}>
                        {type.data.cac === 0 ? 'N/A' : `$${Math.round(type.data.cac)}`}
                      </div>
                      <div className="text-xs text-gray-500">CAC</div>
                    </div>
                  </div>

                  {/* Efficiency bar */}
                  <div className="mt-4 pt-4 border-t border-gray-800">
                    <div className="flex justify-between text-xs text-gray-500 mb-1">
                      <span>Spend vs Conversions Efficiency</span>
                      <span>{pctConv > pctSpend ? '+' : ''}{(pctConv - pctSpend).toFixed(1)}%</span>
                    </div>
                    <div className="h-2 bg-gray-800 rounded-full overflow-hidden flex">
                      <div
                        className={`h-full ${pctConv >= pctSpend ? 'bg-green-500' : 'bg-red-500'}`}
                        style={{ width: `${Math.min(pctConv, 100)}%` }}
                      />
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        </section>

        {/* Quick Insights */}
        <section>
          <h2 className="text-xl font-semibold mb-4">Key Insights</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-green-900/20 border border-green-800/50 rounded-xl p-4">
              <div className="font-semibold text-green-300 mb-2">🏆 Best Performer</div>
              <p className="text-2xl font-bold text-green-400">Brand Search</p>
              <p className="text-sm text-gray-400 mt-1">
                ${Math.round(data.search.brand.totals.cac)} CAC | {data.search.brand.totals.cvr.toFixed(2)}% CVR
              </p>
            </div>
            <div className="bg-yellow-900/20 border border-yellow-800/50 rounded-xl p-4">
              <div className="font-semibold text-yellow-300 mb-2">⚠️ Needs Optimization</div>
              <p className="text-2xl font-bold text-yellow-400">Search Non-Brand</p>
              <p className="text-sm text-gray-400 mt-1">
                ${Math.round(data.search.non_brand.totals.cac)} CAC | {data.search.non_brand.totals.cvr.toFixed(2)}% CVR
              </p>
            </div>
            <div className="bg-blue-900/20 border border-blue-800/50 rounded-xl p-4">
              <div className="font-semibold text-blue-300 mb-2">💡 Opportunity</div>
              <p className="text-2xl font-bold text-blue-400">Reduce Non-Brand</p>
              <p className="text-sm text-gray-400 mt-1">
                Non-brand is {Math.round(data.search.non_brand.totals.cac / data.search.brand.totals.cac)}x more expensive than brand
              </p>
            </div>
          </div>
        </section>

        {/* Search Breakdown Preview */}
        <section>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Search Campaign Breakdown</h2>
            <Link href="/ads-analysis/search" className="text-blue-400 hover:text-blue-300 text-sm">
              View Full Analysis →
            </Link>
          </div>
          <div className="bg-gray-900 rounded-xl overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-800">
                <tr>
                  <th className="text-left px-4 py-3">Segment</th>
                  <th className="text-right px-4 py-3">Spend</th>
                  <th className="text-right px-4 py-3">Subs</th>
                  <th className="text-right px-4 py-3">CVR</th>
                  <th className="text-right px-4 py-3">CAC</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                <tr className="bg-green-900/20">
                  <td className="px-4 py-3 font-medium">Brand Search</td>
                  <td className="px-4 py-3 text-right">${Math.round(data.search.brand.totals.total_spend).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right font-bold text-green-400">{Math.round(data.search.brand.totals.total_conversions).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right text-green-400">{data.search.brand.totals.cvr.toFixed(2)}%</td>
                  <td className="px-4 py-3 text-right text-green-400">${Math.round(data.search.brand.totals.cac)}</td>
                </tr>
                <tr className="bg-red-900/20">
                  <td className="px-4 py-3 font-medium">Non-Brand Search</td>
                  <td className="px-4 py-3 text-right">${Math.round(data.search.non_brand.totals.total_spend).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right font-bold text-red-400">{Math.round(data.search.non_brand.totals.total_conversions).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right text-red-400">{data.search.non_brand.totals.cvr.toFixed(2)}%</td>
                  <td className="px-4 py-3 text-right text-red-400">${Math.round(data.search.non_brand.totals.cac)}</td>
                </tr>
              </tbody>
              <tfoot className="bg-gray-800/50">
                <tr>
                  <td className="px-4 py-3 font-bold">Total Search</td>
                  <td className="px-4 py-3 text-right font-bold">${Math.round(data.search.all.totals.total_spend).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right font-bold">{Math.round(data.search.all.totals.total_conversions).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right font-bold">{data.search.all.totals.cvr.toFixed(2)}%</td>
                  <td className="px-4 py-3 text-right font-bold">${Math.round(data.search.all.totals.cac)}</td>
                </tr>
              </tfoot>
            </table>
          </div>
        </section>

        {/* Footer */}
        <div className="text-center text-gray-500 text-sm pt-8 border-t border-gray-800">
          Data Range: {data.date_range.start} to {data.date_range.end} ({daysInRange} days)
          <br />
          <span className="text-xs">Conversions = ph_subscription_created (SUBSCRIBE_PAID)</span>
          <br />
          <span className="text-xs text-gray-600">Note: Demand Gen excluded (uses different conversion event: registration_started)</span>
        </div>
      </div>
    </main>
  );
}
