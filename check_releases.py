from requests import post, get
import json
import os
from dotenv import dotenv_values
import hashlib

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

headers = {"Accept": "application/vnd.github+json","Authorization": f"Bearer {TOKEN}"}

def get_release_assets_sha(repo, release_tag, asset_name):
    url = f"https://github.com/{repo}releases/download/{release_tag}/{asset_name}"
    sha = hashlib.sha256()
    asset = get(url, headers=headers, allow_redirects=True)
    sha.update(asset.content)
    return sha.hexdigest()

#for each release in package-syncer releases, there must be a corresponding package in artifactory:

branch_map = {"nightly":"develop", "unstable":"release", "stable": "main"}
