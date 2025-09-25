import boto3
import json
import argparse
from botocore.exceptions import ClientError

# -------------------------------------------------------------------
# Get all enabled AWS regions for the current account
# -------------------------------------------------------------------
def get_all_regions():
    ec2 = boto3.client("ec2")
    regions = ec2.describe_regions(AllRegions=False)  # only returns regions you can actually use
    return [r["RegionName"] for r in regions["Regions"]]

# -------------------------------------------------------------------
# Find an EC2 instance by ID across all regions
# Returns full metadata if found, otherwise raises an exception
# -------------------------------------------------------------------
def get_instance_metadata(instance_id):
    regions = get_all_regions()

    for region in regions:
        ec2 = boto3.client("ec2", region_name=region)
        try:
            # Try to describe the instance in this region
            response = ec2.describe_instances(InstanceIds=[instance_id])
            reservations = response.get("Reservations", [])
            
            if reservations:
                # Found it → grab the instance details
                instance = reservations[0]["Instances"][0]
                instance["Region"] = region  # add region info for clarity
                return instance

        except ClientError as e:
            # If instance doesn’t exist in this region, move on
            if "InvalidInstanceID.NotFound" in str(e):
                continue
            # If it’s another error (e.g. permissions), stop and raise
            else:
                raise e

    # If we finish the loop without finding the instance
    raise Exception(f"Instance {instance_id} not found in any region.")

# -------------------------------------------------------------------
# Main script entry point
# -------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch AWS EC2 Instance Metadata")
    parser.add_argument("--instance-id", required=True, help="EC2 Instance ID (e.g. i-0abcd1234efgh5678)")
    parser.add_argument("--key", required=False, help="Optional: Return only a single metadata key (e.g. InstanceType)")
    args = parser.parse_args()

    # Retrieve the metadata
    metadata = get_instance_metadata(args.instance_id)

    if args.key:
        # Print just the requested key if it exists
        if args.key in metadata:
            print(metadata[args.key])
        else:
            print(f"Key '{args.key}' not found in metadata.")
    else:
        # Otherwise, print the full metadata in pretty JSON
        print(json.dumps(metadata, indent=4, default=str))
 