import argparse
import datetime
import logging
import os
import time

from github import Github, GithubException, RateLimitExceededException

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

parser = argparse.ArgumentParser(description="Find inactive repositories")
parser.add_argument(
    "--org", default="flathub", help="GitHub organization name (default: 'flathub')"
)
parser.add_argument(
    "--output", default="inactive.txt", help="Output file (default: 'inactive.txt')"
)
args = parser.parse_args()

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ORG_NAME = args.org
output_file = args.output
earliest = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(weeks=3)
g = Github(GITHUB_TOKEN)
org = g.get_organization(ORG_NAME)
repos = org.get_repos(type="public", sort="updated", direction="desc")

excludes = set()
if os.path.exists("exclude.txt"):
    with open("exclude.txt", encoding="utf-8") as f:
        excludes = {line.strip() for line in f if line.strip()}

if os.path.exists(output_file):
    os.remove(output_file)

for repo in repos:
    if repo.archived:
        continue

    try:
        flathubbot_prs = [
            pr
            for pr in repo.get_pulls(state="open")
            if pr.user.login in ("flathubbot", "dependabot[bot]", "github-actions[bot]")
        ]

        if len(flathubbot_prs) < 5:
            continue

        last_commit = next(iter(repo.get_commits(sha=repo.default_branch)), None)

        if not last_commit:
            continue

        last_commit_time = last_commit.commit.committer.date.astimezone(
            datetime.timezone.utc
        )

        if last_commit_time < earliest:
            repo_name = repo.full_name.split("/")[-1]
            if repo_name not in excludes:
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(f"{repo_name}\n")

    except RateLimitExceededException:
        reset_time = g.get_rate_limit().core.reset.replace(tzinfo=datetime.timezone.utc)
        sleep_time = (
            reset_time - datetime.datetime.now(datetime.timezone.utc)
        ).total_seconds() + 10
        logging.warning("Rate limited. Sleeping %d seconds...", int(sleep_time))
        time.sleep(sleep_time)

    except GithubException as e:
        logging.error("%s: %s", repo.full_name, e)
        continue
