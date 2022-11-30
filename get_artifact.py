from requests import post, get
import json, re
import subprocess as sp
import os
import sys
from dotenv import dotenv_values
# OWNER = "XRPLF"
# REPO = "clio"
OWNER = "legleux"
REPO = "test_repo"
URL = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/artifacts"

if os.environ.get('GITHUB_ACTIONS'):
  TOKEN = os.environ['PAT_TOKEN']
else:
  TOKEN = dotenv_values().get('PAT_TOKEN')

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}"
}

def get_artifacts():
  resp = json.loads(get(URL, headers=headers).content)
  artifacts = resp['artifacts'][0]
  # print(artifacts['workflow_run']['head_sha'])
  dl_url = artifacts['archive_download_url']
  wf_url = artifacts['url']
  r = get(dl_url, headers=headers, allow_redirects=True)
  return resp['artifacts']

def get_latest_artifact_urls(git_rev, branch):
  artifacts = get_artifacts()

  a = [ a for a in artifacts if a['workflow_run']['head_sha'] == git_rev and a['workflow_run']['head_branch'] == branch]
  # breakpoint()
  # for i in a:
  #   print(i['archive_download_url'])
  return a

def download_artifact(artifact_json):
    dl_url = artifact_json['archive_download_url']
    name =  artifact_json['name']
    filename = name.split('-')[3]
    r = get(dl_url, headers=headers, allow_redirects=True)
    zip_file = open(name, 'wb')
    zip_file.write(r.content)
    zip_file.close()
    o = sp.check_output(['unzip', name])
    zip_output = o.decode()
    # breakpoint()
    # archive_name = re.search("Archive: *(.*)\\n", zip_output)[1]
    artifact = re.search("inflating: (\S*)", zip_output)[1]
    # return the filename and sha256s

    # sha_output = sp.check_output(['sha256sum', artifact_name])
    # sha = sha_output.decode().split(' ')[0]
    ## or
    sha = name.split('-')[2]
    return (artifact, sha)


git_rev = sys.argv[1]
branch = sys.argv[2]
artifacts = get_latest_artifact_urls(git_rev, branch)
pkg_shas = []

for art in artifacts:
  pkg_shas.append(download_artifact(art))

for info in pkg_shas:
  print(f"File: {info[0]}\nsha256: {info[1]}")
