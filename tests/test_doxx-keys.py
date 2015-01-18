#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
from doxx.datatypes.key import DoxxKey

class DoxxASCIIKeysTest(unittest.TestCase):

    def setUp(self):
        self.main_test_dir = os.getcwd()
        self.good_ascii_key_path = "ascii_singletempl_key.yaml"  # need to chdir into keys directory to use this path
        self.good_ascii_key_path_outside = "keys/ascii_singletempl_key.yaml"
        self.good_unicode_key_path = ""
        self.bad_key_path = "boguskey.yaml"

    def tearDown(self):
        pass
    
    ## Single template ASCII key file tests
    
    # test instance attributes on construction
    def test_doxxkey_key_read_successful(self):
        os.chdir('keys')
        key = DoxxKey(self.good_ascii_key_path)
        
        os.chdir(self.main_test_dir)
        
    def test_doxxkey_metadata_template_attr(self):
        os.chdir('keys')  # switch to keys directory to test file load from inside the directory
        key = DoxxKey(self.good_ascii_key_path)
        self.assertTrue('template' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        self.assertEqual('test.doxt', key.meta_data['template'])  # assert that the template path string is defined relative to the key file when key file in CWD
        
        os.chdir(self.main_test_dir)
        
    def test_doxxkey_metadata_template_attr_diffdir(self):
        key = DoxxKey(self.good_ascii_key_path_outside)
        self.assertTrue('template' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        self.assertEqual('keys/test.doxt', key.meta_data['template'])  # assert that the template path remains relative to the key directory when key file outside CWD
        
    def test_doxxkey_keydata_string_attr(self):  # test a single word string value in the key data
        key = DoxxKey(self.good_ascii_key_path_outside)
        self.assertTrue('string' in key.key_data.keys())
        self.assertEqual('Chris', key.key_data['string'])
        
    def test_doxxkey_keydata_stringspaces_attr(self):  # test multi-word string value that includes spaces in the key data
        key = DoxxKey(self.good_ascii_key_path_outside)
        self.assertTrue('string-spaces' in key.key_data.keys())
        self.assertEqual('more cowbell', key.key_data['string-spaces'])
        
    def test_doxxkey_keydata_number_attr(self):  # test an integer value in the key data
        key = DoxxKey(self.good_ascii_key_path_outside)
        self.assertTrue('number' in key.key_data.keys())
        self.assertEqual('2015', key.key_data['number'])
        
    def test_doxxkey_keydata_multilinestring_attr(self):  # test how multiline YAML strings are handled (the newlines are folded, becomes string without newlines)
        key = DoxxKey(self.good_ascii_key_path_outside)
        self.assertTrue('multiline' in key.key_data.keys())
        self.assertEqual("This is a multiple line string with more input", key.key_data['multiline'])  # assert that multiline strings fold newlines
        
    def test_doxxkey_keydata_date_attr(self):  # test whether date converted to a string
        key = DoxxKey(self.good_ascii_key_path_outside)
        self.assertTrue('date' in key.key_data.keys())
        self.assertEqual('10/10/2010', key.key_data['date'])
        
    def test_doxxkey_keydata_colons_attr(self):  # test that string that contains colons parses without issues
        key = DoxxKey(self.good_ascii_key_path_outside)
        self.assertTrue('colons' in key.key_data.keys())
        self.assertEqual('contains:colons', key.key_data['colons'])
    
    def test_doxxkey_keydata_url_attr(self):
        key = DoxxKey(self.good_ascii_key_path_outside)
        self.assertTrue('url' in key.key_data.keys())
        self.assertEqual('http://test.com/dir/file.txt', key.key_data['url'])        
    
    ## Error tests