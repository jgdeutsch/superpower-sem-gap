'use client';

import { useState, useMemo } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Target, TrendingUp, XCircle, Users, FlaskConical } from 'lucide-react';
import gapFitData from '../../data/gap_product_fit.json';
import competitorOverlap from '../../data/competitor_overlap.json';

interface Opportunity {
  category: string;
  topic: string;
  competitor: string;
  keyword_count: number;
  total_volume: number;
  top_keywords: string[];
  sample_kw: string;
  reason: string;
}

interface GapFitData {
  pursue: Opportunity[];
  maybe: Opportunity[];
  skip: Opportunity[];
  competitor_brand: Opportunity[];
}

interface OverlapKeyword {
  competitors: string[];
  volume: number;
  cpc: number;
}

interface CompetitorOverlapData {
  all_5_competitors: Record<string, OverlapKeyword>;
  '3plus_competitors': Record<string, OverlapKeyword>;
  summary: {
    total_keywords: number;
    keywords_3plus: number;
    keywords_4plus: number;
    keywords_all_5: number;
  };
}

const data = gapFitData as GapFitData;
const overlap = competitorOverlap as CompetitorOverlapData;

// CVR benchmarks from Google Ads data
const CVR_BY_CATEGORY: Record<string, number> = {
  glucose: 7.69,
  cortisol: 5.56,
  cancer: 2.66,
  competitor: 1.91,
  blood_tests: 1.73,
  hormones: 1.66,
  metabolic: 1.54,
  default: 1.43,
  vitamins: 1.38,
};

// CAC (Cost per Acquisition) from Google Ads data
const CAC_BY_CATEGORY: Record<string, number> = {
  glucose: 87,
  cortisol: 99,
  cancer: 233,
  competitor: 360,
  blood_tests: 361,
  hormones: 410,
  metabolic: 352,
  default: 441,
  vitamins: 304,
};

// Monthly subscriptions from Google Ads data (Aug 23 - Sep 21, 2025)
const SUBS_BY_CATEGORY: Record<string, number> = {
  glucose: 1.0,
  cortisol: 2.0,
  cancer: 5.5,
  competitor: 18.6,
  blood_tests: 13.0,
  hormones: 5.0,
  metabolic: 1.0,
  default: 77.2,  // total
  vitamins: 3.6,
};

const CTR_ESTIMATE = 3.5; // 3.5% CTR assumption

function getCvrForTopic(topic: string, category: string): number {
  const topicLower = topic.toLowerCase();
  const catLower = category.toLowerCase();

  if (topicLower.includes('cortisol') || topicLower.includes('stress')) return CVR_BY_CATEGORY.cortisol;
  if (topicLower.includes('glucose') || topicLower.includes('diabetes') || topicLower.includes('a1c')) return CVR_BY_CATEGORY.glucose;
  if (topicLower.includes('cancer')) return CVR_BY_CATEGORY.cancer;
  if (topicLower.includes('hormone') || topicLower.includes('testosterone')) return CVR_BY_CATEGORY.hormones;
  if (topicLower.includes('vitamin')) return CVR_BY_CATEGORY.vitamins;
  if (topicLower.includes('metabolic')) return CVR_BY_CATEGORY.metabolic;
  if (catLower.includes('blood') || catLower.includes('panel')) return CVR_BY_CATEGORY.blood_tests;
  return CVR_BY_CATEGORY.default;
}

function aggregateOpportunities(opps: Opportunity[]) {
  const map = new Map<string, {
    category: string;
    topic: string;
    competitors: string[];
    keyword_count: number;
    total_volume: number;
    top_keywords: string[];
    reason: string;
    est_cvr: number;
    est_monthly_conversions: number;
    est_annual_conversions: number;
  }>();

  opps.forEach(opp => {
    const key = `${opp.category}::${opp.topic}`;
    const cvr = getCvrForTopic(opp.topic, opp.category);
    const clicks = opp.total_volume * (CTR_ESTIMATE / 100);
    const monthlyConv = clicks * (cvr / 100);

    const existing = map.get(key);
    if (existing) {
      if (!existing.competitors.includes(opp.competitor)) {
        existing.competitors.push(opp.competitor);
      }
      existing.keyword_count = Math.max(existing.keyword_count, opp.keyword_count);
      existing.total_volume = Math.max(existing.total_volume, opp.total_volume);
      opp.top_keywords.forEach(kw => {
        if (!existing.top_keywords.includes(kw)) existing.top_keywords.push(kw);
      });
    } else {
      map.set(key, {
        category: opp.category,
        topic: opp.topic,
        competitors: [opp.competitor],
        keyword_count: opp.keyword_count,
        total_volume: opp.total_volume,
        top_keywords: [...opp.top_keywords],
        reason: opp.reason,
        est_cvr: cvr,
        est_monthly_conversions: monthlyConv,
        est_annual_conversions: monthlyConv * 12,
      });
    }
  });

  return Array.from(map.values()).sort((a, b) => b.est_annual_conversions - a.est_annual_conversions);
}

export default function Home() {
  const pathname = usePathname();
  const [activeTab, setActiveTab] = useState<'pursue' | 'skip' | 'maybe' | 'overlap'>('pursue');
  const [minVolume, setMinVolume] = useState(0);

  const pursue = useMemo(() => aggregateOpportunities(data.pursue), []);
  const skip = useMemo(() => aggregateOpportunities(data.skip), []);
  const maybe = useMemo(() => aggregateOpportunities(data.maybe), []);

  const pursueConversions = pursue.reduce((sum, o) => sum + o.est_annual_conversions, 0);
  const maybeConversions = maybe.reduce((sum, o) => sum + o.est_annual_conversions, 0);
  const skipVolume = skip.reduce((sum, o) => sum + o.total_volume, 0);

  const activeData = activeTab === 'pursue' ? pursue : activeTab === 'skip' ? skip : maybe;
  const filteredData = activeData.filter(o => o.total_volume >= minVolume);

  const overlapKeywords = useMemo(() => {
    return Object.entries(overlap['3plus_competitors'])
      .map(([keyword, info]) => ({ keyword, ...info }))
      .sort((a, b) => b.volume - a.volume);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-indigo-100">
              <Target className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">SEM Gap Analysis</h1>
              <p className="text-sm text-gray-600">
                Based on Superpower&apos;s actual CVR by category (1.4-7.7%) and 3.5% CTR assumption
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-gray-200 px-6">
        <div className="max-w-7xl mx-auto flex gap-1">
          <Link
            href="/"
            className={`px-4 py-3 text-sm font-medium border-b-2 transition ${
              pathname === '/'
                ? 'border-indigo-500 text-indigo-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center gap-2">
              <Target className="w-4 h-4" />
              Competitor Gap
            </div>
          </Link>
          <Link
            href="/tests"
            className={`px-4 py-3 text-sm font-medium border-b-2 transition ${
              pathname === '/tests'
                ? 'border-emerald-500 text-emerald-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center gap-2">
              <FlaskConical className="w-4 h-4" />
              Testing Gap
            </div>
          </Link>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <button
            onClick={() => setActiveTab('pursue')}
            className={`bg-white rounded-xl p-5 border shadow-sm text-left transition ${
              activeTab === 'pursue' ? 'border-green-500 ring-2 ring-green-200' : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-green-100 p-2 rounded-lg">
                <TrendingUp className="w-5 h-5 text-green-600" />
              </div>
              <span className="text-gray-500 text-sm">PURSUE</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{Math.round(pursueConversions / 12)}</p>
            <p className="text-sm text-gray-500">est. subscriptions/mo</p>
            <p className="text-xs text-gray-400 mt-1">{pursue.length} topics</p>
          </button>

          <button
            onClick={() => setActiveTab('maybe')}
            className={`bg-white rounded-xl p-5 border shadow-sm text-left transition ${
              activeTab === 'maybe' ? 'border-yellow-500 ring-2 ring-yellow-200' : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-yellow-100 p-2 rounded-lg">
                <Target className="w-5 h-5 text-yellow-600" />
              </div>
              <span className="text-gray-500 text-sm">MAYBE</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{Math.round(maybeConversions / 12)}</p>
            <p className="text-sm text-gray-500">potential subs/mo</p>
            <p className="text-xs text-gray-400 mt-1">{maybe.length} topics to review</p>
          </button>

          <button
            onClick={() => setActiveTab('skip')}
            className={`bg-white rounded-xl p-5 border shadow-sm text-left transition ${
              activeTab === 'skip' ? 'border-red-500 ring-2 ring-red-200' : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-red-100 p-2 rounded-lg">
                <XCircle className="w-5 h-5 text-red-600" />
              </div>
              <span className="text-gray-500 text-sm">SKIP</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{(skipVolume / 1000).toFixed(0)}K</p>
            <p className="text-sm text-gray-500">volume to avoid</p>
            <p className="text-xs text-gray-400 mt-1">{skip.length} topics (no product)</p>
          </button>

          <button
            onClick={() => setActiveTab('overlap')}
            className={`bg-white rounded-xl p-5 border shadow-sm text-left transition ${
              activeTab === 'overlap' ? 'border-purple-500 ring-2 ring-purple-200' : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-purple-100 p-2 rounded-lg">
                <Users className="w-5 h-5 text-purple-600" />
              </div>
              <span className="text-gray-500 text-sm">OVERLAP</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{overlap.summary.keywords_3plus}</p>
            <p className="text-sm text-gray-500">keywords 3+ comps target</p>
            <p className="text-xs text-gray-400 mt-1">High-signal opportunities</p>
          </button>
        </div>

        {activeTab !== 'overlap' && (
          <>
            {/* Filter */}
            <div className="flex items-center gap-4 mb-4">
              <span className="text-sm text-gray-600">Min Volume:</span>
              <select
                value={minVolume}
                onChange={e => setMinVolume(Number(e.target.value))}
                className="bg-white border border-gray-300 rounded-md px-3 py-1.5 text-sm focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              >
                <option value={0}>All</option>
                <option value={1000}>1K+</option>
                <option value={5000}>5K+</option>
                <option value={10000}>10K+</option>
              </select>
              <span className="text-sm text-gray-500">
                Showing {filteredData.length} of {activeData.length}
              </span>
            </div>

            {/* Opportunities Table */}
            <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="text-left text-sm text-gray-600 border-b border-gray-200 bg-gray-50">
                    <th className="px-5 py-3 font-medium">Topic</th>
                    <th className="px-5 py-3 font-medium">Reason</th>
                    <th className="px-5 py-3 text-right font-medium">Volume</th>
                    <th className="px-5 py-3 text-right font-medium">CVR</th>
                    <th className="px-5 py-3 text-right font-medium">Est. Subs/Mo</th>
                    <th className="px-5 py-3 font-medium">Keywords</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredData.map((opp, i) => (
                    <tr key={i} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="px-5 py-4">
                        <p className="text-xs text-gray-500">{opp.category}</p>
                        <p className="font-medium text-gray-900">{opp.topic}</p>
                      </td>
                      <td className="px-5 py-4">
                        <span className={`text-xs px-2 py-1 rounded font-medium ${
                          activeTab === 'pursue' ? 'bg-green-100 text-green-700' :
                          activeTab === 'skip' ? 'bg-red-100 text-red-700' :
                          'bg-yellow-100 text-yellow-700'
                        }`}>
                          {opp.reason.replace('Strong fit: ', '').replace('Not offered: ', '').replace(/_/g, ' ')}
                        </span>
                      </td>
                      <td className="px-5 py-4 text-right text-gray-700">{(opp.total_volume / 1000).toFixed(0)}K</td>
                      <td className="px-5 py-4 text-right text-green-600 font-medium">{opp.est_cvr.toFixed(1)}%</td>
                      <td className="px-5 py-4 text-right font-bold text-blue-600">{opp.est_monthly_conversions.toFixed(1)}</td>
                      <td className="px-5 py-4">
                        <p className="text-xs text-gray-500 max-w-xs truncate">
                          {opp.top_keywords.slice(0, 3).join(', ')}
                        </p>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}

        {/* Competitor Overlap View */}
        {activeTab === 'overlap' && (
          <div>
            <div className="bg-purple-50 border border-purple-200 rounded-xl p-4 mb-6">
              <h3 className="font-semibold text-purple-700 mb-2">High-Signal Keywords</h3>
              <p className="text-sm text-gray-600">
                These keywords are targeted by 3+ competitors (Function Health, Everlywell, InsideTracker, Rupa Health, Mito Health).
                Multiple competitors bidding = validated demand.
              </p>
              <div className="grid grid-cols-3 gap-4 mt-4">
                <div className="bg-white rounded-lg p-3 text-center border border-purple-100">
                  <div className="text-2xl font-bold text-purple-600">{overlap.summary.keywords_3plus}</div>
                  <div className="text-xs text-gray-500">3+ competitors</div>
                </div>
                <div className="bg-white rounded-lg p-3 text-center border border-purple-100">
                  <div className="text-2xl font-bold text-purple-600">{overlap.summary.keywords_4plus}</div>
                  <div className="text-xs text-gray-500">4+ competitors</div>
                </div>
                <div className="bg-white rounded-lg p-3 text-center border border-purple-100">
                  <div className="text-2xl font-bold text-purple-600">{overlap.summary.total_keywords}</div>
                  <div className="text-xs text-gray-500">total unique keywords</div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="text-left text-sm text-gray-600 border-b border-gray-200 bg-gray-50">
                    <th className="px-5 py-3 font-medium">Keyword</th>
                    <th className="px-5 py-3 text-right font-medium">Volume</th>
                    <th className="px-5 py-3 text-right font-medium">CPC</th>
                    <th className="px-5 py-3 font-medium">Competitors</th>
                  </tr>
                </thead>
                <tbody>
                  {overlapKeywords.slice(0, 50).map((kw, i) => (
                    <tr key={i} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="px-5 py-4 font-medium text-gray-900">{kw.keyword}</td>
                      <td className="px-5 py-4 text-right text-gray-700">{kw.volume.toLocaleString()}</td>
                      <td className="px-5 py-4 text-right text-gray-700">${kw.cpc.toFixed(2)}</td>
                      <td className="px-5 py-4">
                        <div className="flex flex-wrap gap-1">
                          {kw.competitors.map(c => (
                            <span key={c} className="text-xs px-1.5 py-0.5 bg-purple-100 text-purple-700 rounded font-medium">
                              {c.split(' ')[0]}
                            </span>
                          ))}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Skip explanation */}
        {activeTab === 'skip' && (
          <div className="mt-8 grid grid-cols-3 gap-4">
            <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
              <div className="text-red-600 font-semibold mb-2">STD/STI Testing</div>
              <p className="text-sm text-gray-600">No herpes, HIV, chlamydia, gonorrhea testing</p>
            </div>
            <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
              <div className="text-red-600 font-semibold mb-2">Food Allergy Tests</div>
              <p className="text-sm text-gray-600">No food sensitivity or intolerance testing</p>
            </div>
            <div className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm">
              <div className="text-red-600 font-semibold mb-2">Physical Locations</div>
              <p className="text-sm text-gray-600">No &quot;near me&quot; or walk-in lab services</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
