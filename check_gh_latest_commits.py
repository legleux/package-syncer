import requests
import json

USERNAME = "XRPLF"
REPOSITORY = "clio"
# USERNAME = "legleux"
REPOSITORY = "clio"
REPO=f"{USERNAME}/{REPOSITORY}"
# BRANCH = "develop"
BRANCHES_URL = f"https://api.github.com/repos/{REPO}/branches?per_page=100"
TAGS_URL = f"https://api.github.com/repos/{REPO}/git/ref/tags"
# URL = f"https://api.github.com/repos/{REPO}/commits/{BRANCH}"


def get_hash_from_tag(tag):
    url = TAGS_URL + f"/{tag}"
    response = requests.get(url)
    resp = json.loads(response.content)
    try:
        sha = resp['object']['sha']
        return sha
    except Exception as e:
        if resp:
            print(resp)
            print(f"Couldn't find tag: {tag}")
            print(str(e))

def get_last_commits_from_target_branches():
    response = requests.get(BRANCHES_URL)
    all_branches = json.loads(response.content)
    # TODO: match release/x.y.z[-bN,-rcN] better
    branches = [branch for branch in all_branches if branch['name'] in ['develop', 'master'] or branch['name'].startswith('release')]
    shas = [(branch['name'], branch['commit']['sha']) for branch in branches]
    return shas
