import requests
import subprocess
PAT_TOKEN="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"
PACKAGE_NAME = "clio_rpm_packages"
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization" : f"Bearer {PAT_TOKEN}",
    "X-GitHub-Api-Version" : "2022-11-28"
}
OWNER = "legleux"
REPO = "clio"

def get_artifact(branch):
    s = requests.Session()
    s.headers.update(headers)
    URL = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/artifacts"
    result = s.get(URL) # , json=body)
    data = result.json()
    artifacts = data['artifacts']
    develop_artifacts = [artifact for artifact in artifacts if artifact['workflow_run']['head_branch'] == branch and artifact['name'] == PACKAGE_NAME]
    art = develop_artifacts[0]
    breakpoint()
    dl_url = art['archive_download_url']
    name = art['name']
    redir = s.get(dl_url, allow_redirects=False)

    filename = art['name']
    dl_url = redir.headers['Location']
    r = s.get(dl_url, headers=headers, allow_redirects=True)
    zip_file = open(f"{filename}.zip", 'wb')
    zip_file.write(r.content)
    zip_file.close()
    return filename, art['workflow_run']['head_sha']
