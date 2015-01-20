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