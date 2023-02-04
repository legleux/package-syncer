import requests
import subprocess

PACKAGE_NAME = "clio_deb_packages"
headers = {
    "Accept": "application/vnd.github+json",
    # "Authorization" : f"Bearer {PAT_TOKEN}",
    "X-GitHub-Api-Version" : "2022-11-28"
}
OWNER = "legleux"
REPO = "clio"



s = requests.Session()
s.headers.update(headers)
URL = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/artifacts"
result = s.get(URL) # , json=body)
data = result.json()
breakpoint()
# URL = "https://api.github.com/repos/XRPLF/clio/actions/artifacts/539216767/zip"
# result = s.get(URL)
artifacts = data['artifacts']
develop_artifacts = [artifact for artifact in artifacts if artifact['workflow_run']['head_branch'] == 'develop' and artifact['name'] == PACKAGE_NAME]
# for art in develop_artifacts:
#     dl_url = art['archive_download_url']
#     name =  art['name']
#     print(f"{name}  {dl_url}")
art = develop_artifacts[0]
dl_url = art['archive_download_url']
filename = art['name']
# breakpoint()
r = s.get(dl_url, headers=headers, allow_redirects=True)
zip_file = open(f"{filename}.zip", 'wb')
zip_file.write(r.content)
zip_file.close()
# o = subprocess.check_output(['unzip', filename])
# zip_output = o.decode()
# print(zip_output)
