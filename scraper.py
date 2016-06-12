# encoding: utf-8

from github3 import login
import json

try:  # input was named raw_input in Python 2
    input = raw_input
except NameError:
    pass

token = input("Enter Auth Token (https://github.com/settings/tokens/new)\n")

gh = login(token=token)
metadata = {}
counter = 0

print("fetching all repository metadata")
for r in gh.repositories():
    metadata[r.name] = {
        "langs": {l[0]: l[1] for l in r.languages()},
        "contributors": [cs.as_dict() for cs in r.contributor_statistics()]}
    counter += 1
    if counter % 10 == 0:
        print counter

print("writing data to disk")
with open("github_repository_dump.json", 'w') as f:
    f.write(json.dumps(metadata))
