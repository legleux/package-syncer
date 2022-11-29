# get head commits of branches
from check_gh_latest_commits import get_last_commits_from_target_branches, get_hash_from_tag
from check_releases import get_releases

SOURCE_REPO = "legleux/package-syncer"

def check_releases_needed(repo=SOURCE_REPO, git_rev=None):

    source_repo_latest_commits = get_last_commits_from_target_branches()
    releases = get_releases(repo)
    released_tags = [ release['tag_name'] for release in releases ]

    for latest_commit in source_repo_latest_commits:
        release_tag = f"{latest_commit[0]}-{latest_commit[1][:8]}"
        if release_tag not in released_tags:
            # log print(f"need a release for {latest_commit[0]} -- {release_tag}")
            print(release_tag)
            exit()
        else:
            print("false")
            return False

check_releases_needed()
