'use client';

import { useState, useMemo } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { FlaskConical, Target, Check, X, ChevronDown, ChevronRight } from 'lucide-react';
import testsData from '../../../data/superpower_tests.json';

interface Test {
  name: string;
  slug: string;
  has_ads: boolean;
  in_baseline?: boolean;
}

interface Category {
  name: string;
  type: string;
  tests: Test[];
  count: number;
  with_ads: number;
  without_ads: number;
}

interface TestsData {
  categories: Category[];
  summary: {
    total_tests: number;
    with_ads: number;
    without_ads: number;
    coverage_pct: number;
  };
}

const data = testsData as TestsData;

export default function TestsPage() {
  const pathname = usePathname();
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set());
  const [filterType, setFilterType] = useState<'all' | 'with_ads' | 'without_ads'>('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Group categories by type
  const categoryGroups = useMemo(() => {
    const groups: Record<string, Category[]> = {};
    data.categories.forEach(cat => {
      if (!groups[cat.type]) groups[cat.type] = [];
      groups[cat.type].push(cat);
    });
    return groups;
  }, []);

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

  const filteredTests = (tests: Test[]) => {
    let filtered = tests;
    if (filterType === 'with_ads') {
      filtered = tests.filter(t => t.has_ads);
    } else if (filterType === 'without_ads') {
      filtered = tests.filter(t => !t.has_ads);
    }
    if (searchTerm) {
      filtered = filtered.filter(t =>
        t.name.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    return filtered;
  };

  // Priority opportunities (high-value categories with 0% coverage)
  const priorityOpportunities = data.categories
    .filter(c => c.with_ads === 0 && c.count >= 10)
    .sort((a, b) => b.count - a.count);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-emerald-100">
              <FlaskConical className="w-6 h-6 text-emerald-600" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Superpower Testing Gap Analysis</h1>
              <p className="text-sm text-gray-600">
                Which tests have Google Ads vs. untapped opportunities
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
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-gray-100 p-2 rounded-lg">
                <FlaskConical className="w-5 h-5 text-gray-600" />
              </div>
              <span className="text-gray-500 text-sm">Total Tests</span>
            </div>
            <p className="text-2xl font-bold text-gray-900">{data.summary.total_tests}</p>
            <p className="text-sm text-gray-500">across {data.categories.length} categories</p>
          </div>

          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-green-100 p-2 rounded-lg">
                <Check className="w-5 h-5 text-green-600" />
              </div>
              <span className="text-gray-500 text-sm">With Ads</span>
            </div>
            <p className="text-2xl font-bold text-green-600">{data.summary.with_ads}</p>
            <p className="text-sm text-gray-500">{data.summary.coverage_pct}% coverage</p>
          </div>

          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-red-100 p-2 rounded-lg">
                <X className="w-5 h-5 text-red-600" />
              </div>
              <span className="text-gray-500 text-sm">Without Ads</span>
            </div>
            <p className="text-2xl font-bold text-red-600">{data.summary.without_ads}</p>
            <p className="text-sm text-gray-500">untapped opportunities</p>
          </div>

          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
            <div className="flex items-center gap-3 mb-3">
              <div className="bg-orange-100 p-2 rounded-lg">
                <Target className="w-5 h-5 text-orange-600" />
              </div>
              <span className="text-gray-500 text-sm">0% Coverage</span>
            </div>
            <p className="text-2xl font-bold text-orange-600">{priorityOpportunities.length}</p>
            <p className="text-sm text-gray-500">high-priority categories</p>
          </div>
        </div>

        {/* Priority Opportunities */}
        <div className="bg-orange-50 border border-orange-200 rounded-xl p-5 mb-8">
          <h2 className="font-semibold text-orange-700 mb-3">High-Priority Opportunities (0% Ad Coverage)</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {priorityOpportunities.slice(0, 8).map(cat => (
              <div key={cat.name} className="bg-white rounded-lg p-3 border border-orange-100">
                <p className="font-medium text-gray-900 text-sm">{cat.name}</p>
                <p className="text-xs text-gray-500">{cat.count} tests, 0 ads</p>
              </div>
            ))}
          </div>
        </div>

        {/* Filters */}
        <div className="flex items-center gap-4 mb-6">
          <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setFilterType('all')}
              className={`px-4 py-2 text-sm rounded-md transition ${
                filterType === 'all' ? 'bg-white shadow text-gray-900' : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              All Tests
            </button>
            <button
              onClick={() => setFilterType('with_ads')}
              className={`px-4 py-2 text-sm rounded-md transition ${
                filterType === 'with_ads' ? 'bg-green-600 text-white' : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              With Ads
            </button>
            <button
              onClick={() => setFilterType('without_ads')}
              className={`px-4 py-2 text-sm rounded-md transition ${
                filterType === 'without_ads' ? 'bg-red-600 text-white' : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Without Ads
            </button>
          </div>

          <input
            type="text"
            placeholder="Search tests..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 w-64"
          />
        </div>

        {/* Categories by Type */}
        {Object.entries(categoryGroups).map(([groupType, categories]) => (
          <div key={groupType} className="mb-8">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">{groupType}</h2>
            <div className="space-y-3">
              {categories.map(category => {
                const filtered = filteredTests(category.tests);
                if (filtered.length === 0 && (filterType !== 'all' || searchTerm)) return null;

                const isExpanded = expandedCategories.has(category.name);
                const coveragePct = category.count > 0 ? Math.round((category.with_ads / category.count) * 100) : 0;

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
                            {category.count} tests
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="text-right">
                          <div className="flex items-center gap-2">
                            <span className={`text-sm font-medium ${coveragePct > 0 ? 'text-green-600' : 'text-red-600'}`}>
                              {coveragePct}% coverage
                            </span>
                          </div>
                          <p className="text-xs text-gray-500">
                            {category.with_ads} with ads, {category.without_ads} without
                          </p>
                        </div>
                        {/* Coverage bar */}
                        <div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-green-500 rounded-full"
                            style={{ width: `${coveragePct}%` }}
                          />
                        </div>
                      </div>
                    </button>

                    {isExpanded && (
                      <div className="border-t border-gray-200 px-5 py-4 bg-gray-50">
                        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
                          {filtered.map(test => (
                            <div
                              key={test.name}
                              className={`px-3 py-2 rounded-lg text-sm flex items-center gap-2 ${
                                test.has_ads
                                  ? 'bg-green-100 text-green-700 border border-green-200'
                                  : 'bg-white text-gray-700 border border-gray-200'
                              }`}
                            >
                              {test.has_ads ? (
                                <Check className="w-4 h-4 text-green-600 flex-shrink-0" />
                              ) : (
                                <X className="w-4 h-4 text-gray-400 flex-shrink-0" />
                              )}
                              <span className="truncate">{test.name}</span>
                              {test.in_baseline && (
                                <span className="text-xs bg-blue-100 text-blue-600 px-1 rounded flex-shrink-0">
                                  baseline
                                </span>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </main>
    </div>
  );
}
