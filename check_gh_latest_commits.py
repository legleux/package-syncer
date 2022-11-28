import requests
import json

USERNAME = "XRPLF"
REPOSITORY = "clio"
USERNAME = "legleux"
REPOSITORY = "test_repo"
REPO=f"{USERNAME}/{REPOSITORY}"
BRANCH = "develop"
BRANCHES_URL = f"https://api.github.com/repos/{REPO}/branches"
TAGS_URL = f"https://api.github.com/repos/{REPO}/git/ref/tags"
URL = f"https://api.github.com/repos/{REPO}/commits/{BRANCH}"


def get_hash_from_tag(tag):
    url = TAGS_URL + f"/{tag}"
    response = requests.get(url)
    resp = json.loads(response.content)
    breakpoint()
    return resp['object']['sha']

def get_branch_sha():
    response = requests.get(BRANCHES_URL)
    res = response.content
    branches = json.loads(res)
    branches = [branch for branch in branches if branch['name'] in ['develop', 'main'] or branch['name'].startswith('release')]
# print(branches)
    shas = [(branch['name'], branch['commit']['sha']) for branch in branches]
    return shas
