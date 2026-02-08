# Runbook: Add Checkout Personalization for a New Slug

## Prerequisites

- The landing page exists in Webflow CMS and is published
- You have the slug, condition focus, and key biomarkers

## Steps

### 1. Check if the slug already exists

```bash
grep '"your-slug"' /Users/jeffy/superpower-sem-gap/app/data/personalization_data.json
```

If it exists, you're done (or update it).

### 2. Add entry to `personalization_data.json`

Open `app/data/personalization_data.json` and add a new entry. Use `fatty-liver-test` as the gold standard reference for format and quality.

All 12 fields are required:

```json
{
  "your-slug": {
    "headline": "Screen for [Condition] and 1,000+ Conditions.",
    "ctaText": "Start Testing",
    "subtitleOverride": "100+ biomarkers in one blood draw. [Key markers]. Results in ~10 days.",
    "testimonialQuote": "[Specific story with biomarker numbers - 3+ specific values]",
    "testimonialName": "First L.",
    "testimonialResult": "[Concrete outcome with numbers]",
    "benefit1": "[Condition-specific, <10 words]",
    "benefit2": "100+ biomarkers including [relevant panel]",
    "benefit3": "AI [specific pattern detection]",
    "benefit4": "24/7 care team access",
    "stat1Number": "[Prevalence stat]",
    "stat1Text": "[Context for the stat]"
  }
}
```

**Content rules**:
- No em-dashes (use " - ")
- No emojis
- CTA always "Start Testing"
- Testimonial must have specific biomarker numbers
- Benefits under 10 words each
- If slug contains "home"/"at-home": mention $99 phlebotomist in subtitle
- If slug ends in `-ny`: use $399 and 90+ instead of $199 and 100+

### 3. Regenerate the GTM tag HTML

The tag HTML file at `app/gtm/register_personalization_tag.html` contains the baked-in JSON data. After editing `personalization_data.json`, you need to regenerate this file.

The generation process:
1. Read all entries from `personalization_data.json`
2. Compress the JSON (`json.dumps(data, separators=(',', ':'))`)
3. Embed it in the JavaScript template as the `DATA` variable
4. Write to `app/gtm/register_personalization_tag.html`

### 4. Check tag size

```python
with open('app/gtm/register_personalization_tag.html') as f:
    content = f.read()
print(f"Tag size: {len(content):,} chars")
print(f"Limit: 102,400 chars")
print(f"Headroom: {102400 - len(content):,} chars")
```

If the tag exceeds 102,400 chars, you need to split into 2 tags. See the 3-tag split instructions in `CRO_CLAUDE_README.md`.

### 5. Deploy to GTM

```bash
cd /Users/jeffy/superpower-sem-gap/app
python3 scripts/deploy_gtm_cleanup.py
```

This will:
- Delete all existing SP tags
- Create the new single personalization tag
- Recreate the link rewriter tag
- Publish a new container version

If rate limited (HTTP 429), the script will retry with exponential backoff. If you can't wait, publish manually via the GTM web UI.

### 6. Verify

Visit the checkout page with the new slug (use incognito, allow 2 min for GTM propagation):

```
https://superpower.com/checkout/membership?sp_variant=your-slug
```

Verify:
- [ ] Headline changed
- [ ] Subtitle changed
- [ ] CTA says "Start Testing"
- [ ] Benefits list shows 4 condition-specific items
- [ ] Testimonial card appears below the form with name and result
- [ ] No JavaScript errors in console

### 7. Commit and push

```bash
cd /Users/jeffy/superpower-sem-gap/app
git add data/personalization_data.json gtm/register_personalization_tag.html
git commit -m "Add checkout personalization for [slug] ([total] total slugs)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push
```

### 8. Update status

- Update `SEM_CLAUDE_CRO_STATUS.md` with new slug count and GTM version
- Update MEMORY.md with new GTM version and slug count
