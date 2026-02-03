'use client';

import { AdsDataProvider } from '@/context/AdsDataContext';

export default function AdsAnalysisLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AdsDataProvider>
      {children}
    </AdsDataProvider>
  );
}
