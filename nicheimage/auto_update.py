import time
import subprocess
from datetime import datetime, timedelta
import argparse


def is_package_outdated(package_name):
    try:
        # Run pip command and capture the output
        result = subprocess.run(
            ["pip", "list", "--outdated"], capture_output=True, text=True
        )
        if result.returncode != 0:
            # Handle error if pip command fails
            print("Error in executing pip command")
            return False

        # Check if the package is in the list of outdated packages
        outdated_packages = result.stdout
        return package_name in outdated_packages
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


parser = argparse.ArgumentParser(
    description="Auto update script for the Niche Image validator."
)
parser.add_argument(
    "--interval", type=int, default=3600, help="Interval between checks in seconds."
)
parser.add_argument(
    "--process_name",
    type=str,
    default="validator_nicheimage",
    help="Name of the pm2 process.",
)
args = parser.parse_args()

while True:
    # Log the start of the script execution
    print(f"{datetime.now()}: Script started")

    # Save the current HEAD hash
    is_outdated = is_package_outdated("nicheimage")

    # Check if the new HEAD is different from the current HEAD
    if is_outdated:
        # The HEAD has changed, meaning there's a new version
        subprocess.run(["pip", "install", "--upgrade", "nicheimage"])
        print(f"{datetime.now()}: New version detected, restarting the validator.")
        subprocess.run(["pm2", "restart", args.process_name])
    else:
        # No new version, no action needed
        print(f"{datetime.now()}: No new version detected, no restart needed.")

    # Sleep until the beginning of the next hour
    time.sleep(args.interval)
