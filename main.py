# get head commits of branches
from check_gh_latest_commits import get_last_commits_from_target_branches, get_hash_from_tag
from check_releases import get_releases

SOURCE_REPO = "legleux/package-syncer"

def check_releases_needed(repo=SOURCE_REPO, git_rev=None):

    source_repo_latest_commits = get_last_commits_from_target_branches()
    releases = get_releases(repo)
    released_tags = [ release['tag_name'] for release in releases ]
    releases_found = []
    for latest_commit in source_repo_latest_commits:
        branch, git_rev = latest_commit
        release_tag = f"{branch}_{git_rev[:8]}"

        if release_tag not in released_tags:
            # log this somehow write a file and read it to markdown for display in github?
            # print(f"need a release for {latest_commit[0]} -- {release_tag}")
            releases_found.append(release_tag)
        else:
            pass
            # print(f"Found a release for {latest_commit[0]} -- {release_tag}")
    if not releases_found:
        print("false")
    else:
        print(releases_found[0])

check_releases_needed()
