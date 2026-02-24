"""
PAUSE BAD GROUPS - Feb 23, 2026
Based on 1-week (Feb 16-22) and 4-week (Jan 26 - Feb 22) audit data.
All groups were BAD in both time windows.

Total BAD spend being paused: ~$28.7K/week
Expected sub loss: ~38 subs/week (at $760 CPS - terrible efficiency)
"""
import yaml
from google.ads.googleads.client import GoogleAdsClient

config_path = "/Users/jeffy/.config/google-ads-mcp/google-ads.yaml"
with open(config_path) as f:
    config = yaml.safe_load(f)

client = GoogleAdsClient.load_from_dict(config)
service = client.get_service("GoogleAdsService")
customer_id = "8618096874"

# ============================================================
# SEARCH AD GROUPS TO PAUSE (8 groups, ~$14.8K/week)
# ============================================================
search_pauses = [
    # (ad_group_id, campaign_id, name, 1wk_spend, 1wk_cps)
    (186665649814, 23020350152, "Health Check", "$1,719", "$573"),
    (188162570049, 23020350152, "Test", "$3,575", "$581"),
    (188162568649, 23020350152, "Health testing", "$5,292", "$619"),
    (188162568849, 23020350152, "Hormone Testing", "$904", "$904"),
    (188162567169, 23020350152, "Cancer", "$1,254", "0 subs"),
    (192070922079, 23538070207, "Thyroid Tests", "$549", "$549"),
    (192070922119, 23538070207, "Heart & Cholesterol", "$577", "0 subs"),
    (192775259733, 23538070207, "Lab Test", "$1,224", "0 subs"),
]

# ============================================================
# PMAX ASSET GROUPS TO PAUSE (5 groups, ~$13.6K/week)
# ============================================================
pmax_pauses = [
    # (asset_group_id, campaign_id, name, 1wk_spend, 1wk_cps)
    (6667331354, 23449940807, "Blood Test (compliant)", "$7,619", "$641"),
    (6671357427, 23280708146, "Longevity Blood Test", "$2,058", "$686"),
    (6671393476, 23280708146, "Cholesterol & Heart Panel", "$400", "$801"),
    (6674795981, 23572698664, "Top Conv (Male) - Gender", "$2,083", "$1,240"),
    (6671394355, 23280708146, "Lp(a) Heart Risk", "$1,438", "$1,438"),
]

# ============================================================
# EXECUTE PAUSES
# ============================================================

print("=" * 80)
print("  PAUSING BAD GROUPS")
print("=" * 80)

# Pause Search ad groups
ag_service = client.get_service("AdGroupService")
ag_operations = []
for ag_id, camp_id, name, spend, cps in search_pauses:
    op = client.get_type("AdGroupOperation")
    ag = op.update
    ag.resource_name = f"customers/{customer_id}/adGroups/{ag_id}"
    ag.status = client.enums.AdGroupStatusEnum.PAUSED
    from google.protobuf import field_mask_pb2
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))
    ag_operations.append(op)
    print(f"  [Search] Pausing: {name} (AG={ag_id}) | {spend}/wk, CPS={cps}")

print(f"\n  Sending {len(ag_operations)} Search ad group pause operations...")
try:
    response = ag_service.mutate_ad_groups(customer_id=customer_id, operations=ag_operations)
    print(f"  SUCCESS: {len(response.results)} ad groups paused")
    for result in response.results:
        print(f"    - {result.resource_name}")
except Exception as e:
    print(f"  ERROR: {e}")

# Pause PMAX asset groups
asg_service = client.get_service("AssetGroupService")
asg_operations = []
for asg_id, camp_id, name, spend, cps in pmax_pauses:
    op = client.get_type("AssetGroupOperation")
    ag = op.update
    ag.resource_name = f"customers/{customer_id}/assetGroups/{asg_id}"
    ag.status = client.enums.AssetGroupStatusEnum.PAUSED
    op.update_mask.CopyFrom(field_mask_pb2.FieldMask(paths=["status"]))
    asg_operations.append(op)
    print(f"  [PMAX] Pausing: {name} (ASG={asg_id}) | {spend}/wk, CPS={cps}")

print(f"\n  Sending {len(asg_operations)} PMAX asset group pause operations...")
try:
    response = asg_service.mutate_asset_groups(customer_id=customer_id, operations=asg_operations)
    print(f"  SUCCESS: {len(response.results)} asset groups paused")
    for result in response.results:
        print(f"    - {result.resource_name}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "=" * 80)
print("  DONE. 13 BAD groups paused (~$28.7K/week saved)")
print("=" * 80)

