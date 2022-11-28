from requests import post, get
import json
import os
from dotenv import dotenv_values
OWNER = "legleux"
REPOSITORY = "test_repo"
# OWNER = "XRPLF"
# REPOSITORY = "clio"
REPO = f"{OWNER}/{REPOSITORY}"
URL = f"https://api.github.com/repos/{REPO}/actions/artifacts"
if os.environ.get('CI'):
  TOKEN = os.environ['PAT_TOKEN']
else:
  TOKEN = dotenv_values().get('PAT_TOKEN')

def get_releases(repo=REPO):

    headers = {
        "Accept": "application/vnd.github+json",
       "Authorization": f"Bearer {TOKEN}"
    }
    URL = f"https://api.github.com/repos/{repo}/releases"
    resp = json.loads(get(URL, headers=headers).content)
    # breakpoint()
    return resp
