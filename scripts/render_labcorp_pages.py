"""Render pre-baked HTML into page-html field for all Labcorp CMS items.

Reads the body HTML template, substitutes {{wf}} bindings with actual field
values, applies NY/NJ pricing, bakes sp_variant into CTAs, applies CRO
overrides, and PATCHes each item's page-html field via Webflow API.

Usage:
    python render_labcorp_pages.py                  # render + push all
    python render_labcorp_pages.py --dry-run        # preview 2 items, no API writes
    python render_labcorp_pages.py --dry-run --all  # preview all, no API writes
    python render_labcorp_pages.py --item ITEM_ID   # render + push one item
    python render_labcorp_pages.py --limit 10       # render + push first 10 items
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

# ── Config ──────────────────────────────────────────────────────────────
API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
COLLECTION_ID = "69700aae8c29deccea244c21"
SITE_ID = "63792ff4f3d6aa3d62071b61"
BASE_URL = "https://api.webflow.com/v2"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "labcorp-webflow-embed-body.html")
OVERRIDES_PATH = os.path.join(SCRIPT_DIR, "..", "data", "labcorp_overrides.json")

NYNJ_STATES = {"NY", "NJ"}

# National vs NY/NJ pricing
PRICING = {
    "national": {
        "annual": "$199",
        "monthly": "$17",
        "tests": "100+",
        "biomarkers": "100+",
        "annual_number": "199",
        "daily": "55 cents",
    },
    "nynj": {
        "annual": "$399",
        "monthly": "$33",
        "tests": "90+",
        "biomarkers": "90+",
        "annual_number": "399",
        "daily": "$1.09",
    },
}


# ── Webflow API helpers ─────────────────────────────────────────────────
def api_request(url, method="GET", body=None, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, method=method)
            req.add_header("Authorization", f"Bearer {API_KEY}")
            req.add_header("Accept", "application/json")
            if body is not None:
                req.add_header("Content-Type", "application/json")
                req.data = json.dumps(body).encode()
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 10 * (attempt + 1)
                print(f"  Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                err_body = e.read().decode() if e.fp else ""
                if attempt == retries - 1:
                    print(f"  HTTP {e.code}: {err_body[:300]}")
                    raise
                time.sleep(2)
    return None


def fetch_all_items():
    """Fetch all items from the Labcorp collection."""
    all_items = []
    offset = 0
    limit = 100
    while True:
        url = f"{BASE_URL}/collections/{COLLECTION_ID}/items?limit={limit}&offset={offset}"
        data = api_request(url)
        items = data.get("items", [])
        all_items.extend(items)
        total = data.get("pagination", {}).get("total", 0)
        print(f"  Fetched {len(items)} at offset {offset} ({len(all_items)}/{total})")
        if offset + limit >= total:
            break
        offset += limit
        time.sleep(0.3)
    return all_items


def patch_page_html(item_id, rendered_html):
    """PATCH a single item's page-html field."""
    url = f"{BASE_URL}/collections/{COLLECTION_ID}/items/{item_id}"
    body = {"fieldData": {"page-html": rendered_html}}
    return api_request(url, method="PATCH", body=body)


def publish_items(item_ids):
    """Publish items in batches of 100."""
    url = f"{BASE_URL}/collections/{COLLECTION_ID}/items/publish"
    for i in range(0, len(item_ids), 100):
        batch = item_ids[i : i + 100]
        api_request(url, method="POST", body={"itemIds": batch})
        print(f"  Published batch {i // 100 + 1} ({len(batch)} items)")
        time.sleep(1)


# ── Template rendering ──────────────────────────────────────────────────
def load_template():
    with open(TEMPLATE_PATH, "r") as f:
        return f.read()


def load_overrides():
    path = os.path.normpath(OVERRIDES_PATH)
    if not os.path.exists(path):
        print(f"  No overrides file at {path}, using defaults only")
        return {}
    with open(path, "r") as f:
        return json.load(f)


def get_field(field_data, key, default=""):
    """Get a field value, handling nested image refs."""
    val = field_data.get(key, default)
    if val is None:
        return default
    # ImageRef fields come as {"url": "...", ...}
    if isinstance(val, dict) and "url" in val:
        return val["url"]
    return str(val)


def substitute_wf_bindings(template_html, field_data):
    """Replace all {{wf {"path":"xxx","type":"yyy"} }} with field values."""

    def replacer(match):
        inner = match.group(1)
        try:
            spec = json.loads(inner)
        except json.JSONDecodeError:
            return match.group(0)
        path = spec.get("path", "")
        return html.escape(get_field(field_data, path), quote=True)

    # Match {{wf {...} }}
    return re.sub(r'\{\{wf\s+(\{[^}]+\})\s*\}\}', replacer, template_html)


def apply_nynj_pricing(rendered_html, pricing):
    """Replace national pricing with NY/NJ pricing in already-rendered HTML."""
    nat = PRICING["national"]
    replacements = [
        (nat["annual"], pricing["annual"]),           # $199 -> $399
        (nat["tests"], pricing["tests"]),             # 100+ -> 90+
        (nat["monthly"], pricing["monthly"]),         # $17 -> $33
        (f'at ${nat["annual_number"]}', f'at ${pricing["annual_number"]}'),  # at $199 -> at $399
    ]
    for old, new in replacements:
        rendered_html = rendered_html.replace(old, new)
    return rendered_html


def bake_sp_variant(rendered_html, slug):
    """Replace sp_variant=labcorp with sp_variant={slug} in CTA hrefs."""
    return rendered_html.replace(
        "sp_variant=labcorp",
        f"sp_variant={slug}",
    )


def _replace_inner(pattern, new_inner, text):
    """Replace the inner content of an HTML element matched by pattern.

    Uses a lambda to avoid regex group-reference issues with $ in content.
    """
    def replacer(m):
        return m.group(1) + new_inner + m.group(3)
    return re.sub(pattern, replacer, text)


def apply_overrides(rendered_html, overrides, slug, is_nynj):
    """Apply CRO overrides to the rendered HTML."""
    # Build merged override dict: _default < _default_nynj < per-slug
    merged = {}
    default = overrides.get("_default", {})
    merged.update(default)
    if is_nynj:
        nynj_default = overrides.get("_default_nynj", {})
        merged.update(nynj_default)
    slug_override = overrides.get(slug, {})
    merged.update(slug_override)

    if not merged:
        return rendered_html

    # Apply overrides by element ID / known patterns
    if "ad_headline" in merged:
        hsa_tag = ' <span class="lc-hsa-tag" style="font-size: 11px; font-weight: 600; background: rgba(34,197,94,0.15); color: #4ade80; vertical-align: middle; margin-left: 4px;">HSA/FSA eligible</span>'
        new_inner = html.escape(merged["ad_headline"]) + hsa_tag
        rendered_html = _replace_inner(
            r'(<h2 id="ad-headline">)(.*?)(</h2>)', new_inner, rendered_html
        )
    if "ad_subheadline" in merged:
        rendered_html = _replace_inner(
            r'(<p id="ad-subheadline">)(.*?)(</p>)',
            html.escape(merged["ad_subheadline"]),
            rendered_html,
        )
    if "cta_headline" in merged:
        rendered_html = _replace_inner(
            r'(<h2 id="cta-headline">)(.*?)(</h2>)',
            html.escape(merged["cta_headline"]),
            rendered_html,
        )
    if "cta_subheadline" in merged:
        rendered_html = _replace_inner(
            r'(<p id="cta-subheadline">)(.*?)(</p>)',
            html.escape(merged["cta_subheadline"]),
            rendered_html,
        )
    if "testimonial_quote" in merged:
        rendered_html = _replace_inner(
            r'(<div class="lc-testimonial-quote">)(.*?)(</div>)',
            '"' + html.escape(merged["testimonial_quote"]) + '"',
            rendered_html,
        )
    if "testimonial_author" in merged:
        rendered_html = _replace_inner(
            r'(<div class="lc-testimonial-author">)(.*?)(</div>)',
            html.escape(merged["testimonial_author"]),
            rendered_html,
        )
    if "testimonial_result" in merged:
        rendered_html = _replace_inner(
            r'(<div class="lc-testimonial-result">)(.*?)(</div>)',
            html.escape(merged["testimonial_result"]),
            rendered_html,
        )

    return rendered_html


def strip_unnecessary_js(rendered_html):
    """Remove JS blocks that are no longer needed when HTML is pre-rendered.

    We keep:
    - Star rendering JS (still needs data-rating)
    - Sticky bar JS
    - Nearby locations JS (still fetches from GitHub)
    - FAQ toggle (inline onclick, no script block)

    We remove:
    - Headline variant switcher (?v=ogilvy) - overrides handle this now
    - sp_variant URL rewriter - baked into href at render time
    - NY/NJ pricing swap - baked in at render time
    """
    # Remove the variant switcher block
    rendered_html = re.sub(
        r'// Headline variant switcher.*?(?=// Rewrite CTA buttons|// NY/NJ pricing swap|// Dynamic nearby)',
        '',
        rendered_html,
        flags=re.DOTALL,
    )
    # Remove the sp_variant URL rewriter block
    rendered_html = re.sub(
        r'// Rewrite CTA buttons to use page slug.*?(?=// NY/NJ pricing swap|// Dynamic nearby)',
        '',
        rendered_html,
        flags=re.DOTALL,
    )
    # Remove the NY/NJ pricing swap block
    rendered_html = re.sub(
        r'// NY/NJ pricing swap.*?(?=// Dynamic nearby)',
        '',
        rendered_html,
        flags=re.DOTALL,
    )
    return rendered_html


def render_item(template_html, field_data, overrides, slug):
    """Render a single item's page-html from the template."""
    state = get_field(field_data, "state", "").strip().upper()
    is_nynj = state in NYNJ_STATES

    # 1. Substitute {{wf}} bindings
    rendered = substitute_wf_bindings(template_html, field_data)

    # 2. Apply NY/NJ pricing if needed
    if is_nynj:
        rendered = apply_nynj_pricing(rendered, PRICING["nynj"])

    # 3. Bake sp_variant into CTA hrefs
    rendered = bake_sp_variant(rendered, slug)

    # 4. Apply CRO overrides
    rendered = apply_overrides(rendered, overrides, slug, is_nynj)

    # 5. Strip JS that's no longer needed
    rendered = strip_unnecessary_js(rendered)

    # 6. Remove the hidden data div (no longer needed for client-side JS pricing swap)
    # Keep it - nearby locations JS still reads lat/lng from it
    # rendered = re.sub(r'<div id="lc-page-data".*?</div>', '', rendered)

    return rendered


# ── Main ────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Render Labcorp page-html fields")
    parser.add_argument("--dry-run", action="store_true", help="Preview without API writes")
    parser.add_argument("--all", action="store_true", help="With --dry-run, render all items (not just 2)")
    parser.add_argument("--item", type=str, help="Render a single item by ID")
    parser.add_argument("--limit", type=int, help="Render only first N items")
    parser.add_argument("--output-dir", type=str, help="Write rendered HTML files here (for inspection)")
    args = parser.parse_args()

    # Load template
    print(f"Loading template from {TEMPLATE_PATH}")
    template = load_template()

    # Load overrides
    overrides = load_overrides()
    override_slugs = [k for k in overrides if not k.startswith("_")]
    print(f"  Overrides: {len(override_slugs)} per-slug overrides loaded")

    # Fetch items
    print("Fetching all Labcorp items from Webflow...")
    items = fetch_all_items()
    print(f"  Total items: {len(items)}")

    # Filter to single item if requested
    if args.item:
        items = [i for i in items if i["id"] == args.item]
        if not items:
            print(f"Item {args.item} not found!")
            sys.exit(1)

    # In dry-run without --all, just do 2 samples (1 national, 1 NY/NJ)
    if args.dry_run and not args.all and not args.item:
        national_sample = None
        nynj_sample = None
        for item in items:
            fd = item.get("fieldData", {})
            state = fd.get("state", "").strip().upper()
            if state in NYNJ_STATES and nynj_sample is None:
                nynj_sample = item
            elif state not in NYNJ_STATES and national_sample is None:
                national_sample = item
            if national_sample and nynj_sample:
                break
        items = [x for x in [national_sample, nynj_sample] if x]
        print(f"  Dry-run: rendering {len(items)} sample items")

    if args.limit and not args.item:
        items = items[: args.limit]
        print(f"  Limited to {len(items)} items")

    # Create output dir if requested
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    # Render and push
    success = 0
    failed = 0
    start_time = time.time()
    patched_ids = []

    for i, item in enumerate(items):
        item_id = item["id"]
        fd = item.get("fieldData", {})
        slug = fd.get("slug", "unknown")
        name = fd.get("name", "Unknown")
        state = fd.get("state", "??")

        try:
            rendered = render_item(template, fd, overrides, slug)

            if args.output_dir:
                outpath = os.path.join(args.output_dir, f"{slug}.html")
                with open(outpath, "w") as f:
                    f.write(rendered)

            if args.dry_run:
                preview = rendered[:200].replace("\n", " ")
                print(f"  [{i+1}] {slug} ({state}) - {len(rendered)} chars - {preview}...")
            else:
                patch_page_html(item_id, rendered)
                patched_ids.append(item_id)
                success += 1
                if (i + 1) % 25 == 0 or (i + 1) == len(items):
                    elapsed = time.time() - start_time
                    rate = (i + 1) / elapsed * 60 if elapsed > 0 else 0
                    print(f"  [{i+1}/{len(items)}] {name} ({state}) - {rate:.0f}/min")
                time.sleep(1.2)  # ~50 req/min rate limit

        except Exception as e:
            failed += 1
            print(f"  FAILED [{i+1}] {slug}: {e}")

    elapsed = time.time() - start_time

    if args.dry_run:
        print(f"\nDry run complete. {len(items)} items rendered in {elapsed:.1f}s")
        if args.output_dir:
            print(f"  HTML files written to {args.output_dir}/")
    else:
        print(f"\nPatched {success} items in {elapsed/60:.1f} minutes ({failed} failed)")

        # Publish all patched items
        if patched_ids:
            print(f"Publishing {len(patched_ids)} items...")
            publish_items(patched_ids)
            print("Done!")


if __name__ == "__main__":
    main()
