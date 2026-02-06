#!/usr/bin/env python3
"""Unpublish 57 Tier 3 biomarker-test pages - acute/emergency/inappropriate conditions.
These pages have embarrassing template content and hurt brand credibility."""
import requests
import time
import json

API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
LP_COLLECTION = "6981a714e199bac70776d880"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Tier 3: Pages to unpublish
TIER3_SLUGS = [
    # Acute/Emergency conditions
    "sepsis-biomarker-test",
    "sirs-biomarker-test",
    "dic-biomarker-test",
    "diabetic-ketoacidosis-biomarker-test",
    "acute-blood-loss-biomarker-test",
    "gi-bleed-biomarker-test",
    "myocardial-infarction-biomarker-test",
    "acute-kidney-injury-biomarker-test",
    "acute-stress-biomarker-test",
    # Cancers - misleading for consumer wellness test
    "leukemia-biomarker-test",
    "lung-cancer-biomarker-test",
    "liver-cancer-biomarker-test",
    "ovarian-cancer-biomarker-test",
    "pancreatic-cancer-biomarker-test",
    "testicular-cancer-biomarker-test",
    # "thyroid-cancer-biomarker-test",  # NOT in the CMS - not in the 110
    "multiple-myeloma-biomarker-test",
    # Rare/Specialized - negligible search volume
    "acromegaly-biomarker-test",
    "kawasaki-disease-biomarker-test",
    "gh-deficiency-biomarker-test",
    "mgus-biomarker-test",
    "polycythemia-vera-biomarker-test",
    "basophilia-biomarker-test",
    "eosinophilia-biomarker-test",
    "lymphopenia-biomarker-test",
    "neutropenia-biomarker-test",
    "thrombocytopenia-biomarker-test",
    "thrombocytosis-biomarker-test",
    "homocystinuria-biomarker-test",
    "siadh-biomarker-test",
    # Pediatric/Hospital
    "covid-19-severe-biomarker-test",
    # Electrolyte disorders - lab findings not consumer search terms
    "hyperkalemia-biomarker-test",
    "hypokalemia-biomarker-test",
    "hypernatremia-biomarker-test",
    "hyponatremia-biomarker-test",
    "hypercalcemia-biomarker-test",
    "hypocalcemia-biomarker-test",
    # Too tenuous connection to blood testing
    "alzheimers-disease-biomarker-test",
    "dementia-vascular-biomarker-test",
    "stroke-biomarker-test",
    "asthma-biomarker-test",
    "copd-biomarker-test",
    "allergic-rhinitis-biomarker-test",
    "atopic-dermatitis-biomarker-test",
    "peptic-ulcer-disease-biomarker-test",
    "gallstones-biomarker-test",
    "anorexia-nervosa-biomarker-test",
    "sarcopenia-biomarker-test",
    "smoking-related-inflammation-biomarker-test",
    "cancer-associated-inflammation-biomarker-test",
    "dehydration-biomarker-test",
    "malnutrition-biomarker-test",
    "hiv-aids-advanced-biomarker-test",
    "hemolytic-anemia-biomarker-test",
    "nephrotic-syndrome-biomarker-test",
    "thrombophilia-biomarker-test",
    # Duplicate
    "chronic-infection-hep-b-c-hiv-tb-biomarker-test",
]

print(f"Tier 3 slugs to unpublish: {len(TIER3_SLUGS)}")


def fetch_all_pages():
    all_items = []
    offset = 0
    while True:
        url = f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items?limit=100&offset={offset}"
        resp = requests.get(url, headers=HEADERS)
        data = resp.json()
        items = data.get("items", [])
        all_items.extend(items)
        total = data.get("pagination", {}).get("total", 0)
        if offset + 100 >= total:
            break
        offset += 100
        time.sleep(0.3)
    return all_items


def unpublish_items(item_ids):
    """Unpublish by setting isDraft to true via live endpoint removal.
    Webflow v2: We need to use the 'unpublish' approach -
    actually there's no direct unpublish endpoint in v2.
    We'll archive the items instead which removes them from the live site."""
    # Actually, Webflow v2 doesn't have a direct unpublish.
    # Options: 1) Archive items, 2) Set to draft
    # Let's archive them - this removes from live site
    results = []
    for item_id in item_ids:
        url = f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items/{item_id}"
        # Set isDraft = true and isArchived = true
        resp = requests.patch(url, headers=HEADERS, json={
            "isDraft": True,
            "isArchived": True
        })
        if resp.status_code == 200:
            results.append(item_id)
        else:
            print(f"  ERROR archiving {item_id}: {resp.status_code} {resp.text[:200]}")
        time.sleep(0.35)

    # Now publish the collection to reflect the archival on the live site
    # We need to publish remaining items to push the removal live
    if results:
        # Publish in batches of 100
        for i in range(0, len(results), 100):
            batch = results[i:i+100]
            url = f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items/publish"
            resp = requests.post(url, headers=HEADERS, json={"itemIds": batch})
            if resp.status_code not in (200, 202):
                print(f"  Publish response: {resp.status_code} {resp.text[:200]}")
            time.sleep(1)

    return results


def main():
    print("=" * 70)
    print("UNPUBLISH TIER 3 BIOMARKER-TEST PAGES")
    print("=" * 70)

    print("\nFetching all pages from Webflow...")
    all_items = fetch_all_pages()
    slug_map = {}
    for item in all_items:
        slug = item.get("fieldData", {}).get("slug", "")
        if slug:
            slug_map[slug] = item

    print(f"Total items: {len(slug_map)}")

    # Find tier 3 items
    tier3_items = []
    missing = []
    already_archived = []
    for slug in TIER3_SLUGS:
        if slug in slug_map:
            item = slug_map[slug]
            if item.get("isArchived"):
                already_archived.append(slug)
            else:
                tier3_items.append((slug, item["id"]))
        else:
            missing.append(slug)

    print(f"\nTier 3 pages found: {len(tier3_items)}")
    if missing:
        print(f"Not found in CMS: {len(missing)}")
        for s in missing:
            print(f"  - {s}")
    if already_archived:
        print(f"Already archived: {len(already_archived)}")
        for s in already_archived:
            print(f"  - {s}")

    # Archive them
    print(f"\nArchiving {len(tier3_items)} pages...")
    archived_ids = []
    for slug, item_id in tier3_items:
        url = f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items/{item_id}"
        resp = requests.patch(url, headers=HEADERS, json={
            "isDraft": True,
            "isArchived": True
        })
        if resp.status_code == 200:
            archived_ids.append(item_id)
            print(f"  ARCHIVED: {slug}")
        else:
            print(f"  ERROR: {slug} - {resp.status_code} {resp.text[:200]}")
        time.sleep(0.35)

    # Publish to push changes live
    if archived_ids:
        print(f"\nPublishing archived state for {len(archived_ids)} items...")
        for i in range(0, len(archived_ids), 100):
            batch = archived_ids[i:i+100]
            url = f"https://api.webflow.com/v2/collections/{LP_COLLECTION}/items/publish"
            resp = requests.post(url, headers=HEADERS, json={"itemIds": batch})
            print(f"  Batch publish: {resp.status_code}")
            time.sleep(1)

    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"Pages targeted: {len(TIER3_SLUGS)}")
    print(f"Pages archived: {len(archived_ids)}")
    print(f"Pages not found: {len(missing)}")
    print(f"Already archived: {len(already_archived)}")

    # Save log
    log = {
        "action": "unpublish_tier3",
        "archived_count": len(archived_ids),
        "archived_slugs": [s for s, _ in tier3_items if _ in [item_id for item_id in archived_ids]],
        "missing": missing,
        "already_archived": already_archived,
    }
    log_path = "/Users/jeffy/superpower-sem-gap/app/data/tier3_unpublish_log.json"
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)
    print(f"\nLog saved to: {log_path}")


if __name__ == "__main__":
    main()
