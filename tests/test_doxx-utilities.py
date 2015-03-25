#!/usr/bin/env python
# encoding: utf-8

import sys
import shutil
import unittest
from doxx.utilities.filesystem import _make_os_dependent_path, _create_dirs
from Naked.toolshed.system import dir_exists

class DoxxPathUtilitiesTests(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_doxx_rootdir_filepath_returns_filepath(self):
        standard_path = "testfile.txt"
        test_path = _make_os_dependent_path(standard_path)
        self.assertEqual(standard_path, test_path)
    
    def test_doxx_posix_to_posix_paths(self):
        standard_path = "this/is/some/path"
        test_path = _make_os_dependent_path(standard_path)
        
        if sys.platform == "darwin":
            self.assertEqual(standard_path, test_path)
        elif sys.platform.startswith("linux"):
            self.assertEqual(standard_path, test_path)
        elif sys.platform == "win32":
            self.assertEqual(test_path, "this\is\some\path")
        else:
            raise(Exception, "Cannot detect operating system")
        
    def test_doxx_posix_to_posix_paths_with_endslash(self):
        standard_path = "this/is/some/path/"
        test_path = _make_os_dependent_path(standard_path)
        
        if sys.platform == "darwin":
            self.assertEqual(standard_path, test_path)
        elif sys.platform.startswith("linux"):
            self.assertEqual(standard_path, test_path)
        elif sys.platform == "win32":
            self.assertEqual(test_path, "this\is\some\path")
        else:
            raise(Exception, "Cannot detect operating system")        
        
    def test_doxx_dos_to_posix_paths(self):
        standard_path = "this\is\some\path"
        test_path = _make_os_dependent_path(standard_path)
        
        if sys.platform == "darwin":
            self.assertEqual(test_path, "this/is/some/path")
        elif sys.platform.startswith("linux"):
            self.assertEqual(test_path, "this/is/some/path")
        elif sys.platform == "win32":
            self.assertEqual(test_path, "this\is\some\path")
        else:
            raise(Exception, "Cannot detect operating system")   
    
    
class DoxxDirectoryUtilitiesTest(unittest.TestCase):
    
    def setUp(self):
        self.testpath1 = "utilities-tests/testdir1"  # exists
        self.testpath2 = "utilities-tests/testdir2"  # does not exist
        self.testpath2_missingdir = "utilities-tests/testdir2/testfile.txt"
        if dir_exists(self.testpath2):
            shutil.rmtree(self.testpath2)
            
    def test_doxx_make_dirs_exists(self):
        _create_dirs(self.testpath1)
        self.assertTrue(dir_exists(self.testpath1))
        
    def test_doxx_make_dirs_nonexist(self):
        self.assertFalse(dir_exists(self.testpath2))
        _create_dirs(self.testpath2_missingdir)
        self.assertTrue(dir_exists(self.testpath2))
        shutil.rmtree(self.testpath2)
    
    