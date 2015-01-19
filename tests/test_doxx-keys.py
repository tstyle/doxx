#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import unicodedata
from Naked.toolshed.system import make_path
from doxx.datatypes.key import DoxxKey

from Naked.toolshed.python import is_py2, is_py3

class DoxxASCIIKeysTests(unittest.TestCase):

    def setUp(self):
        self.main_test_dir = os.getcwd()
        self.good_key_path = "ascii_singletempl_key.yaml"  # need to chdir into keys directory to use this path
        self.good_key_path_multitempl = "ascii_multitempl_key.yaml"
        self.good_key_path_remtempl = "ascii_singletempl_rem_key.yaml"
        self.good_key_path_rem_multi = "ascii_multitempl_rem_key.yaml"
        self.good_key_path_outside = "keys/ascii_singletempl_key.yaml"
        self.good_key_path_multitempl_outside = "keys/ascii_multitempl_key.yaml"
        self.good_key_path_remtempl_outside = "keys/ascii_singletempl_rem_key.yaml"
        self.good_key_path_rem_multi_outside = "keys/ascii_multitempl_rem_key.yaml"

    def tearDown(self):
        pass
    
    ## Single template ASCII key file tests
    
    # test instance attributes on construction
    def test_doxxkey_key_read_successful(self):
        os.chdir('keys')
        key = DoxxKey(self.good_key_path)
        
        os.chdir(self.main_test_dir)
        
    def test_doxxkey_metadata_template_attr(self):
        os.chdir('keys')  # switch to keys directory to test file load from inside the directory
        key = DoxxKey(self.good_key_path)
        os.chdir(self.main_test_dir)
        self.assertTrue('template' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        self.assertEqual('test.doxt', key.meta_data['template'])  # assert that the template path string is defined relative to the key file when key file in CWD
        
    def test_doxxkey_metadata_template_attr_diffdir(self):
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('template' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        self.assertEqual('keys/test.doxt', key.meta_data['template'])  # assert that the template path remains relative to the key directory when key file outside CWD
        
    def test_doxxkey_keydata_string_attr(self):  # test a single word string value in the key data
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('string' in key.key_data.keys())
        self.assertEqual('Chris', key.key_data['string'])
        
    def test_doxxkey_keydata_stringspaces_attr(self):  # test multi-word string value that includes spaces in the key data
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('string-spaces' in key.key_data.keys())
        self.assertEqual('more cowbell', key.key_data['string-spaces'])
        
    def test_doxxkey_keydata_number_attr(self):  # test an integer value in the key data
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('number' in key.key_data.keys())
        self.assertEqual('2015', key.key_data['number'])
        
    def test_doxxkey_keydata_multilinestring_attr(self):  # test how multiline YAML strings are handled (the newlines are folded, becomes string without newlines)
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('multiline' in key.key_data.keys())
        self.assertEqual("This is a multiple line string with more input", key.key_data['multiline'])  # assert that multiline strings fold newlines
        
    def test_doxxkey_keydata_date_attr(self):  # test whether date converted to a string
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('date' in key.key_data.keys())
        self.assertEqual('10/10/2010', key.key_data['date'])
        
    def test_doxxkey_keydata_colons_attr(self):  # test that string that contains colons parses without issues
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('colons' in key.key_data.keys())
        self.assertEqual('contains:colons', key.key_data['colons'])
        
    def test_doxxkey_keydata_nonalphchars_attr(self):  # test non-alphanumeric characters to confirm no parsing issues
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('nonalph-chars' in key.key_data.keys())
        self.assertEqual('!@#$%^&*()-_=+~``<>,./?:;', key.key_data['nonalph-chars'])
    
    def test_doxxkey_keydata_url_attr(self):  # test that URL symbols do not cause issues
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('url' in key.key_data.keys())
        self.assertEqual('http://test.com/dir/file.txt', key.key_data['url'])
        
    def test_doxxkey_attr_multitemp_false(self):  # assert that the multitemplate attribute is set to False
        key = DoxxKey(self.good_key_path_outside)
        self.assertFalse(key.multi_template_key) 
        
    
    
    
    ## Multi-template ASCII tests
    
    # test instance attributes on construction
    def test_doxxkey_multiascii_key_read_successful(self):
        os.chdir('keys')
        key = DoxxKey(self.good_key_path_multitempl)

        os.chdir(self.main_test_dir)

    def test_doxxkey_multiascii_metadata_template_attr(self):
        os.chdir('keys')  # switch to keys directory to test file load from inside the directory
        key = DoxxKey(self.good_key_path_multitempl)
        os.chdir(self.main_test_dir)
        self.assertTrue('templates' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        meta_keys = key.meta_data['templates']
        self.assertEqual('test1.doxt', meta_keys[0])  # assert that the multiple template path strings are defined relative to the key file when key file in CWD
        self.assertEqual('test2.doxt', meta_keys[1])
        self.assertEqual('test3.doxt', meta_keys[2])

    def test_doxxkey_multiascii_metadata_template_attr_diffdir(self):
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue('templates' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        self.assertEqual('keys/test1.doxt', key.meta_data['templates'][0])  # assert that the multiple template paths remain relative to the key directory when key file outside CWD
        self.assertEqual('keys/test2.doxt', key.meta_data['templates'][1])
        self.assertEqual('keys/test3.doxt', key.meta_data['templates'][2])

    def test_doxxkey_multiascii_keydata_string_attr(self):  # test a single word string value in the key data
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue('string' in key.key_data.keys())
        self.assertEqual('Chris', key.key_data['string'])

    def test_doxxkey_multiascii_keydata_stringspaces_attr(self):  # test multi-word string value that includes spaces in the key data
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue('string-spaces' in key.key_data.keys())
        self.assertEqual('more cowbell', key.key_data['string-spaces'])

    def test_doxxkey_multiascii_keydata_number_attr(self):  # test an integer value in the key data
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue('number' in key.key_data.keys())
        self.assertEqual('2015', key.key_data['number'])

    def test_doxxkey_multiascii_keydata_multilinestring_attr(self):  # test how multiline YAML strings are handled (the newlines are folded, becomes string without newlines)
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue('multiline' in key.key_data.keys())
        self.assertEqual("This is a multiple line string with more input", key.key_data['multiline'])  # assert that multiline strings fold newlines

    def test_doxxkey_multiascii_keydata_date_attr(self):  # test whether date converted to a string
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue('date' in key.key_data.keys())
        self.assertEqual('10/10/2010', key.key_data['date'])

    def test_doxxkey_multiascii_keydata_colons_attr(self):  # test that string that contains colons parses without issues
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue('colons' in key.key_data.keys())
        self.assertEqual('contains:colons', key.key_data['colons'])

    def test_doxxkey_multiascii_keydata_nonalphchars_attr(self):  # test non-alphanumeric characters to confirm no parsing issues
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue('nonalph-chars' in key.key_data.keys())
        self.assertEqual('!@#$%^&*()-_=+~``<>,./?:;', key.key_data['nonalph-chars'])

    def test_doxxkey_multiascii_keydata_url_attr(self):  # test that URL symbols do not cause issues
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue('url' in key.key_data.keys())
        self.assertEqual('http://test.com/dir/file.txt', key.key_data['url'])

    def test_doxxkey_multiascii_attr_multitemp_false(self):  # assert that the multitemplate attribute is set to True for a multitemplate key file
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue(key.multi_template_key)
    
    
    
    
    ## Single remote template tests
    # test instantiation
    def test_doxxkey_remascii_key_read_successful(self):
        os.chdir('keys')
        key = DoxxKey(self.good_key_path_remtempl)

        os.chdir(self.main_test_dir)
        
    def test_doxxkey_remascii_metadata_templates_attr(self):  # test meta data load with URL
        os.chdir('keys')  # switch to keys directory to test file load from inside the directory
        key = DoxxKey(self.good_key_path_remtempl)
        os.chdir(self.main_test_dir)
        self.assertTrue('template' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        self.assertEqual('http://test.com/dir/test.doxt', key.meta_data['template'])
        
    def test_doxxkey_remascii_metadata_templates_samedir_attr(self):  # test meta data load with URL, key file run from outside working directory
        key = DoxxKey(self.good_key_path_remtempl_outside)
        self.assertTrue('template' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        self.assertEqual('http://test.com/dir/test.doxt', key.meta_data['template'])    
    
    
    
    ## Multiple remote template tests
    
    # test instantiation
    def test_doxxkey_remascii_multi_read_successful(self):
        os.chdir('keys')
        key = DoxxKey(self.good_key_path_rem_multi)

        os.chdir(self.main_test_dir)
        
    def test_doxxkey_remascii_multi_metadata_templates_attr(self):  # test meta data load with URL
        os.chdir('keys')  # switch to keys directory to test file load from inside the directory
        key = DoxxKey(self.good_key_path_rem_multi)
        os.chdir(self.main_test_dir)  
        self.assertTrue('templates' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        self.assertEqual('http://test.com/dir/test1.doxt', key.meta_data['templates'][0])
        self.assertEqual('https://test.com/dir/test2.doxt', key.meta_data['templates'][1])
        self.assertEqual('https://test.com/dir/test3.doxt', key.meta_data['templates'][2])
    
    def test_doxxkey_remascii_multi_metadata_templates_samedir_attr(self):
        key = DoxxKey(self.good_key_path_rem_multi_outside)
        self.assertTrue('templates' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        self.assertEqual('http://test.com/dir/test1.doxt', key.meta_data['templates'][0])
        self.assertEqual('https://test.com/dir/test2.doxt', key.meta_data['templates'][1])
        self.assertEqual('https://test.com/dir/test3.doxt', key.meta_data['templates'][2])
        


class DoxxUnicodeKeysTests(unittest.TestCase):

    def setUp(self):
        self.main_test_dir = os.getcwd()
        self.good_key_path = "uni_singletemp_key.yaml"  # need to chdir into keys directory to use this path
        self.good_key_path_multitempl = "uni_multitemp_key.yaml"
        self.good_key_path_outside = "keys/uni_singletemp_key.yaml"
        self.good_key_path_multitempl_outside = "keys/uni_multitemp_key.yaml"
        
    def make_nfkd_string(self, the_string):
        return unicodedata.normalize("NFKD", the_string)
    
    ## Single template unicode tests
    
    # test instance attributes on construction
    def test_doxxkey_unicode_key_read_successful(self):
        os.chdir('keys')
        key = DoxxKey(self.good_key_path)

        os.chdir(self.main_test_dir)

    def test_doxxkey_unicode_metadata_template_attr(self):
        os.chdir('keys')  # switch to keys directory to test file load from inside the directory
        key = DoxxKey(self.good_key_path)
        os.chdir(self.main_test_dir)
        self.assertTrue('template' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        
        norm_path = self.make_nfkd_string(u'ţéśť.doxt')
        self.assertEqual(norm_path, key.meta_data['template'])  # assert that the template path string is defined relative to the key file when key file in CWD


    def test_doxxkey_unicode_metadata_template_attr_diffdir(self):
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('template' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        
        norm_path = self.make_nfkd_string(u'keys/ţéśť.doxt')  # have to NFKD normalize the unicode in order to perform the string comparison below
        self.assertEqual(norm_path, key.meta_data['template'])
            
    
    def test_doxxkey_unicode_keydata_string_attr(self):  # test a single word string value in the key data
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('string' in key.key_data.keys())
        
        self.assertEqual(u'ΔϾϘ', key.key_data['string'])
        
    def test_doxxkey_unicode_keydata_stringspaces_attr(self):
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('string-spaces' in key.key_data.keys())
    
        self.assertEqual(u'༄པ࿔ དར྅', key.key_data['string-spaces'])
        
    def test_doxxkey_unicode_keydata_number_attr(self):
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('number' in key.key_data.keys())
    
        norm_number = self.make_nfkd_string(u'⅒')
        self.assertEqual(norm_number, key.key_data['number'])
        
    def test_doxxkey_unicode_keydata_mathops_attr(self):
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('math-operators' in key.key_data.keys())
        
        self.assertEqual(u"∑∏∫≈⊕", key.key_data['math-operators'])
        
    def test_doxxkey_unicode_keydata_multiline_attr(self):
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('multiline' in key.key_data.keys())
        
        norm_multiline = self.make_nfkd_string(u'Ǝǆǎ Ǣǧǰ Ǧǭ Ǳǵǽ')
        self.assertEqual(norm_multiline, key.key_data['multiline'])
        
    def test_doxxkey_unicode_keydata_symbols_attr(self):
        key = DoxxKey(self.good_key_path_outside)
        self.assertTrue('symbols' in key.key_data.keys())
        
        self.assertEqual(u'♠♻★©', key.key_data['symbols'])
    
    
    
    ## Multi-template unicode tests
    
    def test_doxxkey_multiunicode_metadata_template_attr(self):
        os.chdir('keys')  # switch to keys directory to test file load from inside the directory
        key = DoxxKey(self.good_key_path_multitempl)
        os.chdir(self.main_test_dir)
        self.assertTrue('templates' in key.meta_data.keys())  # assert that 'template' is one of keys in the meta_data attribute
        meta_keys = key.meta_data['templates']
        norm_path = unicodedata.normalize("NFKD", u'ţéśť.doxt')
        self.assertEqual(norm_path, meta_keys[0])  # assert that the multiple template path strings are defined relative to the key file when key file in CWD
        self.assertEqual('https://test.com/dir/test.doxt', meta_keys[1])
        self.assertEqual('http://test.com/dir/test2.doxt', meta_keys[2])
        
    def test_doxxkey_multiunicode_keydata_string_attr(self):
        key = DoxxKey(self.good_key_path_multitempl_outside)
        self.assertTrue('string' in key.key_data.keys())
    
        self.assertEqual(u'ΔϾϘ', key.key_data['string'])
        
    ## Error tests
    
class DoxxKeysErrorTests(unittest.TestCase):

    def setUp(self):
        self.nohead_key = "keys/errors/nohead_key.yaml"          
        self.emptymeta_key = "keys/errors/emptymeta_key.yaml"    
        self.two_templates_key = "keys/errors/twotemp_key.yaml"
        self.nometa_key = "keys/errors/nometa_key.yaml"
        
        self.nokey_key = "keys/errors/nokey_key.yaml"
        self.emptykey_key = "keys/errors/emptykey_key.yaml"
        
    # there is no head meta data section
    def test_doxxkey_errors_nohead(self):
        with self.assertRaises(SystemExit):
            key = DoxxKey(self.nohead_key)
    
    # there is an empty head meta data section
    def test_doxxkey_errors_emptymeta(self):
        with self.assertRaises(SystemExit):
            key = DoxxKey(self.emptykey_key)
    
    # there are template AND templates definitions in the meta data header
    def test_doxxkey_errors_twotemplates(self):
        with self.assertRaises(SystemExit):
            key = DoxxKey(self.two_templates_key)
    
    # there is a template or templates but it is undefined
    def test_doxxkey_errors_nometa(self):
        with self.assertRaises(SystemExit):
            key = DoxxKey(self.nometa_key)
    
    # there is no key data present in the key file
    def test_doxxkey_errors_nokey(self):
        with self.assertRaises(SystemExit):
            key = DoxxKey(self.nokey_key)
    
    # there are key fields, but none are defined with replacement text
    def test_doxxkey_errors_emptykey(self):
        with self.assertRaises(SystemExit):
            key = DoxxKey(self.emptykey_key)
        
    