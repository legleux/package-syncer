# get head commits of branches
from check_gh_latest_commits import get_branch_sha, get_hash_from_tag
from check_releases import get_releases

# get latest commits from source repo, "clio"
latest_commits = get_branch_sha()

REPO = "legleux/package-syncer"

def check_if_release_needed(repo=REPO, git_rev=None):
    hash_needs_release = True
# check if pkg-sync repo has a release has a release for each
    releases = get_releases(repo)
    # for release in releases:
    #     print(release['tag_name'])
    #     print(release['published_at'])

    releases = [ release['tag_name'] for release in releases ]
    released_shas = [ sha[1] for sha in releases if len(sha.split('-')) > 1]
    for commit in latest_commits:
        if not commit in released_shas:
            # print(f"Need to release: {commit}")
            print(commit[1])
            return commit[1]
        else:
            print("false")
            return False
    # released_shas = [ get_hash_from_tag(release) for release in releases ]
    # breakpoint()
    # for commit in latest_commits:
        # sha = commit[1]
        # breakpoint()
        # if get_hash_from_tag(tag)
        # print()

check_if_release_needed()
