# Superpower SEM Gap Analysis Dashboard

Dashboard for analyzing competitor SEM keywords and planning Superpower's Google Ads strategy.

**Live Dashboard**: https://app-five-orcin-50.vercel.app
**Password**: `laks9713`

---

## Overview

This dashboard analyzes **3,930 paid keywords** from 11 health testing competitors to identify opportunities for Superpower Health's Google Ads campaigns.

### Competitors Analyzed
- Everlywell (1,468 keywords)
- Quest Health (1,177 keywords)
- Function Health (641 keywords)
- Labcorp (545 keywords)
- Ulta Lab Tests (307 keywords)
- Exact Sciences (229 keywords)
- Walk-In Lab (202 keywords)
- TruDiagnostic (93 keywords)
- PrivateMD Labs (54 keywords)
- Rythm Health (35 keywords)
- Clock Foundation (8 keywords)

---

## Data Files

### `/data/competitor_gap_analysis.json`
Raw keyword gap analysis with PURSUE/MAYBE/SKIP classification.

- **PURSUE**: 1,400 keywords (1.82M volume) - Tests Superpower offers
- **MAYBE**: 1,268 keywords - Unclear/partial offerings
- **SKIP**: 1,262 keywords - Tests not offered

### `/data/keyword_intent_groups.json`
Keywords grouped by **exact search intent**. Keywords in the same group share identical user intent and can be served by a single landing page.

**Structure:**
```json
{
  "metadata": {
    "total_keywords": 2795,
    "grouped_keywords": 1004,
    "ungrouped_keywords": 1791,
    "total_groups": 75
  },
  "categories": {
    "Hormone Testing": {
      "groups": [
        {
          "id": "cortisol_test",
          "intent": "User wants to get a cortisol test",
          "keywords": [...],
          "keyword_count": 14,
          "total_volume": 38230
        }
      ]
    }
  }
}
```

### `/data/keyword_outline.json`
Higher-level keyword categorization by test type (less granular than intent groups).

### `/data/superpower_tests.json`
Superpower's test offerings from Webflow CMS, showing which tests have Google Ads coverage.

### `/KEYWORD_STRATEGY.md`
Human-readable strategy document with keyword outline and priority recommendations.

---

## Intent Groups

Keywords are grouped by **exact search intent** - meaning users searching these keywords want the same thing and can land on the same page.

### Hormone Testing (152 keywords, 162K volume)

| Group ID | Intent | Keywords | Volume |
|----------|--------|----------|--------|
| `cortisol_high_symptoms` | User researching high cortisol symptoms | 19 | 53,600 |
| `cortisol_test` | User wants to get a cortisol test | 14 | 38,230 |
| `testosterone_test` | User wants a testosterone test | 21 | 18,360 |
| `testosterone_levels` | User researching testosterone levels | 24 | 18,000 |
| `hormone_panel` | User wants a hormone panel test | 48 | 16,550 |
| `cortisol_test_at_home` | User wants at-home cortisol test | 4 | 4,010 |
| `dhea_test` | User wants a DHEA test | 3 | 1,000 |
| `prolactin_test` | User wants a prolactin test | 2 | 3,700 |

### Thyroid Testing (86 keywords, 308K volume)

| Group ID | Intent | Keywords | Volume |
|----------|--------|----------|--------|
| `hashimotos` | User researching Hashimoto's | 23 | 165,800 |
| `thyroid_symptoms` | User researching thyroid symptoms | 8 | 43,450 |
| `hyperthyroidism` | User researching hyperthyroidism | 12 | 42,100 |
| `tsh_test` | User wants a TSH test | 8 | 24,110 |
| `thyroid_panel` | User wants a thyroid panel | 18 | 16,470 |
| `hypothyroidism` | User researching hypothyroidism | 6 | 9,700 |
| `thyroid_nodules` | User researching thyroid nodules | 3 | 1,700 |
| `thyroid_test_at_home` | User wants at-home thyroid test | 3 | 2,600 |

### Heart & Cholesterol (70 keywords, 180K volume)

| Group ID | Intent | Keywords | Volume |
|----------|--------|----------|--------|
| `triglycerides_high` | User researching high triglycerides | 8 | 59,350 |
| `high_cholesterol` | User researching high cholesterol | 10 | 35,380 |
| `cholesterol_test` | User wants a cholesterol test | 17 | 14,500 |
| `cholesterol_foods` | User researching foods and cholesterol | 1 | 13,000 |
| `apob_test` | User wants an ApoB test | 3 | 12,300 |
| `ldl_hdl` | User researching LDL vs HDL | 5 | 11,300 |
| `lipid_panel` | User wants a lipid panel | 5 | 9,500 |
| `homocysteine` | User wants homocysteine test | 3 | 7,600 |

### Metabolic / Diabetes (59 keywords, 134K volume)

| Group ID | Intent | Keywords | Volume |
|----------|--------|----------|--------|
| `metabolic_panel` | User wants a metabolic panel | 17 | 49,790 |
| `glucose_monitoring` | User interested in CGM | 6 | 36,210 |
| `a1c_test` | User wants an A1C test | 12 | 22,220 |
| `diabetes_test` | User wants a diabetes test | 7 | 11,000 |
| `a1c_levels` | User researching A1C levels | 15 | 8,920 |
| `prediabetes` | User researching prediabetes | 2 | 5,400 |

### Vitamins & Nutrients (42 keywords, 56K volume)

| Group ID | Intent | Keywords | Volume |
|----------|--------|----------|--------|
| `ferritin_test` | User wants a ferritin test | 2 | 27,100 |
| `vitamin_d_test` | User wants a vitamin D test | 14 | 10,280 |
| `vitamin_panel` | User wants a vitamin panel | 12 | 5,480 |
| `magnesium_test` | User wants a magnesium test | 3 | 4,760 |
| `b12_test` | User wants a B12 test | 4 | 3,200 |

### Inflammation (31 keywords, 79K volume)

| Group ID | Intent | Keywords | Volume |
|----------|--------|----------|--------|
| `inflammatory_foods` | User researching inflammatory foods | 9 | 47,320 |
| `ana_test` | User wants an ANA test | 4 | 24,080 |
| `crp_test` | User wants a CRP test | 7 | 2,800 |
| `autoimmune_test` | User wants autoimmune testing | 8 | 2,390 |

### Kidney & Liver (26 keywords, 154K volume)

| Group ID | Intent | Keywords | Volume |
|----------|--------|----------|--------|
| `adrenal` | User researching adrenal function | 4 | 78,590 |
| `liver_panel` | User wants a liver function test | 11 | 37,960 |
| `liver_enzymes` | User researching liver enzymes | 6 | 20,900 |
| `kidney_panel` | User wants a kidney function test | 3 | 15,570 |

### Aging & Longevity (24 keywords, 46K volume)

| Group ID | Intent | Keywords | Volume |
|----------|--------|----------|--------|
| `telomeres_info` | User researching telomeres | 5 | 22,390 |
| `biological_age_test` | User wants biological age test | 4 | 10,000 |
| `epigenetics_info` | User researching epigenetics | 5 | 8,970 |

### Blood Tests (445 keywords, 367K volume)

| Group ID | Intent | Keywords | Volume |
|----------|--------|----------|--------|
| `blood_test_general` | User wants general blood testing | 437 | 359,690 |
| `cbc_test` | User wants a CBC test | 6 | 6,450 |

---

## Skip Categories (Not Offered)

These keyword categories were excluded because Superpower doesn't offer the tests:

- **STD/STI Testing** - herpes, HIV, chlamydia, etc.
- **Drug Testing** - THC, marijuana, drug screens
- **Food Allergy/Sensitivity** - allergy tests, food intolerance
- **Lab Locations** - "near me" searches
- **Pregnancy & Fertility** - pregnancy tests, ovulation
- **Genetic Testing** - DNA, ancestry, paternity
- **Multi-Cancer Detection** - Galleri, Grail (excluded per business decision)
- **Gut Microbiome** - stool tests, microbiome (excluded per business decision)
- **Toxin Testing** - heavy metals, toxins (excluded per business decision)

---

## Traffic Estimates

Based on 1.82M monthly search volume:

| Metric | Conservative | Moderate | Aggressive |
|--------|-------------|----------|------------|
| CTR | 3% | 3.5% | 5% |
| Impression Share | 40% | 50% | 60% |
| Monthly Clicks | 21,800 | 31,850 | 54,600 |
| CVR | 1.5% | 1.8% | 2% |
| Monthly Conversions | 327 | 573 | 1,092 |

---

## Dashboard Pages

1. **Competitor Gap** (`/`) - Raw PURSUE/MAYBE/SKIP keyword analysis
2. **Testing Gap** (`/tests`) - Which Superpower tests have Google Ads
3. **Strategy** (`/strategy`) - Keywords grouped by test type with priority tiers

---

## Development

```bash
npm install
npm run dev
```

Open http://localhost:3000

## Deployment

```bash
npx vercel --prod
```

---

## Data Sources

- **Competitor keywords**: Ahrefs Paid Keywords export (Feb 2026)
- **Superpower tests**: Webflow CMS database (`/Users/jeffy/superpower-cookie-extension/superpower_marketplace.db`)
- **CVR benchmarks**: Superpower Google Ads historical data (1.4-7.7% by category)
