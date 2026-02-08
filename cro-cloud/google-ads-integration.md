# Google Ads Integration

How Google Ads campaigns connect to landing pages, which connect to checkout personalization.

## Account Details

| Item | Value |
|------|-------|
| Customer ID | `8618096874` |
| MCC (Login Customer ID) | `8461075268` |
| API Version | v19 |

## The Funnel

```
Google Ads Campaign
  |
  |  Ad with final URL: https://superpower.com/welcome-cms/{slug}
  |
  v
Landing Page (Webflow CMS)
  |
  |  Link rewriter appends ?sp_variant={slug}
  |
  v
Checkout (React App)
  |
  |  GTM reads sp_variant, personalizes DOM
  |
  v
Conversion: ph_subscription_created
```

## Conversion Tracking

### Primary Conversion Event

**`ph_subscription_created`** (category: `SUBSCRIBE_PAID`)

- **Conversion Action ID**: `7229395888`
- **Type**: `UPLOAD_CLICKS` (offline conversion uploaded via PostHog pipeline using GCLID matching)
- **primaryForGoal**: `True` (biddable - included in `metrics.conversions`)
- **PostHog equivalent**: `SUBSCRIPTION_CREATED` (server-side event)

### Events That Are NOT the Goal

- `ph_registration_started` (SUBMIT_LEAD_FORM) - lead, not sale
- `ph_registration_started_web` (SUBMIT_LEAD_FORM) - lead, not sale
- `PostHog Revenue Action` (PURCHASE) - revenue tracking
- `Purchase (all value events)` (PURCHASE) - aggregate

### Important API Quirk

When segmenting by `segments.conversion_action_name`, you CANNOT include `metrics.clicks` or `metrics.cost_micros` in the same query. You must run two separate queries and join them client-side. See `app/scripts/slugfest.py` for the working implementation.

## Active Campaigns (as of Feb 2026)

### National Campaigns

| Campaign | ID | Budget | Bidding | CMS Slugs |
|----------|-----|--------|---------|:---------:|
| Gap (SEM-Gap Testing Keywords) | 23538070207 | varies | tCPA $400 | 31 |
| Best KWs (From Discovery) | 23033071439 | varies | ROAS | 28 |
| Diagnostic-Discovery | 23020350152 | $2,000/day | tCPA | 27 |
| Competitors | 21904393390 | varies | tCPA | 1 |
| Brand | 21893543504 | varies | tCPA | 0 (homepage) |

### NY/NJ Campaigns

| Campaign | ID | Budget | Bidding | CMS Slugs |
|----------|-----|--------|---------|:---------:|
| NY-NJ Generic | 23544806539 | $500/day | tCPA $399 | 27 |
| NY-NJ Brand | 23544911674 | $200/day | tCPA $64 | 0 (homepage) |
| NY-NJ Competitors | 23535201240 | $500/day | tCPA $700 | 6 |

All national campaigns have NY (21164) and NJ (21167) as negative location criteria.

## Change Logging SOP

**Every time changes are made to the Google Ads account:**

1. **Create a label**: `[Change Type] [M.D.YY]` (e.g., "SEM Overhaul 2.6.26")
   - Note: the label `description` field causes API errors - use name only
2. **Apply label** to all affected campaigns
3. **Add entry** to `/Users/jeffy/superpower-sem-gap/GOOGLE_ADS_CHANGE_LOG.md`
4. Include: date, label name, what changed, why, pending follow-ups

## How Ad URLs Map to Checkout Personalization

The mapping is direct: the slug in the landing page URL becomes the `sp_variant` parameter on checkout.

```
Ad final URL:     https://superpower.com/welcome-cms/cholesterol-test
Link rewriter:    appends ?sp_variant=cholesterol-test
Checkout URL:     https://superpower.com/checkout/membership?sp_variant=cholesterol-test
Personalization:  looks up "cholesterol-test" in baked-in JSON data
```

For NY/NJ pages, the slug includes the `-ny` suffix:

```
Ad final URL:     https://superpower.com/welcome-cms/cholesterol-test-ny
Checkout URL:     https://superpower.com/checkout/membership?sp_variant=cholesterol-test-ny
```

## Non-CMS Ad URLs

These pages have active ads but are NOT in the CMS personalization system:

| URL | Type | Notes |
|-----|------|-------|
| `superpower.com` | Homepage | Brand traffic |
| `superpower.com/welcome` | Static Webflow | Generic welcome (has known content issues) |
| `superpower.com/labs-new-york` | Static Webflow | NY/NJ specific |
| `superpower.com/superpower-vs-function-health` | Static Webflow | Competitor comparison |
| `superpower.com/superpower-vs-marek-health` | Static Webflow | Competitor comparison |

These use their own page designs and don't need CMS personalization entries.

## API Credentials

OAuth credentials for the Google Ads API are stored in `/Users/jeffy/superpower-sem-gap/update_gap_ads.py` (lines 13-18).

## Google Ads API Notes

- Sitelink `finalUrls` goes on the asset level, NOT inside `sitelinkAsset`
- Sitelink description1/description2 max: **25 chars** (not 35!)
- No tildes (~) in ad copy - Google SYMBOLS policy rejects them
- RSA description max: 90 chars, headline max: 30 chars
- Campaign creation REQUIRES `containsEuPoliticalAdvertising: DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING`
- Use `MAXIMIZE_CONVERSIONS` with `maximizeConversions.targetCpaMicros` (NOT `TARGET_CPA`)
- Budget + campaign CANNOT share a mutate call with temp resource names - create budget first
- HEALTH_IN_PERSONALIZED_ADS policy: use `exemptPolicyViolationKeys` (isExemptible: true)
