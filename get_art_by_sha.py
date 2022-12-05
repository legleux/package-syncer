import subprocess
import sys, os, json
from dotenv import dotenv_values
import requests
import argparse
from logger import log
dotenv_values()

ARTIFACTORY ="https://artifactory.ops.ripple.com"
USER = dotenv_values().get('USER')
PASSWORD = dotenv_values().get('USER_ART_KEY')
ARCHITECTURE="amd_64"
URL = f"https://artifactory.ops.ripple.com:443/artifactory"
REPO = "rippled-deb-test-mirror"
REPO = "rippled-deb"

#search_artifactory.py

#curl -u<user>:<password> -X POST
    # -k -H 'Content-Type:text/plain'
    # -i https://<artifactory_host>/artifactory/api/search/aql
    # --data 'items.find({"repo": "<repo_name>"}).sort({"$desc" : ["modified"]}).limit(5)'


def search_query():
    # curl -X POST -uUSER:PASSWORD 'http://HOST:PORT/artifactory/api/search/aql' -Taql.query
    url = URL + "/api/search/aql"
    data = 'items.find({"repo": "rippled-deb", "path":"pool/stable"}, {"@deb.name":"clio-server"}).sort({"$desc" : ["modified"]})'
    r = requests.post(url, data=data,  auth=(USER, PASSWORD))

    return json.loads(r.content)


def search_file_by_sha256(repo, component, sha):
    # curl -X POST -uUSER:PASSWORD 'http://HOST:PORT/artifactory/api/search/aql' -Taql.query
    if 'deb' in repo:
        path = f"pool/{component}"
    elif  'rpm' in repo:
        path = f"{component}"

    url = URL + "/api/search/aql"
    data = 'items.find({"repo": "' f"{repo}" '", "path":"' f"{path}" + '"}, {"@sha256":"' + f"{sha}" + '"})'
    r = requests.post(url, data=data,  auth=(USER, PASSWORD))
    # breakpoint()
    try:
        result = json.loads(r.content)['results'][0]
        if result:
            repo, path, name = result['repo'], result['path'], result['name']
            print(f"repo: {repo}")
            print(f"path: {path}")
            print(f"name: {name}")
            print(f"")
            return json.loads(r.content)
        else:
            print("couldn't find!")
    except IndexError as e:
        # TODO: handle this not as an error
        log.debug(f"{repo}, {component}, {sha} not found")
        log.debug(f"{e}")
        return None

def get_rpm_package_url(package="clio_server", component="nightly", version=None):
    repo = "rippled-rpm-test-mirror"
    url = URL+f"/api/storage/{repo}/{component}"
    raw_response = requests.get(url, auth=(USER, PASSWORD) )
    response = json.loads(raw_response.content)
    packages = response['children']
    breakpoint()
    for p in packages:
        fields = p['uri'].split("_")
        if len(fields) > 2:
            # breakpoint()
            # print(fields[1])
            version_found = fields[1]
            if version_found == version:
                # breakpoint()
                return url + p['uri']


def get_deb_package_url(package="clio_server", component="nightly", version=None):
    repo = REPO
    url = URL+f"/api/storage/{repo}/pool/{component}"
    # url = f"{URL}/{repo}/pool/{component}/"
    raw_response = requests.get(url, auth=(USER, PASSWORD) )
    response = json.loads(raw_response.content)
    packages = response['children']
    breakpoint()
    for p in packages:
        fields = p['uri'].split("_")
        if len(fields) > 2:
            # breakpoint()
            # print(fields[1])
            version_found = fields[1]
            if version_found == version:
                # breakpoint()
                return url + p['uri']


def find_rpm_pkg(component, file_name):
    url = f"{URL}/rippled-rpm/{component}/{file_name}"
    raw_response = requests.get(url, auth=(USER, PASSWORD) )
    breakpoint()
    response = json.loads(raw_response.content)

def get_pkg_sha(url):
    raw_response = requests.get(url, auth=(USER, PASSWORD) )
    response = json.loads(raw_response.content)
    return response['checksums']['sha256']

    # matches = [ pkg for pkg in packages if pkg['uri'].split('_')[1] == version]
    # return matches
# GET /api/storage/libs-release-local/org/acme

# data = 'items.find({"repo": "rippled-rpm", "path":"unstable"})'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("repo")
    parser.add_argument("sha")
    # parser.add_argument("version")
    args = parser.parse_args()
    repo, sha = args.repo, args.sha
    search_file_by_sha256(repo, sha)
