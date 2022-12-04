from requests import post, get
import json, re
import subprocess as sp
import os
import sys
from logger import log
from dotenv import dotenv_values
# OWNER = "XRPLF"
# REPO = "clio"
OWNER = "legleux"
REPO = "clio"
URL = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/artifacts?per_page=100"

if os.environ.get('GITHUB_ACTIONS'):
  TOKEN = os.environ['PAT_TOKEN']
else:
  TOKEN = dotenv_values().get('PAT_TOKEN')

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}"
}

def get_artifacts(url=URL, num=0):
  try:
    resp = json.loads(get(url, headers=headers).content)
  # breakpoint()
  except Exception as e:
    log.error("Couldn't get all artifact URLs")
    log.error(e)

  try:
    artifacts = resp['artifacts'][num]
  except KeyError as e:
    log.error("Couldn't find any artifacts")
    log.error(e)
    # NOTE: pagination set to 100 in URL, hopefully that'll always be enough
  # print(artifacts['workflow_run']['head_sha'])
  dl_url = artifacts['archive_download_url']
  wf_url = artifacts['url']
  r = get(dl_url, headers=headers, allow_redirects=True)
  return resp['artifacts']


def get_latest_artifact_urls(package, git_rev, branch):
  pkg_names = [f"clio_{pkg_type}_packages" for pkg_type in ['rpm', 'deb']]
  found_pkg = False
  all_artifacts = get_artifacts(URL, 0)
  breakpoint()
  artifacts = [artifact for artifact in all_artifacts if artifact['name'] in pkg_names ]
  # breakpoint()
  a = [ a for a in artifacts if a['workflow_run']['head_sha'] == git_rev and a['workflow_run']['head_branch'] == branch]
  if a:
    return a
  else:
    sys.exit(f"Couldn't find {package} built from {git_rev} in {branch} branch")

  # for i in a:
  #   print(i['archive_download_url'])


def download_artifact(artifact_json):
    dl_url = artifact_json['archive_download_url']
    name =  artifact_json['name']
    # breakpoint()
    # filename = name.split('-')[3]
    log.debug(f"Downloading: {name} from {dl_url}")
    r = get(dl_url, headers=headers, allow_redirects=True)
    zip_file = open(name, 'wb')
    zip_file.write(r.content)
    zip_file.close()
    o = sp.check_output(['unzip', name])
    zip_output = o.decode()
    # archive_name = re.search("Archive: *(.*)\\n", zip_output)[1]
    artifact = re.search("inflating: (\S*)", zip_output)[1]
    # return the filename and sha256s

    # sha_output = sp.check_output(['sha256sum', artifact_name])
    # sha = sha_output.decode().split(' ')[0]
    ## or
    # breakpoint()
    # sha = name.split('-')[2]
    # return (artifact, sha)
    print(f"Downloaded: {artifact}\n")

def get_artifact_shas(url):
  # this is wrong bc "get_artifacts" is only getting the latest artifacts
  artifacts = get_artifacts(url)
  # TODO: This could match incorrectly names releases
  breakpoint()
  shas = [ f"{a['name'].split('-')[0]} - {a['name'].split('-')[2]}" for a in artifacts if len(a['name'].split("-")) == 4]
  return shas


if __name__ == "__main__":
  package = sys.argv[1]
  git_rev = sys.argv[2]
  branch = sys.argv[3]
  artifacts = get_latest_artifact_urls(package, git_rev, branch)
  # breakpoint()
  pkg_shas = []

  for art in artifacts:
    # pkg_shas.append(download_artifact(art))
    download_artifact(art)

  # for info in pkg_shas:
  #   print(f"File: {info[0]}\nsha256: {info[1]}")
