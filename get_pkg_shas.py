import subprocess
import sys, os, json
from dotenv import dotenv_values
import requests
import argparse

dotenv_values()

ARTIFACTORY ="https://artifactory.ops.ripple.com"
USER = dotenv_values().get('USER')
PASSWORD = dotenv_values().get('USER_ART_KEY')
ARCHITECTURE="amd_64"
URL = f"https://artifactory.ops.ripple.com:443/artifactory"

artifact = ""
repo = "rippled-deb-test-mirror"
component = "nightly"
pkg = "clio_1.0.2_all.deb"
url = f"{URL}/{repo}/pool/{component}/{pkg}"
properties = "?properties\deb.component=nightly\deb.name=clio"
url = f"{url}{properties}"
# headers = {'Content-type': 'application/octet-stream', 'Slug': fileName}
# resp = requests.get(url, headers=headers, auth=(USER, PASSWORD))

def get(url):
    resp = requests.get(url, auth=(USER, PASSWORD))
    return resp

# project = "clio"
# component="nightly"
# url = f"{URL}/api/storage/rippled-deb-test-mirror/pool/nightly"
# x = get(url)
# s = json.loads(x.content)
# pkgs = []
# for pkg in s['children']:
#     # breakpoint()
#     if pkg['uri'].startswith(f"/{project}"):
#         pkgs.append(pkg['uri'])
# # breakpoint()
# pkg_shas = []
# for pkg in pkgs:
#     # breakpoint()
#     pkg_info = get(f"{url}/{pkg}")
#     pkg_info = json.loads(pkg_info.content)
#     pkg_shas.append(f"{pkg} - {pkg_info['checksums']['sha256']}")

# for pkg in pkg_shas:
#     print(pkg)

def get_pkg_sha(component, pkg):
    url = f"{URL}/api/storage/rippled-deb-test-mirror/pool/{component}"
    pkg_info = get(f"{url}/{pkg}")
    pkg_info = json.loads(pkg_info.content)
    return pkg_info['checksums']['sha256']


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("component")
    parser.add_argument("package")
    # parser.add_argument("version")
    args = parser.parse_args()
    com, pkg = args.component, args.package
    sha256 = get_pkg_sha(com, pkg)
    print(sha256)
