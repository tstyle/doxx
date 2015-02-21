#!/usr/bin/env python
# encoding: utf-8

import json
from doxx.datatypes.cache import DoxxCache
from doxx.datatypes.package import OfficialPackage

from Naked.toolshed.network import HTTP
from Naked.toolshed.system import stdout, stderr

def run_whatis(package_name):
    cache = DoxxCache()
    max_cache_seconds = 86400  # 24 hour description file cache
    stdout("[*] doxx: Looking up the package description...")
    if cache.cached_file_exists('packages.json'):
        if cache.does_cache_file_require_update(cache.package_repo_json_file, max_cache_seconds):
            master_descriptions = _pull_official_repository_descriptions()
            cache.cache_packagerepo_json(master_descriptions)
        else:
            master_descriptions = cache.get_cached_packagerepo_json()
    else:
        master_descriptions = _pull_official_repository_descriptions()
        cache.cache_packagerepo_json(master_descriptions)
    
    if len(master_descriptions) > 0:
        descriptions_dict = json.loads(master_descriptions)
        test_package_name = package_name.lower().strip()
        if test_package_name in descriptions_dict:
            stdout(" ")
            stdout("    Package: " + test_package_name)
            stdout("Description: " + descriptions_dict[test_package_name])
        else:
            stderr("[!] doxx: Unable to locate the package '" + test_package_name + "'", exit=1)
    else:
        stderr("[!] doxx: Unable to read the descriptions file.  It appears to be empty...", exit=1)
        

def _pull_official_repository_descriptions():
    package = OfficialPackage()
    master_package_descriptions = package.get_master_package_description_json_url()
    http = HTTP(master_package_descriptions)
    try:
        if http.get_status_ok():
            master_descriptions = http.res.text
            return master_descriptions.strip()
        else:
            stderr("[!] doxx: Unable to pull remote repository descriptions (HTTP status code: " + str(http.res.status_code) + ")", exit=1)
    except Exception as e:
        stderr("[!] doxx: Unable to pull remote repository descriptions Error: " + str(e) + ")", exit=1)