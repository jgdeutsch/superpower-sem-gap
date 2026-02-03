'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Target, FlaskConical, FileText, ChevronDown, ChevronRight } from 'lucide-react';
import outlineData from '../../../data/keyword_outline.json';

interface Subcategory {
  name: string;
  keywords: string[];
  volume: number;
}

interface Category {
  name: string;
  keywords: number;
  volume: number;
  subcategories: Subcategory[];
}

interface OutlineData {
  title: string;
  total_pursue_keywords: number;
  total_pursue_volume: number;
  categories: Category[];
}

const data = outlineData as OutlineData;

export default function StrategyPage() {
  const pathname = usePathname();
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [expandedSubcategories, setExpandedSubcategories] = useState<Set<string>>(new Set());

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

  const toggleSubcategory = (subName: string) => {
    setExpandedSubcategories(prev => {
      const next = new Set(prev);
      if (next.has(subName)) {
        next.delete(subName);
      } else {
        next.add(subName);
      }
      return next;
    });
  };

  const formatVolume = (vol: number) => {
    if (vol >= 1000000) return `${(vol / 1000000).toFixed(1)}M`;
    if (vol >= 1000) return `${(vol / 1000).toFixed(0)}K`;
    return vol.toString();
  };

  // Calculate estimates
  const ctr = 0.035;
  const impressionShare = 0.5;
  const cvr = 0.018;
  const estClicks = Math.round(data.total_pursue_volume * ctr * impressionShare);
  const estConversions = Math.round(estClicks * cvr);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-blue-100">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Keyword Strategy Outline</h1>
              <p className="text-sm text-gray-600">
                {data.total_pursue_keywords.toLocaleString()} keywords grouped by test type
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
          <Link
            href="/strategy"
            className={`px-4 py-3 text-sm font-medium border-b-2 transition ${
              pathname === '/strategy'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Strategy
            </div>
          </Link>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
            <p className="text-gray-500 text-sm mb-1">Total Keywords</p>
            <p className="text-2xl font-bold text-gray-900">{data.total_pursue_keywords.toLocaleString()}</p>
          </div>
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
            <p className="text-gray-500 text-sm mb-1">Monthly Volume</p>
            <p className="text-2xl font-bold text-gray-900">{formatVolume(data.total_pursue_volume)}</p>
          </div>
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
            <p className="text-gray-500 text-sm mb-1">Est. Clicks/Month</p>
            <p className="text-2xl font-bold text-blue-600">~{estClicks.toLocaleString()}</p>
            <p className="text-xs text-gray-400">3.5% CTR, 50% IS</p>
          </div>
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
            <p className="text-gray-500 text-sm mb-1">Est. Conversions</p>
            <p className="text-2xl font-bold text-green-600">~{estConversions.toLocaleString()}</p>
            <p className="text-xs text-gray-400">1.8% CVR</p>
          </div>
        </div>

        {/* Category Outline */}
        <div className="space-y-4">
          {data.categories.map((category, catIndex) => {
            const isExpanded = expandedCategories.has(category.name);
            const catPct = Math.round((category.volume / data.total_pursue_volume) * 100);

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
                    <div className="flex items-center gap-3">
                      <span className="text-lg font-semibold text-gray-400">{catIndex + 1}.</span>
                      <div className="text-left">
                        <p className="font-semibold text-gray-900">{category.name}</p>
                        <p className="text-sm text-gray-500">
                          {category.keywords} keywords · {formatVolume(category.volume)} volume · {category.subcategories.length} groups
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <span className="text-sm font-medium text-gray-700">{catPct}%</span>
                      <p className="text-xs text-gray-400">of total</p>
                    </div>
                    <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-500 rounded-full"
                        style={{ width: `${catPct}%` }}
                      />
                    </div>
                  </div>
                </button>

                {isExpanded && (
                  <div className="border-t border-gray-200 bg-gray-50">
                    {category.subcategories.map(sub => {
                      const subKey = `${category.name}-${sub.name}`;
                      const isSubExpanded = expandedSubcategories.has(subKey);
                      const subPct = Math.round((sub.volume / category.volume) * 100);

                      return (
                        <div key={sub.name} className="border-b border-gray-200 last:border-b-0">
                          <button
                            onClick={() => toggleSubcategory(subKey)}
                            className="w-full px-5 py-3 pl-12 flex items-center justify-between hover:bg-gray-100 transition"
                          >
                            <div className="flex items-center gap-2">
                              {isSubExpanded ? (
                                <ChevronDown className="w-4 h-4 text-gray-400" />
                              ) : (
                                <ChevronRight className="w-4 h-4 text-gray-400" />
                              )}
                              <div className="text-left">
                                <p className="font-medium text-gray-800">{sub.name}</p>
                                <p className="text-xs text-gray-500">
                                  {sub.keywords.length} keywords · {formatVolume(sub.volume)} volume
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center gap-3">
                              <span className="text-sm text-gray-600">{subPct}%</span>
                              <div className="w-16 h-1.5 bg-gray-300 rounded-full overflow-hidden">
                                <div
                                  className="h-full bg-blue-400 rounded-full"
                                  style={{ width: `${subPct}%` }}
                                />
                              </div>
                            </div>
                          </button>

                          {isSubExpanded && (
                            <div className="px-5 py-3 pl-20 bg-white">
                              <div className="flex flex-wrap gap-2">
                                {sub.keywords.map(kw => (
                                  <span
                                    key={kw}
                                    className="px-2 py-1 text-sm bg-blue-50 text-blue-700 rounded border border-blue-200"
                                  >
                                    {kw}
                                  </span>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Priority Tiers */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-green-50 border border-green-200 rounded-xl p-5">
            <h3 className="font-semibold text-green-700 mb-3">Tier 1: High Priority</h3>
            <p className="text-xs text-gray-600 mb-3">High volume + strong product fit</p>
            <ul className="space-y-2 text-sm">
              <li className="flex justify-between">
                <span>Blood Tests</span>
                <span className="font-medium">304K</span>
              </li>
              <li className="flex justify-between">
                <span>Heart & Cholesterol</span>
                <span className="font-medium">216K</span>
              </li>
              <li className="flex justify-between">
                <span>Hormone Testing</span>
                <span className="font-medium">184K</span>
              </li>
              <li className="flex justify-between">
                <span>Kidney & Liver</span>
                <span className="font-medium">171K</span>
              </li>
              <li className="flex justify-between">
                <span>Thyroid Testing</span>
                <span className="font-medium">168K</span>
              </li>
            </ul>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-5">
            <h3 className="font-semibold text-yellow-700 mb-3">Tier 2: Medium Priority</h3>
            <p className="text-xs text-gray-600 mb-3">Medium volume + good fit</p>
            <ul className="space-y-2 text-sm">
              <li className="flex justify-between">
                <span>Metabolic / Diabetes</span>
                <span className="font-medium">140K</span>
              </li>
              <li className="flex justify-between">
                <span>Vitamins & Nutrients</span>
                <span className="font-medium">88K</span>
              </li>
              <li className="flex justify-between">
                <span>Inflammation</span>
                <span className="font-medium">78K</span>
              </li>
            </ul>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-xl p-5">
            <h3 className="font-semibold text-blue-700 mb-3">Tier 3: Niche / Emerging</h3>
            <p className="text-xs text-gray-600 mb-3">Lower volume but strategic</p>
            <ul className="space-y-2 text-sm">
              <li className="flex justify-between">
                <span>Aging & Longevity</span>
                <span className="font-medium">47K</span>
              </li>
              <li className="flex justify-between">
                <span>Cancer (PSA only)</span>
                <span className="font-medium">7K</span>
              </li>
              <li className="flex justify-between">
                <span>At-Home Testing</span>
                <span className="font-medium">2K</span>
              </li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}
