# CRO Cloud - Operational Knowledge Base

Checkout Rate Optimization operational documentation for Superpower Health's SEM funnel. This is the single source of truth for how the checkout personalization system works, how to deploy changes, and how the three-agent architecture operates.

## Current System State

| Metric | Value |
|--------|-------|
| Personalized checkout slugs | 111 active (trimmed from 235) |
| GTM container version | v210 |
| Tag architecture | 1 single tag (~93K chars) |
| GTM character limit per tag | 102,400 |
| Headroom remaining | ~9.4K chars |
| National pricing | $199/year, 100+ biomarkers |
| NY/NJ pricing | $399/year, 90+ biomarkers |

## Three-Agent Architecture

| Agent | Responsibility | Key Output |
|-------|---------------|------------|
| **LP Claude** | Builds landing pages in Webflow CMS | `/welcome-cms/{slug}` pages |
| **SEM Claude** | Manages Google Ads campaigns, keywords, ad copy | Campaign configs, keyword strategy |
| **CRO Claude** | Personalizes checkout via GTM for each landing page | `personalization_data.json`, GTM tags |

## Documentation Index

### Architecture & Systems

- [System Architecture](system-architecture.md) - Full traffic flow diagram, how all pieces connect
- [GTM Personalization](gtm-personalization.md) - How checkout personalization works (12 fields, DOM selectors, tag structure)
- [GTM Deployment](gtm-deployment.md) - How to deploy GTM changes (scripts, rate limits, gotchas)

### Standards & Integration

- [Content Standards](content-standards.md) - Copy rules, testimonial requirements, pricing standards
- [Webflow API](webflow-api.md) - API patterns, collection IDs, publish workflow
- [Google Ads Integration](google-ads-integration.md) - How ads connect to LPs connect to checkout personalization

### Operations

- [Inter-Agent Protocols](inter-agent-protocols.md) - How LP/SEM/CRO agents hand off work
- [Lessons Learned](lessons-learned.md) - Bugs, fixes, patterns that worked/failed

### Runbooks (Step-by-Step)

- [Add New Slug](runbooks/add-new-slug.md) - Add checkout personalization for a new landing page
- [Deploy GTM Update](runbooks/deploy-gtm-update.md) - Update the GTM container
- [Trim Personalization Data](runbooks/trim-personalization-data.md) - Remove inactive slugs
- [Create NY/NJ Variant](runbooks/create-nynj-variant.md) - Create a NY/NJ pricing variant

## Project Location

| Item | Path |
|------|------|
| Project root | `/Users/jeffy/superpower-sem-gap/` |
| Git repo (.git) | `/Users/jeffy/superpower-sem-gap/app/` |
| GitHub remote | `https://github.com/jgdeutsch/superpower-sem-gap.git` |
| This docs folder | `app/cro-cloud/` |
| Personalization data | `app/data/personalization_data.json` |
| GTM tag HTML | `app/gtm/register_personalization_tag.html` |
| Deploy script | `app/scripts/deploy_gtm_cleanup.py` |
