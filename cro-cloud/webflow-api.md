# Webflow API Reference

## Credentials

- **API Key location**: `app/scripts/add_biomarkers_to_landing_pages.py` (line ~10)
- **Base URL**: `https://api.webflow.com/v2`
- **Auth header**: `Authorization: Bearer {API_KEY}`
- **Rate limit**: ~120 requests/minute (use 0.3-0.5s between calls)

## Collection IDs

| Collection | ID | Purpose |
|-----------|-----|---------|
| Landing Pages | `6981a714e199bac70776d880` | SEM landing pages (`/welcome-cms/{slug}`) |
| SEM FAQs | `6981cbbfb6102bfdf7d05094` | FAQ items linked to landing pages |
| Biomarkers | `662de62e7a966fa325943816` | Biomarker reference pages |

## Site ID

`63792ff4f3d6aa3d62071b61`

## General FAQ IDs (include on every page)

- `6981d6b8f3e7405ce95132ed` - How does Superpower testing work?
- `6981d6ba10e873663bd8c9ed` - How accurate are the results?

## API Patterns

### Fetch All Items (Paginated)

The collection has 100+ items. Max 100 per request. Must loop with offset.

```python
import requests

API_KEY = "your_api_key"
COLLECTION_ID = "6981a714e199bac70776d880"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "accept": "application/json",
    "content-type": "application/json"
}

all_items = []
offset = 0
while True:
    url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items?limit=100&offset={offset}"
    resp = requests.get(url, headers=headers)
    items = resp.json().get('items', [])
    if not items:
        break
    all_items.extend(items)
    offset += 100
    if len(items) < 100:
        break
```

### Create Item

```python
payload = {"fieldData": {
    "name": "Page Name",
    "slug": "page-slug",
    "hero-headline": "Your Headline Here",
    # ... all fields
}}
resp = requests.post(
    f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items",
    headers=headers, json=payload)
item_id = resp.json()['id']
```

### Update Item

```python
resp = requests.patch(
    f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/{item_id}",
    headers=headers,
    json={"fieldData": {"hero-headline": "New Headline"}})
```

### Publish (CRITICAL - Always Do This)

Items are **DRAFTS by default**. You MUST publish after create or update.

```python
resp = requests.post(
    f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/publish",
    headers=headers,
    json={"itemIds": [item_id]})
```

Can publish up to 100 items per call. When creating multiple pages, collect IDs and batch publish at the end.

### Archive Items

```python
# Archive (draft change)
requests.patch(
    f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/{item_id}",
    headers=headers,
    json={"isArchived": True})

# MUST publish after archiving for it to take effect on the live site
requests.post(
    f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items/publish",
    headers=headers,
    json={"itemIds": [item_id]})
```

## Gotchas

### Batch Archive via `_live` Endpoint Fails

Using the `collections/{id}/items/live` endpoint for batch archive operations returns 409 "never been published" errors on some items, even if they show `lastPublished`. Use individual PATCH calls to the standard items endpoint instead.

### MCP `collections_items_update_items_live`

Works for content updates but is unreliable for batch archive operations. Use direct API calls for bulk archive.

### Always Publish After Archiving

Archiving via PATCH is a draft change. You must POST to `/items/publish` for the archive to take effect on the live site.

### Pagination

The collection previously had 780+ items (before cleanup). Always paginate with `limit=100&offset=N`. Never assume you'll get all items in one call.

### `card-price-monthly` Field

Store ONLY the dollar amount (e.g., "$17" or "$33"). The Webflow page template appends "/month" automatically. Putting "$17/month" causes the live page to display "$17/month/month".

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `app/scripts/add_biomarkers_to_landing_pages.py` | Contains the API key; adds biomarker data to pages |
| `app/scripts/fix_headline_lengths.py` | Batch-fix headline/subheadline lengths |
| `app/scripts/populate_sem_faqs.py` | Create FAQs by category |
| `app/scripts/link_faqs_to_pages.py` | Link existing FAQs to pages |
