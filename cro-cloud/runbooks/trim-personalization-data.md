# Runbook: Trim Personalization Data to Active Slugs

## When to Use

When slugs in `personalization_data.json` no longer have active Google Ads pointing to them. Dead weight in the tag increases JS payload on every checkout page load.

## Steps

### 1. Get active slug list from Google Ads

Ask SEM Claude for the current list of active ad slugs, or query Google Ads API directly:

```python
# Query pattern: get all ad groups with enabled ads pointing to /welcome-cms/ URLs
# See app/scripts/slugfest.py for the working API client
```

The active slug list was last provided in `SEM_TO_CRO_GTM_CLEANUP.md` (110 slugs, Feb 8, 2026).

### 2. Filter `personalization_data.json`

```python
import json

with open('app/data/personalization_data.json') as f:
    data = json.load(f)

# Active slugs from SEM Claude
active_slugs = set([
    "adrenal", "alp-test", "alt-ast-test",
    # ... full list from SEM Claude's handoff doc
])

# Keep only active slugs
trimmed = {k: v for k, v in data.items() if k in active_slugs}

# Report
removed = set(data.keys()) - active_slugs
print(f"Before: {len(data)} slugs")
print(f"After: {len(trimmed)} slugs")
print(f"Removed: {len(removed)} slugs")
if removed:
    print(f"Removed slugs: {sorted(removed)}")

# Write
with open('app/data/personalization_data.json', 'w') as f:
    json.dump(trimmed, f, indent=2, ensure_ascii=False)
```

### 3. Regenerate the GTM tag HTML

After trimming the JSON, regenerate `app/gtm/register_personalization_tag.html` with the smaller dataset.

### 4. Verify tag size

```python
with open('app/gtm/register_personalization_tag.html') as f:
    size = len(f.read())
print(f"Tag size: {size:,} chars (limit: 102,400)")
```

A significant trim may allow consolidating from 2 tags to 1 tag. The Feb 8 cleanup went from 235 slugs (2 tags, ~196K) to 111 slugs (1 tag, ~93K) - a 77% reduction.

### 5. Deploy

```bash
cd /Users/jeffy/superpower-sem-gap/app
python3 scripts/deploy_gtm_cleanup.py
```

### 6. Verify removed slugs fall back gracefully

Visit checkout with a removed slug:

```
https://superpower.com/checkout/membership?sp_variant=removed-slug-name
```

Expected behavior: the default (non-personalized) checkout page appears. No errors. The tag simply doesn't find the slug in its data and exits early.

### 7. Verify retained slugs still work

```
https://superpower.com/checkout/membership?sp_variant=cholesterol-test
```

### 8. Commit and push

```bash
cd /Users/jeffy/superpower-sem-gap/app
git add data/personalization_data.json gtm/register_personalization_tag.html
git commit -m "Trim personalization data to N active slugs (removed M inactive)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push
```

### 9. Update documentation

- Update `SEM_CLAUDE_CRO_STATUS.md` with new slug count
- Update MEMORY.md with new slug count and headroom
- Note the trim in a handoff doc if SEM Claude requested it

## Impact

Fewer slugs = smaller tag = faster checkout page loads for every visitor.

| Metric | Before (Feb 7) | After Trim (Feb 8) |
|--------|:-:|:-:|
| Slugs | 235 (2 tags) | 111 (1 tag) |
| Tag payload | ~392K chars | ~93K chars |
| Reduction | - | 77% |
