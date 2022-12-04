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
REPO = "rippled-deb-test-mirror"

#search_artifactory.py

def search_for_package(package="clio_server", component="nightly", version=None):
    repo = REPO
    url = URL+f"/api/storage/{repo}/pool/{component}"
    # url = f"{URL}/{repo}/pool/{component}/"
    raw_response = requests.get(url, auth=(USER, PASSWORD) )
    response = json.loads(raw_response.content)
    packages = response['children']
    for p in packages:
        fields = p['uri'].split("_")
        if len(fields) > 2:
            # breakpoint()
            # print(fields[1])
            version_found = fields[1]
            if version_found == version:
                # breakpoint()
                return url + p['uri']

def get_pkg_sha(url):
    raw_response = requests.get(url, auth=(USER, PASSWORD) )
    response = json.loads(raw_response.content)
    return response['checksums']['sha256']

    # matches = [ pkg for pkg in packages if pkg['uri'].split('_')[1] == version]
    # return matches
# GET /api/storage/libs-release-local/org/acme
