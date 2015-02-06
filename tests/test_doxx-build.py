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


# single template, ASCII text build test
class DoxxLocalMITLicenseBuildTests(unittest.TestCase):

    def setUp(self):
        self.current_dir = os.getcwd()
        self.mit_standard = "standards/mit-license.txt"
        self.mit_verbatim_standard = "standards/mit-verbatim.txt"
        self.mit_test_dir = "build-tests/mit-license"
        self.mit_key = "key.yaml"  # executed inside the mit testing directory, no directory path necessary
        self.mit_key_with_extension = "key-with-extension.yaml"
        self.mit_key_with_destdir = "key-with-destdir.yaml"
        self.mit_key_undefined_destdir = "key-undefined-destdir.yaml"
        self.mit_key_verbatim = "key-verbatim.yaml"
        
        mit_std_reader = FileReader(self.mit_standard)
        self.mit_standard_text = mit_std_reader.read()
        
        mit_v_reader = FileReader(self.mit_verbatim_standard)
        self.mit_verbatim_standard_text = mit_v_reader.read()
    
   
    # default template style test
    # should default to template basename as outfile basename, extension is defined in this template as '.txt'
    def test_mit_license_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.mit_key)
            b.run()
            self.assertTrue(file_exists('mit.txt'))                  # confirm that the rendered file write took place
            fr = FileReader('mit.txt')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('mit.txt')  # remove the rendered file to prepare directory for new tests
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('mit.txt'):
                os.remove('mit.txt')    # remove the generated LICENSE file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e
  
  
    # test build with new basename and extension assigned
    def test_mit_license_with_new_basename_extension_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.mit_key_with_extension)
            b.run()
            self.assertTrue(file_exists('LICENSE.txt'))                  # confirm that the rendered file write took place
            fr = FileReader('LICENSE.txt')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('LICENSE.txt')  # remove the rendered file to prepare directory for new tests
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('LICENSE.txt'):
                os.remove('LICENSE.txt')    # remove the generated LICENSE file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e          
    
    
    # test build with new destination directory path
    def test_mit_license_with_destdir_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.mit_key_with_destdir)
            b.run()
            self.assertTrue(file_exists('build/LICENSE'))                  # confirm that the rendered file write took place
            fr = FileReader('build/LICENSE')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            import shutil
            shutil.rmtree('build')
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('build/LICENSE'):
                import shutil
                shutil.rmtree('build')
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e
        
        
    # test build with destination_directory present but undefined (should default to CWD)
    def test_mit_license_undefined_destdir_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.mit_key_undefined_destdir)
            b.run()
            self.assertTrue(file_exists('LICENSE'))                  # confirm that the rendered file write took place
            fr = FileReader('LICENSE')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('LICENSE')  # remove the rendered file to prepare directory for new tests
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('LICENSE'):
                os.remove('LICENSE')    # remove the generated LICENSE file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e    
      
    
    # test build with verbatim set to true (i.e. skips replacement of text and writes verbatim file data)
    def test_mit_license_verbatim_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.mit_key_verbatim)
            b.run()
            self.assertTrue(file_exists('mit-verbatim'))   
            fr = FileReader('mit-verbatim')
            rendered_text = fr.read()
            self.assertEqual(self.mit_verbatim_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('mit-verbatim')  # remove the rendered file to prepare directory for new tests
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('mit-verbatim'):
                os.remove('mit-verbatim')    # remove the generated LICENSE file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e      



# single template local unicode (Russian translation) file build
class DoxxLocalUnicodeMITLicenseBuildTests(unittest.TestCase):
    
    def setUp(self):
        self.current_dir = os.getcwd()
        self.mit_standard = "standards/russian-mit-license.txt"
        self.mit_verbatim_standard = "standards/russian-mit-verbatim.txt"
        self.mit_test_dir = "build-tests/unicode-mit-license"
        
        self.key = "rus-key.yaml"
        
        mit_std_reader = FileReader(self.mit_standard)
        self.mit_standard_text = mit_std_reader.read()        
        
    
    # default remote template style test
    # should default to template basename as outfile basename, extension is defined in this template as '.txt'
    def test_mit_unicode_license_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.key)
            b.run()
            self.assertTrue(file_exists('rus-mit.txt'))                  # confirm that the rendered file write took place
            fr = FileReader('rus-mit.txt')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('rus-mit.txt')  # remove the rendered file to prepare directory for new tests
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('rus-mit.txt'):
                os.remove('rus-mit.txt')    # remove the generate file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e    
    
    
    

# single template remote ASCII file build
class DoxxRemoteMITLicenseBuildTests(unittest.TestCase):
    
    def setUp(self):
        self.current_dir = os.getcwd()
        self.mit_standard = "standards/mit-license.txt"
        self.mit_verbatim_standard = "standards/mit-verbatim.txt"
        self.mit_test_dir = "build-tests/mit-license"
        
        self.remote_key = 'remote-key.yaml'
        self.remote_key_with_extension = 'remote-key-with-extension.yaml'
        self.remote_key_with_destdir = 'remote-key-with-destdir.yaml'
        self.remote_key_undefined_destdir = "remote-key-undefined-destdir.yaml"
        self.remote_key_verbatim = "remote-key-verbatim.yaml"
        
        
        mit_std_reader = FileReader(self.mit_standard)
        self.mit_standard_text = mit_std_reader.read()
    
        mit_v_reader = FileReader(self.mit_verbatim_standard)
        self.mit_verbatim_standard_text = mit_v_reader.read()
    
    
    # default remote template style test
    # should default to template basename as outfile basename, extension is defined in this template as '.txt'
    def test_mit_remote_license_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.remote_key)
            b.run()
            self.assertTrue(file_exists('mit.txt'))                  # confirm that the rendered file write took place
            fr = FileReader('mit.txt')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('mit.txt')  # remove the rendered file to prepare directory for new tests
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('mit.txt'):
                os.remove('mit.txt')    # remove the generate file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e
        
    
    # test build with new basename and extension assigned
    def test_mit_remote_license_with_new_basename_extension_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.remote_key_with_extension)
            b.run()
            self.assertTrue(file_exists('LICENSE.txt'))                  # confirm that the rendered file write took place
            fr = FileReader('LICENSE.txt')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('LICENSE.txt')  # remove the rendered file to prepare directory for new tests
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('LICENSE.txt'):
                os.remove('LICENSE.txt')    # remove the generated LICENSE file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e
        
    # test build with new destination directory path
    def test_mit_remote_license_with_destdir_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.remote_key_with_destdir)
            b.run()
            self.assertTrue(file_exists('build/LICENSE'))                  # confirm that the rendered file write took place
            fr = FileReader('build/LICENSE')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            import shutil
            shutil.rmtree('build')  # remove the build directory and contained files from the test
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('build/LICENSE'):
                import shutil
                shutil.rmtree('build')
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e        
        
    # test build with destination_directory present but undefined (should default to CWD)
    def test_mit_remote_license_undefined_destdir_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.remote_key_undefined_destdir)
            b.run()
            self.assertTrue(file_exists('LICENSE'))                  # confirm that the rendered file write took place
            fr = FileReader('LICENSE')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('LICENSE')  # remove the rendered file to prepare directory for new tests
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('LICENSE'):
                os.remove('LICENSE')    # remove the generated LICENSE file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e
        
    # test build with verbatim set to true (i.e. skips replacement of text and writes verbatim file data)
    def test_mit_remote_license_verbatim_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.remote_key_verbatim)
            b.run()
            self.assertTrue(file_exists('mit-verbatim'))   
            fr = FileReader('mit-verbatim')
            rendered_text = fr.read()
            self.assertEqual(self.mit_verbatim_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('mit-verbatim')  # remove the rendered file to prepare directory for new tests
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('mit-verbatim'):
                os.remove('mit-verbatim')    # remove the generated LICENSE file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e          

# single template remote unicode (Russian translation) file build
class RemoteMITUnicodeLicenseBuildTests(unittest.TestCase):
    
    def setUp(self):
        self.current_dir = os.getcwd()
        self.mit_standard = "standards/russian-mit-license.txt"
        self.mit_verbatim_standard = "standards/russian-mit-verbatim.txt"
        self.mit_test_dir = "build-tests/unicode-mit-license"        
        
        self.key = "remote-rus-key.yaml"
        
        mit_std_reader = FileReader(self.mit_standard)
        self.mit_standard_text = mit_std_reader.read()
        
    def test_remote_mit_unicode_license_build(self):
        os.chdir(self.mit_test_dir)  # cd to the mit test dir
        try:
            b = Builder(self.key)
            b.run()
            self.assertTrue(file_exists('rus-mit.txt'))                  # confirm that the rendered file write took place
            fr = FileReader('rus-mit.txt')
            rendered_text = fr.read()
            self.assertEqual(self.mit_standard_text, rendered_text)  # confirm that the rendered text matches expected text
            os.remove('rus-mit.txt')  # remove the rendered file to prepare directory for new tests
            os.chdir(self.current_dir)
        except Exception as e:
            if file_exists('rus-mit.txt'):
                os.remove('rus-mit.txt')    # remove the generate file if it is present before the exception was raised
            os.chdir(self.current_dir)  # cd back to the main test directory before exception raised (avoids issues with other tests)
            raise e
        
        
        