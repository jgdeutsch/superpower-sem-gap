# SEM Gap Keyword Expansion - March 6, 2026

## Overview
Identified 93 keywords across 11 themes that competitors (Function Health, Rythm Health + 8 others via DataForSEO) bid on but Superpower does not. Created ad groups, RSA ads, and Webflow CMS landing pages for all 11 themes.

## Pipeline
1. Seed: 338 competitor keywords from CSV
2. Filter: removed 59 already in our 3,123 active keywords -> 279 gap keywords
3. Relevance: filtered for Superpower offerings -> 120 relevant
4. Expand: DataForSEO domain intersection with 8 competitors -> 309 additional keywords
5. Final: 278 passing both tests, organized into 93 actionable keywords across 11 themes

## Campaign
- **Name**: Search_SEM-Gap_Testing-Keywords_tCPA_US
- **ID**: 22443049498
- **Status**: ENABLED, all 33 ads APPROVED

## Ad Groups

| Ad Group | ID | # KWs | LP Slug |
|---|---|---|---|
| Vitamin Deficiency Blood Test | 196708001249 | 11 | vitamin-deficiency-blood-test |
| Hormone Panel Blood Test | 194547929712 | 10 | hormone-panel-blood-test |
| Preventive Health Screening | 194981005618 | 8 | preventive-health-screening |
| Biological Age Test | 194981006578 | 7 | biological-age-test |
| Order Blood Test Online | 192689649286 | 9 | order-blood-test-online |
| Autoimmune Blood Test Panel | 190906304301 | 8 | autoimmune-panel-test |
| Specialty Health Testing | 196708004289 | 8 | specialty-health-testing |
| Comprehensive Blood Panel | 192689652646 | 10 | comprehensive-blood-panel-e80c8 |
| Health Optimization Testing | 194981010618 | 7 | health-optimization-testing |
| Functional Medicine Testing | 199606796808 | 8 | functional-medicine-testing |
| Weight Loss Blood Test | 192689654606 | 7 | weight-loss-blood-test |

## Landing Pages
All at `superpower.com/welcome-cms/{slug}` - Webflow CMS collection `6981a714e199bac70776d880`

## Ads
3 RSAs per ad group (homepage, /welcome, /welcome-cms/{slug}). Each with 15 headlines and 4 descriptions.

## Compliance Review
- **Vera (legal)**: Fixed fabricated testimonials (replaced with survey stats), "24/7" -> "on-demand", "diagnose" -> "identify"
- **Marcus (medical)**: Fixed "$15,000" -> "thousands", "88M" -> "115M" (CDC), B12/Folate clarified as add-on, removed "Root Cause Testing", "Tests Doctors Skip", "Catch It Years Earlier", "4.5 Years to Diagnose?"
- **Thalia (testimonials)**: All 11 fabricated testimonials confirmed replaced

## Blocked Keywords (Google Healthcare Policy)
8 keywords rejected by HEALTH_IN_PERSONALIZED_ADS:
- pre cancer screening, female hormone blood test, fertility blood test at home, hormone imbalance test female, autoimmune disease screening, autoimmune disease test, thyroid antibodies test at home, hormonal imbalance blood test

## Data Sources
- SpyFu API (term ad history - worked for individual KWs but domain endpoint returned 0)
- DataForSEO domain_intersection API (worked well for 8 competitors)
- Google Ads API (keyword check, ad group/keyword/RSA creation)
- Webflow CMS API (LP creation and publishing)
