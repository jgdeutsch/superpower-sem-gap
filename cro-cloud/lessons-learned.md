# Lessons Learned

Bugs, fixes, patterns that worked and failed across the CRO operation. Updated as new issues are encountered.

## GTM Bugs

### Python `{{` Template Bug

**Problem**: When using Python `.format()` or f-strings to generate GTM tag HTML, double braces `{{` in the JavaScript template get consumed by Python's string formatting, producing malformed output.

**Fix**: Use plain string concatenation or `str.replace()` to inject the personalization data JSON into the template. Never use `.format()` on a string that contains JavaScript object literals.

### Unicode Escapes vs Literal Characters

**Problem**: Testimonial quotes containing special characters (curly quotes, accented characters) were stored as unicode escape sequences (`\u2019` instead of `'`) in the JSON data. When baked into the GTM tag and rendered in the DOM, these caused display issues.

**Fix**: Store all text as literal UTF-8 characters in `personalization_data.json`. Use `json.dumps(data, ensure_ascii=False)` when serializing.

### GTM API Rate Limiting

**Problem**: The `create_version` endpoint on the GTM API has aggressive rate limiting - roughly 3-5 version creates per hour. The `deploy_gtm_cleanup.py` script hit this regularly during iterative development.

**Fix**: The deploy script includes exponential backoff (up to 8 retries starting at 120s). For immediate needs, use the GTM web UI to publish manually - workspace changes are saved even if the version creation was rate limited.

**Workaround**: The rate limit applies to version creation, not tag/trigger editing. You can make multiple workspace edits (create/delete tags) without hitting the limit. Only the final publish step is rate-limited.

## Webflow CMS Bugs

### card-price-monthly Double "/month"

**Problem**: 510 out of 780 CMS items had `$17/month` in the `card-price-monthly` field. The Webflow page template already appends "/month" after the field value, causing the live page to display "$17/month/month".

**Fix**: Batch-updated all 510 items to store just "$17" (national) or "$33" (NY/NJ). The template handles the "/month" suffix.

**Prevention**: When creating new pages, always store ONLY the dollar amount in `card-price-monthly`.

### Batch Archive 409 Errors

**Problem**: Using the Webflow `collections/{id}/items/live` endpoint for batch archive operations returned 409 "never been published" errors on some items, even if they showed a `lastPublished` date.

**Fix**: Use individual PATCH calls to the standard items endpoint (`/v2/collections/{id}/items/{item_id}`) with `{"isArchived": true}`, then batch publish to make the archive take effect.

### MCP Unreliable for Batch Archive

**Problem**: The Webflow MCP tool `collections_items_update_items_live` works for content updates but is unreliable for batch archive operations.

**Fix**: Use direct API calls (curl or requests library) for bulk archive operations.

## Content Mistakes

### Blind Cloning Kills Competitor Pages

**Problem**: The original `function-health-review-ny` was cloned from the national version and said "$399 vs $365 - lower price" which is factually wrong ($399 > $365). The testimonial said "I switched for the lower entry point" - also false at $399.

**Fix**: Always audit cloned competitor pages for pricing logic that reverses when you change the price. The NY/NJ version was completely rewritten with "Advanced Health Testing. Finally Affordable." positioning.

**Rule**: Never blindly clone competitor comparison pages. The value proposition changes when the price changes.

### "100+" Remnants in NY/NJ Body Copy

**Problem**: After cloning national pages to create NY/NJ variants, body copy fields (condition-overview, what-is-included, next-steps) often retained "100+" from the national version even though hero/stats/pricing fields were correctly set to "90+".

**Fix**: When creating NY/NJ clones, apply text replacements to ALL text fields - not just the obvious ones. Check condition-overview, what-is-included, next-steps, hero-subheadline, and how-it-works subheadings.

### Competitor Pages - Position, Don't Attack

**Problem**: Early competitor page copy directly attacked Function Health with "Function Health Costs $613+" headlines. Jeff preferred Ogilvy-style positioning.

**Fix**: Lead with Superpower's value prop ("Advanced Health Testing. Finally Affordable."). Let testimonials do the comparison work naturally. Don't assume the visitor knows the competitor well enough for an attack to resonate.

## Winning Patterns

### The Winning LP Formula

From Slugfest data analysis (Feb 8, 2026): `blood-panel-ny` converted at 66.7% registration rate with this formula:

1. **Contrast headline** that challenges what they have now ("Most 'Comprehensive' Panels Aren't.")
2. **Real pain points** as symptoms, not feature lists
3. **Specific testimonial** with 3-4 biomarker numbers and concrete outcomes
4. **Clear value multiplier** ("7x more markers than a standard panel")

Pages that listed features as symptoms (like `hormone-panel-ny` at 0% registration rate) failed.

### Message Match Drives Conversion

The checkout personalization system works because it maintains message continuity from ad -> landing page -> checkout. When the checkout headline, testimonial, and benefits match the condition the user searched for, conversion rates improve.

Key principle: the user should never feel like they've left the topic they searched for, even though checkout is a generic payment page.

## CMS Cleanup (Feb 8, 2026)

613 of 723 live CMS pages were archived because they had zero ad traffic. Categories removed:
- 170 individual biomarker test pages (calcium, sodium, etc.)
- 123 condition/disease pages
- 88 cancer biomarker test pages (BRCA, HER2, etc. - we don't offer these)
- 85 gut microbiome test pages (we don't offer stool testing)
- 59 environmental toxin test pages (we don't offer toxin testing)
- 21 informational/content pages
- 67 miscellaneous pages

~110 active-ad pages + ~57 pre-existing archives remain.

### Misleading Pages Fixed

7 national pages rewritten with honest disclaimers about what we actually test:
- `enlarged-heart` - we test cardiovascular lipid markers, not BNP/NT-proBNP or cardiac imaging
- `hepatitis-biomarker-test` - we test liver enzymes, not hepatitis-specific antibodies
- `kidney-infection-test` - we test kidney function, not infection-specific tests
- `gut-health-test` - we test blood markers related to gut health, not stool/microbiome
- `galleri-test-alternative` - we only offer PSA, not liquid biopsy cancer testing
- `cancer-screening` - we test PSA but not comprehensive cancer screening
- `continuous-glucose-monitor` - CGM is a separate device, not a blood panel

7 more pages fixed in a second wave (NY/NJ variants + `mthfr-test`, body composition pages).

## Biomarker Reference

### What We Actually Test

- **Baseline All States**: 105 biomarkers
- **Baseline NY/NJ**: 103 biomarkers
- **Advanced Add-On Men**: 24 markers
- **Advanced Add-On Women**: 23 markers
- **Specialty Panels**: Nutrients (8), Methylation (5), Cardiovascular (11), Metabolic (6), Female Fertility (12), Autoimmunity (9), OrganAge (11)

### What We Do NOT Test

Never create landing pages or personalization entries for:
- Environmental toxins / heavy metals
- Gut microbiome / stool testing
- Cancer genetic tests (BRCA, HER2, KRAS, etc.)
- Liquid biopsy / multi-cancer detection
- Urinalysis / urine culture
- Allergy / food sensitivity testing
- STD/STI testing
- Drug screening

Full panel CSV: `/Users/jeffy/Downloads/Panel Decomp - Biomarkers - EASY TO READ.csv`
