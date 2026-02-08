# Content Standards for CRO

Content rules that apply to checkout personalization copy. These mirror the LP content standards but are specific to the 12 personalization fields.

## Non-Negotiable Rules

1. **NEVER use em-dashes** - use " - " (space-dash-space) instead
2. **No emojis** anywhere in any content
3. **CTA is always "Start Testing"** - never change the `ctaText` field
4. **Testimonials must include specific biomarker numbers** (e.g., "ferritin was 12", "ApoB was 130")
5. **Benefits must be SHORT** - under 10 words each
6. **At-home phlebotomist ($99)**: Only mention if slug contains "home" or "at-home"

## Pricing Reference

| Market | Annual Price | Monthly | Biomarkers | card-price-monthly |
|--------|:-----------:|:-------:|:----------:|:------------------:|
| National | $199/year | $17/mo | 100+ | "$17" |
| NY/NJ | $399/year | $33/mo | 90+ | "$33" |

- Results time: ~10 days / "about 10 days" (NEVER "5 days")
- `card-price-monthly` stores ONLY the dollar amount - template adds "/month"

## Headline Patterns (Ogilvy Style)

### What Works

- **Challenge assumptions**: "Your Doctor Tests 1 Thyroid Marker. We Test All 7."
- **Startling stats**: "88 Million Americans Have Prediabetes. 84% Don't Know It."
- **Hidden problems**: "Hemoglobin Normal. Ferritin Is 8."
- **Contrast with standard care**: "Your Annual Physical Checks 8 Things. We Check 100+."
- **Pain point questions**: "Exhausted by 2pm Every Day?"

### What Doesn't Work

- Generic statements: "Test Your Cholesterol" (boring, no hook)
- Too long: anything over 45 characters for LP headlines
- Feature lists: listing biomarker names without a narrative

## Testimonial Rules

### Required Structure

1. The specific finding (with numbers): "My fasting insulin was 22"
2. What it explained or revealed: "I was insulin resistant for years while my glucose looked 'normal'"
3. The outcome or resolution: "Diet changes got it down to 6 in 5 months"

### Good Examples

- "My ferritin was 12 - technically 'normal' but functionally deficient. Hair was falling out, couldn't exercise. Got it to 70 and felt like a different person."
- "TSH was 3.8 - 'normal.' Felt terrible. Full panel showed low Free T3 and antibodies at 500+. Hashimoto's for years while doctors said TSH was fine."

### Bad Examples

- "Testing helped me understand my health better." (vague, no numbers)
- "I feel so much better now." (no specifics)

### Critical: Use Exact CMS Quotes

When pulling testimonials from CMS landing pages, use the exact quote. Do NOT paraphrase or shorten testimonials - the specific numbers and wording are what make them credible.

## Membership Benefits Pattern

| Benefit | Pattern | Example |
|---------|---------|---------|
| `benefit1` | Main health outcome (condition-specific) | "Track insulin and glucose trends over time" |
| `benefit2` | Breadth of testing | "100+ biomarkers including full metabolic panel" |
| `benefit3` | AI/tech advantage (brief) | "AI flags early insulin resistance patterns" |
| `benefit4` | Human support | "24/7 care team access" |

**BAD**: "Complete liver panel (ALT, AST, ALP) and kidney markers (BUN, creatinine, eGFR) included" (too long, too technical)

**GOOD**: "Catch liver and kidney problems early" (short, benefit-focused)

## Competitor Page Tone

For competitor comparison pages (e.g., `function-health-review`):

- **Position, don't attack**: Lead with Superpower's value proposition
- **Let testimonials do the comparison work**: "Was on the Function Health waitlist for months. Superpower - no waitlist, $199/year."
- **Be factual about differences**: "$199 vs $365" is fine. "Function Health is a ripoff" is not.
- **Don't assume the visitor knows the competitor well**: Sell the category first, then differentiate.

### NY/NJ Competitor Pages

Function Health costs up to $613/year in NY/NJ ($365 membership + up to $248 Quest lab fees). Superpower is $399 all-in. Lead with "Finally Affordable" positioning, not "they charge hidden fees."

## Style Quick Reference

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Dashes | " - " | em-dash or "--" |
| Biomarkers (national) | "100+" | "90+" |
| Biomarkers (NY/NJ) | "90+" | "100+" |
| Results | "~10 days" | "5 days" |
| CTA | "Start Testing" | "Get Started" |
| Testimonial names | "Diane K." | "Diane" or "D.K." |
| Emojis | Never | Never |
| CTA arrows (LP only) | "->" | unicode arrows |
