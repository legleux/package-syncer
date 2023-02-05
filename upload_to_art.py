import subprocess
import sys, os, json
from dotenv import dotenv_values
import requests
dotenv_values()

ARTIFACTORY ="https://artifactory.ops.ripple.com"
USER = dotenv_values().get('USER')
PASSWORD = dotenv_values().get('USER_ART_KEY')
ARCHITECTURE="amd_64"
URL = f"https://artifactory.ops.ripple.com:443/artifactory"


def upload_package(url, pkg):
    fileName = pkg
    filePath = os.path.abspath(fileName)
    headers = {'Content-type': 'application/octet-stream', 'Slug': fileName}
    resp = requests.put(url, data=open(filePath, 'rb'), headers=headers, auth=(USER, PASSWORD))
    # breakpoint()
    return json.loads(resp.content)


def upload_dpkg(args):
    pkg, component, git_rev = args
    repo = "rippled-deb-test-mirror"
    distros_matrix="deb.distribution=jammy"
    url = f"{URL}/{repo}/pool/{component}/{pkg};{distros_matrix};deb.component={component};deb.architecture={ARCHITECTURE};deb.git_rev={git_rev}"
    return upload_package(url, pkg)


def upload_rpm(args):
    pkg, component, git_rev = args
    repo = "rippled-rpm-test-mirror"
    url = f"{URL}/{repo}/{component}/{pkg};rpm.git_rev={git_rev}"
    return upload_package(url, pkg)


## args pkg, compoenent, git_ref
def upload_package_to_artifactory(args):
  pkg = args[0]
  try:
    if pkg.endswith(".deb"):
      result = upload_dpkg(args)
    elif pkg.endswith(".rpm"):
      result = upload_rpm(args)
  except Exception as e:
    print(f"error: {e}")

  return result


if __name__ == "__main__":
  print(upload_package_to_artifactory(sys.argv[1:]))
