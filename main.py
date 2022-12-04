# get head commits of branches
from check_gh_latest_commits import get_last_commits_from_target_branches, get_hash_from_tag
from check_releases import get_gh_releases

TARGET_REPO = "legleux/package-syncer"

def check_releases_needed(repo=TARGET_REPO, git_rev=None, gh=False, print_all=False):

    target_repo_latest_commits = get_last_commits_from_target_branches()
    releases = get_gh_releases(repo)
    # breakpoint()
    released_tags = [ release['tag_name'] for release in releases ]
    releases_found = []

    for latest_commit in target_repo_latest_commits:
        branch, git_rev = latest_commit
        full_release_tag = f"{branch}_{git_rev}"
        release_tag = f"{branch}_{git_rev[:8]}"

        if release_tag not in released_tags:
            # log this somehow write a file and read it to markdown for display in github?
            # print(f"need a release for {latest_commit[0]} -- {release_tag}")
            releases_found.append(full_release_tag)
        else:
            pass
            # print(f"Found a release for {latest_commit[0]} -- {release_tag}")
    if not releases_found:
        print("false")
    else:
        if(gh):
            if(print_all):
                print(releases_found[0])
            else:
                print(releases_found)
        else:
            print(releases_found) # log this
            return releases_found

if __name__ == "__main__":
    print_all=False
    if len(sys.argv > 1):
        print_all = sys.argv[1] # TODO: argparse
    check_releases_needed(gh=True, print_all=print_all)
# Check which branches in <source_repo> do not have releases in <target_repo>:

# releases_needed = check_releases_needed()
# x = [pair for pair in [pair.split('_') for pair in releases_needed]]
# # flatten
# # # get the latest assets built from these branches/commits available from the source_repo:
# x = [ i for sub in x for i in sub]
# for branch, git_rev in zip(x[::2], x[1::2]):
# # for branch, git_rev in zip(x[0::1],x[1::]):
#     print(f"branch: {branch} git_rev: {git_rev}")
