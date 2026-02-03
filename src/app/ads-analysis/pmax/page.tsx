'use client';

import Link from 'next/link';
import { useAdsData } from '@/context/AdsDataContext';
import DateRangePicker from '@/components/DateRangePicker';

export default function PMaxAnalysis() {
  const { data, isLoading, startDate, endDate, setDateRange } = useAdsData();

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

  const pmax = data.pmax;
  const hasData = pmax.totals.total_spend > 100;
  const brandSearchCac = data.search.brand.totals.cac;
  const nonBrandSearchCac = data.search.non_brand.totals.cac;

  // Calculate days in range
  const startDt = new Date(data.date_range.start);
  const endDt = new Date(data.date_range.end);
  const daysInRange = Math.round((endDt.getTime() - startDt.getTime()) / (1000 * 60 * 60 * 24));

  const getCvrClass = (cvr: number) => {
    if (cvr >= 3) return 'text-green-400';
    if (cvr >= 1.5) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getCacClass = (cac: number) => {
    if (cac === 0) return 'text-gray-500';
    if (cac <= 100) return 'text-green-400';
    if (cac <= 250) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getRowBgClass = (cvr: number) => {
    if (cvr >= 3) return 'bg-green-900/20';
    if (cvr >= 1.5) return 'bg-yellow-900/20';
    return 'bg-red-900/20';
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white">
      <div className="bg-gray-900 border-b border-gray-800 px-6 py-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/ads-analysis" className="text-gray-400 hover:text-white text-sm">&larr; All Campaigns</Link>
              <h1 className="text-2xl font-bold flex items-center gap-2">
                <span>⚡</span> Performance Max Analysis
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
              Overview
            </Link>
            <Link
              href="/ads-analysis/search"
              className="px-3 py-1 bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm rounded-lg transition-colors"
            >
              🔍 Search
            </Link>
            <Link
              href="/ads-analysis/pmax"
              className="px-3 py-1 bg-blue-600 text-white text-sm rounded-lg"
            >
              ⚡ PMax
            </Link>
          </div>
          <p className="text-gray-400 text-sm mt-2">
            Cross-Channel Automated Campaigns | {daysInRange} days of data
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6 space-y-8">
        {/* Status Banner */}
        {hasData ? (
          <section>
            <div className="bg-yellow-900/30 border border-yellow-700/50 rounded-xl p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-3xl">⚠️</span>
                <div>
                  <h2 className="text-xl font-bold text-yellow-300">High CAC Channel</h2>
                  <p className="text-gray-400">
                    PMax at ${Math.round(pmax.totals.cac)} CAC is {Math.round(pmax.totals.cac / brandSearchCac)}x more expensive than Brand Search (${Math.round(brandSearchCac)})
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-4 gap-6">
                <div>
                  <div className="text-4xl font-bold text-yellow-400">${Math.round(pmax.totals.cac)}</div>
                  <div className="text-sm text-gray-400">CAC</div>
                </div>
                <div>
                  <div className="text-4xl font-bold text-yellow-400">{pmax.totals.cvr.toFixed(2)}%</div>
                  <div className="text-sm text-gray-400">CVR</div>
                </div>
                <div>
                  <div className="text-4xl font-bold text-white">{Math.round(pmax.totals.total_conversions).toLocaleString()}</div>
                  <div className="text-sm text-gray-400">Subscriptions</div>
                </div>
                <div>
                  <div className="text-4xl font-bold text-white">${Math.round(pmax.totals.total_spend / 1000)}K</div>
                  <div className="text-sm text-gray-400">Spend</div>
                </div>
              </div>
            </div>
          </section>
        ) : (
          <section>
            <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-3xl">📭</span>
                <div>
                  <h2 className="text-xl font-bold text-white">No Active PMax Campaigns</h2>
                  <p className="text-gray-400">
                    Performance Max campaigns have no significant spend in the selected period
                  </p>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Summary Cards */}
        <section>
          <h2 className="text-xl font-semibold mb-4">Performance Metrics</h2>
          <div className="grid grid-cols-5 gap-4">
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-blue-400">${Math.round(pmax.totals.total_spend / 1000)}K</div>
              <div className="text-sm text-gray-400">Total Spend</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-blue-400">{Math.round(pmax.totals.total_clicks).toLocaleString()}</div>
              <div className="text-sm text-gray-400">Total Clicks</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className="text-3xl font-bold text-yellow-400">{Math.round(pmax.totals.total_conversions).toLocaleString()}</div>
              <div className="text-sm text-gray-400">Subscriptions</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className={`text-3xl font-bold ${getCvrClass(pmax.totals.cvr)}`}>{pmax.totals.cvr.toFixed(2)}%</div>
              <div className="text-sm text-gray-400">CVR</div>
            </div>
            <div className="bg-gray-900 rounded-xl p-4 border border-gray-800">
              <div className={`text-3xl font-bold ${getCacClass(pmax.totals.cac)}`}>${Math.round(pmax.totals.cac)}</div>
              <div className="text-sm text-gray-400">CAC</div>
            </div>
          </div>
        </section>

        {/* Comparison to Other Channels */}
        <section>
          <h2 className="text-xl font-semibold mb-4">CAC Comparison</h2>
          <div className="bg-gray-900 rounded-xl overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-800">
                <tr>
                  <th className="text-left px-4 py-3">Channel</th>
                  <th className="text-right px-4 py-3">Spend</th>
                  <th className="text-right px-4 py-3">Subs</th>
                  <th className="text-right px-4 py-3">CVR</th>
                  <th className="text-right px-4 py-3">CAC</th>
                  <th className="text-right px-4 py-3">vs Brand</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                <tr className="bg-green-900/20">
                  <td className="px-4 py-3 font-medium">Brand Search</td>
                  <td className="px-4 py-3 text-right">${Math.round(data.search.brand.totals.total_spend / 1000)}K</td>
                  <td className="px-4 py-3 text-right">{Math.round(data.search.brand.totals.total_conversions).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right text-green-400">{data.search.brand.totals.cvr.toFixed(2)}%</td>
                  <td className="px-4 py-3 text-right text-green-400">${Math.round(brandSearchCac)}</td>
                  <td className="px-4 py-3 text-right text-green-400">1x</td>
                </tr>
                <tr className={getRowBgClass(pmax.totals.cvr)}>
                  <td className="px-4 py-3 font-medium">Performance Max</td>
                  <td className="px-4 py-3 text-right">${Math.round(pmax.totals.total_spend / 1000)}K</td>
                  <td className="px-4 py-3 text-right">{Math.round(pmax.totals.total_conversions).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right">
                    <span className={getCvrClass(pmax.totals.cvr)}>{pmax.totals.cvr.toFixed(2)}%</span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <span className={getCacClass(pmax.totals.cac)}>${Math.round(pmax.totals.cac)}</span>
                  </td>
                  <td className="px-4 py-3 text-right text-red-400">{Math.round(pmax.totals.cac / brandSearchCac)}x</td>
                </tr>
                <tr className="bg-red-900/20">
                  <td className="px-4 py-3 font-medium">Non-Brand Search</td>
                  <td className="px-4 py-3 text-right">${Math.round(data.search.non_brand.totals.total_spend / 1000)}K</td>
                  <td className="px-4 py-3 text-right">{Math.round(data.search.non_brand.totals.total_conversions).toLocaleString()}</td>
                  <td className="px-4 py-3 text-right text-red-400">{data.search.non_brand.totals.cvr.toFixed(2)}%</td>
                  <td className="px-4 py-3 text-right text-red-400">${Math.round(nonBrandSearchCac)}</td>
                  <td className="px-4 py-3 text-right text-red-400">{Math.round(nonBrandSearchCac / brandSearchCac)}x</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="mt-4 p-4 bg-blue-900/20 border border-blue-800/50 rounded-xl">
            <p className="text-sm text-gray-400">
              <strong className="text-blue-300">Note:</strong> PMax CAC (${Math.round(pmax.totals.cac)}) is better than Non-Brand Search (${Math.round(nonBrandSearchCac)}) but {Math.round(pmax.totals.cac / brandSearchCac)}x worse than Brand Search (${Math.round(brandSearchCac)}).
              {pmax.totals.cac < nonBrandSearchCac && (
                <span className="block mt-2">Consider shifting some Non-Brand Search budget to PMax for better efficiency.</span>
              )}
            </p>
          </div>
        </section>

        {/* Campaigns */}
        {pmax.campaigns.length > 0 && (
          <section>
            <h2 className="text-xl font-semibold mb-4">Campaigns</h2>
            <div className="bg-gray-900 rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-gray-800">
                  <tr>
                    <th className="text-left px-4 py-3">Campaign</th>
                    <th className="text-right px-4 py-3">Spend</th>
                    <th className="text-right px-4 py-3">Clicks</th>
                    <th className="text-right px-4 py-3">Subs</th>
                    <th className="text-right px-4 py-3">CVR</th>
                    <th className="text-right px-4 py-3">CAC</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-800">
                  {pmax.campaigns.map((campaign, idx) => (
                    <tr key={idx} className={getRowBgClass(campaign.cvr)}>
                      <td className="px-4 py-3 font-medium">{campaign.name}</td>
                      <td className="px-4 py-3 text-right">${Math.round(campaign.total_spend).toLocaleString()}</td>
                      <td className="px-4 py-3 text-right">{Math.round(campaign.total_clicks).toLocaleString()}</td>
                      <td className="px-4 py-3 text-right font-bold">
                        <span className={getCvrClass(campaign.cvr)}>{Math.round(campaign.total_conversions)}</span>
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
        )}

        {/* Recommendations */}
        <section>
          <h2 className="text-xl font-semibold mb-4">Recommendations</h2>
          <div className="grid grid-cols-2 gap-6">
            <div className="bg-yellow-900/20 border border-yellow-800/50 rounded-xl p-5">
              <div className="font-semibold text-yellow-300 mb-3 text-lg">Issues</div>
              <ul className="text-sm text-gray-300 space-y-3">
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 mt-0.5">⚠</span>
                  <div>
                    <strong>High CAC at ${Math.round(pmax.totals.cac)}</strong><br/>
                    <span className="text-gray-500">{Math.round(pmax.totals.cac / brandSearchCac)}x more expensive than Brand Search</span>
                  </div>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 mt-0.5">⚠</span>
                  <div>
                    <strong>Low CVR at {pmax.totals.cvr.toFixed(2)}%</strong><br/>
                    <span className="text-gray-500">vs {data.search.brand.totals.cvr.toFixed(2)}% for Brand Search</span>
                  </div>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-yellow-400 mt-0.5">⚠</span>
                  <div>
                    <strong>Limited transparency</strong><br/>
                    <span className="text-gray-500">Can&apos;t see which placements/audiences convert</span>
                  </div>
                </li>
              </ul>
            </div>
            <div className="bg-green-900/20 border border-green-800/50 rounded-xl p-5">
              <div className="font-semibold text-green-300 mb-3 text-lg">Optimization Options</div>
              <ul className="text-sm text-gray-300 space-y-3">
                {pmax.totals.cac < nonBrandSearchCac ? (
                  <li className="flex items-start gap-2">
                    <span className="text-green-400 mt-0.5">✓</span>
                    <div>
                      <strong>Better than Non-Brand Search</strong><br/>
                      <span className="text-gray-500">Consider shifting Non-Brand budget here</span>
                    </div>
                  </li>
                ) : (
                  <li className="flex items-start gap-2">
                    <span className="text-yellow-400 mt-0.5">→</span>
                    <div>
                      <strong>Reduce PMax budget</strong><br/>
                      <span className="text-gray-500">Reallocate to Brand Search</span>
                    </div>
                  </li>
                )}
                <li className="flex items-start gap-2">
                  <span className="text-green-400 mt-0.5">✓</span>
                  <div>
                    <strong>Tighten target CPA</strong><br/>
                    <span className="text-gray-500">Set target closer to ${Math.round(brandSearchCac * 3)}-${Math.round(brandSearchCac * 4)}</span>
                  </div>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-400 mt-0.5">✓</span>
                  <div>
                    <strong>Review asset quality</strong><br/>
                    <span className="text-gray-500">Ensure videos and images are converting</span>
                  </div>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-400 mt-0.5">✓</span>
                  <div>
                    <strong>Add negative brand keywords</strong><br/>
                    <span className="text-gray-500">Prevent cannibalization of Brand Search</span>
                  </div>
                </li>
              </ul>
            </div>
          </div>

          <div className="mt-6 p-5 bg-blue-900/20 border border-blue-800/50 rounded-xl">
            <div className="font-semibold text-blue-300 mb-2">Budget Reallocation Opportunity</div>
            <p className="text-gray-400 mb-4">
              If you moved ${Math.round(pmax.totals.total_spend / 1000)}K from PMax to Brand Search (at current ${Math.round(brandSearchCac)} CAC):
            </p>
            <div className="grid grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-white">{Math.round(pmax.totals.total_conversions)}</div>
                <div className="text-sm text-gray-500">Current PMax Subs</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-400">{Math.round(pmax.totals.total_spend / brandSearchCac).toLocaleString()}</div>
                <div className="text-sm text-gray-500">Potential Brand Subs</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-400">+{Math.round((pmax.totals.total_spend / brandSearchCac) - pmax.totals.total_conversions).toLocaleString()}</div>
                <div className="text-sm text-gray-500">Additional Subs</div>
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-4">
              Note: Brand Search may have limited scale. Test incrementally before fully reallocating.
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}
