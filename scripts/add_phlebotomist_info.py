#!/usr/bin/env python3
"""
Update at-home testing pages to mention the optional $99 phlebotomist add-on.
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

# Pages that specifically focus on at-home testing (from slug)
AT_HOME_SLUGS = [
    "cortisol-test-at-home",
    "thyroid-test-at-home",
    "testosterone-test-at-home",
    "blood-test-online",
]

# Custom FAQ about at-home testing with phlebotomist option
PHLEBOTOMIST_FAQ = {
    "question": "How does at-home testing work?",
    "answer": "<p>You have two options: Use our simple finger-prick collection kit to collect your sample yourself, or add a licensed phlebotomist to come to your home for just $99. Either way, your sample goes to the same CLIA-certified labs, and you get results in about 10 days.</p>"
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


def add_phlebotomist_mention(text, context="general"):
    """Add phlebotomist option to text about at-home testing."""
    if not text:
        return text, False

    original = text

    # Pattern: mentions finger-prick or at-home collection without phlebotomist option
    if "finger-prick" in text.lower() and "phlebotomist" not in text.lower():
        # Add phlebotomist option after finger-prick mention
        text = re.sub(
            r'(finger-prick collection kit|finger-prick kit|simple finger-prick)',
            r'\1 (or opt for a licensed phlebotomist to visit your home for $99)',
            text,
            flags=re.IGNORECASE,
            count=1
        )

    # Pattern: "collect a sample at home" type phrases
    if "collect" in text.lower() and "at home" in text.lower() and "phlebotomist" not in text.lower():
        text = re.sub(
            r'(collect[^.]*at home[^.]*\.)',
            r'\1 Or add a licensed phlebotomist to come to you for $99.',
            text,
            flags=re.IGNORECASE,
            count=1
        )

    return text, text != original


def main():
    print("Fetching landing pages...")
    items = fetch_landing_pages()
    print(f"Found {len(items)} landing pages\n")

    success_count = 0
    error_count = 0
    skipped_count = 0

    # Fields that might mention at-home collection
    fields_to_check = [
        "hero-subheadline",
        "faq-1-answer", "faq-2-answer", "faq-3-answer", "faq-4-answer",
        "what-is-included",
        "how-it-works-1-subheading",
    ]

    for item in items:
        slug = item.get('fieldData', {}).get('slug', '') or ''
        item_id = item.get('id', '')
        field_data = item.get('fieldData', {})

        # Check if this page mentions at-home testing
        all_text = ' '.join([str(field_data.get(f, '') or '') for f in fields_to_check])
        hero = field_data.get('hero-subheadline', '') or ''
        secondary_kws = field_data.get('secondary-keywords', '') or ''

        is_at_home_page = (
            'at-home' in slug or
            'online' in slug or
            'at home' in all_text.lower() or
            'at-home' in all_text.lower() or
            'at home' in secondary_kws.lower() or
            'at-home' in secondary_kws.lower() or
            'finger-prick' in all_text.lower()
        )

        if not is_at_home_page:
            continue

        updates = {}
        changes_made = []

        # Check and update relevant fields
        for field in fields_to_check:
            original_value = field_data.get(field, '') or ''
            if original_value and 'phlebotomist' not in original_value.lower():
                new_value, changed = add_phlebotomist_mention(original_value)
                if changed:
                    updates[field] = new_value
                    changes_made.append(field)

        # For pages with "at-home" in slug, update FAQ about at-home testing
        if slug in AT_HOME_SLUGS or 'at-home' in slug or 'online' in slug:
            # Check if any FAQ already mentions how at-home works
            has_at_home_faq = False
            for i in range(1, 5):
                q = field_data.get(f'faq-{i}-question', '') or ''
                a = field_data.get(f'faq-{i}-answer', '') or ''
                if 'at-home' in q.lower() or 'at home' in q.lower() or 'how does' in q.lower():
                    if 'phlebotomist' not in a.lower():
                        # Update this FAQ answer
                        updates[f'faq-{i}-answer'] = PHLEBOTOMIST_FAQ['answer']
                        changes_made.append(f'faq-{i}-answer (phlebotomist FAQ)')
                    has_at_home_faq = True
                    break

        if not updates:
            print(f"⏭️  {slug}: Already has phlebotomist info or no at-home mentions to update")
            skipped_count += 1
            continue

        # Update the landing page
        status, result = update_landing_page(item_id, updates)

        if status == 200:
            print(f"✅ {slug}: Updated ({', '.join(changes_made)})")
            success_count += 1
        else:
            print(f"❌ {slug}: Error - {result}")
            error_count += 1

        time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"Complete! Success: {success_count}, Errors: {error_count}, Skipped: {skipped_count}")


if __name__ == '__main__':
    main()
