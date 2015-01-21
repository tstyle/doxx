#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest

from Naked.toolshed.system import make_path
from Naked.toolshed.file import FileReader
from Naked.toolshed.python import is_py2
from doxx.datatypes.template import DoxxTemplate, RemoteDoxxTemplate

class DoxxASCIITemplateTests(unittest.TestCase):
    
    def setUp(self):
        self.ascii_template = "templates/ascii_template.doxt"
        self.ascii_standard = "standards/ascii_template_std.txt"
    
    # template ASCII meta data load
    def test_ascii_metadata_load(self):
        temp = DoxxTemplate(self.ascii_template)
        self.assertFalse(temp == None)
        self.assertEqual(self.ascii_template, temp.inpath)
        
    # template meta data 'extension' attribute
    def test_ascii_metadata_attributes(self):
        temp = DoxxTemplate(self.ascii_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()
        self.assertEqual(u"css", temp.meta_data['extension'])
        self.assertEqual(u"test", temp.meta_data['basename'])
        self.assertEqual(u"css", temp.meta_data['destination_directory'])
        self.assertEqual(u".css", temp.extension)
        self.assertEqual(u"test", temp.basename)
        self.assertEqual(u"css/test.css", temp.outfile)
        
    # template ASCII template text load
    def test_ascii_templatetext_attr(self):
        self.maxDiff = None
        fr = FileReader(self.ascii_standard)
        std_template_text = fr.read()
        
        temp = DoxxTemplate(self.ascii_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()
        
        self.assertEqual(std_template_text, temp.text)
        
    # template ASCII template - text reads in as unicode (py2) or str (py3)
    def test_ascii_templatetext_is_unicode(self):
        temp = DoxxTemplate(self.ascii_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()
        
        if is_py2():
            self.assertEqual(unicode, type(temp.text))
        else:
            self.assertEqual(str, type(temp.text))
    
    
class DoxxUnicodeTemplateTests(unittest.TestCase):
    
    def setUp(self):
        self.unicode_template = "templates/unicode_template.doxt"
        self.unicode_standard = "standards/unicode_template_std.txt"
    
    # template unicode meta data load
    def test_unicode_metadata_load(self):
        temp = DoxxTemplate(self.unicode_template)
        self.assertFalse(temp == None)
        self.assertEqual(self.unicode_template, temp.inpath)    
    
    # template meta data load
    def test_unicode_metadata_attributes(self):
        temp = DoxxTemplate(self.unicode_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()
        self.assertEqual(u"txt", temp.meta_data['extension'])
        self.assertEqual(u"тысячи", temp.meta_data['basename'])
        self.assertEqual(u"text", temp.meta_data['destination_directory'])
        self.assertEqual(u".txt", temp.extension)
        self.assertEqual(u"тысячи", temp.basename)
        self.assertEqual(u"text/тысячи.txt", temp.outfile)

    # template unicode template text load
    def test_unicode_templatetext_attr(self):
        self.maxDiff = None
        fr = FileReader(self.unicode_standard)
        std_template_text = fr.read()

        temp = DoxxTemplate(self.unicode_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()

        self.assertEqual(std_template_text, temp.text)
        
    # unicode template - text reads in as unicode (py2) or str (py3)
    def test_unicode_templatetext_is_unicode(self):
        temp = DoxxTemplate(self.unicode_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()

        if is_py2():
            self.assertEqual(unicode, type(temp.text))
        else:
            self.assertEqual(str, type(temp.text))
    
    
class DoxxRemoteTemplateTests(unittest.TestCase):
    
    def setUp(self):
        self.remote_ascii_template = "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/templates/ascii_template.doxt"
        self.remote_unicode_template = "https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/templates/unicode_template.doxt"
        self.ascii_standard = "standards/ascii_template_std.txt"
        self.unicode_standard = "standards/unicode_template_std.txt"
    
    ##
    # REMOTE ASCII TESTS
    ##
    
    # remote template ASCII meta data load
    def test_remote_ascii_metadata_load(self):
        temp = RemoteDoxxTemplate(self.remote_ascii_template)
        self.assertFalse(temp == None)
        self.assertEqual(self.remote_ascii_template, temp.inpath)

    # remote template meta data 'extension' attribute
    def test_remote_ascii_metadata_attributes(self):
        temp = RemoteDoxxTemplate(self.remote_ascii_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()
        self.assertEqual(u"css", temp.meta_data['extension'])
        self.assertEqual(u"test", temp.meta_data['basename'])
        self.assertEqual(u"css", temp.meta_data['destination_directory'])
        self.assertEqual(u".css", temp.extension)
        self.assertEqual(u"test", temp.basename)
        self.assertEqual(u"css/test.css", temp.outfile)

    # remote template ASCII template text load
    def test_remote_ascii_templatetext_attr(self):
        self.maxDiff = None
        fr = FileReader(self.ascii_standard)
        std_template_text = fr.read()

        temp = RemoteDoxxTemplate(self.remote_ascii_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()

        self.assertEqual(std_template_text, temp.text)

    # remote template ASCII template - text reads in as unicode (py2) or str (py3)
    def test_remote_ascii_templatetext_is_unicode(self):
        temp = RemoteDoxxTemplate(self.remote_ascii_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()

        if is_py2():
            self.assertEqual(unicode, type(temp.text))
        else:
            self.assertEqual(str, type(temp.text))
    
    ##
    # REMOTE UNICODE TESTS
    ##
            
    # remote template unicode meta data load
    def test_remote_unicode_metadata_load(self):
        temp = RemoteDoxxTemplate(self.remote_unicode_template)
        self.assertFalse(temp == None)
        self.assertEqual(self.remote_unicode_template, temp.inpath)

    # remote template meta data load tests
    def test_remote_unicode_metadata_attributes(self):
        temp = RemoteDoxxTemplate(self.remote_unicode_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()
        self.assertEqual(u"txt", temp.meta_data['extension'])
        self.assertEqual(u"тысячи", temp.meta_data['basename'])
        self.assertEqual(u"text", temp.meta_data['destination_directory'])
        self.assertEqual(u".txt", temp.extension)
        self.assertEqual(u"тысячи", temp.basename)
        self.assertEqual(u"text/тысячи.txt", temp.outfile)

    # remote unicode template text load
    def test_remote_unicode_templatetext_attr(self):
        self.maxDiff = None
        fr = FileReader(self.unicode_standard)
        std_template_text = fr.read()

        temp = RemoteDoxxTemplate(self.remote_unicode_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()

        self.assertEqual(std_template_text, temp.text)

    # remote unicode template - text reads in as unicode (py2) or str (py3)
    def test_remote_unicode_templatetext_is_unicode(self):
        temp = RemoteDoxxTemplate(self.remote_unicode_template)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()

        if is_py2():
            self.assertEqual(unicode, type(temp.text))
        else:
            self.assertEqual(str, type(temp.text))
            

class DoxxTemplateErrors(unittest.TestCase):
    
    def setUp(self):
        self.bad_template_path = "templates/bogus.doxt"
        self.missing_extension = "templates/errors/missing_extension.doxt"
        self.missing_ext_val = "templates/errors/missing_extension_value.doxt"
        self.undefined_dest_dir = "templates/errors/undefined_destination.doxt"
        self.undefined_basename = "templates/errors/undefined_basename.doxt"
        self.nonexist_url_template = "http://www.google.com/templates/doxx/doxx.doxt"
        
    
    # bad local file path
    def test_template_error_bad_local_path(self):
        with self.assertRaises(SystemExit):
            temp = DoxxTemplate(self.bad_template_path)
            temp.load_data()
            temp.split_data()
            temp.parse_template_for_errors()
            temp.parse_template_text()
            
    # malformed template file - absent header meta data section    
    def test_template_error_missing_header(self):
        with self.assertRaises(SystemExit):
            temp = DoxxTemplate(self.bad_template_path)
            temp.load_data()
            temp.split_data()
            temp.parse_template_for_errors()
            temp.parse_template_text()
            
    # malformed template file - missing extension field
    def test_template_error_missing_extension_field(self):
        with self.assertRaises(SystemExit):
            temp = DoxxTemplate(self.missing_extension)
            temp.load_data()
            temp.split_data()
            temp.parse_template_for_errors()
            temp.parse_template_text()
        
    def test_template_error_missing_extension_value(self):
        temp = DoxxTemplate(self.missing_ext_val)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()
        self.assertEqual('.doxr', temp.extension)  # uses a default of '.doxr' if user does not set it    
        
    # destination_directory specified but not defined in the template meta data
    def test_template_error_undefined_destdir(self):
        temp = DoxxTemplate(self.undefined_dest_dir)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()
        self.assertEqual('undefined_destination.txt', temp.outfile)  # defaults to working directory with template name as base file name
    
    # basename specified but not defined in the file
    def test_template_error_undefined_basename(self):
        temp = DoxxTemplate(self.undefined_basename)
        temp.load_data()
        temp.split_data()
        temp.parse_template_for_errors()
        temp.parse_template_text()
        self.assertEqual('undefined_basename.txt', temp.outfile) 
    
    # malformed template file - absent template data

    
    # URL 404 error - nonexistent page
    # URL timeout error - ? need to handle with try/except block    