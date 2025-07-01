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

total_open_prs = 0
total_open_issues = 0
total_closed_issues = 0
total_stars = 0
total_forks = 0
total_releases = 0
total_watchers = 0
total_tags = 0

for repo in repos:
    print(f"Processing repository: {repo.name}", flush=True)

    # Get contributors
    print("Fetching contributors...", flush=True)
    try:
        repo_contributors_count = 0
        for contributor in repo.get_contributors():
            if contributor and contributor.id is not None:
                contributors_set.add(contributor.id)
                repo_contributors_count += 1
        print(f"Contributors found in {repo.name}: {repo_contributors_count}", flush=True)
    except Exception:
        print(f"Failed to fetch contributors for {repo.name}", flush=True)
        pass  # Some repos may be empty or restricted

    # Get commits (default branch)
    print("Fetching commits...", flush=True)
    try:
        branch = repo.default_branch
        commits = repo.get_commits(sha=branch)
        repo_commits_count = commits.totalCount
        total_commits += repo_commits_count
        print(f"Commits found in {repo.name}: {repo_commits_count}", flush=True)
    except Exception:
        print(f"Failed to fetch commits for {repo.name}", flush=True)
        pass

    # Get closed pull requests
    print("Fetching closed pull requests...", flush=True)
    try:
        closed_prs = repo.get_pulls(state="closed")
        repo_closed_prs_count = closed_prs.totalCount
        total_closed_prs += repo_closed_prs_count
        print(f"Closed pull requests found in {repo.name}: {repo_closed_prs_count}", flush=True)
    except Exception:
        print(f"Failed to fetch closed pull requests for {repo.name}", flush=True)
        pass

    # Get open pull requests
    print("Fetching open pull requests...", flush=True)
    try:
        open_prs = repo.get_pulls(state="open")
        repo_open_prs_count = open_prs.totalCount
        total_open_prs += repo_open_prs_count
        print(f"Open pull requests found in {repo.name}: {repo_open_prs_count}", flush=True)
    except Exception:
        print(f"Failed to fetch open pull requests for {repo.name}", flush=True)
        pass

    # Get open issues
    print("Fetching open issues...", flush=True)
    try:
        open_issues = repo.get_issues(state="open")
        repo_open_issues_count = open_issues.totalCount
        total_open_issues += repo_open_issues_count
        print(f"Open issues found in {repo.name}: {repo_open_issues_count}", flush=True)
    except Exception:
        print(f"Failed to fetch open issues for {repo.name}", flush=True)
        pass

    # Get closed issues
    print("Fetching closed issues...", flush=True)
    try:
        closed_issues = repo.get_issues(state="closed")
        repo_closed_issues_count = closed_issues.totalCount
        total_closed_issues += repo_closed_issues_count
        print(f"Closed issues found in {repo.name}: {repo_closed_issues_count}", flush=True)
    except Exception:
        print(f"Failed to fetch closed issues for {repo.name}", flush=True)
        pass

    # Get stars
    repo_stars = repo.stargazers_count
    total_stars += repo_stars
    print(f"Stars in {repo.name}: {repo_stars}", flush=True)

    # Get forks
    repo_forks = repo.forks_count
    total_forks += repo_forks
    print(f"Forks in {repo.name}: {repo_forks}", flush=True)

    # Get releases
    try:
        releases = repo.get_releases()
        repo_releases_count = releases.totalCount
        total_releases += repo_releases_count
        print(f"Releases in {repo.name}: {repo_releases_count}", flush=True)
    except Exception:
        print(f"Failed to fetch releases for {repo.name}", flush=True)
        pass

    # Get watchers (subscribers)
    try:
        watchers = repo.get_subscribers()
        repo_watchers_count = watchers.totalCount
        total_watchers += repo_watchers_count
        print(f"Watchers (subscribers) in {repo.name}: {repo_watchers_count}", flush=True)
    except Exception:
        print(f"Failed to fetch watchers for {repo.name}", flush=True)
        pass

    # Get tags
    try:
        tags = repo.get_tags()
        repo_tags_count = tags.totalCount
        total_tags += repo_tags_count
        print(f"Tags in {repo.name}: {repo_tags_count}", flush=True)
    except Exception:
        print(f"Failed to fetch tags for {repo.name}", flush=True)
        pass

print("Processing complete.", flush=True)
print(f"Total number of repositories: {total_repos}", flush=True)
print(f"Total number of contributors across all repos: {len(contributors_set)}", flush=True)
print(f"Total number of commits across default branches: {total_commits}", flush=True)
print(f"Total number of closed pull requests across all repos: {total_closed_prs}", flush=True)
print(f"Total number of open pull requests across all repos: {total_open_prs}", flush=True)
print(f"Total number of open issues across all repos: {total_open_issues}", flush=True)
print(f"Total number of closed issues across all repos: {total_closed_issues}", flush=True)
print(f"Total number of stars across all repos: {total_stars}", flush=True)
print(f"Total number of forks across all repos: {total_forks}", flush=True)
print(f"Total number of releases across all repos: {total_releases}", flush=True)
print(f"Total number of watchers (subscribers) across all repos: {total_watchers}", flush=True)
print(f"Total number of tags across all repos: {total_tags}", flush=True)