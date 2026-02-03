#!/usr/bin/env python3
"""
Update ALL pages with at-home testing FAQs to include phlebotomist option.
"""
import json
import requests
import time

WEBFLOW_API_KEY = "87be5982f1938a9143a7368af984a9863971dd55314fd5a60f482cc02425a0c7"
LANDING_PAGES_COLLECTION = "6981a714e199bac70776d880"

HEADERS = {
    "Authorization": f"Bearer {WEBFLOW_API_KEY}",
    "Content-Type": "application/json"
}

# Updated FAQ answers with phlebotomist option
# Maps FAQ question patterns to updated answers
FAQ_UPDATES = {
    # General at-home testing
    "how does at-home": "<p>You have two options: Use our simple finger-prick collection kit to collect your sample yourself, or add a licensed phlebotomist to come to your home for just $99. Either way, your sample goes to the same CLIA-certified labs, and you get results in about 10 days.</p>",

    "how do i order a blood test": "<p>Sign up for Superpower membership, and we'll ship a collection kit to your door. No doctor's visit required. Collect your sample at home with our finger-prick kit, or add a licensed phlebotomist visit for $99. Mail your sample back and get results in about 10 days.</p>",

    "how is the at-home": "<p>Using our simple finger-prick kit, you collect a small blood sample at home. Prefer a professional draw? Add a licensed phlebotomist visit for $99. Either way, mail it back and receive your results in about 10 days.</p>",

    "how does at-home thyroid": "<p>We send you a simple finger-prick collection kit. Prefer a professional blood draw? Add a licensed phlebotomist to come to your home for just $99. Collect your sample, mail it back in the prepaid envelope, and get results in about 10 days.</p>",

    "how does at-home cortisol": "<p>We send you a collection kit. Do a simple finger-prick at home, or add a licensed phlebotomist visit for $99 for a professional blood draw. Mail it back in the prepaid envelope, and get results in about 10 days.</p>",

    "how does at-home testosterone": "<p>We ship a collection kit to your door. Collect a finger-prick blood sample in the morning, or add a licensed phlebotomist visit for $99. Mail it back and get results in about 10 days.</p>",

    # Sample collection questions
    "how do i collect": "<p>You have two options: Use our simple finger-prick collection kit following the easy instructions, or add a licensed phlebotomist to come to your home for just $99 for a professional blood draw. Either method provides accurate results.</p>",
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


def main():
    print("Fetching landing pages...")
    items = fetch_landing_pages()
    print(f"Found {len(items)} landing pages\n")

    success_count = 0
    error_count = 0
    skipped_count = 0

    for item in items:
        slug = item.get('fieldData', {}).get('slug', '') or ''
        item_id = item.get('id', '')
        field_data = item.get('fieldData', {})

        updates = {}
        changes_made = []

        # Check all 4 FAQ questions
        for i in range(1, 5):
            question = (field_data.get(f'faq-{i}-question', '') or '').lower()
            answer = field_data.get(f'faq-{i}-answer', '') or ''

            # Skip if already has phlebotomist mention
            if 'phlebotomist' in answer.lower():
                continue

            # Check if question matches any of our patterns
            for pattern, new_answer in FAQ_UPDATES.items():
                if pattern in question:
                    updates[f'faq-{i}-answer'] = new_answer
                    changes_made.append(f'faq-{i}')
                    break

        if not updates:
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
