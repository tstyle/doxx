#!/usr/bin/env python
# encoding: utf-8

import json
from Naked.toolshed.network import HTTP

url = "https://api.github.com/orgs/doxx-repo/repos"

http = HTTP(url)
the_json = http.get()
json_obj = json.loads(the_json)

repo_list = []

for x in xrange(len(json_obj)):
    repository_name = json_obj[x]['name']
    if repository_name == "bin":
        pass
    elif repository_name == "master":
        pass
    else:
        repo_list.append(repository_name)
        
print(sorted(repo_list))