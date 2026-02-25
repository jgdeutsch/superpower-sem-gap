# Google Ads Change Log - Superpower Health

Account ID: 8618096874 (MCC: 8461075268)

---

## 2026-02-25 | VTC Spike Investigation - UGC Video Audience Overlap

**Label:** N/A (investigation, no account changes)

### Finding

Demand Gen view-through conversions spiked from 0-4/day to **24 on Feb 25** (8x increase). This coincides exactly with UGC video assets going live in PMAX-Test on Feb 24.

### Root Cause

Audience overlap between PMAX video placements (YouTube/Discover/Display) and Demand Gen campaigns. Users see the PMAX UGC video, don't click, then convert via another channel. Google attributes a VTC to Demand Gen even though the impression came from PMAX.

This is almost certainly **double-counting, not incremental conversions.** Total account conversions should be checked to confirm.

### Data (Demand Gen campaigns, Feb 19-25)

| Date | Clicks | Cost | Conv | VTCs |
|---|---|---|---|---|
| Thu Feb 19 | 1,824 | $4,778 | 127.43 | 4 |
| Fri Feb 20 | 1,779 | $4,233 | 68.23 | 0 |
| Sat Feb 21 | 1,890 | $4,065 | 53.58 | 2 |
| Sun Feb 22 | 1,800 | $4,080 | 56.56 | 2 |
| Mon Feb 23 | 1,575 | $4,058 | 75.84 | 2 |
| Tue Feb 24 | 1,602 | $5,095 | 54.00 | 0 |
| **Wed Feb 25** | **524** | **$1,654** | **18.00** | **24** |

### Recommendations (not yet actioned)

1. Check whether total account conversions actually increased or just shifted attribution
2. Consider tightening VTC lookback window from 30 days to 7 or 1 day on Demand Gen
3. Monitor whether VTC count normalizes after initial spike
4. Consider excluding overlapping audiences between PMAX video groups and Demand Gen

---

## 2026-02-24 | UGC Video PMAX Asset Groups + Shahid Budget Increases + DQ Manual Changes

**Label:** TBD

### Context

KT's SP-892 UGC video batch (Meta ad graduates) added to PMAX-Test campaign for YouTube testing. Shahid increased budgets across 5 campaigns (+$3,400/day total). DQ made manual pauses, re-enables, ad swaps, and added ~95 negatives to Diagnostic-Discovery.

### Changes

**1. UGC Video Asset Groups (Jeff, API ~1:10pm):**

Created 2 new asset groups in PMAX-Test_Prospecting_Max-Conversion-Value_US_Blood-Test (23280708146):

**Asset Group: "UGC Video Test" (ID: 6679730465, ENABLED) - 5 videos:**
- Alex Bolivar (wmtHSVm3izI)
- Amber Blu (bA-o0b66c0g)
- Brit SP-626 (Q425noMQx0M)
- Grail Britt (MCzBMx21Pek)
- Jamal Cancer (uQPg_iMJh0A)

**Asset Group: "UGC Video Test 2" (ID: 6679730495, ENABLED) - 3 videos:**
- Jamal Cancer 2 (UcB-WdeCBLQ)
- Rachel Test (3eq9g6H5eY0)
- SP-262 (t5ykNpbDvp4)

Split into 2 groups (PMAX limit: 5 videos per asset group). Both reuse headlines/descriptions/images from existing Blood Test group. Final URL: superpower.com.

12 additional video assets uploaded but NOT linked to any asset group.

**2. Shahid Budget Increases (~6:21-6:27pm):**
- PMAX Prospecting US Main: $3,500/day -> $4,500/day (+$1,000)
- PMAX-Test US: $2,000/day -> $2,500/day (+$500)
- Search SEM-Gap: $1,500/day -> $2,000/day (+$500)
- Search Brand: $600/day -> $1,000/day (+$400)
- Demand-Gen YouTube: $1,000/day -> $2,000/day (+$1,000)
- **Total increase: +$3,400/day**

**3. DQ Manual Changes (~10:20-10:47am):**
- Paused PMAX Gender campaign
- Cut PMAX-Test Top States budget: $1,000/day -> $500/day
- Paused Competitors campaign entirely
- Paused all NY/NJ campaigns
- Re-enabled 5 of our Feb 23 Search pauses (Health Check, Test, Health testing, Hormone Testing, Cancer)
- Paused 8 D-D ad groups (Heart Testing, Nutrient test, Metabolic, Cholesterol test, Celiac Test, Glucose test, T blood tests, Cardiovascular)
- Swapped active RSA ads in ~12 D-D ad groups
- Added ~95 phrase-match campaign-level negatives to Diagnostic-Discovery
- Added negatives to PMAX Top States (insurance, clinical study, career, eating, costco, function health, enclomiphene + others)

**4. Tirz RX Campaign (Jeff, API ~1:10-1:15pm):**
- Created Search_RX_Tirzepatide_Max-Conversions_US (23597608007) - PAUSED, enable Feb 28
- 5 ad groups, 46 keywords, 5 RSAs, $500/day budget
- LP: superpower.com/tirzepatide

### Current Active Daily Budgets (post-Shahid)

| Campaign | Budget/Day |
|---|---|
| PMAX Prospecting US Main | $4,500 |
| Search Diagnostic-Discovery | $3,000 |
| PMAX-Test US | $2,500 |
| Search SEM-Gap | $2,000 |
| Demand-Gen YouTube | $2,000 |
| Search Brand | $1,000 |
| PMAX-Test Top States | $500 |
| **Total** | **$15,500** |

---

## 2026-02-23 | Pause 13 BAD Groups + Homepage LP Experiment

**Label:** `Audit Cleanup 2.23.26`

### Context

Full brand-excluded audit of Search + PMAX for Feb 16-22 (1wk) and Jan 26 - Feb 22 (4wk). Identified 13 groups that were BAD in both time windows (CPS >$500 or zero subs with significant spend). Also discovered Search sends 92% of traffic to `/welcome-cms/*` pages at $454 CPS while homepage converts at $313 CPS - launched a controlled experiment instead of mass-redirecting.

### Changes

**1. Paused 13 BAD groups (~$28.7K/week, ~38 subs at $732 blended CPS):**

Search ad groups (8 groups, ~$14.8K/wk):
- Health Check (186665649814) in D-D campaign - $1,719/wk, $573 CPS
- Test (188162570049) in D-D campaign - $3,575/wk, $581 CPS
- Health testing (188162568649) in D-D campaign - $5,292/wk, $619 CPS
- Hormone Testing (188162568849) in D-D campaign - $904/wk, $904 CPS
- Cancer (188162567169) in D-D campaign - $1,254/wk, 0 subs
- Thyroid Tests (192070922079) in SEM-Gap campaign - $549/wk, $549 CPS
- Heart & Cholesterol (192070922119) in SEM-Gap campaign - $577/wk, 0 subs
- Lab Test (192775259733) in SEM-Gap campaign - $1,224/wk, 0 subs

PMAX asset groups (5 groups, ~$13.6K/wk):
- Blood Test compliant (6667331354) in Top States campaign - $7,619/wk, $641 CPS
- Longevity Blood Test (6671357427) in Max-Conv-Value campaign - $2,058/wk, $686 CPS
- Cholesterol & Heart Panel (6671393476) in Max-Conv-Value campaign - $400/wk, $801 CPS
- Top Conv Male - Gender (6674795981) in Gender campaign - $2,083/wk, $1,240 CPS
- Lp(a) Heart Risk (6671394355) in Max-Conv-Value campaign - $1,438/wk, $1,438 CPS

**2. Created 5 homepage experiment RSAs in Diagnostic-Discovery (23020350152):**

Added a second RSA in each ad group pointing to `https://superpower.com/` (homepage) with identical headlines/descriptions as existing CMS RSA. Google auto-rotates ~50/50.

| Ad Group | AG ID | New Ad ID |
|---|---|---|
| Biomarker | 188162566689 | 798164805966 |
| Gene test | 188162568369 | 798164805969 |
| igf 1 test | 188162568929 | 798164805972 |
| Medical test | 188162569569 | 798164805975 |
| Body composition | 188162566969 | 798164805978 |

### Why Controlled Experiment, Not Mass Redirect

- QS risk: Swapping final URLs tanks Quality Score. CPC increase of 30-50% could eat LP savings.
- Data contamination: Homepage CPS ($313) from different traffic mix (mostly PMAX). Can't assume Search converts same.
- Irreversibility: Mass swap affects all groups at once. QS doesn't bounce back quickly.

### Expected Impact

- Pauses save ~$28.7K/week. At $732 CPS these were 2x+ worse than GOOD threshold ($350).
- Experiment will show whether homepage or CMS converts better for Search within 2-3 weeks.

### Review Plan

- Monitor experiment daily for first week (spend pacing, impression share)
- Full CPS comparison at week 2-3
- If homepage wins, roll out to remaining Search ad groups
- If CMS wins, investigate and optimize CMS pages

### Scripts

- `audit-reports/pause_bad_groups.py`
- `audit-reports/create_homepage_experiment.py`

---

## 2026-02-16 | DSA Labcorp Campaign — CPC Cap + Feed Lock + Negatives

**Label:** `DSA Fix 2.16.26`

### Context

DSA Labcorp Locations campaign had wild CPC variance ($0.20–$15.04) because it was on Maximize Conversions with no bid cap. 96% of spend ($121 of $126) went to non-labcorp queries like "blood test cincinnati", "quest diagnostics", "health testing near me". The page feed setting `use_supplied_urls_only` was False, so Google was matching queries to `/biomarkers`, `/welcome`, and other non-Labcorp pages. Zero conversions across 41 clicks and $207 total spend.

### Changes

**1. Switched bidding from Maximize Conversions to Manual CPC at $1.00:**
- Campaign 23568629474: MAXIMIZE_CONVERSIONS → MANUAL_CPC
- Ad Group "All Labcorp Locations" (196901920201): default CPC bid set to $1.00
- Rationale: No competition on "labcorp" queries, $1 is more than enough. Previous CPCs were $5-$15 on irrelevant broad queries.

**2. Locked page feed to Labcorp URLs only:**
- `campaign.dynamic_search_ads_setting.use_supplied_urls_only`: False → True
- This stops Google from serving ads against any page on superpower.com — now restricted to the 1,138 Labcorp location page feed URLs only.

**3. Added 3 campaign-level BROAD match negative keywords:**
- "quest" — blocks Quest Diagnostics competitor traffic
- "quest diagnostics" — blocks Quest Diagnostics competitor traffic
- "superpower" — blocks own brand from bleeding into this DSA campaign

### Search Term Analysis (All-Time)

228 total search terms. Only 33 contained "labcorp" — the other 195 were irrelevant:
- "blood test cincinnati" — $30.08, 2 clicks
- "health testing near me" — $17.38, 2 clicks
- "base lab testing" — $11.94, 1 click
- "quest diagnostics" — $6.33, 1 click
- "quest diagnostics location finder" — $5.80, 2 clicks
- "superpower blood test" — $3.82, 4 clicks (own brand)

### Impression Share

Google reports 0% impression share — campaign too low-volume (720 impressions all-time) for IS calculation. Confirms no competition on labcorp queries.

### Expected Impact

- CPC drops from $5.04 avg to ~$0.20–$1.00 range
- All spend now directed to actual "labcorp near me" type queries
- No more competitor, brand, or generic health query leakage

---

## 2026-02-11 | Budget Increase on DUX-Feeding Search Campaigns

**Label:** `DUX Budget Ramp 2.11.26`

### Context

National DUX Search running at $164 CAC (best in account). Both DUX-feeding campaigns at only 10% impression share, losing 53-70% of impressions to budget. Increasing budgets to capture more of this high-converting traffic.

### Changes

**Budget increases on 2 campaigns:**
- Search_Generic_Diagnostic-Discovery_tCPA_US (23020350152): $2,000/day → **$3,000/day** (+50%)
- Search_SEM-Gap_Testing-Keywords_tCPA_US (23538070207): $1,000/day → **$2,000/day** (+100%)

Combined daily budget increase: +$2,000/day (+$14K/week)

### Expected Impact

At current $164 DUX CAC, the additional $2K/day could yield ~12 incremental subs/day. Even with CAC degradation at higher spend (e.g., $220 CAC), expect ~9 incremental subs/day.

### Revert Plan

Check Slugfest in 3-4 days (by Feb 15). If DUX CAC rises above $250, consider pulling back. Key metric: impression share should climb from 10% toward 20%+.

---

## 2026-02-11 | Pause NY/NJ PMAX Campaign - Zero Conversions

**Label:** `NY/NJ PMAX Pause 2.11.26`

### Context

NY/NJ PMAX campaign (23533786927) spent $1,424/week with zero subscriptions over the 7-day period (Feb 4-10). NY/NJ Generic Search also produced 0 subs on $726. DUX Search is the only NY/NJ channel converting (4.5 subs at $622 CAC). Pausing the PMAX campaign to eliminate waste.

### Changes

**Paused 1 campaign:**
- PMAX_Prospecting_Max-Conversions_US_NY_Blood-Test (23533786927): ENABLED → PAUSED

### Revert Plan

Re-enable if NY/NJ DUX Search proves the market converts at acceptable CAC and we want to scale NY/NJ via PMAX.

---

## 2026-02-11 | Pause Generic Blood Test Asset Group for DUX Clean Test

**Label:** `DUX Test 2.11.26`

### Context

The generic "Blood Test" asset group in PMAX Max-Conv-Value campaign (23280708146) was running at $479 CAC last week - worst-performing PMAX bucket. 14 condition-specific DUX asset groups were added Feb 9. Pausing the generic group gives the DUX groups a clean test without budget cannibalization.

### Changes

**Paused 1 asset group in PMAX-Test_Prospecting_Max-Conversion-Value_US_Blood-Test (23280708146):**
- "Blood Test" (6634288482): ENABLED → PAUSED

**Kept ENABLED:**
- "Blood Test - Top Converting Search Interests (Female & Unknown)" (6634201853) - $233 CAC over 90 days
- "Blood Test - Top Converting Search Interests (Male & Unknown)" (6634202102) - $230 CAC over 90 days
- 14 condition-specific DUX asset groups (added Feb 9)

### Revert Plan

Re-enable "Blood Test" (6634288482) after 1 week (Feb 18) if DUX groups don't sustain performance. Check Slugfest on Feb 18.

---

## 2026-02-10 | Geo Targeting Audit & Fix - Stop International Ad Leakage

**Label:** `Geo Fix 2.10.26`

### Context

Jeff saw a Superpower "Function Health Alternative" ad in Australia. The NY/NJ-specific ad was showing internationally because 3 campaigns used `PRESENCE_OR_INTEREST` instead of `PRESENCE` for positive geo targeting. This means anyone who *showed interest in* NY/NJ (e.g., searching for "Function Health," a NY-based competitor) could see the ad worldwide.

Additionally, PMAX national campaigns were missing restricted US state exclusions, and Demand Gen campaigns were missing foreign country exclusions.

### Changes

**1. Fixed PRESENCE_OR_INTEREST → PRESENCE on 3 NY/NJ campaigns:**
- Search_Brand_NY-NJ_tCPA_US (23544911674) - positive geo: PRESENCE_OR_INTEREST → PRESENCE
- Search_Generic_NY-NJ_tCPA_US (23544806539) - positive geo: PRESENCE_OR_INTEREST → PRESENCE
- Search_Competitors_NY-NJ_tCPA_US (23535201240) - positive geo: PRESENCE_OR_INTEREST → PRESENCE

All 13 enabled campaigns now use PRESENCE only.

**2. Added 94 geo exclusions to 2 PMAX national campaigns (2 → 96 each):**
- PMAX-Test_Prospecting_Max-Conversion-Value_US_Blood-Test (23280708146)
- PMAX_Prospecting_Max-Conversions_US_Blood-Test (22192179721)

Added: 12 restricted US states (AK, AR, HI, ID, IA, KS, KY, LA, MS, ND, OK, RI, SD, WY) + 63 foreign countries + 4 regions. Now matches Search campaign exclusion list.

**3. Added 83 geo exclusions to 2 Demand Gen campaigns (13 → 96 each):**
- Demand-Gen_YouTube_Prospecting_Conversion_Registration-and-subs-v2-landscape
- Demand-Gen_YouTube_Prospecting_Internal_Conversion_Registration-and-subs

Added: 3 missing US states (ID, KS, OK) + 63 foreign countries + 4 regions. Now matches Search campaign exclusion list.

### Verification

All 13 enabled campaigns now have:
- `positive_geo_target_type: PRESENCE` (no more PRESENCE_OR_INTEREST)
- 96 geo exclusions each (except NY-only campaigns which correctly target just NY+NJ)

### Scripts Created
- `app/scripts/geo_target_audit.py` - Re-run anytime to audit all campaigns
- `app/scripts/fix_geo_targeting.py` - Fixed NY/NJ PRESENCE_OR_INTEREST
- `app/scripts/fix_geo_target_competitors.py` - Fixed third NY/NJ campaign
- `app/scripts/sync_pmax_geo_exclusions.py` - Synced PMAX exclusions
- `app/scripts/sync_geo_exclusions_demandgen.py` - Synced Demand Gen exclusions

---

## 2026-02-09 | PMAX Condition-Specific Asset Groups + Budget Increase

**Label:** `PMAX DUX Launch 2.9.26` (label TBD - create in UI)

### Context

PMAX sending 100% of clicks to homepage despite 122 DUX landing pages existing. Search DUX pages convert at $140 CAC vs $388 static. Created condition-specific asset groups in Max-Conv-Value campaign, each pointing to a matched DUX page.

### Changes

**14 Asset Groups Created in Campaign 23280708146 (Max-Conv-Value):**
1. Blood Test - General -> /welcome-cms/blood-test-general (63.4% of PMAX clicks)
2. Lp(a) Heart Risk -> /welcome-cms/lipoprotein-a-test (8.7%)
3. Best Blood Test Service -> /welcome-cms/best-blood-test-service (6.5%)
4. Longevity Blood Test -> /welcome-cms/longevity-blood-test (6.2%)
5. Hormone Panel -> /welcome-cms/hormone-test (2.7%)
6. At-Home Blood Test -> /welcome-cms/blood-test-at-home (1.5%)
7. Cholesterol & Heart Panel -> /welcome-cms/cholesterol-test (1.4%)
8. Kidney Function Test -> /welcome-cms/kidney-function-test (1.1%)
9. Iron & Ferritin Panel -> /welcome-cms/ferritin-test (1.1%)
10. Diabetes & Metabolic Panel -> /welcome-cms/diabetes-test (0.4%)
11. Thyroid Panel -> /welcome-cms/thyroid-panel (0.2%)
12. Liver Function Panel -> /welcome-cms/liver-function-test (<0.2%)
13. Autoimmune Panel -> /welcome-cms/autoimmune-test (<0.2%)
14. Heart Health Panel -> /welcome-cms/heart-health-test (<0.1%)

All groups reuse existing assets (headlines, descriptions, images, videos) from the Blood Test asset group. Each has condition-specific search themes with HEALTH_IN_PERSONALIZED_ADS policy exemptions.

**Budget Increase:**
- Campaign 23280708146 budget: $1,000/day -> $2,000/day
- Plan to ramp to $4,000/day pending performance check

### Expected Impact
- Conservative: +66 subs/month (+$26K revenue)
- Median: +151 subs/month (+$60K revenue)
- Liberal: +261 subs/month (+$104K revenue)

### Open Question
Two PMAX campaigns track different conversion actions (ph_subscription_created vs PostHog Revenue Action). Must verify whether baseline sub count is accurate.

---

## 2026-02-08 | FH Ad Swap - Redirect Function Health Traffic to Proven Pages

**Label:** `FH Ad Swap 2.8.26` (Label ID: 22114921036)

### Context

90-day analysis of Function Health search terms showed landing page CPA divergence:
- `/welcome`: $110.68 CPA (WINNER)
- `/superpower-vs-function-health`: $335.18 CPA
- CMS `function-health-review`: $225.63 CPA (only 82 clicks)

NY/NJ comparison page shows wrong $199 pricing. CMS `-ny` page had factually incorrect claims.

### Changes

**Ads Paused (5):**
1. National Competitors AG 181819692478: CMS `function-health-review` ad 796290257464
2. National SEM-Gap AG 190636610857: CMS `function-health-review` ad 796367116961
3. NY/NJ Competitors AG 189843373621: CMS `function-health-review-ny` ad 796513183640
4. NY/NJ Generic AG 191643603543: CMS `function-health-review-ny` ad 796424837896
5. NY/NJ Brand AG 189842428061: `/superpower-vs-function-health` ad 796401362055 (wrong $199 pricing for NY/NJ)

**Ads Created (5):**
1. National Competitors AG 181819692478 -> `/welcome` (existing comparison page ad also stays enabled)
2. National SEM-Gap AG 190636610857 -> `/welcome`
3. NY/NJ Competitors AG 189843373621 -> `/labs-new-york`
4. NY/NJ Generic AG 191643603543 -> `/labs-new-york`
5. NY/NJ Brand AG 189842428061 -> `/labs-new-york` (ad 796513790526)

### Campaigns Affected
- Search_Generic_Competitors_tCPA_US_Blood-Test (21904393390)
- Search_SEM-Gap_Testing-Keywords_tCPA_US (23538070207)
- Search_Competitors_NY-NJ_tCPA_US (23535201240)
- Search_Generic_NY-NJ_tCPA_US (23544806539)
- Search_Brand_NY-NJ_tCPA_US (23544911674)

### Expected Impact
National FH traffic redirected from $335 CPA page to $110 CPA page. NY/NJ traffic redirected from incorrect pricing pages to `/labs-new-york` ($399 all-in, correct).

---

## 2026-02-07 | Webflow CMS Fix - Card Price Monthly Double "/month"

**Label:** N/A (Webflow CMS fix, not Google Ads)

### Issue

The `card-price-monthly` field in the SEM Landing Pages CMS collection contained `$17/month` for 510 out of 780 items. Since the Webflow page template already appends "/month" in the design, this caused the live pricing card to display `$17/month/month`.

### Fix

1. **Updated 510 CMS items** in the SEM Landing Pages collection (`6981a714e199bac70776d880`):
   - `$17/month` -> `$17` (510 national items)
   - `$33` left unchanged (27 NY/NJ items, already correct)
   - `$17` left unchanged (243 items that were already correct)

2. **Verified:** All 780 items now have clean values - 753 with `$17` and 27 with `$33`. Zero items contain `/month` in the field.

3. **Root cause:** The field was likely populated with the full `$17/month` string during initial bulk creation, not accounting for the template already rendering "/month" after the field value.

### Impact

All 780 SEM landing pages under `/welcome-cms/*` were affected (510 displaying wrong price). The pricing card is the primary conversion element on these pages. Fixing this removes a credibility-damaging display error that made the price look like a typo.

---

## 2026-02-07 | A/B Test Ads - Pre-existing NY/NJ Blood Test Campaign

**Label:** `NY-NJ Launch 2.7.26` (same label)

### Campaign: Search_Generic_Blood-Test_tCPA_US_NY-and-NJ (23353538548)

1. **Added 1 new RSA ad per ad group** (5 total) as A/B test against existing `/labs-new-york` ads:
   - Blood Test (190156109979) -> `blood-test-general-ny` (Ad: 796403328372)
   - Blood Panel (190156110139) -> `comprehensive-blood-panel-ny` (Ad: 796403328945)
   - Lab work (190156110379) -> `blood-work-ny` (Ad: 796432897162)
   - CBC Blood Test (190156110179) -> `full-body-blood-test-ny` (Ad: 796514039645)
   - RBC Blood Test (190156110219) -> `blood-test-general-ny` (Ad: 796513995530)
2. **Existing ads:** Point to `/labs-new-york` with $499 pricing and 100+ biomarkers
3. **New A/B ads:** Point to `/welcome-cms/{slug}-ny` with $399 pricing and 90+ biomarkers
4. **Goal:** Test if condition-specific CMS landing pages with checkout personalization outperform the generic `/labs-new-york` page

---

## 2026-02-07 | PMAX NY/NJ Geo Exclusions

**Label:** `NY-NJ Launch 2.7.26` (same label)

1. **Added NY (21164) and NJ (21167) as negative location criteria** on 2 national PMAX campaigns:
   - PMAX_Prospecting_Max-Conversions_US_Blood-Test (22192179721) - $298K spend
   - PMAX-Test_Prospecting_Max-Conversion-Value_US_Blood-Test (23280708146) - $81K spend
   - Both required EU political ads declaration first
2. **Not modified:** PMAX_Prospecting_Max-Conversions_US_NY_Blood-Test (23533786927) - already targets NY/NJ only with `/labs-new-york` pages
3. **Not modified:** PMAX-Test top-states (23449940807) - targets FL/GA/IL/PA/TX/VA only, no NY/NJ overlap

---

## 2026-02-07 | NY/NJ Competitors Campaign Launch

**Label:** `NY-NJ Launch 2.7.26` (same label)

### New Campaign: Search_Competitors_NY-NJ_tCPA_US (23535201240)

1. **Created new competitors campaign** targeting only New York and New Jersey with $399 pricing:
   - **Geo targets:** NY (21164) + NJ (21167) only
   - **Budget:** $500/day
   - **Bidding:** Maximize Conversions with tCPA $700 (2x national $350)
   - **Status:** ENABLED

2. **6 ad groups** mirroring national Competitors campaign enabled ad groups:
   - Function Health (189843373621) - 70 keywords, RSA -> function-health-review-ny
   - InsideTracker (188108115050) - 4 keywords, RSA -> superpower.com
   - Mito (193822011598) - 3 keywords, RSA -> superpower.com
   - Marek Health (193822020198) - 2 keywords, RSA -> superpower-vs-marek-health
   - Whoop Labs (192414661826) - 64 keywords, RSA -> superpower.com
   - Hims (189843375541) - 63 keywords, RSA -> superpower.com
   - All ad copy adapted: $199 -> $399, 100+ -> 90+ biomarkers, $17/mo -> $33/mo

3. **31 campaign-level negative keywords** (same as national Competitors campaign)

4. **Campaign-level extensions:**
   - 4 sitelinks: $399/Yr - Not $499+, At-Home Blood Draw, See All 90+ Biomarkers, HSA/FSA Eligible
   - 8 callouts: 90+ Biomarkers Tested, $399/Year - Not $499, No Waitlist, etc.
   - 1 structured snippet: Types (5 values)

---

## 2026-02-07 | NY/NJ Brand Campaign Launch

**Label:** `NY-NJ Launch 2.7.26` (same label)

### Brand Geo Exclusion

1. **Added NY (21164) and NJ (21167) as negative location criteria** on the national brand campaign:
   - Search_Brand_tCPA_US (21893543504) - $104K spend, was showing $199 brand ads in NY/NJ

### New Campaign: Search_Brand_NY-NJ_tCPA_US (23544911674)

2. **Created new brand campaign** targeting only New York and New Jersey with $399 pricing:
   - **Geo targets:** NY (21164) + NJ (21167) only
   - **Budget:** $200/day
   - **Bidding:** Maximize Conversions with tCPA $64
   - **Status:** ENABLED

3. **3 ad groups** created:
   - Brand - Exact (193684273580) - 19 EXACT keywords
   - Brand - Phrase (201390236868) - 12 PHRASE keywords
   - Brand - Function (189842428061) - 19 EXACT keywords
   - All RSA ad copy adapted: $199 -> $399, 100+ -> 90+ biomarkers, $17/mo -> $33/mo
   - Brand - Exact/Phrase ads -> superpower.com (homepage)
   - Brand - Function ads -> superpower.com/superpower-vs-function-health

4. **Campaign-level extensions:**
   - 4 sitelinks: How It Works, See All 90+ Biomarkers, Only $399/Year, Real Member Results
   - 8 callouts: 90+ Biomarkers, Results in About 10 Days, $399/Year Membership, etc.
   - 2 structured snippets: Types (8 health categories), Service catalog (4 values)

### Note: Competitors Coverage Gap in NY/NJ

The Competitors campaign (21904393390) also has NY/NJ geo exclusions. This means competitor searches like "function health" in NY/NJ have no coverage. Options: create NY/NJ Competitors campaign or add competitor keywords to existing NY/NJ campaigns.

---

## 2026-02-07 | NY/NJ $399 Market Launch

**Label:** `NY-NJ Launch 2.7.26`

### Pre-Step: National Campaign Geo Exclusions

1. **Added NY (21164) and NJ (21167) as negative location criteria** on all 4 national Search campaigns to prevent $199 ads showing in NY/NJ:
   - Search_SEM-Gap_Testing-Keywords_tCPA_US (23538070207)
   - Search_Generic_Best-KWs-From-Discovery_ROAS_US (23033071439) - required EU political ads declaration first
   - Search_Generic_Diagnostic-Discovery_tCPA_US (23020350152)
   - Search_Generic_Competitors_tCPA_US_Blood-Test (21904393390)

### New Campaign: Search_Generic_NY-NJ_tCPA_US (23544806539)

2. **Created new campaign** targeting only New York and New Jersey with $399 pricing:
   - **Geo targets:** NY (21164) + NJ (21167) only
   - **Budget:** $500/day
   - **Bidding:** Maximize Conversions with tCPA $399
   - **Status:** ENABLED (was PAUSED; enabled after LP + CRO confirmed complete)

3. **27 ad groups** created, one per slug, each with:
   - 1 RSA ad pointing to `-ny` landing page variant (e.g., `blood-panel-ny`)
   - PHRASE match keywords copied from national ad groups (deduped, capped at 20)
   - Ad copy adapted from national ads: $199 -> $399, 100+ -> 90+ biomarkers
   - 13 ad groups required HEALTH_IN_PERSONALIZED_ADS policy exemptions

4. **Campaign-level extensions:**
   - 4 sitelinks: How It Works, See All 90+ Biomarkers, Only $399/Year, Real Member Results
   - 8 callouts: 90+ Biomarkers, Results in About 10 Days, $399/Year Membership, No Prescription Needed, At-Home Blood Draw, Harvard-Backed Science, HSA/FSA Eligible, CLIA-Certified Labs
   - 2 structured snippets: Types (8 health categories), Service catalog (4 values)

5. **3 campaign-level negative PHRASE keywords:** "superpower", "super power", "superhuman"

### Ad Groups Created (27 total)

| Slug | Ad Group Name | AG ID | KWs |
|---|---|---|---|
| function-health-review | Function Health | 191643603543 | 20 |
| blood-test-at-home | at home blood test | 193923291018 | 4 |
| at-home-blood-work | at home blood work | 196783067990 | 4 |
| blood-panel | blood panel test | 193635134835 | 6 |
| comprehensive-blood-panel | mito blood test | 193923293738 | 8 |
| mens-blood-test | marek health | 190154293342 | 11 |
| biological-age | biohacking | 193635136755 | 17 |
| heart-health-test | heart scan test | 195991819427 | 16 |
| full-body-blood-test | extensive blood test | 193370139976 | 11 |
| lipid-panel | lipid profile test | 193246104415 | 1 |
| blood-test-general | Blood Tests General | 196783102510 | 20 |
| body-composition-test | dexa scan | 196783119270 | 20 |
| liver-function-test | Liver Function Test | 193635146075 | 5 |
| autoimmune-test | Inflammation & Autoimmune | 195992030387 | 20 |
| blood-test-online | blood test analysis online | 194471234122 | 3 |
| vitamin-deficiency-test | Vitamin Deficiency Test | 199716019824 | 9 |
| gut-health-test | microbiome test | 199716038344 | 10 |
| womens-blood-test | women's health blood tests | 191643633583 | 2 |
| blood-work | Blood Work | 190154123222 | 20 |
| hormone-panel | Hormone Tests | 191643638343 | 20 |
| wellness-testing | wellness test | 190154217062 | 1 |
| health-test-at-home | at home health test | 190153993902 | 1 |
| comprehensive-metabolic-panel | comprehensive metabolic panel test | 196474144241 | 12 |
| cancer-screening | cancer screening tests | 198098813452 | 14 |
| galleri-test-alternative | galleri test cost | 191643654143 | 14 |
| cortisol-test | cortisol test | 194529182124 | 1 |
| cholesterol-test | Heart & Cholesterol | 191269822685 | 20 |

### Handoff Documents Written

- `SEM_TO_LP_HANDOFF_NYNJ.md` - Instructions for LP Claude to build 27 `-ny` landing pages
- `SEM_TO_CRO_HANDOFF_NYNJ.md` - Instructions for CRO Claude to add checkout personalization for 27 `-ny` slugs

### Completion Status

- LP Claude: 27 `-ny` landing pages built and live (HTTP 200 verified)
- CRO Claude: 27 entries added to personalization_data.json, GTM republished (v206, 235 total slugs)
- Campaign ENABLED on 2026-02-07 after all prerequisites confirmed complete
- **Remaining:** Verify conversion goals are set to SUBSCRIBE_PAID (biddable) in Google Ads UI

---

## 2026-02-06 | Best KWs LP Wiring - 90 Ad Groups

**Label:** `Best KWs LP Wiring 2.6.26`

### Best KWs from Discovery Campaign (23033071439)

1. **Added 90 second RSA ads** pointing to CMS landing pages (A/B test vs homepage). Every enabled ad group now has a homepage ad + a landing page ad. Google will rotate between them.

2. **90 ad groups mapped to 28 unique landing pages**, including the 6 newly built blood test intent pages:
   - `blood-panel` (6 ad groups) - blood panel test, blood panel near me, etc.
   - `mens-blood-test` (11 ad groups) - mens blood test, testosterone lab work, hormone testing for men, etc.
   - `full-body-blood-test` (10 ad groups) - all in one blood test, complete blood workup, full body blood panel, etc.
   - `blood-test-general` (10 ad groups) - affordable blood test near me, blood test near me, etc.
   - `comprehensive-blood-panel` (5 ad groups) - superhuman blood test, lifeforce, wellness fx, etc.
   - `cancer-screening` (5 ad groups) - cancer screening, cancer tests, tumor marker testing, etc.
   - `at-home-blood-work` (4 ad groups) - at home blood work, at home blood panel test, mail in blood work, etc.
   - `blood-test-at-home` (4 ad groups) - at home blood test, at home tests, lab test at home, etc.
   - `biological-age` (4 ad groups) - biohacking, biological age blood test, huberman test, etc.
   - `vitamin-deficiency-test` (4 ad groups) - blood test for all vitamins and minerals, full vitamin deficiency test, etc.
   - 18 more slugs with 1-3 ad groups each

3. **Campaign spends ~$5.3K/month at $219 CPA** (most efficient non-brand Search campaign). Previously ALL 90 ad groups sent traffic to the homepage. Now each has a relevant landing page with checkout personalization.

---

## 2026-02-06 | D-D Budget Increase

**Label:** `DD Budget 2x 2.6.26`

### Diagnostic-Discovery Campaign (23020350152)

1. **Raised daily budget from $1,000 to $2,000.** Campaign was losing 74% of impressions to budget. This is the single biggest lever in the growth model for adding non-brand conversions.

---

## 2026-02-06 | DD Final Batch - 100% LP Coverage

**Label:** `DD LP A/B Test 2.6.26` (same label, Diagnostic-Discovery)

### Diagnostic-Discovery Campaign (23020350152)

1. **Added 3 second RSA ads for NEW landing pages** (built by LP Claude, final must-builds from SEM_TO_LP_HANDOFF_DD_FINAL.md):
   - T blood tests -> `t3-t4-test` ($102/90d spend)
   - Gluten intolerance -> `gluten-intolerance-test` ($41/90d)
   - Energy test -> `energy-test` ($5/90d)

2. **Added 5 second RSA ads wired to EXISTING landing pages** (skipped building dedicated pages per SEM Claude recommendation):
   - Alt alkaline phosphatase -> `alt-ast-test` ($9/90d)
   - Alkaline -> `alp-test` ($9/90d)
   - Alp ggt -> `alp-test` ($0/90d)
   - Alk -> `alp-test` ($0/90d)
   - Creatine kinase test -> `comprehensive-blood-panel` ($0/90d)

**Total: 56 of 61 D-D ad groups now have landing page A/B tests running.** Combined with the 48 from earlier batches. Remaining 5 ad groups are paused (Blood testing, Blood work, Competitor, Lab test, Microbiome).

---

## 2026-02-06 | DD LP A/B Test Batch 2

**Label:** `DD LP A/B Test 2.6.26` (same label, Diagnostic-Discovery)

### Diagnostic-Discovery Campaign (23020350152)

1. **Added 6 second RSA ads** for LP Claude Batch 2 landing pages (A/B test vs homepage):
   - Comprehensive panel -> `comprehensive-blood-panel` ($344/mo spend)
   - Gene test -> `mthfr-test` ($222/mo)
   - Immune system -> `immune-system-test` ($85/mo)
   - Alp -> `alp-test` ($69/mo)
   - Estrogen test -> `estrogen-test` ($55/mo)
   - Body fat -> `body-fat-test` ($35/mo)

**Total: 44 of 61 D-D ad groups now have landing page A/B tests running.** Combined with the 38 from earlier batches. Remaining 17 ad groups have $0 spend.

---

## 2026-02-06 | Gap Missing Pages Fix

**Label:** `SEM Overhaul 2.6.26` (same label, Gap campaign)

### Gap Campaign (23538070207)

1. **Created 5 missing ad groups** with RSA ads and 25 PHRASE-match keywords for landing pages that were built but never got ads:
   - Lab Tests Online (`lab-tests-online`) - 5 keywords
   - Lab Test (`lab-test`) - 5 keywords
   - Vitamin D3 Info (`vitamin-d3-info`) - 5 keywords
   - Vitamin Deficiency Test (`vitamin-deficiency-test`) - 5 keywords
   - Worst Inflammatory Foods (`worst-inflammatory-foods`) - 5 keywords

All 5 required HEALTH_IN_PERSONALIZED_ADS policy exemptions. All 36 SEM project landing pages now have active ads.

---

## 2026-02-06 | SEM Overhaul 2.6.26

**Label:** `SEM Overhaul 2.6.26` (applied to Gap, Diagnostic-Discovery, Competitors)

### Gap Campaign (23538070207)

1. **Rewrote all 29 RSA ads** - Replaced "More Than a X Test" headline pattern with intent-matching copy. New ads lead with the specific test the user searched for, differentiate on marker depth, and include competitive positioning vs Function Health ($199 vs $365, Harvard-backed, HSA/FSA eligible, at-home blood draw).

2. **Created 19 new ad groups** with RSA ads and 71 PHRASE-match keywords for newly launched landing pages (liver-function-test, kidney-function-test, alt-ast-test, hepatic-panel, kidney-infection-test, high-liver-enzymes, thyroid-issues, overactive-thyroid, thyroid-symptoms-female, tsh-levels, hashimotos-symptoms, enlarged-heart, cholesterol-test-at-home, continuous-glucose-monitor, at-home-diabetes-test, blood-work, epigenetics-test, health-wellness, function-health-review). 7 required HEALTH_IN_PERSONALIZED_ADS policy exemptions.

3. **Set $400 tCPA** on the campaign (was uncapped Maximize Conversions).

4. **Campaign-level extensions already existed** (4 sitelinks, 8 callouts, 2 structured snippets) - no changes needed.

### Diagnostic-Discovery Campaign (23020350152)

5. **Added 16 second RSA ads** pointing to condition-specific landing pages (A/B test vs homepage). Ad groups: Vitamin, Testosterone, Hormone Testing, Thyroid, Health testing, Health Check, Biomarker, Cardiovascular, Metabolic, Longevity, Medical test, Test, Inflammation test, Cortisol, Glucose test.

6. **Added campaign-level extensions:**
   - 4 sitelinks: How It Works, See All 100+ Biomarkers, Only $199/Year, Real Member Results
   - 8 callouts: 100+ Biomarkers, Results in About 10 Days, $199/Year Membership, No Prescription Needed, At-Home Blood Draw, Harvard-Backed Science, HSA/FSA Eligible, CLIA-Certified Labs
   - 2 structured snippets: Types (8 health categories), Service catalog (4 services)

7. **Added 31 campaign-level negative PHRASE keywords** to prevent cannibalization with Gap campaign:
   - 12 exact overlap keywords: thyroid issues, thyroid problems, overactive thyroid, overactive thyroid symptoms, hashimoto's thyroiditis symptoms, hashimoto thyroiditis, continuous glucose monitoring, liver function test, liver function tests, liver blood test, kidney function test, renal function test
   - 19 distinctive Gap terms: hepatic panel, kidney infection, high liver enzymes, elevated liver enzymes, alt ast, tsh levels, hashimotos symptoms, thyroid symptoms female, thyroid symptoms in women, at home diabetes test, cholesterol test at home, enlarged heart, epigenetics meaning, biological age test, worst inflammatory foods, lab tests online, function health review, function health alternative, function health cost

### Competitors Campaign (21904393390)

8. **Added 1 second RSA ad** to the Function Health ad group pointing to function-health-review landing page.

9. **Added campaign-level extensions:**
   - 4 sitelinks: $199/Yr - Not $365+, At-Home Blood Draw, See All 100+ Biomarkers, HSA/FSA Eligible
   - 8 callouts: 100+ Biomarkers Tested, $199/Year - Not $365, No Waitlist, At-Home Blood Draw, Harvard-Backed Science, HSA/FSA Eligible, Results in About 10 Days, CLIA-Certified Labs
   - 1 structured snippet: Types (100+ Biomarkers, At-Home Testing, $199/Year, HSA/FSA Eligible, Harvard-Backed)

### Pending / Handoff

- **Keyword overlap monitoring**: Gap vs D-D broad match collision risk remains. Monitor search terms report weekly.

---

## 2026-02-06 | DD LP A/B Test 2.6.26

**Label:** `DD LP A/B Test 2.6.26` (applied to Diagnostic-Discovery)

### Diagnostic-Discovery Campaign (23020350152)

LP Claude built 11 new landing pages. CRO Claude set up checkout personalization (GTM v199). Added second RSA ads to complete the A/B test funnels.

1. **Added 11 second RSA ads for NEW landing pages** (built by LP Claude, checkout by CRO Claude):
   - Cancer -> cancer-screening ($1,214/mo spend)
   - Body composition -> body-composition-test ($767/mo)
   - Galleri test -> galleri-test-alternative ($602/mo)
   - Gut test -> gut-health-test ($577/mo)
   - igf 1 test -> igf-1-test ($332/mo)
   - Health assessment -> functional-health-assessment ($264/mo)
   - CMP -> comprehensive-metabolic-panel ($249/mo)
   - Nutrient test -> nutrient-deficiency-test ($243/mo)
   - Heart Testing -> heart-health-test ($219/mo)
   - bmp -> basic-metabolic-panel ($214/mo)
   - Mineral deficiency test -> mineral-deficiency-test ($103/mo)

2. **Added 12 second RSA ads for EXISTING landing pages** (already in CMS):
   - CBC -> cbc-test ($358/mo)
   - Age blood test -> biological-age ($306/mo)
   - Epigenetics test -> epigenetics-test ($296/mo)
   - Cholestrol test -> cholesterol-test ($238/mo)
   - Ferritin test -> ferritin-test ($198/mo)
   - LDL -> ldl-cholesterol-test ($174/mo)
   - Biological Age -> biological-age ($120/mo)
   - Celiac Test -> celiac-test-at-home ($89/mo)
   - Apop -> apob-test ($64/mo)
   - Lipid test -> lipid-panel ($43/mo)
   - CRP -> crp-test ($41/mo)
   - Hyperthyroid -> hyperthyroidism-biomarker-test ($16/mo)

**Total: 23 new second RSA ads** across D-D ad groups representing $4,790/mo in spend. Combined with the 15 added earlier (SEM Overhaul), **38 of 61 D-D ad groups now have landing page A/B tests running.**

### Remaining D-D Ad Groups Without Landing Pages (23 groups)

Low-spend or poor-fit groups not yet addressed: Adrenal glands test, Alk, Alkaline, Alp, Alp ggt, Alt alkaline phosphatase, Alanine aminotransferase, Blood testing, Blood work, Body fat, Competitor, Comprehensive panel, Creatine kinase test, Energy test, Estrogen test, Gene test, Gluten intolerance, Health assessment (duplicate?), Immune system, Microbiome, T blood tests, TSH, Urea.

---

## SOP: Change Logging

**Every time changes are made to the Google Ads account:**

1. Create a Google Ads label with format: `[Change Type] [M.D.YY]` (e.g., "SEM Overhaul 2.6.26")
2. Apply the label to all affected campaigns
3. Add an entry to this change log with:
   - Date and label name
   - What was changed, by campaign
   - Why it was changed
   - Any pending follow-ups
4. Keep entries in reverse chronological order (newest first)
