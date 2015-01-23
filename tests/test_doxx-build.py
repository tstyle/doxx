#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import unicodedata
from Naked.toolshed.system import make_path, file_exists
from Naked.toolshed.file import FileReader
from doxx.datatypes.key import DoxxKey
from doxx.commands.build import Builder

from Naked.toolshed.python import is_py2, is_py3


# single template, ASCII text build test
class DoxxLocalMITLicenseBuildTests(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.getcwd()
        self.mit_standard = "standards/mit-license.txt"
        self.mit_test_dir = "build-tests/mit-license"
        self.mit_key = "key.yaml"  # executed inside the mit testing directory, no directory path necessary
        
        mit_std_reader = FileReader(self.mit_standard)
        self.mit_standard_text = mit_std_reader.read()
        
    def tearDown(self):
        pass
    
    def test_mit_license_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            doxxkey = DoxxKey(self.mit_key)
            b = Builder()
            b.run(doxxkey)
            self.assertTrue(file_exists('LICENSE'))                  # confirm that the rendered file write took place
            fr = FileReader('LICENSE')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('LICENSE')  # remove the rendered file to prepare directory for new tests
        except Exception as e:
            if file_exists('LICENSE'):
                os.remove('LICENSE')    # remove the generated LICENSE file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e
        
    # test build with new destination directory path
    # test build with extension assigned
    # test build with a different file name
    
    