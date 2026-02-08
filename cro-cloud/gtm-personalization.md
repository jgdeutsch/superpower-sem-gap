# GTM Personalization - How It Works

## Overview

When a user clicks a CTA on a landing page, the link rewriter tag appends `?sp_variant={slug}` to the checkout URL. On the checkout page, the personalization tag reads that parameter, looks up the slug in its baked-in JSON data, and manipulates the DOM to show condition-specific content.

## The 12 Personalization Fields

Each entry in `personalization_data.json` has these fields:

| Field | What It Does on Checkout | Content Rules |
|-------|--------------------------|---------------|
| `headline` | Replaces the main h3 heading | "Screen for [X] and 1,000+ Conditions." or price-forward like "100+ Biomarkers. One Blood Draw. $199/Year." |
| `ctaText` | Replaces the submit button text | **Always "Start Testing"** |
| `subtitleOverride` | Replaces the paragraph below the headline | "100+ biomarkers in one blood draw. [relevant markers]." For at-home pages: "$199/year membership + $99 at-home phlebotomist. [markers]." |
| `testimonialQuote` | Injected as a testimonial card below the form | Must include **specific biomarker numbers** |
| `testimonialName` | Name on testimonial | "First L." format |
| `testimonialResult` | Result line on testimonial | Concrete outcome with numbers |
| `benefit1` | Checkmark benefit line 1 | Condition-specific, SHORT (<10 words) |
| `benefit2` | Checkmark benefit line 2 | Usually about breadth: "100+ biomarkers including [X]" |
| `benefit3` | Checkmark benefit line 3 | Usually AI advantage |
| `benefit4` | Checkmark benefit line 4 | Usually "24/7 care team access" |
| `stat1Number` | Used in subtitle fallback | Condition-specific stat |
| `stat1Text` | Used in subtitle fallback | Context for stat |

### Example Entry

```json
{
  "fatty-liver-test": {
    "headline": "Screen for Fatty Liver and 1,000+ Conditions.",
    "ctaText": "Start Testing",
    "subtitleOverride": "100+ biomarkers in one blood draw. Liver, metabolic, thyroid, heart, and more.",
    "testimonialQuote": "I don't drink at all but my ALT was 68 and GGT was 55 - both elevated. Doctor had never tested liver enzymes before. Turned out I had grade 2 fatty liver from insulin resistance. Weight loss and dietary changes normalized everything in 8 months.",
    "testimonialName": "Linda M.",
    "testimonialResult": "Liver enzymes normalized in 8 months",
    "benefit1": "Track liver enzymes and metabolic markers yearly",
    "benefit2": "100+ biomarkers including full liver panel",
    "benefit3": "AI connects liver and metabolic patterns",
    "benefit4": "24/7 care team access",
    "stat1Number": "25%",
    "stat1Text": "of adults have NAFLD - non-alcoholic fatty liver disease"
  }
}
```

## Content Patterns by Page Type

### Condition-specific pages (most common)
- headline: "Screen for [Condition] and 1,000+ Conditions."
- subtitleOverride: "100+ biomarkers in one blood draw. [Key markers for this condition]."
- benefit1: Condition-specific monitoring
- benefit4: "24/7 care team access"

### Broad/generic test pages (blood-work, blood-panel, health-screening)
- headline: "100+ Biomarkers. One Blood Draw. $199/Year."
- subtitleOverride: "Heart, hormones, thyroid, liver, kidney, vitamins, and more. Results in about 10 days."
- benefit1: "100+ biomarkers - 5x a standard physical" or similar

### At-home pages (slugs containing "home" or "at-home")
- headline: "100+ Biomarkers. Drawn at Home. $199/Year."
- subtitleOverride: "$199/year membership + $99 at-home phlebotomist. [scope]."
- benefit1: "At-home licensed phlebotomist ($99 add-on)"
- ONLY mention phlebotomist if the slug contains "home" or "at-home"

### Competitor pages (function-health-review, galleri-test-alternative)
- headline: Price comparison focused
- subtitleOverride: Feature comparison
- Testimonial: Competitor experience + Superpower advantage

### NY/NJ pages (slugs ending in `-ny`)
- Clone national counterpart
- Replace $199 -> $399 everywhere
- Replace 100+ -> 90+ everywhere

## Tag Architecture

### Single Tag (`SP - Checkout Personalization`)

The personalization data is baked directly into the tag HTML as a compressed JSON object. The tag is a self-executing JavaScript function:

```javascript
(function() {
  // Prevent duplicate execution
  if (document.getElementById('sp-testimonial')) return;

  // Get the slug from URL parameter
  var params = new URLSearchParams(window.location.search);
  var variant = params.get('sp_variant');
  if (!variant) return;

  // Look up the slug in baked-in data
  var DATA = {/* all 111 slug entries as compressed JSON */};
  var page = DATA[variant];
  if (!page) return;

  // Retry polling (React renders async - DOM may not be ready)
  var MAX_ATTEMPTS = 50;  // 50 x 100ms = 5 seconds max
  var attempt = 0;

  function apply() {
    attempt++;
    // Find and replace DOM elements...
    // Push dataLayer event for tracking
  }
  apply();
})();
```

### DOM Selectors

| Selector | What It Finds |
|----------|---------------|
| `h3.typography-heading3` (first) | Main page headline |
| `h3.typography-heading3` (second) | "Superpower Membership" heading |
| `button[type="submit"]` | CTA button ("Continue" by default) |
| `<p>` sibling after first h3 | Subtitle/description text |
| `<p>` sibling after second h3 | Membership benefits description |
| `form` parent element | Where testimonial card gets injected |

**These selectors match the server-rendered HTML.** If the checkout app changes its markup, the selectors will need updating.

### Link Rewriter Tag (`SP - Landing Page Link Rewriter`)

Runs on Webflow landing pages (`/welcome-cms/*`). Extracts the slug from the URL path and appends `?sp_variant={slug}` to every `/checkout` and `/register` link on the page.

```javascript
(function() {
  var path = window.location.pathname;
  var match = path.match(/\/(?:welcome-cms|sem-landing-pages)\/([^\/]+)/);
  if (!match) return;
  var slug = match[1];
  var links = document.querySelectorAll('a[href*="/checkout"], a[href*="/register"]');
  for (var i = 0; i < links.length; i++) {
    var href = links[i].getAttribute('href');
    if (href && href.indexOf('sp_variant') === -1) {
      var separator = href.indexOf('?') === -1 ? '?' : '&';
      links[i].setAttribute('href', href + separator + 'sp_variant=' + slug);
    }
  }
})();
```

## Capacity

| Metric | Value |
|--------|-------|
| GTM character limit per tag | 102,400 |
| Current tag size | ~93K chars |
| Headroom | ~9.4K chars |
| Active slugs | 111 |
| Average chars per slug | ~840 |
| Approx slugs before hitting limit | ~11 more |

If more than ~11 slugs need to be added, the tag must split into 2 tags again. See [lessons-learned.md](lessons-learned.md) for the history of the 2-tag -> 1-tag consolidation.

## Verification

Test URLs (use incognito, allow 2 min for GTM propagation):

```
# National
https://superpower.com/checkout/membership?sp_variant=cholesterol-test
https://superpower.com/checkout/membership?sp_variant=blood-work

# At-home (should show $99 phlebotomist)
https://superpower.com/checkout/membership?sp_variant=blood-test-at-home

# NY/NJ (should show $399/90+)
https://superpower.com/checkout/membership?sp_variant=cholesterol-test-ny
```
