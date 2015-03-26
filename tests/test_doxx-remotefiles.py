#!/usr/bin/env python
# encoding: utf-8

import os
import shutil
import unittest

from Naked.toolshed.system import file_exists, dir_exists
from doxx.datatypes.remotefiles import pull_textfile_runner, pull_binaryfile_runner, pull_github_repo_runner

class DoxxTextFileKeyBuildSpecPullTests(unittest.TestCase):
    
    def setUp(self):
        self.cwd = os.getcwd()
        self.test_dir = "pull-tests/remotefiles"
        self.test_text_file_dict = {"testfile.txt": "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/testfile.txt"}
        self.test_text_file_two_dict = {"testfile": "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/testfile"}
        self.test_text_file_three_dict = {"existdir/testfile.txt": "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/testfile.txt"}
        self.test_text_file_four_dict = {"nonexistdir/testfile.txt": "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/testfile.txt"}
        
        self.test_multi_text_files_dict = {"testfile.txt": "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/testfile.txt", "testfile": "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/testfile"}
        self.test_multi_text_files_two_dict = {"existdir/testfile.txt": "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/testfile.txt", "nonexistdir/testfile": "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/testfile"} 
        
        self.test_bad_text_file_dict = {"testfile.txt": "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/nonexistenttextfile.txt"}
        
        # remove test files and directories if they exist from last test
        if file_exists("pull-tests/remotefiles/testfile.txt"):
            os.remove("pull-tests/remotefiles/testfile.txt")
            self.assertFalse(file_exists("pull-tests/remotefiles/testfile.txt"))
            
        if file_exists("pull-tests/remotefiles/existdir/testfile.txt"):
            os.remove("pull-tests/remotefiles/existdir/testfile.txt")
            self.assertFalse(file_exists("pull-tests/remotefiles/existdir/testfile.txt"))
            
        if dir_exists("pull-tests/nonexistdir"):
            shutil.rmtree("pull-tests/nonexistdir")
            self.assertFalse(dir_exists("pull-tests/nonexistdir"))
        
    def test_doxx_pull_single_text_file_remotefiles_module(self):
        try:
            os.chdir(self.test_dir)
            local_writepath = "testfile.txt"
            pull_textfile_runner(self.test_text_file_dict)
            self.assertTrue(file_exists(local_writepath))
            os.remove(local_writepath)
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
    def test_doxx_pull_single_text_file_noextension_remotefiles_module(self):
        try:
            os.chdir(self.test_dir)
            local_writepath = "testfile"
            pull_textfile_runner(self.test_text_file_two_dict)
            self.assertTrue(file_exists(local_writepath))
            os.remove(local_writepath)
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
    def test_doxx_pull_single_text_file_existdirpath_remotefiles_module(self):
        try:
            os.chdir(self.test_dir)
            local_writepath = "existdir/testfile.txt"
            pull_textfile_runner(self.test_text_file_three_dict)
            self.assertTrue(file_exists(local_writepath))
            os.remove(local_writepath)
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
    def test_doxx_pull_single_text_file_nonexistdirpath_remotefiles_module(self):
        try:
            os.chdir(self.test_dir)
            local_writepath = "nonexistdir/testfile.txt"
            pull_textfile_runner(self.test_text_file_four_dict)
            self.assertTrue(file_exists(local_writepath))
            shutil.rmtree("nonexistdir")
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e        
    
    def test_doxx_pull_multiple_text_files_remotefiles_module(self):
        try:
            os.chdir(self.test_dir)
            local_writepath_one = "testfile.txt"
            local_writepath_two = "testfile"
            pull_textfile_runner(self.test_multi_text_files_dict)
            self.assertTrue(file_exists(local_writepath_one))
            self.assertTrue(file_exists(local_writepath_two))
            os.remove(local_writepath_one)
            os.remove(local_writepath_two)
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
    def test_doxx_pull_multiple_text_files_subdirs_remotefiles_module(self):
        try:
            os.chdir(self.test_dir)
            local_writepath_one = "existdir/testfile.txt"
            local_writepath_two = "nonexistdir/testfile"
            pull_textfile_runner(self.test_multi_text_files_two_dict)
            self.assertTrue(file_exists(local_writepath_one))
            self.assertTrue(file_exists(local_writepath_two))
            os.remove(local_writepath_one)
            shutil.rmtree("nonexistdir")
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e        
    
    
    def test_doxx_pull_badURL_text_file_remotefiles_module(self):
        try:
            os.chdir(self.test_dir)
            local_writepath = "testfile.txt"
            with self.assertRaises(SystemExit):
                pull_textfile_runner(self.test_bad_text_file_dict)
            self.assertFalse(file_exists(local_writepath))
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e         
    
    
class DoxxBinaryFileKeyBuildSpecPullTest(unittest.TestCase):
    
    def setUp(self):
        self.test_binary_file = "https://github.com/bit-store/testfiles/raw/master/doxx/pull-tests/packed.tar.gz"
    
class DoxxGithubRepoKeyBuildSpecPullTest(unittest.TestCase):
    
    def setUp(self):
        self.test_gh_repo = "https://github.com/bit-store/testfiles/archive/master.tar.gz"
    