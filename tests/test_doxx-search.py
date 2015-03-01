#!/usr/bin/env python
# encoding: utf-8

import os
import unittest

from Naked.toolshed.system import file_exists, dir_exists

from doxx.commands.search import run_search
from doxx.commands.whatis import run_whatis
from doxx.datatypes.cache import DoxxCache

class DoxxSearchCommandTests(unittest.TestCase):
    
    def setUp(self):
        d = DoxxCache()
        self.cache_directory = d._get_platform_specific_cache_dirpath()
        self.package_list_path = 'list.txt'
        self.cached_package_list_path = os.path.join(self.cache_directory, self.package_list_path)
        
        if file_exists(self.cached_package_list_path):
            os.remove(self.cached_package_list_path)  # remove any cached files to begin tests
        
    def test_doxx_search_command(self):
        run_search('license')  # confirm that this does not raise Exception when downloads new package list
        if not file_exists(self.cached_package_list_path):
            stderr("The cached list.txt file was not generated following execution of the doxx search command", exit=1)
        run_search('license')  # execute it a second time to confirm that it does not raise Exception when it runs from the cached file
            
    
    
class DoxxWhatisCommandTests(unittest.TestCase):
    
    def setUp(self):
        d = DoxxCache()
        self.cache_directory = d._get_platform_specific_cache_dirpath()
        self.package_json_path = 'packages.json'
        self.cached_package_json_path = os.path.join(self.cache_directory, self.package_json_path)
    
        if file_exists(self.cached_package_json_path):
            os.remove(self.cached_package_json_path)  # remove any cached files to begin tests        
        
    def test_doxx_whatis_command_good_package(self):
        run_whatis('license-mit')  # assert that is does not raise Exception when downloads new packages.json data
        run_whatis('license-mit')  # execute it again to confirm that it runs without issues with the cached file after the first run
        
    def test_doxx_whatis_command_missing_package(self):
        with self.assertRaises(SystemExit):
            run_whatis('completely-bogus-package')
        self.assertTrue(file_exists(self.cached_package_json_path))  # confirm that despite the exception, a cached packages.json file was generated