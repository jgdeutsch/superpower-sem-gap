# GTM Setup - Checkout Page Personalization

Personalizes `superpower.com/checkout` based on which SEM landing page the user came from (`?sp_variant={slug}`).

## Architecture

```
SEM Landing Page (Webflow, has GTM)
  -> Link Rewriter tag appends ?sp_variant={slug} to /checkout and /register links
  -> User clicks CTA -> arrives at /checkout?sp_variant=cortisol-test

Checkout Page (React app, needs GTM added)
  -> Personalization tag reads sp_variant
  -> Swaps headline, subtitle, CTA, membership benefits, injects testimonial
```

## PREREQUISITE: Add GTM to the Checkout App

The Webflow marketing site (`superpower.com`) has GTM container `GTM-PBS5NFXN`.
The checkout app (`superpower.com/checkout`) does **NOT** currently load GTM.

**Engineering must add the GTM snippet to the checkout app's `<head>`:**

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-PBS5NFXN');</script>
```

Until this is done, the personalization tag will not fire on `/checkout`.

### Alternative: Direct Script Injection (No GTM)

If adding GTM to the checkout app is not feasible, engineering can instead add a `<script>` tag that loads the personalization data and script directly. See `checkout_personalization.js` for the standalone version.

---

## GTM Configuration Steps

### Step 1: Create URL Query Variable

1. **Variables > User-Defined Variables > New**
2. Type: **URL**
3. Component Type: **Query**
4. Query Key: `sp_variant`
5. Name: `SP Variant`

### Step 2: Create Personalization Data Variable

1. **Variables > User-Defined Variables > New**
2. Type: **Custom JavaScript**
3. Paste contents of `app/data/gtm_personalization_variable.js`
4. Name: `SP Personalization Data`

### Step 3: Create Landing Page Link Rewriter (Webflow)

This works NOW - GTM is already on the Webflow pages.

1. **Triggers > New**
   - Type: **DOM Ready**
   - Fires on: Some DOM Ready Events
   - Condition: `Page Path` **matches RegEx** `/(welcome-cms|sem-landing-pages)/`
   - Name: `DOM Ready - SEM Landing Pages`

2. **Tags > New**
   - Type: **Custom HTML**
   - Paste contents of `app/gtm/landing_page_link_rewriter.html`
   - Trigger: `DOM Ready - SEM Landing Pages`
   - Name: `SP - Link Rewriter`

### Step 4: Create Checkout Personalization Tag

This requires GTM on `/checkout` (see prerequisite above).

1. **Triggers > New**
   - Type: **DOM Ready**
   - Fires on: Some DOM Ready Events
   - Conditions:
     - `Page Path` **contains** `/checkout`
     - `SP Variant` **does not equal** (empty - checks sp_variant exists)
   - Name: `DOM Ready - Checkout with SP Variant`

2. **Tags > New**
   - Type: **Custom HTML**
   - Paste contents of `app/gtm/register_personalization_tag.html`
   - Trigger: `DOM Ready - Checkout with SP Variant`
   - Name: `SP - Checkout Personalization`

---

## Testing

### Test Link Rewriter (works now)

1. GTM Preview mode
2. Visit `https://www.superpower.com/welcome-cms/cortisol-test`
3. Inspect CTA links - should have `?sp_variant=cortisol-test` appended

### Test Checkout Personalization (after GTM is on /checkout)

Visit: `https://superpower.com/checkout?sp_variant=cortisol-test`

Expected changes:
- Headline: "Is Stress Destroying Your Body From the Inside?"
- CTA button: "Test Cortisol Now"
- Subtitle: "75% of doctor visits are stress-related. Find out where you stand."
- Membership benefits: personalized cortisol-specific list
- Testimonial from Jennifer M. injected below the form

### Quick DevTools Test (no GTM needed)

1. Open `https://superpower.com/checkout` in Chrome
2. Open DevTools Console
3. Paste the personalization data:
   ```js
   window.__SP_PERSONALIZATION_DATA = { /* paste JSON from personalization_data.json */ };
   ```
4. Then paste `checkout_personalization.js` contents
5. Observe DOM changes

---

## DOM Selectors Used

| Element | Selector | Default Text |
|---------|----------|-------------|
| Headline | `h3.typography-heading3` (first) | "Get Actionable Insights in 10 days" |
| Subtitle | next `<p>` sibling of headline | "Your membership auto-renews..." |
| CTA Button | `button[type="submit"]` | "Continue" |
| Membership Heading | `h3.typography-heading3` (second) | "Superpower Membership" |
| Membership Description | next `<p>` sibling of above | "100+ lab tests, results tracked..." |

These selectors match the server-rendered HTML. If the checkout app changes its markup, the selectors will need updating.

---

## Updating Data

```bash
python3 app/scripts/extract_personalization_data.py
```

Then paste the new `gtm_personalization_variable.js` into the GTM variable.

---

## Files Reference

| File | Purpose |
|------|---------|
| `app/scripts/extract_personalization_data.py` | Extracts data from Webflow CMS |
| `app/data/personalization_data.json` | Raw JSON (99 pages) |
| `app/data/gtm_personalization_variable.js` | Ready-to-paste GTM variable |
| `app/gtm/register_personalization_tag.html` | GTM Custom HTML tag for /checkout |
| `app/gtm/landing_page_link_rewriter.html` | GTM Custom HTML tag for landing pages |
| `app/gtm/checkout_personalization.js` | Standalone script (no GTM dependency) |
| `app/gtm/GTM_SETUP.md` | This file |
