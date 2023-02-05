from upload_to_art import upload_package_to_artifactory
from get_latest_workflow_artifact import get_artifact
import requests
import subprocess
import re
s = requests.Session()
# headers = {"Authorization":"token "}
# s.headers.update(headers)

# download from nigthly release branch

filename, rev = get_artifact('develop')

# check if hash in art

# sign

# create correct metadata

# unzip
o = subprocess.check_output(['unzip', filename])
zip_output = o.decode()
# breakpoint()
print(zip_output)
RE = re.compile('inflating: (.*deb|.*rpm)')
matches = re.search(RE, zip_output)
name = matches[1]
# upload to art
filename = name
component = "nightly"
print(f"filename: {filename}")
args = [filename, component, rev]
results = upload_package_to_artifactory(args)
print(results)
