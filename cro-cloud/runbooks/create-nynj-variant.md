# Runbook: Create NY/NJ Checkout Variant

## When to Use

When a national landing page needs a NY/NJ counterpart with $399/90+ pricing.

## NY/NJ Pricing Reference

| Field | National | NY/NJ |
|-------|:--------:|:-----:|
| Annual price | $199 | $399 |
| Monthly price | $17 | $33 |
| Biomarkers | 100+ | 90+ |
| card-price-monthly | "$17" | "$33" |
| card-price-annual | "Billed annually at $199" | "Billed annually at $399" |

## Steps

### 1. Find the national entry

```bash
grep -A 15 '"cholesterol-test"' /Users/jeffy/superpower-sem-gap/app/data/personalization_data.json
```

### 2. Clone and modify

The NY/NJ entry is a copy of the national entry with pricing and biomarker count swapped. Apply these replacements to ALL text fields:

| Find | Replace |
|------|---------|
| `$199/year` | `$399/year` |
| `$199/yr` | `$399/yr` |
| `$199` (in pricing context) | `$399` |
| `100+ biomarkers` | `90+ biomarkers` |
| `100+ other biomarkers` | `90+ other biomarkers` |
| `100+` (in biomarker context) | `90+` |

**Python pattern:**

```python
import json, copy

with open('app/data/personalization_data.json') as f:
    data = json.load(f)

national_slug = "cholesterol-test"
ny_slug = f"{national_slug}-ny"

# Clone
ny_entry = copy.deepcopy(data[national_slug])

# Swap pricing and biomarker count in all string fields
for key, value in ny_entry.items():
    if isinstance(value, str):
        value = value.replace('$199', '$399')
        value = value.replace('100+', '90+')
        ny_entry[key] = value

data[ny_slug] = ny_entry

with open('app/data/personalization_data.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

### 3. Manual review checklist

After cloning, manually review the NY/NJ entry:

- [ ] **All prices say $399** (check headline, subtitle, benefits, stat text)
- [ ] **All biomarker counts say 90+** (check subtitle, benefits - body copy often retains "100+" from cloning)
- [ ] **Testimonial makes sense at $399** (if it mentions price, update it)
- [ ] **Competitor comparisons are accurate** (if the national entry compares to Function Health at "$199 vs $365", the NY/NJ comparison should be "$399 vs $613+" with the hidden lab fees angle)
- [ ] **At-home pricing is correct** (if the page mentions phlebotomist: "$399/year membership + $99 at-home phlebotomist")

### 4. Special case: Competitor pages

Competitor comparison pages (e.g., `function-health-review-ny`) CANNOT be blindly cloned. The value proposition changes when the price changes:

- **National**: "$199 vs $365 - less than half the cost"
- **NY/NJ**: "$399 vs $613+ - $214 savings (Function Health charges $365 + up to $248 in hidden NY lab fees)"

The competitive angle shifts from "we're cheaper" to "we're all-in, they have hidden fees."

### 5. Regenerate tag HTML and deploy

```bash
cd /Users/jeffy/superpower-sem-gap/app
# Regenerate tag HTML from updated personalization_data.json
# Then deploy:
python3 scripts/deploy_gtm_cleanup.py
```

### 6. Verify

```
https://superpower.com/checkout/membership?sp_variant=cholesterol-test-ny
```

Check:
- [ ] Pricing shows $399, not $199
- [ ] Biomarker count shows 90+, not 100+
- [ ] Testimonial and benefits are condition-appropriate
- [ ] No remnant "100+" in any text

### 7. Commit and push

```bash
cd /Users/jeffy/superpower-sem-gap/app
git add data/personalization_data.json gtm/register_personalization_tag.html
git commit -m "Add NY/NJ checkout variant for [slug]-ny ($399/90+)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push
```

## Common Mistakes

1. **Forgetting body copy fields** - The clone-and-replace catches pricing in obvious places but misses `subtitleOverride` and `benefit2` text that says "100+ biomarkers including..."
2. **Competitor page logic inversion** - "$399 vs $365" makes Superpower MORE expensive, not less. The value prop for NY/NJ must emphasize Function Health's hidden $248 lab fees.
3. **Testimonial price references** - If the testimonial mentions "$199" or "less than half", update it for the $399 context.

## NY/NJ Quest Lab Locations

NY/NJ pages can mention "3,000+ Quest locations" for in-person testing. The at-home phlebotomist is still available as a $99 add-on.
