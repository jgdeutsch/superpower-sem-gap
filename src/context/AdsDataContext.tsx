'use client';

import { createContext, useContext, useState, useCallback, useEffect, ReactNode } from 'react';

interface TotalsData {
  total_spend: number;
  total_clicks: number;
  total_conversions: number;
  total_impressions?: number;
  monthly_spend?: number;
  monthly_clicks?: number;
  monthly_conversions?: number;
  cvr: number;
  cac: number;
}

interface CampaignData {
  name: string;
  campaign_id: number;
  total_spend: number;
  total_clicks: number;
  total_conversions: number;
  cvr: number;
  cac: number;
}

interface AdGroupLandingPage {
  url: string;
  total_spend: number;
  total_clicks: number;
  total_conversions: number;
  cvr: number;
  cac: number;
}

interface AdGroupData {
  ad_group_name: string;
  campaign_name: string;
  campaign_id: number;
  ad_group_id: number;
  total_spend: number;
  total_clicks: number;
  total_conversions: number;
  cvr: number;
  cac: number;
  landing_pages?: Record<string, AdGroupLandingPage>;
}

interface LandingPageData {
  total_spend: number;
  total_clicks: number;
  total_conversions: number;
  cvr: number;
  cac: number;
}

interface SegmentData {
  totals: TotalsData;
  campaigns: CampaignData[];
  ad_groups: AdGroupData[];
  landing_pages?: Record<string, LandingPageData>;
}

export interface AdsAnalysisData {
  date_range: {
    start: string;
    end: string;
    months: number;
  };
  customer_id: string;
  manager_id: string;
  search: {
    all: SegmentData;
    brand: SegmentData;
    non_brand: SegmentData;
  };
  demand_gen: SegmentData;
  pmax: SegmentData;
  shopping: SegmentData;
}

interface AdsDataContextType {
  data: AdsAnalysisData | null;
  isLoading: boolean;
  error: string | null;
  startDate: string;
  endDate: string;
  setDateRange: (start: string, end: string) => void;
  refreshData: () => void;
}

const AdsDataContext = createContext<AdsDataContextType | null>(null);

// Default to last 90 days
const getDefaultDates = () => {
  const end = new Date();
  const start = new Date();
  start.setDate(start.getDate() - 90);
  return {
    start: start.toISOString().split('T')[0],
    end: end.toISOString().split('T')[0],
  };
};

export function AdsDataProvider({ children }: { children: ReactNode }) {
  const defaultDates = getDefaultDates();
  const [data, setData] = useState<AdsAnalysisData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [startDate, setStartDate] = useState(defaultDates.start);
  const [endDate, setEndDate] = useState(defaultDates.end);

  const fetchData = useCallback(async (start: string, end: string) => {
    setIsLoading(true);
    setError(null);

    try {
      // First try to fetch from API
      const response = await fetch(`/api/ads-data?start=${start}&end=${end}`);

      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }

      const jsonData = await response.json();
      setData(jsonData);
    } catch (err) {
      console.error('Error fetching data:', err);

      // Fallback to static file for default date range
      try {
        const staticResponse = await fetch('/data/full_campaign_analysis.json');
        if (staticResponse.ok) {
          const staticData = await staticResponse.json();
          setData(staticData);
          setError('Using cached data. Live API fetch failed.');
        } else {
          setError('Failed to load data');
        }
      } catch {
        setError('Failed to load data');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const setDateRange = useCallback((start: string, end: string) => {
    setStartDate(start);
    setEndDate(end);
    fetchData(start, end);
  }, [fetchData]);

  const refreshData = useCallback(() => {
    fetchData(startDate, endDate);
  }, [fetchData, startDate, endDate]);

  // Initial load - try static file first for speed
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const staticResponse = await fetch('/data/full_campaign_analysis.json');
        if (staticResponse.ok) {
          const staticData = await staticResponse.json();
          setData(staticData);
          setStartDate(staticData.date_range.start);
          setEndDate(staticData.date_range.end);
          setIsLoading(false);
        } else {
          fetchData(startDate, endDate);
        }
      } catch {
        fetchData(startDate, endDate);
      }
    };

    loadInitialData();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <AdsDataContext.Provider
      value={{
        data,
        isLoading,
        error,
        startDate,
        endDate,
        setDateRange,
        refreshData,
      }}
    >
      {children}
    </AdsDataContext.Provider>
  );
}

export function useAdsData() {
  const context = useContext(AdsDataContext);
  if (!context) {
    throw new Error('useAdsData must be used within an AdsDataProvider');
  }
  return context;
}
