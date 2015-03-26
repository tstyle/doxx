#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import unicodedata
import shutil

from Naked.toolshed.system import make_path, file_exists, dir_exists
from Naked.toolshed.file import FileReader, FileWriter
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
        
# multi-template build from ASCII & unicode text template files, including verbatim file build
class LocalMultiTemplateBuildTests(unittest.TestCase):
    
    def setUp(self):
        self.cwd = os.getcwd()
        
        self.local_multi_testdir = "build-tests/local-multifile"
        self.local_multi_key = "key.yaml"  # executed from the same directory
        
        self.mit_path = "standards/mit-license.txt"
        self.mit_rus_path = "standards/russian-mit-license.txt"
        self.mit_verbatim_path = "standards/mit-verbatim.txt"
        
        fr_mit = FileReader(self.mit_path)
        fr_rusmit = FileReader(self.mit_rus_path)
        fr_verbatim = FileReader(self.mit_verbatim_path)
        
        self.mit_text = fr_mit.read()
        self.mit_rus_text = fr_rusmit.read()
        self.mit_verbatim_text = fr_verbatim.read()
        
    def test_multifile_local_build(self):
        try:
            os.chdir(self.local_multi_testdir)
            b = Builder(self.local_multi_key)
            b.run()
            # assert that files were made
            self.assertTrue(file_exists('mit.txt'))
            self.assertTrue(file_exists('rus-mit.txt'))
            self.assertTrue(file_exists('mit-verbatim'))  # uses 'extension: ' in the template metadata
            
            fr_m = FileReader('mit.txt')
            fr_r = FileReader('rus-mit.txt')
            fr_v = FileReader('mit-verbatim')
            
            rendered_mit_text = fr_m.read()
            rendered_rus_text = fr_r.read()
            rendered_ver_text = fr_v.read()
            
            # assert that the rendered text is as expected
            self.assertEqual(self.mit_text, rendered_mit_text)
            self.assertEqual(self.mit_rus_text, rendered_rus_text)
            self.assertEqual(self.mit_verbatim_text, rendered_ver_text)
            
            # remove the rendered files
            os.remove('mit.txt')
            os.remove('rus-mit.txt')
            os.remove('mit-verbatim')
            
            os.chdir(self.cwd)
        except Exception as e:
            if file_exists('mit.txt'):
                os.remove('mit.txt')
            if file_exists('rus-mit.txt'):
                os.remove('rus-mit.txt')
            if file_exists('mit-verbatim'):
                os.remove('mit-verbatim')
            os.chdir(self.cwd)
            raise e
        

# multi-template build from ASCII and unicode REMOTE templates
class RemoteMultiTemplateBuildTests(unittest.TestCase):
    
    def setUp(self):
        self.cwd = os.getcwd()
    
        self.remote_multi_testdir = "build-tests/remote-multifile"
        self.remote_multi_key = "key.yaml"  # executed from the same directory
    
        self.mit_path = "standards/mit-license.txt"
        self.mit_rus_path = "standards/russian-mit-license.txt"
        self.mit_verbatim_path = "standards/mit-verbatim.txt"
    
        fr_mit = FileReader(self.mit_path)
        fr_rusmit = FileReader(self.mit_rus_path)
        fr_verbatim = FileReader(self.mit_verbatim_path)
    
        self.mit_text = fr_mit.read()
        self.mit_rus_text = fr_rusmit.read()
        self.mit_verbatim_text = fr_verbatim.read()
    
    def test_multifile_remote_build(self):
        try:
            os.chdir(self.remote_multi_testdir)
            b = Builder(self.remote_multi_key)
            b.run()
            # assert that files were made
            self.assertTrue(file_exists('mit.txt'))
            self.assertTrue(file_exists('rus-mit.txt'))
            self.assertTrue(file_exists('mit-verbatim'))  # uses 'extension: ' in the template metadata

            fr_m = FileReader('mit.txt')
            fr_r = FileReader('rus-mit.txt')
            fr_v = FileReader('mit-verbatim')

            rendered_mit_text = fr_m.read()
            rendered_rus_text = fr_r.read()
            rendered_ver_text = fr_v.read()

            # assert that the rendered text is as expected
            self.assertEqual(self.mit_text, rendered_mit_text)
            self.assertEqual(self.mit_rus_text, rendered_rus_text)
            self.assertEqual(self.mit_verbatim_text, rendered_ver_text)

            # remove the rendered files
            os.remove('mit.txt')
            os.remove('rus-mit.txt')
            os.remove('mit-verbatim')

            os.chdir(self.cwd)
        except Exception as e:
            if file_exists('mit.txt'):
                os.remove('mit.txt')
            if file_exists('rus-mit.txt'):
                os.remove('rus-mit.txt')
            if file_exists('mit-verbatim'):
                os.remove('mit-verbatim')
            os.chdir(self.cwd)
            raise e
        
        
# Local tar.gz project build test
class LocalProjectTarGZBuildTests(unittest.TestCase):
    
    def setUp(self):
        self.cwd = os.getcwd()
    
        self.local_project_testdir = "build-tests/local-project/build"
        self.local_proj_targz_key = "targz_key.yaml"  # executed from the same directory
        
        # remove all contents of the build directory and build directory path from prior test run
        if dir_exists('build-tests/local-project/build'):
            shutil.rmtree('build-tests/local-project/build')
            
        self.assertFalse(dir_exists('build-tests/local-project/build'))
        
        # create the build directory path
        os.makedirs('build-tests/local-project/build')
        
        self.assertTrue(dir_exists('build-tests/local-project/build'))
    
        # move the tar.gz file into the build directory
        fr = FileReader('build-tests/local-project/initializr.tar.gz')
        targz_data = fr.read_bin()
        fw = FileWriter('build-tests/local-project/build/initializr.tar.gz')
        fw.write_bin(targz_data)
        
        
        # move the key into the build directory
        fr_key = FileReader('build-tests/local-project/targz_key.yaml')
        targz_key_data = fr_key.read()
        fw_key = FileWriter('build-tests/local-project/build/targz_key.yaml')
        fw_key.write(targz_key_data)
        
        
        # confirm that the build files are present
        self.assertTrue(file_exists('build-tests/local-project/build/initializr.tar.gz'))
        self.assertTrue(file_exists('build-tests/local-project/build/targz_key.yaml'))
        
        # get the expected text for outfile write assertions
        self.fourohfour_text = FileReader('standards/404.html').read()
        self.indexhtml_text = FileReader('standards/index.html').read()
        self.jquery_text = FileReader('standards/jquery.js').read()
        self.normalize_text = FileReader('standards/normalize-min.css').read()

    
    def test_local_project_targz_build(self):
        try:
            # make the build directory the CWD
            os.chdir(self.local_project_testdir)
            # run the project build
            b = Builder(self.local_proj_targz_key)
            b.run()
            
            # confirm directory unpacked with correct directory structure
            self.assertTrue(dir_exists('html-initializr-master'))
            self.assertTrue(dir_exists('html-initializr-master/css'))
            self.assertTrue(dir_exists('html-initializr-master/js/vendor'))
            self.assertTrue(dir_exists('html-initializr-master/templates'))
            
            # confirm presence of files
            self.assertTrue(file_exists('html-initializr-master/index.html'))
            self.assertTrue(file_exists('html-initializr-master/404.html'))
            self.assertTrue(file_exists('html-initializr-master/pkey.yaml'))
            self.assertTrue(file_exists('html-initializr-master/project.yaml'))
            self.assertTrue(file_exists('html-initializr-master/js/vendor/jquery-1.11.1.min.js'))
            self.assertTrue(file_exists('html-initializr-master/js/vendor/modernizr-2.6.2.min.js'))
            self.assertTrue(file_exists('html-initializr-master/css/normalize.min.css'))
            
            # confirm that the project archive file was removed during build
            self.assertFalse(file_exists('initializr.tar.gz'))
            
            # confirm that the key file still present in the directory after the build
            self.assertTrue(file_exists('targz_key.yaml'))
            
            # read the new outfiles that were generated from templates
            rendered_fourohfour = FileReader('html-initializr-master/404.html').read()
            rendered_index = FileReader('html-initializr-master/index.html').read()
            rendered_jquery = FileReader('html-initializr-master/js/vendor/jquery-1.11.1.min.js').read()
            rendered_normalize = FileReader('html-initializr-master/css/normalize.min.css').read()
            
            # assert correct contents of the files developed from templates
            self.assertEqual(self.fourohfour_text, rendered_fourohfour)
            self.assertEqual(self.indexhtml_text, rendered_index)
            self.assertEqual(self.jquery_text, rendered_jquery)
            self.assertEqual(self.normalize_text, rendered_normalize)           
            
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e


# local .zip project build
class LocalProjectZipBuildTests(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()

        self.local_project_testdir = "build-tests/local-project/build"
        self.local_proj_zip_key = "zip_key.yaml"  # executed from the same directory

        # remove all contents of the build directory and build directory path from prior test run
        if dir_exists('build-tests/local-project/build'):
            shutil.rmtree('build-tests/local-project/build')

        self.assertFalse(dir_exists('build-tests/local-project/build'))

        # create the build directory path
        os.makedirs('build-tests/local-project/build')

        self.assertTrue(dir_exists('build-tests/local-project/build'))

        # move the tar.gz file into the build directory
        fr = FileReader('build-tests/local-project/initializr.zip')
        zip_data = fr.read_bin()
        fw = FileWriter('build-tests/local-project/build/initializr.zip')
        fw.write_bin(zip_data)


        # move the key into the build directory
        fr_key = FileReader('build-tests/local-project/zip_key.yaml')
        zip_key_data = fr_key.read()
        fw_key = FileWriter('build-tests/local-project/build/zip_key.yaml')
        fw_key.write(zip_key_data)


        # confirm that the build files are present
        self.assertTrue(file_exists('build-tests/local-project/build/initializr.zip'))
        self.assertTrue(file_exists('build-tests/local-project/build/zip_key.yaml'))

        # get the expected text for outfile write assertions
        self.fourohfour_text = FileReader('standards/404.html').read()
        self.indexhtml_text = FileReader('standards/index.html').read()
        self.jquery_text = FileReader('standards/jquery.js').read()
        self.normalize_text = FileReader('standards/normalize-min.css').read()


    def test_local_project_zip_build(self):
        try:
            # make the build directory the CWD
            os.chdir(self.local_project_testdir)
            # run the project build
            b = Builder(self.local_proj_zip_key)
            b.run()

            # confirm directory unpacked with correct directory structure
            self.assertTrue(dir_exists('html-initializr-master'))
            self.assertTrue(dir_exists('html-initializr-master/css'))
            self.assertTrue(dir_exists('html-initializr-master/js/vendor'))
            self.assertTrue(dir_exists('html-initializr-master/templates'))

            # confirm presence of files
            self.assertTrue(file_exists('html-initializr-master/index.html'))
            self.assertTrue(file_exists('html-initializr-master/404.html'))
            self.assertTrue(file_exists('html-initializr-master/pkey.yaml'))
            self.assertTrue(file_exists('html-initializr-master/project.yaml'))
            self.assertTrue(file_exists('html-initializr-master/js/vendor/jquery-1.11.1.min.js'))
            self.assertTrue(file_exists('html-initializr-master/js/vendor/modernizr-2.6.2.min.js'))
            self.assertTrue(file_exists('html-initializr-master/css/normalize.min.css'))

            # confirm that the project archive file was removed during build
            self.assertFalse(file_exists('initializr.zip'))

            # confirm that the key file still present in the directory after the build
            self.assertTrue(file_exists('zip_key.yaml'))

            # read the new outfiles that were generated from templates
            rendered_fourohfour = FileReader('html-initializr-master/404.html').read()
            rendered_index = FileReader('html-initializr-master/index.html').read()
            rendered_jquery = FileReader('html-initializr-master/js/vendor/jquery-1.11.1.min.js').read()
            rendered_normalize = FileReader('html-initializr-master/css/normalize.min.css').read()

            # assert correct contents of the files developed from templates
            self.assertEqual(self.fourohfour_text, rendered_fourohfour)
            self.assertEqual(self.indexhtml_text, rendered_index)
            self.assertEqual(self.jquery_text, rendered_jquery)
            self.assertEqual(self.normalize_text, rendered_normalize)           

            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
        
# remote .tar.gz project build
class RemoteProjectTarGZBuildTests(unittest.TestCase):
    
    def setUp(self):
        self.cwd = os.getcwd()
    
        self.local_project_testdir = "build-tests/remote-project/build"
        self.local_proj_targz_key = "targz_key.yaml"  # executed from the same directory
    
        # remove all contents of the build directory and build directory path from prior test run
        if dir_exists('build-tests/remote-project/build'):
            shutil.rmtree('build-tests/remote-project/build')
    
        self.assertFalse(dir_exists('build-tests/remote-project/build'))
    
        # create the build directory path
        os.makedirs('build-tests/remote-project/build')
    
        self.assertTrue(dir_exists('build-tests/remote-project/build'))
    
        # move the key into the build directory
        fr_key = FileReader('build-tests/remote-project/targz_key.yaml')
        targz_key_data = fr_key.read()
        fw_key = FileWriter('build-tests/remote-project/build/targz_key.yaml')
        fw_key.write(targz_key_data)
    
    
        # confirm that the build files are present
        self.assertTrue(file_exists('build-tests/remote-project/build/targz_key.yaml'))
    
        # get the expected text for outfile write assertions
        self.fourohfour_text = FileReader('standards/404.html').read()
        self.indexhtml_text = FileReader('standards/index.html').read()
        self.jquery_text = FileReader('standards/jquery.js').read()
        self.normalize_text = FileReader('standards/normalize-min.css').read()        
    
    def test_remote_targz_project_build(self):
        try:
            # make the build directory the CWD
            os.chdir(self.local_project_testdir)
            # run the project build
            b = Builder(self.local_proj_targz_key)
            b.run()
    
            # confirm directory unpacked with correct directory structure
            self.assertTrue(dir_exists('html-initializr-master'))
            self.assertTrue(dir_exists('html-initializr-master/css'))
            self.assertTrue(dir_exists('html-initializr-master/js/vendor'))
            self.assertTrue(dir_exists('html-initializr-master/templates'))
    
            # confirm presence of files
            self.assertTrue(file_exists('html-initializr-master/index.html'))
            self.assertTrue(file_exists('html-initializr-master/404.html'))
            self.assertTrue(file_exists('html-initializr-master/pkey.yaml'))
            self.assertTrue(file_exists('html-initializr-master/project.yaml'))
            self.assertTrue(file_exists('html-initializr-master/js/vendor/jquery-1.11.1.min.js'))
            self.assertTrue(file_exists('html-initializr-master/js/vendor/modernizr-2.6.2.min.js'))
            self.assertTrue(file_exists('html-initializr-master/css/normalize.min.css'))
    
    
            # confirm that the key file still present in the directory after the build
            self.assertTrue(file_exists('targz_key.yaml'))
    
            # read the new outfiles that were generated from templates
            rendered_fourohfour = FileReader('html-initializr-master/404.html').read()
            rendered_index = FileReader('html-initializr-master/index.html').read()
            rendered_jquery = FileReader('html-initializr-master/js/vendor/jquery-1.11.1.min.js').read()
            rendered_normalize = FileReader('html-initializr-master/css/normalize.min.css').read()
    
            # assert correct contents of the files developed from templates
            self.assertEqual(self.fourohfour_text, rendered_fourohfour)
            self.assertEqual(self.indexhtml_text, rendered_index)
            self.assertEqual(self.jquery_text, rendered_jquery)
            self.assertEqual(self.normalize_text, rendered_normalize)           
    
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
        
        
# remote .zip project build
class RemoteProjectZipBuildTests(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()

        self.local_project_testdir = "build-tests/remote-project/build"
        self.local_proj_zip_key = "zip_key.yaml"  # executed from the same directory

        # remove all contents of the build directory and build directory path from prior test run
        if dir_exists('build-tests/remote-project/build'):
            shutil.rmtree('build-tests/remote-project/build')

        self.assertFalse(dir_exists('build-tests/remote-project/build'))

        # create the build directory path
        os.makedirs('build-tests/remote-project/build')

        self.assertTrue(dir_exists('build-tests/remote-project/build'))

        # move the key into the build directory
        fr_key = FileReader('build-tests/remote-project/zip_key.yaml')
        zip_key_data = fr_key.read()
        fw_key = FileWriter('build-tests/remote-project/build/zip_key.yaml')
        fw_key.write(zip_key_data)


        # confirm that the build files are present
        self.assertTrue(file_exists('build-tests/remote-project/build/zip_key.yaml'))

        # get the expected text for outfile write assertions
        self.fourohfour_text = FileReader('standards/404.html').read()
        self.indexhtml_text = FileReader('standards/index.html').read()
        self.jquery_text = FileReader('standards/jquery.js').read()
        self.normalize_text = FileReader('standards/normalize-min.css').read()        

    def test_remote_zip_project_build(self):
        try:
            # make the build directory the CWD
            os.chdir(self.local_project_testdir)
            # run the project build
            b = Builder(self.local_proj_zip_key)
            b.run()

            # confirm directory unpacked with correct directory structure
            self.assertTrue(dir_exists('html-initializr-master'))
            self.assertTrue(dir_exists('html-initializr-master/css'))
            self.assertTrue(dir_exists('html-initializr-master/js/vendor'))
            self.assertTrue(dir_exists('html-initializr-master/templates'))

            # confirm presence of files
            self.assertTrue(file_exists('html-initializr-master/index.html'))
            self.assertTrue(file_exists('html-initializr-master/404.html'))
            self.assertTrue(file_exists('html-initializr-master/pkey.yaml'))
            self.assertTrue(file_exists('html-initializr-master/project.yaml'))
            self.assertTrue(file_exists('html-initializr-master/js/vendor/jquery-1.11.1.min.js'))
            self.assertTrue(file_exists('html-initializr-master/js/vendor/modernizr-2.6.2.min.js'))
            self.assertTrue(file_exists('html-initializr-master/css/normalize.min.css'))


            # confirm that the key file still present in the directory after the build
            self.assertTrue(file_exists('zip_key.yaml'))

            # read the new outfiles that were generated from templates
            rendered_fourohfour = FileReader('html-initializr-master/404.html').read()
            rendered_index = FileReader('html-initializr-master/index.html').read()
            rendered_jquery = FileReader('html-initializr-master/js/vendor/jquery-1.11.1.min.js').read()
            rendered_normalize = FileReader('html-initializr-master/css/normalize.min.css').read()

            # assert correct contents of the files developed from templates
            self.assertEqual(self.fourohfour_text, rendered_fourohfour)
            self.assertEqual(self.indexhtml_text, rendered_index)
            self.assertEqual(self.jquery_text, rendered_jquery)
            self.assertEqual(self.normalize_text, rendered_normalize)           

            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        

# test a build from the doxx Package Repository
class OfficialPackageRepositoryTests(unittest.TestCase):
    
    def setUp(self):
        self.cwd = os.getcwd()
        
        self.remote_packagerepo_testdir = "build-tests/remote-package-repo/build"
        self.package_repo_keypath = "build-tests/remote-package-repo/key.yaml"
        self.package_repo_missing_keypath = "build-tests/remote-package-repo/key_missingpackage.yaml"
        
        # remove all contents of the build directory and build directory path from prior test run
        if dir_exists(self.remote_packagerepo_testdir):
            shutil.rmtree(self.remote_packagerepo_testdir)
    
        self.assertFalse(dir_exists(self.remote_packagerepo_testdir))
        
        # create the build directory path with empty directory
        os.makedirs(self.remote_packagerepo_testdir)
    
        self.assertTrue(dir_exists(self.remote_packagerepo_testdir))
        
        # move the key with good file path into the build directory
        fr_key = FileReader('build-tests/remote-package-repo/key.yaml')
        key_data = fr_key.read()
        fw_key = FileWriter('build-tests/remote-package-repo/build/key.yaml')
        fw_key.write(key_data)
        
        # confirm that the build files are present
        self.assertTrue(file_exists('build-tests/remote-package-repo/build/key.yaml'))
        
    
    def test_package_repo_build_realpackage(self):
        try:
            # make the build directory the CWD
            os.chdir(self.remote_packagerepo_testdir)
            # run the project build
            b = Builder('key.yaml')
            b.run()
            
            self.assertTrue(file_exists('LICENSE'))
            
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
    
    def test_package_repo_build_badpackage(self):
        pass