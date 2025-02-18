#!/usr/bin/env python3
"""
GitLab User Domains Extractor (Optimized Version)

This script retrieves all users from a GitLab instance, extracts their email domains, and saves them to a file.
Optimized to reduce API calls, improve file writing efficiency, and speed up processing.

Features:
- Fetches all users from GitLab API in batches (faster than all=True)
- Extracts unique email domains using a set comprehension (faster processing)
- Saves full user list and unique domains to separate files
- Provides logging and error handling
- Supports CLI arguments for flexibility

Author: GurbanV
GitHub: https://github.com/GurbanV/gitlab-user-domains
"""

import gitlab
import re
import warnings
import sys
import os
import logging
import argparse
from tqdm import tqdm
from requests.exceptions import RequestException
from dotenv import load_dotenv
from pathlib import Path


warnings.filterwarnings("ignore")

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)

# Load environment variables
load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(description="Extract GitLab user domains")
    parser.add_argument("--gitlab-url", type=str, help="GitLab instance URL")
    parser.add_argument("--token", type=str, help="GitLab private token")
    return parser.parse_args()

args = parse_args()
GITLAB_URL = args.gitlab_url or os.getenv("GITLAB_URL")
PRIVATE_TOKEN = args.token or os.getenv("PRIVATE_TOKEN")

if not GITLAB_URL or not PRIVATE_TOKEN:
    logging.error("❌ Missing required environment variables: GITLAB_URL or PRIVATE_TOKEN.")
    sys.exit(1)

USERS_FILE = Path("all_users_with_domains.txt")
DOMAINS_FILE = Path("unique_domains.txt")


def connect_gitlab():
    """Connect to GitLab with error handling."""
    try:
        gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN, ssl_verify=False)
        gl.auth()
        logging.info("✅ Successfully connected to GitLab!\n")
        return gl
    except gitlab.exceptions.GitlabAuthenticationError:
        logging.error("❌ Authentication error: Check your token.")
        sys.exit(2)
    except RequestException as e:
        logging.error(f"❌ Connection error: {e}")
        sys.exit(3)


def get_users(gl):
    """Retrieve GitLab users in batches (faster than all=True)."""
    logging.info("🔄 Fetching user list...\n")
    users = []
    page = 1

    while True:
        batch = gl.users.list(per_page=100, page=page)  # Load 100 users per request
        if not batch:
            break
        users.extend(batch)
        page += 1

    logging.info(f"👥 Total users in GitLab: {len(users)}\n")
    return users


def extract_domains(users):
    """Extract unique domains from user emails efficiently."""
    domain_pattern = re.compile(r'@([a-zA-Z0-9.-]+)')
    skipped_users = 0

    # Open file before the loop (improves file writing performance)
    with USERS_FILE.open("w") as uf:
        domains = {
            match.group(1).lower()
            for user in tqdm(users, desc="📄 Processing users", unit="user", leave=True)
            if user.email and (match := domain_pattern.search(user.email))
        }
    
        tqdm.write("")
    
        # Write users to file
        for user in users:
            if user.email:
                uf.write(f"{user.username} - {user.email}\n")
            else:
                skipped_users += 1

    logging.info(f"⚠️ Skipped {skipped_users} users without emails.\n")
    return domains


def save_domains(domains):
    """Save unique domains to a file."""
    try:
        with DOMAINS_FILE.open("w") as f:
            f.write("\n".join(sorted(domains)) + "\n")
    except IOError as e:
        logging.error(f"❌ Error writing to {DOMAINS_FILE}: {e}")
        sys.exit(6)

    logging.info("✅ Unique domains found: %d\n", len(domains))
    logging.info("📂 Unique domains saved in %s\n", DOMAINS_FILE)


def main():
    """Main script execution."""
    try:
        gl = connect_gitlab()
        users = get_users(gl)
        unique_domains = extract_domains(users)
        save_domains(unique_domains)
        
        logging.info("📂 All users saved in %s\n", USERS_FILE)
        logging.info("🚀 Process completed successfully!\n")
    except Exception as e:
        logging.critical(f"❌ Unexpected error: {e}", exc_info=True)
        sys.exit(7)


if __name__ == "__main__":
    main()
