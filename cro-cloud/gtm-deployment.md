# GTM Deployment Procedures

## Authentication

- **OAuth2 Desktop flow** via Google APIs
- **Client secret file**: `/Users/jeffy/Downloads/client_secret_2_435686878764-dq7jpfr5ph19sugf962l4bd842gpuk8r.apps.googleusercontent.com (2).json`
- **Token file**: `app/.gtm_token.json`
- **Account**: `superpower@superpower.com`
- **Scopes**: `tagmanager.edit.containers`, `tagmanager.edit.containerversions`, `tagmanager.publish`, `tagmanager.manage.accounts`

## Container Details

| Item | Value |
|------|-------|
| Account ID | `6255639144` |
| Container ID | `198767392` |
| Container path | `accounts/6255639144/containers/198767392` |
| Public ID | `GTM-PBS5NFXN` |

## Deploy Script: `deploy_gtm_cleanup.py`

Located at `app/scripts/deploy_gtm_cleanup.py`. This is the primary deployment tool.

### What It Does

1. Authenticates via OAuth2 (reads/refreshes `app/.gtm_token.json`)
2. Finds the GTM container by public ID (`GTM-PBS5NFXN`)
3. Gets the Default Workspace
4. Deletes ALL existing `SP -` prefixed tags
5. Deletes the Biomarker Pages trigger (keeps trigger 332 and 333)
6. Creates 1 new `SP - Checkout Personalization` tag (reads from `app/gtm/register_personalization_tag.html`)
7. Creates 1 new `SP - Landing Page Link Rewriter` tag (reads from `app/gtm/landing_page_link_rewriter.html`)
8. Creates a new container version and publishes it

### Running the Deploy

```bash
cd /Users/jeffy/superpower-sem-gap/app
python3 scripts/deploy_gtm_cleanup.py
```

**Python dependencies**: `google-auth`, `google-auth-oauthlib`, `google-api-python-client`

## Rate Limiting

The GTM API `create_version` endpoint has aggressive rate limiting:

- **Limit**: ~3-5 version creates per hour
- **Error**: HTTP 429 (Too Many Requests)
- **The deploy script handles this** with exponential backoff: up to 8 retries, starting at 120s and increasing by 120s per retry

If you get rate limited and can't wait:
1. Use the GTM web UI (tagmanager.google.com) to publish manually
2. The workspace changes are already saved - just create a version and publish

## Version History

| Version | Date | Description |
|:---:|------|-------------|
| v207 | Feb 8 | GTM Cleanup: 4 tags -> 1 tag, 463 -> 111 slugs, ~392K -> ~93K chars |
| v208 | Feb 8 | Added welcome-ny slug |
| v209 | Feb 8 | welcome-ny content updates |
| v210 | Feb 8 | welcome-ny finalized |
| v206 | Feb 7 | 235 slugs (208 national + 27 NY/NJ), 2 tags |
| v205 | Feb 7 | Added 2 audit slugs (208 total) |
| v204 | Feb 7 | At-home pricing updates ($99 phlebotomist) |
| v196-v203 | Earlier | Expansion batches (see CRO_CLAUDE_README.md for full history) |

## GTM Template Gotchas

### Python `{{` in templates

When generating tag HTML with Python string formatting, `{{` in the template must resolve to a literal `{` in the output. Use plain strings and avoid `.format()` or f-strings on the template itself. This has caused bugs where personalization data JSON was malformed.

### Unicode escapes vs literal characters

Ensure testimonial quotes and special characters are stored as literal UTF-8 in the JSON data, not as unicode escape sequences. GTM tags execute as inline JavaScript - escaped unicode can cause rendering issues in the DOM.

### Tag size validation

Always check tag HTML size before deploying:

```python
with open(tag_path) as f:
    content = f.read()
if len(content) > 102400:
    print(f"ERROR: {len(content)} chars exceeds 102,400 limit!")
    sys.exit(1)
```

The deploy script does this check automatically.

## Files Reference

| File | Purpose |
|------|---------|
| `app/scripts/deploy_gtm_cleanup.py` | Primary deploy script (delete old tags, create new, publish) |
| `app/scripts/setup_gtm_personalization.py` | Legacy deploy script (2-tag architecture) |
| `app/gtm/register_personalization_tag.html` | Single personalization tag HTML (~93K) |
| `app/gtm/landing_page_link_rewriter.html` | Link rewriter tag HTML |
| `app/data/personalization_data.json` | 111 slug entries (source data) |
| `app/.gtm_token.json` | OAuth token (superpower@superpower.com) |
