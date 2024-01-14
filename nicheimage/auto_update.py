import time
import subprocess
from datetime import datetime, timedelta
import argparse

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
    current_head = subprocess.getoutput("git rev-parse HEAD")

    # Pull the latest changes from the repository
    subprocess.run(["git", "stash"])
    subprocess.run(["git", "pull", "-f"])

    # Get the new HEAD hash
    new_head = subprocess.getoutput("git rev-parse HEAD")

    # Check if the new HEAD is different from the current HEAD
    if current_head != new_head:
        # The HEAD has changed, meaning there's a new version
        print(f"{datetime.now()}: New version detected, restarting the validator.")
        subprocess.run(["pm2", "restart", args.process_name])
    else:
        # No new version, no action needed
        print(f"{datetime.now()}: No new version detected, no restart needed.")

    # Sleep until the beginning of the next hour
    time.sleep(args.interval)
