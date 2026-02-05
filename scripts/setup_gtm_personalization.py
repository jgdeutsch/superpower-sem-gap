#!/usr/bin/env python3
"""
Set up GTM personalization tags via the Tag Manager API.

Creates:
  1. DOM Ready trigger for /register or /checkout with sp_variant
  2. DOM Ready trigger for landing pages
  3. Self-contained Custom HTML tag (personalization data baked in, ~75KB)
  4. Custom HTML tag (link rewriter)
  5. Publishes the container version

Note: SP Variant variable was already created in a prior run (ID: 250).
The personalization data is baked directly into the Custom HTML tag
because GTM's Custom JS variable has a 20,000 char limit (our data is 73K).

Uses OAuth2 Desktop flow for authentication.
"""
import json
import os
import sys

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
        containers = service.accounts().containers().list(
            parent=f"accounts/{account_id}"
        ).execute()
        for container in containers.get("container", []):
            if container.get("publicId") == GTM_CONTAINER_PUBLIC_ID:
                return account_id, container["containerId"], container["path"]
    return None, None, None


def get_latest_workspace(service, container_path):
    """Get the default workspace."""
    workspaces = service.accounts().containers().workspaces().list(
        parent=container_path
    ).execute()
    for ws in workspaces.get("workspace", []):
        if ws.get("name") == "Default Workspace":
            return ws["path"]
    if workspaces.get("workspace"):
        return workspaces["workspace"][0]["path"]
    return None


def check_existing_items(service, workspace_path):
    """Check for existing SP personalization items to avoid duplicates."""
    existing = {"variables": [], "triggers": [], "tags": []}

    variables = service.accounts().containers().workspaces().variables().list(
        parent=workspace_path
    ).execute()
    for v in variables.get("variable", []):
        if v["name"].startswith("SP "):
            existing["variables"].append(v)
            print(f"  Found existing variable: {v['name']} (ID: {v['variableId']})")

    triggers = service.accounts().containers().workspaces().triggers().list(
        parent=workspace_path
    ).execute()
    for t in triggers.get("trigger", []):
        if "SP Variant" in t.get("name", "") or "SEM Landing" in t.get("name", ""):
            existing["triggers"].append(t)
            print(f"  Found existing trigger: {t['name']} (ID: {t['triggerId']})")

    tags = service.accounts().containers().workspaces().tags().list(
        parent=workspace_path
    ).execute()
    for tag in tags.get("tag", []):
        if tag["name"].startswith("SP -"):
            existing["tags"].append(tag)
            print(f"  Found existing tag: {tag['name']} (ID: {tag['tagId']})")

    return existing


def delete_items(service, existing):
    """Delete existing SP personalization items."""
    for tag in existing["tags"]:
        service.accounts().containers().workspaces().tags().delete(
            path=tag["path"]
        ).execute()
        print(f"  Deleted tag: {tag['name']}")

    for trigger in existing["triggers"]:
        service.accounts().containers().workspaces().triggers().delete(
            path=trigger["path"]
        ).execute()
        print(f"  Deleted trigger: {trigger['name']}")

    for var in existing["variables"]:
        service.accounts().containers().workspaces().variables().delete(
            path=var["path"]
        ).execute()
        print(f"  Deleted variable: {var['name']}")


def create_register_checkout_trigger(service, workspace_path):
    """Create DOM Ready trigger for /register OR /checkout with sp_variant."""
    body = {
        "name": "DOM Ready - Register/Checkout with SP Variant",
        "type": "domReady",
        "filter": [
            {
                "type": "MATCH_REGEX",
                "parameter": [
                    {"type": "TEMPLATE", "key": "arg0", "value": "{{Page Path}}"},
                    {"type": "TEMPLATE", "key": "arg1", "value": "/(register|checkout)"},
                ],
            },
            {
                "type": "MATCH_REGEX",
                "parameter": [
                    {"type": "TEMPLATE", "key": "arg0", "value": "{{Page URL}}"},
                    {"type": "TEMPLATE", "key": "arg1", "value": "sp_variant=.+"},
                ],
            },
        ],
    }
    result = service.accounts().containers().workspaces().triggers().create(
        parent=workspace_path, body=body
    ).execute()
    print(f"  Created trigger: {result['name']} (ID: {result['triggerId']})")
    return result


def create_landing_page_trigger(service, workspace_path):
    """Create DOM Ready trigger for SEM landing pages."""
    body = {
        "name": "DOM Ready - SEM Landing Pages",
        "type": "domReady",
        "filter": [
            {
                "type": "MATCH_REGEX",
                "parameter": [
                    {"type": "TEMPLATE", "key": "arg0", "value": "{{Page Path}}"},
                    {"type": "TEMPLATE", "key": "arg1", "value": "/(welcome-cms|sem-landing-pages)/"},
                ],
            },
        ],
    }
    result = service.accounts().containers().workspaces().triggers().create(
        parent=workspace_path, body=body
    ).execute()
    print(f"  Created trigger: {result['name']} (ID: {result['triggerId']})")
    return result


def create_personalization_tags(service, workspace_path, trigger_id):
    """Create self-contained Custom HTML tags with baked-in personalization data.

    Split into two tags (Part 1 and Part 2) because GTM has a 102,400 char
    limit per Custom HTML tag and 155 slugs exceed that in a single tag.
    """
    for part in [1, 2]:
        tag_path = os.path.join(APP_DIR, "gtm", f"register_personalization_tag_part{part}.html")
        with open(tag_path, "r") as f:
            html_content = f.read()

        print(f"  Part {part} HTML size: {len(html_content):,} chars")

        body = {
            "name": f"SP - Register Page Personalization (Part {part})",
            "type": "html",
            "parameter": [
                {"type": "TEMPLATE", "key": "html", "value": html_content},
                {"type": "BOOLEAN", "key": "supportDocumentWrite", "value": "false"},
            ],
            "firingTriggerId": [trigger_id],
        }
        result = service.accounts().containers().workspaces().tags().create(
            parent=workspace_path, body=body
        ).execute()
        print(f"  Created tag: {result['name']} (ID: {result['tagId']})")


def create_link_rewriter_tag(service, workspace_path, trigger_id):
    """Create Custom HTML tag for landing page link rewriting."""
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
    result = service.accounts().containers().workspaces().tags().create(
        parent=workspace_path, body=body
    ).execute()
    print(f"  Created tag: {result['name']} (ID: {result['tagId']})")
    return result


def publish_container(service, container_path):
    """Create a version and publish it."""
    workspace_path = get_latest_workspace(service, container_path)

    version_result = service.accounts().containers().workspaces().create_version(
        path=workspace_path,
        body={
            "name": "SEM Register Personalization - POC",
            "notes": "Personalizes /register and /checkout based on sp_variant URL parameter. Self-contained tag with 99 landing page variants baked in. Link rewriter for Webflow landing pages.",
        },
    ).execute()

    version = version_result.get("containerVersion", {})
    version_id = version.get("containerVersionId")
    print(f"  Created version: {version_id}")

    publish_result = service.accounts().containers().versions().publish(
        path=f"{container_path}/versions/{version_id}"
    ).execute()
    print(f"  Published version: {version_id}")
    return publish_result


def main():
    print("=== GTM Personalization Setup ===\n")

    # 1. Authenticate
    print("1. Authenticating...")
    creds = get_credentials()
    service = build("tagmanager", "v2", credentials=creds)
    print("   Authenticated.\n")

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

    # 4. Check for existing items and clean up
    print("4. Checking for existing SP items...")
    existing = check_existing_items(service, workspace_path)
    has_existing = any(existing[k] for k in existing)
    if has_existing:
        print("   Cleaning up existing items...")
        delete_items(service, existing)
        print("   Cleaned up.\n")
    else:
        print("   None found.\n")

    # 5. Create triggers
    print("5. Creating triggers...")
    reg_trigger = create_register_checkout_trigger(service, workspace_path)
    lp_trigger = create_landing_page_trigger(service, workspace_path)
    print()

    # 6. Create tags
    print("6. Creating tags...")
    create_personalization_tags(service, workspace_path, reg_trigger["triggerId"])
    create_link_rewriter_tag(service, workspace_path, lp_trigger["triggerId"])
    print()

    # 7. Publish
    print("7. Publishing container version...")
    publish_container(service, container_path)
    print()

    print("=== Done! GTM personalization is now live. ===")
    print("Test URLs:")
    print("  https://superpower.com/register?sp_variant=cortisol-test")
    print("  https://superpower.com/checkout?sp_variant=cortisol-test")


if __name__ == "__main__":
    main()
