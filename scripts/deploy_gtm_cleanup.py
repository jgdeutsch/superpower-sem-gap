#!/usr/bin/env python3
"""
GTM Cleanup Deploy: Trim SEM to single tag, remove biomarker tags.

What this does:
  1. Deletes ALL existing SP tags (SEM Part 1/2, Biomarker Part 1/2, Biomarker Link Rewriter)
  2. Deletes the Biomarker Pages trigger
  3. Keeps the register/checkout trigger (ID: 332) and SEM landing pages trigger (ID: 333)
  4. Creates 1 new single SEM personalization tag (111 slugs, ~93K chars)
  5. Publishes the container version

Result: 4 tags -> 1 tag, ~392K -> ~93K chars (77% reduction).
"""
import json
import os
import sys
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(SCRIPT_DIR)

CLIENT_SECRET_FILE = "/Users/jeffy/Downloads/client_secret_2_435686878764-dq7jpfr5ph19sugf962l4bd842gpuk8r.apps.googleusercontent.com (2).json"
TOKEN_FILE = os.path.join(APP_DIR, ".gtm_token.json")
SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
    "https://www.googleapis.com/auth/tagmanager.publish",
    "https://www.googleapis.com/auth/tagmanager.manage.accounts",
]

GTM_CONTAINER_PUBLIC_ID = "GTM-PBS5NFXN"
TAG_PART1_PATH = os.path.join(APP_DIR, "gtm", "register_personalization_tag_part1.html")
TAG_PART2_PATH = os.path.join(APP_DIR, "gtm", "register_personalization_tag_part2.html")


def get_credentials():
    """Get or refresh OAuth2 credentials."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return creds


def find_container(service):
    """Find the GTM container by its public ID."""
    accounts = service.accounts().list().execute()
    for account in accounts.get("account", []):
        account_id = account["accountId"]
        containers = (
            service.accounts()
            .containers()
            .list(parent=f"accounts/{account_id}")
            .execute()
        )
        for container in containers.get("container", []):
            if container.get("publicId") == GTM_CONTAINER_PUBLIC_ID:
                return account_id, container["containerId"], container["path"]
    return None, None, None


def get_latest_workspace(service, container_path):
    """Get the default workspace."""
    workspaces = (
        service.accounts()
        .containers()
        .workspaces()
        .list(parent=container_path)
        .execute()
    )
    for ws in workspaces.get("workspace", []):
        if ws.get("name") == "Default Workspace":
            return ws["path"]
    if workspaces.get("workspace"):
        return workspaces["workspace"][0]["path"]
    return None


def cleanup_tags(service, workspace_path):
    """Delete all SP tags (SEM + Biomarker)."""
    tags = (
        service.accounts()
        .containers()
        .workspaces()
        .tags()
        .list(parent=workspace_path)
        .execute()
    )
    deleted = 0
    for tag in tags.get("tag", []):
        if tag["name"].startswith("SP -"):
            service.accounts().containers().workspaces().tags().delete(
                path=tag["path"]
            ).execute()
            print(f"  Deleted tag: {tag['name']} (ID: {tag['tagId']})")
            deleted += 1
    return deleted


def cleanup_biomarker_trigger(service, workspace_path):
    """Delete the Biomarker Pages trigger (keep SEM triggers)."""
    triggers = (
        service.accounts()
        .containers()
        .workspaces()
        .triggers()
        .list(parent=workspace_path)
        .execute()
    )
    deleted = 0
    for trigger in triggers.get("trigger", []):
        if "Biomarker" in trigger.get("name", ""):
            service.accounts().containers().workspaces().triggers().delete(
                path=trigger["path"]
            ).execute()
            print(f"  Deleted trigger: {trigger['name']} (ID: {trigger['triggerId']})")
            deleted += 1
    return deleted


def find_register_checkout_trigger(service, workspace_path):
    """Find the existing register/checkout trigger."""
    triggers = (
        service.accounts()
        .containers()
        .workspaces()
        .triggers()
        .list(parent=workspace_path)
        .execute()
    )
    for trigger in triggers.get("trigger", []):
        name = trigger.get("name", "")
        if "Register" in name and "Checkout" in name and "SP Variant" in name:
            return trigger
    return None


def find_landing_page_trigger(service, workspace_path):
    """Find the existing SEM landing page trigger."""
    triggers = (
        service.accounts()
        .containers()
        .workspaces()
        .triggers()
        .list(parent=workspace_path)
        .execute()
    )
    for trigger in triggers.get("trigger", []):
        name = trigger.get("name", "")
        if "SEM Landing" in name:
            return trigger
    return None


def create_personalization_tag(service, workspace_path, trigger_id, tag_path, tag_name):
    """Create a personalization tag from an HTML file."""
    with open(tag_path, "r") as f:
        html_content = f.read()

    print(f"  {tag_name}: {len(html_content):,} chars")
    if len(html_content) > 102400:
        print(f"  ERROR: {tag_name} exceeds 102,400 char limit!")
        sys.exit(1)

    body = {
        "name": tag_name,
        "type": "html",
        "parameter": [
            {"type": "TEMPLATE", "key": "html", "value": html_content},
            {"type": "BOOLEAN", "key": "supportDocumentWrite", "value": "false"},
        ],
        "firingTriggerId": [trigger_id],
    }
    result = (
        service.accounts()
        .containers()
        .workspaces()
        .tags()
        .create(parent=workspace_path, body=body)
        .execute()
    )
    print(f"  Created tag: {result['name']} (ID: {result['tagId']})")
    return result


def create_link_rewriter_tag(service, workspace_path, trigger_id):
    """Recreate the SEM link rewriter tag."""
    tag_path = os.path.join(APP_DIR, "gtm", "landing_page_link_rewriter.html")
    with open(tag_path, "r") as f:
        html_content = f.read()

    body = {
        "name": "SP - Landing Page Link Rewriter",
        "type": "html",
        "parameter": [
            {"type": "TEMPLATE", "key": "html", "value": html_content},
            {"type": "BOOLEAN", "key": "supportDocumentWrite", "value": "false"},
        ],
        "firingTriggerId": [trigger_id],
    }
    result = (
        service.accounts()
        .containers()
        .workspaces()
        .tags()
        .create(parent=workspace_path, body=body)
        .execute()
    )
    print(f"  Created tag: {result['name']} (ID: {result['tagId']})")
    return result


def publish_container(service, container_path):
    """Create a version and publish it, with retry for rate limits."""
    workspace_path = get_latest_workspace(service, container_path)

    for attempt in range(8):
        try:
            version_result = (
                service.accounts()
                .containers()
                .workspaces()
                .create_version(
                    path=workspace_path,
                    body={
                        "name": "v231: Remove organ-age-test entry",
                        "notes": "Removed organ-age-test from personalization data. "
                        "152 entries (down from 153).",
                    },
                )
                .execute()
            )
            break
        except HttpError as e:
            if e.resp.status == 429 and attempt < 7:
                wait = 120 * (attempt + 1)
                print(f"  Rate limited. Waiting {wait}s (attempt {attempt + 1}/8)...")
                time.sleep(wait)
            else:
                raise

    version = version_result.get("containerVersion", {})
    version_id = version.get("containerVersionId")
    print(f"  Created version: {version_id}")

    time.sleep(5)

    publish_result = (
        service.accounts()
        .containers()
        .versions()
        .publish(path=f"{container_path}/versions/{version_id}")
        .execute()
    )
    print(f"  Published version: {version_id}")
    return publish_result


def main():
    print("=== GTM Deploy (2 Personalization Tags) ===\n")

    # 1. Authenticate
    print("1. Authenticating...")
    creds = get_credentials()
    service = build("tagmanager", "v2", credentials=creds)
    print("   OK\n")

    # 2. Find container
    print("2. Finding GTM container...")
    account_id, container_id, container_path = find_container(service)
    if not container_path:
        print(f"   ERROR: Could not find container {GTM_CONTAINER_PUBLIC_ID}")
        sys.exit(1)
    print(f"   Found: {container_path}\n")

    # 3. Get workspace
    print("3. Getting workspace...")
    workspace_path = get_latest_workspace(service, container_path)
    if not workspace_path:
        print("   ERROR: Could not find workspace")
        sys.exit(1)
    print(f"   Using: {workspace_path}\n")

    # 4. Delete all SP tags
    print("4. Deleting all SP tags...")
    deleted_tags = cleanup_tags(service, workspace_path)
    print(f"   Deleted {deleted_tags} tags\n")

    # 5. Delete biomarker trigger
    print("5. Deleting biomarker trigger...")
    deleted_triggers = cleanup_biomarker_trigger(service, workspace_path)
    print(f"   Deleted {deleted_triggers} triggers\n")

    # 6. Find existing triggers
    print("6. Finding existing triggers...")
    reg_trigger = find_register_checkout_trigger(service, workspace_path)
    if not reg_trigger:
        print("   ERROR: Register/checkout trigger not found!")
        sys.exit(1)
    print(f"   Register/checkout: {reg_trigger['name']} (ID: {reg_trigger['triggerId']})")

    lp_trigger = find_landing_page_trigger(service, workspace_path)
    if not lp_trigger:
        print("   ERROR: SEM landing page trigger not found!")
        sys.exit(1)
    print(f"   Landing pages: {lp_trigger['name']} (ID: {lp_trigger['triggerId']})\n")

    # 7. Create new tags
    print("7. Creating new tags...")
    create_personalization_tag(
        service, workspace_path, reg_trigger["triggerId"],
        TAG_PART1_PATH, "SP - Checkout Personalization Part 1"
    )
    create_personalization_tag(
        service, workspace_path, reg_trigger["triggerId"],
        TAG_PART2_PATH, "SP - Checkout Personalization Part 2"
    )
    create_link_rewriter_tag(service, workspace_path, lp_trigger["triggerId"])
    print()

    # 8. Publish
    print("8. Publishing container version...")
    publish_container(service, container_path)
    print()

    print("=== Done! ===")
    print("  3 tags: Personalization Part 1 + Part 2 + Link Rewriter")
    print()
    print("Test URLs:")
    print("  https://superpower.com/checkout/membership?sp_variant=cholesterol-test  (Part 1)")
    print("  https://superpower.com/checkout/membership?sp_variant=thyroid-panel     (Part 2)")
    print("  https://superpower.com/checkout/membership?sp_variant=welcome-ny        (Part 2)")


if __name__ == "__main__":
    main()
