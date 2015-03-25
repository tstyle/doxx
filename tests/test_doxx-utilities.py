#!/usr/bin/env python
# encoding: utf-8

import sys
import unittest
from doxx.utilities.filesystem import _make_os_dependent_path

class DoxxPathUtilitiesTests(unittest.TestCase):
    
    def setUp(self):
        pass
    
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
    
    
    