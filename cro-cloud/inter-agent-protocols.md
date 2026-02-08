# Inter-Agent Protocols

How the three Claude agents (LP Claude, SEM Claude, CRO Claude) hand off work to each other.

## Handoff Flow

```
SEM Claude                    LP Claude                    CRO Claude
    |                             |                            |
    |-- SEM_TO_LP_HANDOFF_*.md -->|                            |
    |   (keywords, ad groups,     |                            |
    |    page requirements)       |                            |
    |                             |                            |
    |                             |-- LP_TO_CRO_*.md --------->|
    |                             |   (slugs, item IDs,        |
    |                             |    biomarkers, pricing)    |
    |                             |                            |
    |                             |-- LP_TO_SEM_*.md --------->|
    |                             |   (live URLs, keywords,    |
    |                             |    ad angle suggestions)   |
    |                             |                            |
    |<-- SEM_TO_CRO_*.md ---------|--------------------------- |
    |   (active slug audits,      |                            |
    |    GTM cleanup requests)    |                            |
    |                             |                            |
    |                             |         CRO status ------->|
    |                             |      SEM_CLAUDE_CRO_STATUS |
```

## Handoff Document Naming Convention

Format: `{FROM}_TO_{TO}_{TOPIC}.md`

All handoff documents live at the project root: `/Users/jeffy/superpower-sem-gap/`

### Examples

- `SEM_TO_LP_HANDOFF_DD_PAGES.md` - SEM Claude asks LP Claude to build Diagnostic-Discovery pages
- `LP_TO_CRO_NYNJ_COMPLETE.md` - LP Claude tells CRO Claude that NY/NJ pages are built
- `SEM_TO_CRO_GTM_CLEANUP.md` - SEM Claude requests GTM tag cleanup

## LP -> CRO Handoff Protocol

**When LP Claude finishes building pages:**

The handoff doc (`LP_TO_CRO_{batch}_COMPLETE.md`) must include:

1. **List of slugs** with Webflow item IDs
2. **Key biomarkers** and condition focus for each page
3. **Special notes**:
   - At-home pages: mention $99 phlebotomist pricing
   - NY/NJ pages: confirm $399/90+ pricing
   - Competitor pages: note comparison angle
4. **What CRO Claude needs to do**: Add entries to `personalization_data.json`, deploy to GTM

### CRO Claude's Response

After processing the handoff:

1. Add entries to `personalization_data.json`
2. Regenerate GTM tag HTML
3. Deploy to GTM via `deploy_gtm_cleanup.py`
4. Commit and push to git
5. Update `SEM_CLAUDE_CRO_STATUS.md` with new slug count and GTM version

## SEM -> CRO Handoff Protocol

**When SEM Claude needs GTM changes:**

Common requests:
- **Audit**: "Here's a list of active ad slugs - verify all have checkout personalization"
- **Cleanup**: "Remove inactive slugs from personalization data" (see `SEM_TO_CRO_GTM_CLEANUP.md`)
- **Add**: "These new pages need checkout personalization"

### The Active Slug Audit Pattern

SEM Claude provides a list of slugs with active Google Ads. CRO Claude cross-references against `personalization_data.json`:

```python
# Python pattern for audit
import json
active_slugs = set([...])  # from SEM Claude's list
with open('app/data/personalization_data.json') as f:
    data = json.load(f)
existing = set(data.keys())
missing = active_slugs - existing
extra = existing - active_slugs
```

## SEM -> LP Handoff Protocol

**When SEM Claude needs new landing pages:**

The handoff doc (`SEM_TO_LP_HANDOFF_{batch}.md`) includes:
- Keywords and ad groups that need pages
- Monthly search volumes
- Suggested slug names
- Condition focus and key biomarkers
- Ad spend data (priority indicator)

## LP -> SEM Handoff Protocol

**When LP Claude finishes building pages:**

The handoff doc (`LP_TO_SEM_{batch}_COMPLETE.md`) includes:
- List of slugs with live URLs
- Primary keywords for each
- Suggested ad angles/hooks from the copy
- Monthly search volumes

## Status Tracking

### `SEM_CLAUDE_CRO_STATUS.md`

CRO Claude maintains this file as a living status report for SEM Claude. It contains:
- Total personalized checkout slugs
- GTM container version
- Tag architecture details (number of tags, sizes, headroom)
- Coverage stats (national/NY-NJ)
- Batch history table
- Test URLs for verification
- Ad copy notes from CRO perspective (checkout messaging angles that should match ad copy)

## Historical Handoff Files

| File | From -> To | Content |
|------|-----------|---------|
| `CRO_HANDOFF_NEW_PAGES.md` | CRO -> SEM | 25 expansion pages |
| `LP_TO_CRO_DD_PAGES_COMPLETE.md` | LP -> CRO | 11 DD batch 1 |
| `LP_TO_CRO_DD_BATCH2_COMPLETE.md` | LP -> CRO | 6 DD batch 2 |
| `LP_TO_CRO_DD_FINAL_COMPLETE.md` | LP -> CRO | 3 DD final |
| `LP_TO_CRO_BLOOD_TEST_PAGES_COMPLETE.md` | LP -> CRO | 6 blood test intent |
| `LP_TO_CRO_ATHOME_PHLEBOTOMY_PRICING.md` | LP -> CRO | $99 pricing update for 9 at-home slugs |
| `LP_TO_CRO_NYNJ_COMPLETE.md` | LP -> CRO | 27 NY/NJ pages |
| `SEM_TO_CRO_ALL_SLUGS_NEEDING_CHECKOUT.md` | SEM -> CRO | 94-slug audit |
| `SEM_TO_CRO_GTM_CLEANUP.md` | SEM -> CRO | Trim to 110 active slugs, remove biomarker tags |
| `SEM_TO_LP_DELETION_HANDOFF.md` | SEM -> LP | Archive 613 unused CMS pages |
| `LP_TO_CRO_NYNJ_AUDIT_COMPLETE.md` | LP -> CRO | NY/NJ page audit results |
