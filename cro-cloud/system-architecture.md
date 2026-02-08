# System Architecture

## Traffic Flow

```
Google Ads
  |
  v
Landing Page (Webflow - superpower.com/welcome-cms/{slug})
  |  GTM fires "SP - Landing Page Link Rewriter"
  |  Appends ?sp_variant={slug} to all /checkout and /register links
  |
  v  (user clicks CTA)
Checkout Page (React App - superpower.com/checkout/membership?sp_variant={slug})
  |  GTM fires "SP - Checkout Personalization"
  |  Reads sp_variant, looks up slug in baked-in JSON data
  |  Replaces headline, subtitle, CTA, benefits, injects testimonial
  |
  v
Conversion (ph_subscription_created)
```

## Domain Architecture

| Domain/Path | Served By | GTM Present? | Purpose |
|-------------|-----------|:---:|---------|
| `superpower.com` (homepage) | Webflow | Yes | Brand landing |
| `superpower.com/welcome-cms/*` | Webflow CMS | Yes | SEM landing pages |
| `superpower.com/checkout` | React App (TanStack Router) | Yes | Checkout flow |
| `superpower.com/checkout/membership` | React App | Yes | Membership checkout |
| `app.superpower.com/register` | Separate app | Yes | Registration flow |
| `superpower.com/welcome` | Webflow (static) | Yes | Generic welcome page |
| `superpower.com/labs-new-york` | Webflow (static) | Yes | NY/NJ static page |

**Key insight**: Webflow serves the marketing pages. The React app serves checkout. These are separate applications sharing the same domain. GTM container `GTM-PBS5NFXN` is loaded on both.

## GTM Container Layout

**Container**: `GTM-PBS5NFXN`
**Account/Container path**: `accounts/6255639144/containers/198767392`

### Tags (2 active)

| Tag Name | What It Does | Fires On |
|----------|-------------|----------|
| `SP - Checkout Personalization` | Single tag with 111 baked-in slug entries (~93K chars). Reads `sp_variant` from URL, personalizes checkout DOM. | Trigger 332 |
| `SP - Landing Page Link Rewriter` | Extracts slug from `/welcome-cms/{slug}` path, appends `?sp_variant={slug}` to all checkout/register links on the page. | Trigger 333 |

### Triggers (2 active)

| Trigger ID | Name | Conditions |
|:---:|------|------------|
| 332 | DOM Ready - Register/Checkout with SP Variant | Path matches `/register` or `/checkout` AND URL contains `sp_variant=` |
| 333 | DOM Ready - SEM Landing Pages | Path matches `/welcome-cms/` or `/sem-landing-pages/` |

## Data Flow

```
personalization_data.json (111 entries)
  |
  v  (baked into tag HTML as compressed JSON)
register_personalization_tag.html (~93K chars)
  |
  v  (deployed via GTM API)
GTM Container (published version)
  |
  v  (loaded on page)
Checkout DOM manipulation
```

## Three-Agent Workflow

```
SEM Claude                    LP Claude                    CRO Claude
    |                             |                            |
    |-- SEM_TO_LP_HANDOFF_*.md -->|                            |
    |                             |-- LP_TO_CRO_*.md --------->|
    |                             |                            |
    |                             |-- LP_TO_SEM_*.md --------->|
    |<-- SEM_TO_CRO_*.md ------------------------------------- |
    |                             |                            |
    |  (creates campaigns,        | (builds Webflow CMS        | (adds to
    |   keywords, ad copy)        |  landing pages)            |  personalization_data.json,
    |                             |                            |  deploys to GTM)
```

All handoff documents live at the project root: `/Users/jeffy/superpower-sem-gap/`
