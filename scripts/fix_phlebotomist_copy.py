#!/usr/bin/env python3
"""
Fix awkward phlebotomist copy and ensure clean messaging across all pages.
"""
import json
import requests
import time
import re

WEBFLOW_API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
LANDING_PAGES_COLLECTION = "6981a714e199bac70776d880"

HEADERS = {
    "Authorization": f"Bearer {WEBFLOW_API_KEY}",
    "Content-Type": "application/json"
}


def fetch_landing_pages():
    """Fetch all landing page items from Webflow."""
    url = f"https://api.webflow.com/v2/collections/{LANDING_PAGES_COLLECTION}/items?limit=100"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data.get('items', [])


def update_landing_page(item_id, updates):
    """Update a landing page with new field data."""
    url = f"https://api.webflow.com/v2/collections/{LANDING_PAGES_COLLECTION}/items/{item_id}"
    payload = {"fieldData": updates}
    response = requests.patch(url, headers=HEADERS, json=payload)
    return response.status_code, response.json()


def fix_phlebotomist_copy(text):
    """Fix awkward phlebotomist copy patterns."""
    if not text:
        return text, False

    original = text

    # Fix: "finger-prick (or opt for a licensed phlebotomist to visit your home for $99) kit"
    # Should be: "finger-prick kit, or add a licensed phlebotomist visit for $99"
    text = re.sub(
        r'finger-prick \(or opt for a licensed phlebotomist to visit your home for \$99\) (collection )?kit',
        'finger-prick kit—or add a licensed phlebotomist visit for $99',
        text,
        flags=re.IGNORECASE
    )

    # Fix: "Collect your sample at home and mail it back. Or add a licensed phlebotomist"
    # Clean up double sentences
    text = re.sub(
        r'Collect your sample at home and mail it back\. Or add',
        'Collect your sample at home with our finger-prick kit, or add',
        text,
        flags=re.IGNORECASE
    )

    # Fix any remaining awkward parenthetical insertions
    text = re.sub(
        r'\(or opt for a licensed phlebotomist to visit your home for \$99\)',
        '—or add a licensed phlebotomist visit for $99—',
        text,
        flags=re.IGNORECASE
    )

    return text, text != original


def main():
    print("Fetching landing pages...")
    items = fetch_landing_pages()
    print(f"Found {len(items)} landing pages\n")

    success_count = 0
    error_count = 0
    skipped_count = 0

    # Fields to check
    fields_to_check = [
        "hero-subheadline",
        "faq-1-answer", "faq-2-answer", "faq-3-answer", "faq-4-answer",
        "what-is-included",
    ]

    for item in items:
        slug = item.get('fieldData', {}).get('slug', '') or ''
        item_id = item.get('id', '')
        field_data = item.get('fieldData', {})

        updates = {}
        changes_made = []

        for field in fields_to_check:
            original_value = field_data.get(field, '') or ''
            if original_value and 'phlebotomist' in original_value.lower():
                new_value, changed = fix_phlebotomist_copy(original_value)
                if changed:
                    updates[field] = new_value
                    changes_made.append(field)

        if not updates:
            skipped_count += 1
            continue

        # Update the landing page
        status, result = update_landing_page(item_id, updates)

        if status == 200:
            print(f"✅ {slug}: Fixed ({', '.join(changes_made)})")
            success_count += 1
        else:
            print(f"❌ {slug}: Error - {result}")
            error_count += 1

        time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"Complete! Success: {success_count}, Errors: {error_count}, Skipped: {skipped_count}")


if __name__ == '__main__':
    main()
