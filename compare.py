# from get_artifact import get_artifacts
# from check_releases import get_gh_releases

from check_releases import get_gh_releases

releases = [release['tag_name'] for release in get_gh_releases('legleux/package-syncer')]

x = [pair for pair in [pair.split('_') for pair in releases]]
# flatten
# # get the latest assets built from these branches/commits available from the source_repo:
x = [ i for sub in x for i in sub]
for branch, git_rev in zip(x[::2], x[1::2]):
# for branch, git_rev in zip(x[0::1],x[1::]):
    print(f"branch: {branch} git_rev: {git_rev}")

branch_map = {"master":"stable", "release":"unstable", "develop":"nightly"}
