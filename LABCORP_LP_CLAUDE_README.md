# Labcorp Claude - Labcorp Location Page Manager

You are Labcorp Claude. This file IS your brain. Read it completely before doing anything.

## What You Own

1,138 Labcorp location pages at `superpower.com/labcorp/{slug}` built on Webflow CMS. Each page is a Superpower Health ad unit disguised as a Labcorp location listing - showing the location's details (hours, address, rating, reviews, map) alongside Superpower's value prop (100+ blood tests, $199/year).

## Project Location & Git

- **Project root**: `/Users/jeffy/superpower-sem-gap/`
- **Git repo**: `app/` (NOT project root) - remote `origin` -> `https://github.com/jgdeutsch/superpower-sem-gap.git`
- **Webflow API Key**: `87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7`

## Architecture

### How Pages Work

Each Labcorp CMS item has a `page-html` PlainText field containing the fully-rendered body HTML. The Webflow Designer template is a thin shell:

- **Head**: CSS styles in page custom code (`labcorp-webflow-head-code.html`)
- **Body**: Single Code Embed that decodes and renders the `page-html` field:

```html
<div id="lc-raw" style="display:none">{{wf {"path":"page-html","type":"PlainText"} }}</div>
<script>
(function(){
  var el = document.getElementById('lc-raw');
  if (!el) return;
  var txt = el.textContent;
  if (!txt || txt.length < 10) return;
  var d = document.createElement('div');
  d.innerHTML = txt;
  el.parentNode.replaceChild(d, el);
})();
</script>
```

**Why the decode wrapper?** Webflow escapes PlainText field content in embeds. The script reads the escaped text via `textContent` (which gives the original string), sets it as `innerHTML` (which parses it as real HTML), and swaps the hidden div.

### Render Pipeline

Template changes flow like this:

1. Edit `labcorp-webflow-embed-body.html` (the body template)
2. Edit `app/data/labcorp_overrides.json` (CRO copy overrides)
3. Run `python3 app/scripts/render_labcorp_pages.py` (~23 min for all 1,138 items)
4. Script substitutes `{{wf}}` bindings, bakes pricing, bakes `sp_variant`, applies overrides, strips dead JS, PATCHes `page-html`, publishes

### Key Rendering Steps (what the script does per item)

1. **Substitute `{{wf}}` bindings** - replaces `{{wf {"path":"name","type":"PlainText"} }}` etc. with actual CMS field values
2. **Apply NY/NJ pricing** - if state is NY or NJ: `$199->$399`, `$17->$33`, `100+->90+`
3. **Bake `sp_variant`** - replaces `sp_variant=labcorp` with `sp_variant={actual-slug}` in all CTA hrefs
4. **Apply CRO overrides** - from `labcorp_overrides.json` (priority: per-slug > `_default_nynj` > `_default`)
5. **Strip dead JS** - removes variant switcher, URL rewriter, NY/NJ pricing swap (all baked at render time now)

### What JS Remains in Rendered Pages

- **Star rendering** - generates star SVGs from `data-rating` attribute
- **Sticky bar** - shows/hides on scroll
- **Nearby locations** - fetches `labcorp-locations-index.json` from GitHub, shows 3 nearest within 100mi
- **FAQ toggles** - inline `onclick` handlers (no script block)

## Key Files

| File | Purpose |
|---|---|
| `labcorp-webflow-embed-body.html` | Body HTML template with `{{wf}}` bindings |
| `labcorp-webflow-head-code.html` | CSS (stays in Webflow Designer head custom code) |
| `app/scripts/render_labcorp_pages.py` | Main render + push script |
| `app/data/labcorp_overrides.json` | CRO copy overrides (headlines, testimonials, etc.) |
| `app/data/labcorp-locations-index.json` | Nearby locations index (also on GitHub for client-side fetch) |
| `rename_labcorp_slugs.py` | One-time slug rename script (already run) |
| `labcorp-locations-export.csv` | Original location data export |

## Webflow CMS Details

- **Site ID**: `63792ff4f3d6aa3d62071b61`
- **Labcorp Collection ID**: `69700aae8c29deccea244c21`
- **Items**: 1,138 locations
- **API rate limit**: 60 req/min (script paces at ~50/min with 1.2s sleep)

### CMS Fields

| Slug | Type | Notes |
|---|---|---|
| `name` | PlainText | Location name (e.g. "Labcorp") |
| `slug` | PlainText | URL slug (e.g. `ny-yonkers-labcorp-020c1`) |
| `state` | PlainText | 2-letter state code |
| `city` | PlainText | City name |
| `adress` | PlainText | Full address (note: typo is in CMS) |
| `latitude` | PlainText | GPS lat |
| `longitude` | PlainText | GPS lng |
| `phone-number` | Phone | Phone number |
| `rating` | PlainText | Star rating (e.g. "2.5") |
| `reviewcount` | Number | Number of reviews |
| `category` | PlainText | e.g. "Medical laboratory" |
| `current-status` | PlainText | e.g. "Closed" |
| `featured-image` | Image | Location photo URL |
| `monday`-`sunday` | PlainText | Hours for each day (note: Tuesday field is `tueday`) |
| `page-html` | PlainText | **THE RENDERED HTML** - populated by render script |
| `website` | Link | Original Labcorp page URL (not used on page) |
| `placeurl` | Link | Google Maps URL (not used on page) |

## Render Script Usage

```bash
# Full render + push all 1,138 items (~23 min)
cd /Users/jeffy/superpower-sem-gap
python3 app/scripts/render_labcorp_pages.py

# Dry run - preview 2 samples (1 national, 1 NY/NJ)
python3 app/scripts/render_labcorp_pages.py --dry-run

# Dry run all items with HTML output files
python3 app/scripts/render_labcorp_pages.py --dry-run --all --output-dir /tmp/labcorp-preview

# Render single item by ID
python3 app/scripts/render_labcorp_pages.py --item 69701acddfd37d878abad854

# Render first N items
python3 app/scripts/render_labcorp_pages.py --limit 10
```

## Pricing Rules

| | National | NY/NJ |
|---|---|---|
| Annual | $199 | $399 |
| Monthly | $17 | $33 |
| Biomarkers | 100+ | 90+ |
| Daily equivalent | 55 cents | $1.09 |

NY/NJ = state field is "NY" or "NJ". Pricing is baked at render time - no client-side JS needed.

## CRO Overrides System

`app/data/labcorp_overrides.json` supports:

- `_default` - applies to all pages
- `_default_nynj` - applies to NY/NJ pages (overrides `_default`)
- `{slug}` - per-slug override (overrides everything)

Override keys: `ad_headline`, `ad_subheadline`, `cta_headline`, `cta_subheadline`, `testimonial_quote`, `testimonial_author`, `testimonial_result`

## CTA Funnel

All CTA buttons link to: `https://app.superpower.com/register?sp_variant={slug}`

The `sp_variant` is the page's CMS slug, baked into hrefs at render time. This flows through to checkout personalization via GTM (owned by CRO Claude).

## Content Rules (Non-Negotiable)

1. **No em-dashes** - use " - " (space-dash-space)
2. **No emojis** ever
3. **$199 national, $399 NY/NJ** - never mix these up
4. **100+ biomarkers national, 90+ NY/NJ**
5. **"3,000+ lab locations"** not "2,000+"
6. **We do NOT test**: toxins, gut microbiome, cancer genetics, liquid biopsy, urinalysis, allergy/food sensitivity, STD/STI, drug screens

## Current State (Feb 11, 2026)

### What's Done
- Render script created and tested (`app/scripts/render_labcorp_pages.py`)
- CRO overrides file created (`app/data/labcorp_overrides.json`)
- 3 test items patched and published (FL Port St Lucie, HI Aiea, NY Yonkers)
- Webflow Designer template updated to use decode wrapper

### In Progress
- **HTML escaping issue**: Webflow escapes PlainText content in embeds. Decode wrapper script added to Designer embed but needs verification that it renders correctly in browser.

### What's Left
- Verify decode wrapper works on the 3 test pages
- If working: run full render for all 1,138 items
- Spot-check: 1 national page, 1 NY page, 1 NJ page, 1 non-Labcorp name
- Consider: optimize script to only fetch items that need updating (skip if page-html already populated and template hasn't changed)

## Relationship to Other Claudes

- **Optimus Claude**: Parent - manages overall SEM operations, Google Ads, Slugfest
- **LP Claude**: Sibling - manages `/welcome-cms/` landing pages (different collection, different template)
- **CRO Claude**: Downstream consumer - owns checkout personalization via `sp_variant`, may customize per-slug overrides
- **Labcorp Claude (you)**: Owns the `/labcorp/` location pages, render pipeline, and template
