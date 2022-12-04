from requests import post, get
import json, re
import subprocess as sp
import os
import sys
from logger import log
from dotenv import dotenv_values
# OWNER = "XRPLF"
# REPO = "clio"
OWNER = "XRPLF"
REPO = "clio"
URL = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/artifacts"

if os.environ.get('GITHUB_ACTIONS'):
  TOKEN = os.environ['PAT_TOKEN']
else:
  TOKEN = dotenv_values().get('PAT_TOKEN')

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}"
}

def get_artifacts(url=URL, page=1):

  try:
    url=URL+f"?page={page}"
    raw_response = get(url, headers=headers)
    response = json.loads(raw_response.content)
  except Exception as e:
    log.error("Couldn't get all artifact URLs")
    log.error(e)

  # try:
  #   breakpoint()
  #   artifacts = response['artifacts'][0]
  # except KeyError as e:
  #   log.error("Couldn't find any artifacts")
  #   log.error(e)
  #   # NOTE: pagination set to 100 in URL, hopefully that'll always be enough
  # # print(artifacts['workflow_run']['head_sha'])
  # dl_url = artifacts['archive_download_url']
  # wf_url = artifacts['url']
  # r = get(dl_url, headers=headers, allow_redirects=True)
  return response['artifacts']


def get_latest_artifact_urls(package, git_rev, branch, page=1):
  pkg_names = [f"clio_{pkg_type}_packages" for pkg_type in ['rpm', 'deb']]
  no_pkg_found = True
  page = 1
  last_page = 10
  last_workflow_run = None
  while(no_pkg_found and page != last_page):
    log.debug(f"Checking page: {page}")
    all_artifacts = get_artifacts(URL, page=page)
    # breakpoint()
    artifacts = [artifact for artifact in all_artifacts if artifact['name'] in pkg_names ]
    artifacts_from_branch = [ a for a in artifacts if a['workflow_run']['head_sha'] == git_rev and a['workflow_run']['head_branch'] == branch]
    if artifacts_from_branch:
      # TODO: go back and get the last workflow somehow
      last_workflow_id = artifacts_from_branch[0]['workflow_run']['id']
      last_workflow_run = [wf for wf in artifacts_from_branch if wf['workflow_run']['id'] == last_workflow_id]
      no_pkg_found = False
    page += 1
  return last_workflow_run


def download_artifact(artifact_json):
    dl_url = artifact_json['archive_download_url']
    name =  artifact_json['name']
    # breakpoint()
    # filename = name.split('-')[3]
    log.debug(f"Trying to download: {name} from {dl_url}")
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
    log.debug(f"Downloaded: {artifact}\n")


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
  log.debug("Getting latest artifacts:") # for {package}, {git_rev}, {branch}")
  log.debug(f"\tPackage: {package}")
  log.debug(f"\tBranch: {branch}")
  log.debug(f"\tGit ref: {git_rev}")
  artifacts = get_latest_artifact_urls(package, git_rev, branch)
  # breakpoint()
  pkg_shas = []
  if artifacts:
    for art in artifacts:
      download_artifact(art)
  else:
    log.debug(f"Couldn't find {package} built from {git_rev} in {branch} branch")
    print(f"Couldn't find {package} built from {git_rev} in {branch} branch")

  # for info in pkg_shas:
  #   print(f"File: {info[0]}\nsha256: {info[1]}")
