# Runbook: Deploy GTM Update

## When to Use

After modifying the personalization data or tag HTML and needing to push changes to the live GTM container.

## Prerequisites

- OAuth token at `app/.gtm_token.json` (superpower@superpower.com)
- Python packages: `google-auth`, `google-auth-oauthlib`, `google-api-python-client`
- Updated source files (personalization data JSON, tag HTML)

## Steps

### 1. Edit source files

Depending on what changed:

- **Added/removed/edited slugs**: Edit `app/data/personalization_data.json`, then regenerate `app/gtm/register_personalization_tag.html`
- **Changed tag behavior**: Edit `app/gtm/register_personalization_tag.html` directly
- **Changed link rewriter**: Edit `app/gtm/landing_page_link_rewriter.html`

### 2. Validate tag size

```python
with open('app/gtm/register_personalization_tag.html') as f:
    size = len(f.read())
print(f"Size: {size:,} / 102,400 chars ({102400 - size:,} headroom)")
```

Must be under 102,400 chars.

### 3. Run deploy script

```bash
cd /Users/jeffy/superpower-sem-gap/app
python3 scripts/deploy_gtm_cleanup.py
```

The script will output progress:
```
=== GTM Cleanup Deploy ===
1. Authenticating...      OK
2. Finding container...   Found: accounts/6255639144/containers/198767392
3. Getting workspace...   Using: ...
4. Deleting all SP tags... Deleted N tags
5. Deleting biomarker trigger... Deleted N triggers
6. Finding triggers...    Register/checkout: ... (ID: 332)
                          Landing pages: ... (ID: 333)
7. Creating new tags...   Created: SP - Checkout Personalization
                          Created: SP - Landing Page Link Rewriter
8. Publishing...          Created version: NNN
                          Published version: NNN
```

### 4. Handle rate limits

If you see "Rate limited. Waiting Ns..." messages:

**Option A (recommended)**: Wait. The script retries with exponential backoff.

**Option B**: Cancel the script. Go to [tagmanager.google.com](https://tagmanager.google.com). The workspace changes are already saved. Manually:
1. Click "Submit" in the top right
2. Name the version
3. Click "Publish"

### 5. Verify in GTM Preview

1. Go to [tagmanager.google.com](https://tagmanager.google.com)
2. Click "Preview" for container `GTM-PBS5NFXN`
3. Enter URL: `https://superpower.com/checkout/membership?sp_variant=cholesterol-test`
4. Verify the `SP - Checkout Personalization` tag fires
5. Check that DOM changes appear correctly

### 6. Verify on live site

Wait 2 minutes for GTM propagation, then visit in incognito:

```
https://superpower.com/checkout/membership?sp_variant=cholesterol-test
```

Check:
- [ ] Headline personalized
- [ ] Testimonial card injected
- [ ] Benefits list shows condition-specific items
- [ ] No console errors

### 7. Commit changes

```bash
cd /Users/jeffy/superpower-sem-gap/app
git add data/personalization_data.json gtm/register_personalization_tag.html
git commit -m "Update GTM personalization (vNNN, N slugs)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push
```

## Troubleshooting

### Token expired

If authentication fails, delete `app/.gtm_token.json` and run again. The script will open a browser for re-authentication.

### Container not found

Verify the public ID `GTM-PBS5NFXN` is correct. The script searches all accounts/containers.

### Tag too large

Split into 2 tags. Sort slugs alphabetically, split in half, create 2 tag HTML files, update the deploy script to create 2 tags instead of 1.

### Trigger not found

The script looks for triggers by name pattern. If someone renamed triggers in the GTM UI, update the name patterns in `deploy_gtm_cleanup.py`.
