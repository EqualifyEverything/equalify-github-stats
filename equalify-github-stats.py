import os
from github import Github
from dotenv import load_dotenv
load_dotenv()

ORG_NAME = "EQUALIFYEVERYTHING"
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise RuntimeError("Please set the GITHUB_TOKEN environment variable.")

g = Github(TOKEN)
org = g.get_organization(ORG_NAME)

# Total number of repositories
repos = list(org.get_repos())
total_repos = len(repos)

# For contributors: use a set to avoid duplicates
contributors_set = set()
# For commits
total_commits = 0
# For closed PRs
total_closed_prs = 0

for repo in repos:
    print(f"Processing repository: {repo.name}")

    # Get contributors
    print("Fetching contributors...")
    try:
        repo_contributors_count = 0
        for contributor in repo.get_contributors():
            if contributor and contributor.id is not None:
                contributors_set.add(contributor.id)
                repo_contributors_count += 1
        print(f"Contributors found in {repo.name}: {repo_contributors_count}")
    except Exception:
        print(f"Failed to fetch contributors for {repo.name}")
        pass  # Some repos may be empty or restricted

    # Get commits (default branch)
    print("Fetching commits...")
    try:
        branch = repo.default_branch
        commits = repo.get_commits(sha=branch)
        repo_commits_count = commits.totalCount
        total_commits += repo_commits_count
        print(f"Commits found in {repo.name}: {repo_commits_count}")
    except Exception:
        print(f"Failed to fetch commits for {repo.name}")
        pass

    # Get closed pull requests
    print("Fetching closed pull requests...")
    try:
        closed_prs = repo.get_pulls(state="closed")
        repo_closed_prs_count = closed_prs.totalCount
        total_closed_prs += repo_closed_prs_count
        print(f"Closed pull requests found in {repo.name}: {repo_closed_prs_count}")
    except Exception:
        print(f"Failed to fetch closed pull requests for {repo.name}")
        pass

print("Processing complete.")
print(f"Total number of repositories: {total_repos}")
print(f"Total number of contributors across all repos: {len(contributors_set)}")
print(f"Total number of commits across default branches: {total_commits}")
print(f"Total number of closed pull requests across all repos: {total_closed_prs}")