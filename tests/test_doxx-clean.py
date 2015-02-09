#!/usr/bin/env python
# encoding: utf-8

import os
import unittest
from Naked.toolshed.system import make_path, file_exists, dir_exists
from Naked.toolshed.file import FileWriter

from doxx.commands.clean import run_clean

class DoxxCleanCommandTests(unittest.TestCase):
    
    def setUp(self):
        self.onlytemplates_dir = "clean-tests/with-only-templates"
        self.otherfiles_dir = "clean-tests/with-templates-other-files"
        self.replace_test_files()  # set up the test directories with the test files (removed during last test run)
        self.cwd = os.getcwd()
        
    def replace_test_files(self):
        """replace the erased test files in the test directories"""
        # replace the files in the with-only-templates directory
          # make the directory
        if not dir_exists(make_path(self.onlytemplates_dir, 'templates')):
            os.makedirs(make_path(self.onlytemplates_dir, 'templates'))
            
        with_only_templates_files = ['key.yaml', 'pkey.yaml', 'project.yaml', 'templates/404.doxt', 'templates/index.doxt', 'templates/normalize.doxt']
        
        for the_file in with_only_templates_files:
            fw = FileWriter(make_path(self.onlytemplates_dir, the_file))
            fw.write("unimportant text")
            
        # replace the files in the with-templates-other-files directory
            # make the directory if not present
        if not dir_exists(make_path(self.otherfiles_dir, 'templates')):
            os.makedirs(make_path(self.otherfiles_dir, 'templates'))
            
        with_other_files = ['key.yaml', 'pkey.yaml', 'project.yaml', 'templates/404.doxt', 'templates/index.doxt', 'templates/normalize.doxt', 'templates/dontdeleteme.txt']
        for the_file in with_other_files:
            fw = FileWriter(make_path(self.otherfiles_dir, the_file))
            fw.write("unimportant text")
            
    
    def test_doxx_clean_only_templates_in_directory(self):
        try:
            os.chdir('clean-tests/with-only-templates')
            # confirm files present before clean is executed
            self.assertTrue(file_exists('key.yaml'))
            self.assertTrue(file_exists('pkey.yaml'))
            self.assertTrue(file_exists('project.yaml'))
            self.assertTrue(file_exists('templates/404.doxt'))
            self.assertTrue(file_exists('templates/index.doxt'))
            self.assertTrue(file_exists('templates/normalize.doxt'))
            
            # execute clean
            run_clean()
            
            # confirm that the files are now gone
            self.assertFalse(file_exists('key.yaml'))
            self.assertFalse(file_exists('pkey.yaml'))
            self.assertFalse(file_exists('project.yaml'))
            self.assertFalse(file_exists('templates/404.doxt'))
            self.assertFalse(file_exists('templates/index.doxt'))
            self.assertFalse(file_exists('templates/normalize.doxt'))
            
            # confirm that the templates directory was removed
            self.assertFalse(dir_exists('templates'))
            
            # confirm that the other project files are still present
            self.assertTrue(file_exists('crossdomain.xml'))
            self.assertTrue(file_exists('index.html'))
            self.assertTrue(file_exists('humans.txt'))
            self.assertTrue(file_exists('robots.txt'))
            
            # return to the testing working directory
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)  # make sure that the CWD is re-established before rasing the exception
            raise e
            
        
    def test_doxx_clean_other_files_in_templates_directory(self):
        try:
            os.chdir('clean-tests/with-templates-other-files')
            # confirm files present before clean is executed
            self.assertTrue(file_exists('key.yaml'))
            self.assertTrue(file_exists('pkey.yaml'))
            self.assertTrue(file_exists('project.yaml'))
            self.assertTrue(file_exists('templates/404.doxt'))
            self.assertTrue(file_exists('templates/index.doxt'))
            self.assertTrue(file_exists('templates/normalize.doxt'))

            # execute clean
            run_clean()

            # confirm that the files are now gone
            self.assertFalse(file_exists('key.yaml'))
            self.assertFalse(file_exists('pkey.yaml'))
            self.assertFalse(file_exists('project.yaml'))
            self.assertFalse(file_exists('templates/404.doxt'))
            self.assertFalse(file_exists('templates/index.doxt'))
            self.assertFalse(file_exists('templates/normalize.doxt'))

            # confirm that the templates directory is still present
            self.assertTrue(dir_exists('templates'))
            
            # and that the non-doxx file that was present in it is still there
            self.assertTrue(file_exists('templates/dontdeleteme.txt'))

            # confirm that the other project files are still present
            self.assertTrue(file_exists('crossdomain.xml'))
            self.assertTrue(file_exists('index.html'))
            self.assertTrue(file_exists('humans.txt'))
            self.assertTrue(file_exists('robots.txt'))

            # return to the testing working directory
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)  # make sure that the CWD is re-established before rasing the exception
            raise e