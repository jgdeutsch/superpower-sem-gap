'use client';

import { useState, useMemo } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Target, TrendingUp, XCircle, Users, FlaskConical, ChevronDown, ChevronRight } from 'lucide-react';
import gapData from '../../data/competitor_gap_analysis.json';

interface Keyword {
  keyword: string;
  volume: number;
  cpc: number;
  competitors: string[];
  competitor_count: number;
  category?: string;
}

interface Category {
  name: string;
  pursue: Keyword[];
  maybe: Keyword[];
  skip: Keyword[];
  pursue_count: number;
  maybe_count: number;
  skip_count: number;
  pursue_volume: number;
  maybe_volume: number;
  skip_volume: number;
}

interface GapData {
  competitors: Record<string, { total_keywords: number; total_volume: number; total_traffic: number }>;
  summary: {
    total_keywords: number;
    total_volume: number;
    pursue_keywords: number;
    maybe_keywords: number;
    skip_keywords: number;
    pursue_volume: number;
    maybe_volume: number;
    skip_volume: number;
    high_overlap_count: number;
  };
  categories: Category[];
  high_overlap: Keyword[];
}

const data = gapData as GapData;

export default function Home() {
  const pathname = usePathname();
  const [activeTab, setActiveTab] = useState<'pursue' | 'skip' | 'maybe' | 'overlap'>('pursue');
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [searchTerm, setSearchTerm] = useState('');

  const toggleCategory = (catName: string) => {
    setExpandedCategories(prev => {
      const next = new Set(prev);
      if (next.has(catName)) {
        next.delete(catName);
      } else {
        next.add(catName);
      }
      return next;
    });
  };

  // Sort categories by volume for current tab
  const sortedCategories = useMemo(() => {
    return [...data.categories].sort((a, b) => {
      if (activeTab === 'pursue') return b.pursue_volume - a.pursue_volume;
      if (activeTab === 'maybe') return b.maybe_volume - a.maybe_volume;
      if (activeTab === 'skip') return b.skip_volume - a.skip_volume;
      return 0;
    });
  }, [activeTab]);

  // Filter keywords by search
  const filterKeywords = (keywords: Keyword[]) => {
    if (!searchTerm) return keywords;
    return keywords.filter(k =>
      k.keyword.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const formatVolume = (vol: number) => {
    if (vol >= 1000000) return `${(vol / 1000000).toFixed(1)}M`;
    if (vol >= 1000) return `${(vol / 1000).toFixed(0)}K`;
    return vol.toString();
  };

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
                {Object.keys(data.competitors).length} competitors · {data.summary.total_keywords.toLocaleString()} keywords
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
            <p className="text-2xl font-bold text-gray-900">{data.summary.pursue_keywords.toLocaleString()}</p>
            <p className="text-sm text-gray-500">{formatVolume(data.summary.pursue_volume)} monthly volume</p>
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
            <p className="text-2xl font-bold text-gray-900">{data.summary.maybe_keywords.toLocaleString()}</p>
            <p className="text-sm text-gray-500">{formatVolume(data.summary.maybe_volume)} monthly volume</p>
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
            <p className="text-2xl font-bold text-gray-900">{data.summary.skip_keywords.toLocaleString()}</p>
            <p className="text-sm text-gray-500">{formatVolume(data.summary.skip_volume)} monthly volume</p>
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
              <span className="text-gray-500 text-sm">HIGH OVERLAP</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{data.summary.high_overlap_count}</p>
            <p className="text-sm text-gray-500">3+ competitors bidding</p>
          </button>
        </div>

        {/* Competitor Overview */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5 mb-8">
          <h2 className="font-semibold text-gray-900 mb-4">Competitors Analyzed</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
            {Object.entries(data.competitors)
              .sort(([, a], [, b]) => b.total_keywords - a.total_keywords)
              .map(([name, stats]) => (
                <div key={name} className="bg-gray-50 rounded-lg p-3">
                  <p className="font-medium text-gray-900 text-sm truncate">{name}</p>
                  <p className="text-xs text-gray-500">{stats.total_keywords} keywords</p>
                </div>
              ))}
          </div>
        </div>

        {/* Search */}
        <div className="mb-6">
          <input
            type="text"
            placeholder="Search keywords..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 w-64"
          />
        </div>

        {/* Categories View (for pursue/maybe/skip) */}
        {activeTab !== 'overlap' && (
          <div className="space-y-4">
            {sortedCategories.map(category => {
              const keywords = activeTab === 'pursue' ? category.pursue :
                              activeTab === 'maybe' ? category.maybe :
                              category.skip;
              const count = activeTab === 'pursue' ? category.pursue_count :
                           activeTab === 'maybe' ? category.maybe_count :
                           category.skip_count;
              const volume = activeTab === 'pursue' ? category.pursue_volume :
                            activeTab === 'maybe' ? category.maybe_volume :
                            category.skip_volume;

              if (count === 0) return null;

              const filteredKeywords = filterKeywords(keywords);
              if (searchTerm && filteredKeywords.length === 0) return null;

              const isExpanded = expandedCategories.has(category.name);

              return (
                <div key={category.name} className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                  <button
                    onClick={() => toggleCategory(category.name)}
                    className="w-full px-5 py-4 flex items-center justify-between hover:bg-gray-50 transition"
                  >
                    <div className="flex items-center gap-3">
                      {isExpanded ? (
                        <ChevronDown className="w-5 h-5 text-gray-400" />
                      ) : (
                        <ChevronRight className="w-5 h-5 text-gray-400" />
                      )}
                      <div className="text-left">
                        <p className="font-medium text-gray-900">{category.name}</p>
                        <p className="text-sm text-gray-500">
                          {count} keywords · {formatVolume(volume)} volume
                        </p>
                      </div>
                    </div>
                  </button>

                  {isExpanded && (
                    <div className="border-t border-gray-200 overflow-x-auto">
                      <table className="w-full">
                        <thead>
                          <tr className="text-left text-sm text-gray-500 bg-gray-50">
                            <th className="px-5 py-3 font-medium">Keyword</th>
                            <th className="px-5 py-3 font-medium text-right">Volume</th>
                            <th className="px-5 py-3 font-medium text-right">CPC</th>
                            <th className="px-5 py-3 font-medium">Competitors</th>
                          </tr>
                        </thead>
                        <tbody>
                          {filteredKeywords.slice(0, 25).map((kw, i) => (
                            <tr key={i} className="border-t border-gray-100 hover:bg-gray-50">
                              <td className="px-5 py-3">
                                <p className="text-gray-900">{kw.keyword}</p>
                              </td>
                              <td className="px-5 py-3 text-right text-gray-700">
                                {kw.volume.toLocaleString()}
                              </td>
                              <td className="px-5 py-3 text-right text-gray-700">
                                ${kw.cpc.toFixed(2)}
                              </td>
                              <td className="px-5 py-3">
                                <div className="flex flex-wrap gap-1">
                                  {kw.competitors.slice(0, 4).map(c => (
                                    <span key={c} className="text-xs px-1.5 py-0.5 bg-gray-100 text-gray-600 rounded">
                                      {c.split(' ')[0]}
                                    </span>
                                  ))}
                                  {kw.competitors.length > 4 && (
                                    <span className="text-xs px-1.5 py-0.5 bg-gray-100 text-gray-600 rounded">
                                      +{kw.competitors.length - 4}
                                    </span>
                                  )}
                                </div>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                      {filteredKeywords.length > 25 && (
                        <div className="px-5 py-3 bg-gray-50 text-center text-sm text-gray-500">
                          Showing 25 of {filteredKeywords.length} keywords
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* High Overlap View */}
        {activeTab === 'overlap' && (
          <div>
            <div className="bg-purple-50 border border-purple-200 rounded-xl p-5 mb-6">
              <h2 className="font-semibold text-purple-700 mb-2">High-Signal Keywords</h2>
              <p className="text-sm text-gray-600">
                These keywords are targeted by 3+ competitors. Multiple competitors bidding = validated demand.
              </p>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
              <table className="w-full">
                <thead>
                  <tr className="text-left text-sm text-gray-500 bg-gray-50 border-b border-gray-200">
                    <th className="px-5 py-3 font-medium">Keyword</th>
                    <th className="px-5 py-3 font-medium">Category</th>
                    <th className="px-5 py-3 font-medium text-right">Volume</th>
                    <th className="px-5 py-3 font-medium text-right">CPC</th>
                    <th className="px-5 py-3 font-medium text-center"># Competitors</th>
                    <th className="px-5 py-3 font-medium">Competitors</th>
                  </tr>
                </thead>
                <tbody>
                  {filterKeywords(data.high_overlap).slice(0, 50).map((kw, i) => (
                    <tr key={i} className="border-t border-gray-100 hover:bg-gray-50">
                      <td className="px-5 py-3">
                        <p className="text-gray-900 font-medium">{kw.keyword}</p>
                      </td>
                      <td className="px-5 py-3">
                        <span className="text-xs px-2 py-1 bg-purple-100 text-purple-700 rounded-full">
                          {kw.category}
                        </span>
                      </td>
                      <td className="px-5 py-3 text-right text-gray-700">
                        {kw.volume.toLocaleString()}
                      </td>
                      <td className="px-5 py-3 text-right text-gray-700">
                        ${kw.cpc.toFixed(2)}
                      </td>
                      <td className="px-5 py-3 text-center">
                        <span className="inline-flex items-center justify-center w-6 h-6 bg-purple-600 text-white text-xs rounded-full font-medium">
                          {kw.competitor_count}
                        </span>
                      </td>
                      <td className="px-5 py-3">
                        <div className="flex flex-wrap gap-1">
                          {kw.competitors.map(c => (
                            <span key={c} className="text-xs px-1.5 py-0.5 bg-purple-100 text-purple-700 rounded">
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
          <div className="mt-8 bg-red-50 border border-red-200 rounded-xl p-5">
            <h3 className="font-semibold text-red-700 mb-2">Why Skip These?</h3>
            <p className="text-sm text-gray-600 mb-4">
              These keywords are for services Superpower doesn&apos;t offer or can&apos;t compete effectively on:
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="bg-white rounded-lg p-3 border border-red-100">
                <p className="font-medium text-gray-900 text-sm">STD/STI Testing</p>
                <p className="text-xs text-gray-500">Not offered</p>
              </div>
              <div className="bg-white rounded-lg p-3 border border-red-100">
                <p className="font-medium text-gray-900 text-sm">Food Allergies</p>
                <p className="text-xs text-gray-500">Not offered</p>
              </div>
              <div className="bg-white rounded-lg p-3 border border-red-100">
                <p className="font-medium text-gray-900 text-sm">Drug Testing</p>
                <p className="text-xs text-gray-500">Not offered</p>
              </div>
              <div className="bg-white rounded-lg p-3 border border-red-100">
                <p className="font-medium text-gray-900 text-sm">Lab Locations</p>
                <p className="text-xs text-gray-500">&quot;Near me&quot; searches</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
