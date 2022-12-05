from requests import post, get
import json
import os
from dotenv import dotenv_values
import hashlib
from logger import log
import check_artifactory
import get_art_by_sha
from get_artifact import download_release_artifact

if os.environ.get('GITHUB_ACTIONS'):
  TOKEN = os.environ['PAT_TOKEN']
else:
  TOKEN = dotenv_values().get('PAT_TOKEN')

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}"
}

def get_gh_releases(repo):
    url = f"https://api.github.com/repos/{repo}/releases"
    releases = json.loads(get(url, headers=headers).content)
    return releases

def get_workflows(repo):
    url = f"https://api.github.com/repos/{repo}/actions/workflows"
#           https://api.github.com/repos/OWNER/REPO/actions/workflows
    workflows = json.loads(get(url, headers=headers).content)
    return workflows


def get_release_assets(repo, tag):
    releases = get_gh_releases(repo)
    release = [r for r in releases if r['name'] == tag][0]
    assets = [asset['name'] for asset in release['assets']]
    return assets


def get_release_assets_sha(repo, release_tag, asset_name):
    url = f"https://github.com/{repo}/releases/download/{release_tag}/{asset_name}"
    # log.debug(f"Getting asset {asset_name} at {url}")
    sha = hashlib.sha256()
    asset = get(url, headers=headers, allow_redirects=True)
    sha.update(asset.content)
    sha = sha.hexdigest()
    log.info(f"computed {sha} for {asset_name} -  {release_tag}")
    return sha

def get_all_release_shas(repo):
    assets_list = []
    releases = get_gh_releases(repo)
    for release in releases:
        tag = release['tag_name']
        assets = get_release_assets(repo, tag)
        if assets:
            for asset in assets:
                sha = get_release_assets_sha(repo, tag, asset)
                assets_list.append(f"{tag} - {asset} - {sha}")
        else:
            print(f"{tag} has no assets!")
    # for asset in assets_list:
    #     print(asset)
    return assets_list
#for each release in package-syncer releases, there must be a corresponding package in artifactory:

def get_branch(branch):
    if branch.startswith("release"):
        branch = branch.split('/')[0]
    return branch


branch_map = {"develop":"nightly", "release":"unstable", "master": "stable"}
assets_repo = 'legleux/package-syncer'
all_released = get_all_release_shas(assets_repo)
releases_needed = []

if __name__ == "__main__":
    for release in all_released:

        print((release))
        # breakpoint()
        tag, asset, shasum = release.split(" - ")
        branch, ref = tag.split('_')
        if asset.endswith('deb'):
            branch = get_branch(branch)
            path = get_art_by_sha.search_file_by_sha256('rippled-deb', branch_map[branch], shasum)
            if path:
                log.info(f"already have {release} in art!")
            else:
                log.info(f"Artifactory needs {release}")
                releases_needed.append(release)

    print('Artifactory needs:')
    dl_dir = "artifactory_uploads"
    if not os.path.exists(dl_dir):
        os.mkdir(dl_dir)
    os.chdir(dl_dir)
    for release in releases_needed:
        tag, asset, shasum = release.split(" - ")
        print(release)

        dirname = tag
        if tag.startswith('release'):
            dirname = tag.replace("/", "-")
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        os.chdir(dirname)
        download_release_artifact(assets_repo, tag, asset)
        os.chdir('..')
