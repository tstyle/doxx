#!/usr/bin/env python
# encoding: utf-8

import os
import unittest
import shutil

from Naked.toolshed.shell import muterun
from Naked.toolshed.system import file_exists, dir_exists

from doxx.commands.make import Maker

class DoxxMakeCommandTests(unittest.TestCase):
    
    def setUp(self):
        self.cwd = os.getcwd()
        self.test_dir = "make-tests"
        self.template_file = "stub.doxt"
        self.templates_dir = "templates"
        
        # paths (with test_dir as root directory)
        self.template_file_path = os.path.join(self.templates_dir, self.template_file)
        self.key_file_path = "key.yaml"
        self.pkey_file_path = "pkey.yaml"
        self.projyaml_file_path = "project.yaml"
        
        # clean up directory from last test run (if any files left over)
        # remove key file
        if file_exists(os.path.join(self.test_dir, self.key_file_path)):
            os.remove(os.path.join(self.test_dir, self.key_file_path))
            if file_exists(os.path.join(self.test_dir, self.key_file_path)):
                stderr("Unable to remove test file '" + os.path.join(self.test_dir, self.key_file_path) + "' for make command tests")
                
        # remove template file
        if file_exists(os.path.join(self.test_dir, self.template_file_path)):
            os.remove(os.path.join(self.test_dir, self.template_file_path))
            if file_exists(os.path.join(self.test_dir, self.template_file_path)):
                stderr("Unable to remove test file '" + os.path.join(self.test_dir, self.template_file_path) + "' for make command tests")
                
        if file_exists(os.path.join(self.test_dir, self.pkey_file_path)):
            os.remove(os.path.join(self.test_dir, self.pkey_file_path))
            if file_exists(os.path.join(self.test_dir, self.pkey_file_path)):
                stderr("Unable to remove test file '" + os.path.join(self.test_dir, self.pkey_file_path) + "' for make command tests")
                
        if file_exists(os.path.join(self.test_dir, self.projyaml_file_path)):
            os.remove(os.path.join(self.test_dir, self.projyaml_file_path))
            if file_exists(os.path.join(self.test_dir, self.projyaml_file_path)):
                stderr("Unable to remove test file '" + os.path.join(self.test_dir, self.projyaml_file_path) + "' for make command tests")
                
        # remove templates directory and any files in the directory
        if dir_exists(os.path.join(self.test_dir, self.templates_dir)):
            shutil.rmtree(os.path.join(self.test_dir, self.templates_dir))
            
            
    def test_make_key_file(self):
        try:
            os.chdir(self.test_dir)
            response = muterun('doxx make key')
            if not response.exitcode == 0:
                stderr("Error with 'doxx make key' command. Error: " + response.stderr, exit=1)
            else:
                self.assertTrue(file_exists(self.key_file_path))  # confirm that the key file was made
                os.remove(self.key_file_path)  # remove the test file after the test
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
    
    def test_make_template_file(self):
        try:
            os.chdir(self.test_dir)
            response = muterun('doxx make template')
            if not response.exitcode == 0:
                stderr("Error with 'doxx make template' command. Error: " + response.stderr, exit=1)
            else:
                self.assertTrue(file_exists(self.template_file))  # confirm that the template file was made
                os.remove(self.template_file)  # remove the test file after the test
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e        
    
    def test_make_project(self):
        try:
            os.chdir(self.test_dir)
            response = muterun('doxx make project')
            if not response.exitcode == 0:
                stderr("Error with 'doxx make project' command. Error: " + response.stderr, exit=1)
            else:
                self.assertTrue(file_exists(self.pkey_file_path))  # confirm that the pkey.yaml file was made
                self.assertTrue(file_exists(self.projyaml_file_path))  # confirm that the project.yaml file was made
                self.assertTrue(file_exists(self.template_file_path))  # confirm that the template file was made
                self.assertTrue(dir_exists(self.templates_dir))  # confirm that the 'templates' directory was made
                os.remove(self.pkey_file_path)  # remove the test key file after the test
                os.remove(self.projyaml_file_path)
                os.remove(self.template_file_path)  # remove the test template file
                shutil.rmtree(self.templates_dir)  # remove the templates directory
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e        