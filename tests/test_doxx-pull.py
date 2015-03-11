#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest
import shutil

from Naked.toolshed.system import file_exists, dir_exists
from Naked.toolshed.file import FileReader

from doxx.commands.pull import get_file_name, is_gzip_file, is_url, is_tar_gz_archive, is_zip_archive, run_pull
from doxx.commands.pullkey import run_pullkey


class DoxxPullTests(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        self.targz_pull_dir = "pull-tests/targz"
        self.zip_pull_dir = "pull-tests/zip"
        self.gzip_pull_dir = "pull-tests/gzip"
        self.text_pull_dir = "pull-tests/text"
        if dir_exists(self.targz_pull_dir):
            if file_exists(os.path.join(self.targz_pull_dir, 'key.yaml')):
                os.remove(os.path.join(self.targz_pull_dir, 'key.yaml'))
            if file_exists(os.path.join(self.targz_pull_dir, 'test.doxt')):
                os.remove(os.path.join(self.targz_pull_dir, 'test.doxt'))
            if file_exists(os.path.join(self.targz_pull_dir, 'test2.doxt')):
                os.remove(os.path.join(self.targz_pull_dir, 'test2.doxt'))
        if dir_exists(self.zip_pull_dir):
            if file_exists(os.path.join(self.zip_pull_dir, 'key.yaml')):
                os.remove(os.path.join(self.zip_pull_dir, 'key.yaml'))
            if file_exists(os.path.join(self.zip_pull_dir, 'test.doxt')):
                os.remove(os.path.join(self.zip_pull_dir, 'test.doxt'))
            if file_exists(os.path.join(self.zip_pull_dir, 'test2.doxt')):
                os.remove(os.path.join(self.zip_pull_dir, 'test2.doxt'))
        if dir_exists(self.gzip_pull_dir):
            if file_exists(os.path.join(self.gzip_pull_dir, 'mit.doxt')):
                os.remove(os.path.join(self.gzip_pull_dir, 'mit.doxt'))
        if dir_exists(self.text_pull_dir):
            if file_exists(os.path.join(self.text_pull_dir, 'mit.doxt')):
                os.remove(os.path.join(self.text_pull_dir, 'mit.doxt'))        
            
    
    # File extension tests
    def test_doxx_pull_is_url_http_correct(self):
        self.assertTrue(is_url('http://www.test.com/bogus'))
    
    def test_doxx_pull_is_url_https_correct(self):
        self.assertTrue(is_url('https://www.test.com/bogus'))    
        
    def test_doxx_pull_is_url_http_incorrect(self):
        self.assertFalse(is_url('www.test.com/bogus'))
        
    def test_doxx_pull_targz_correct(self):
        self.assertTrue(is_tar_gz_archive('test.tar.gz'))
        
    def test_doxx_pull_targz_correct_alternate(self):
        self.assertTrue(is_tar_gz_archive('test.tar.gzip'))
        
    def test_doxx_pull_targz_correct_caps(self):
        self.assertTrue(is_tar_gz_archive('test.TAR.GZ'))
        
    def test_doxx_pull_targz_incorrect(self):
        self.assertFalse(is_tar_gz_archive('test.txt'))
        
    def test_doxx_pull_zip_correct(self):
        self.assertTrue(is_zip_archive('test.zip'))
        
    def test_doxx_pull_zip_correct_alternate(self):
        self.assertTrue(is_zip_archive('test.ZIP'))
        
    def test_doxx_pull_zip_incorrect(self):
        self.assertFalse(is_zip_archive('test.txt'))
        
    def test_doxx_pull_gz_file_correct(self):
        self.assertTrue(is_gzip_file('test.gz'))
        
    def test_doxx_pull_gz_file_correct_alternate(self):
        self.assertTrue(is_gzip_file('test.gzip'))
        
    def test_doxx_pull_gz_file_correct_caps(self):
        self.assertTrue(is_gzip_file('test.GZ'))
        
    def test_doxx_pull_gz_file_incorrect(self):
        self.assertFalse(is_gzip_file('test.txt'))
    
        
    # file name from URL tests
    def test_doxx_pull_url_split_filename(self):
        self.assertEqual('test.doxt.gz', get_file_name('http://test.com/templates/test.doxt.gz'))
        
    def test_doxx_pull_url_split_filename_empty(self):
        self.assertEqual('', get_file_name('http://test.com/templates/'))  # when only directory paths without filename, get an empty string - becomes 'pullfile' in run_pull function
        
    
    # pull tests
    
    # pull tar.gz project archive from GitHub
    def test_doxx_pull_targz_archive(self):
        try:
            os.chdir(self.targz_pull_dir)
            run_pull('https://github.com/bit-store/testfiles/raw/master/doxx/pull-tests/packed.tar.gz')
            self.assertTrue(file_exists('key.yaml'))
            self.assertTrue(file_exists('test.doxt'))
            self.assertTrue(file_exists('test2.doxt'))
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
    
    
    # pull .zip project archive
    def test_doxx_pull_zip_archive(self):
        try:
            os.chdir(self.zip_pull_dir)
            run_pull('https://github.com/bit-store/testfiles/raw/master/doxx/pull-tests/packed.zip')
            self.assertTrue(file_exists('key.yaml'))
            self.assertTrue(file_exists('test.doxt'))
            self.assertTrue(file_exists('test2.doxt'))
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
    
    
    # pull .gzip file
    def test_doxx_pull_gzip_file(self):
        try:
            os.chdir(self.gzip_pull_dir)
            run_pull('https://github.com/bit-store/testfiles/raw/master/doxx/pull-tests/mit.doxt.gz')
            self.assertTrue(file_exists('mit.doxt'))            
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
    
    # pull text file
    def test_doxx_pull_text_file(self):
        try:
            os.chdir(self.text_pull_dir)
            run_pull('https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/pull-tests/mit.doxt')
            self.assertTrue(file_exists('mit.doxt'))            
            os.chdir(self.cwd)            
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
    def test_doxx_pull_bad_url(self):
        with self.assertRaises(SystemExit):
            run_pull('https://raw.githubusercontent.com/bit-store/testfiles/master/doxx/pull-tests/completelybogus.html')
    
    

class DoxxPullkeyCommandTests(unittest.TestCase):
    
    def setUp(self):
        self.cwd = os.getcwd()
        self.key_pull_dir = "pull-tests/key"
        self.pulled_key_file = "key.yaml"
        
        if dir_exists(self.key_pull_dir):
            if file_exists(os.path.join(self.key_pull_dir, self.pulled_key_file)):
                os.remove(os.path.join(self.key_pull_dir, self.pulled_key_file))  # remove the file from the last test
        else:
            os.mkdir(self.key_pull_dir)
            
    def test_doxx_pullkey_command_goodpackage(self):
        try:
            os.chdir(self.key_pull_dir)
            run_pullkey('license-mit')
            self.assertTrue(file_exists(self.pulled_key_file))
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
    def test_doxx_pullkey_command_badpackage(self):
        try:
            os.chdir(self.key_pull_dir)
            with self.assertRaises(SystemExit):
                run_pullkey('completely-bogus-package')
            self.assertFalse(file_exists(self.pulled_key_file))
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
        
class DoxxPullGithubRepoShortcodeTests(unittest.TestCase):
    
    def setUp(self):
        self.cwd = os.getcwd()
        self.test_dir = "pull-tests/ghrepo"
        self.repo_shortcode_master = "bit-store/testfiles"
        self.repo_shortcode_version = "bit-store/testfiles:v1.1"
        self.repo_shortcode_master_cherry_file = "bit-store/testfiles+doxx/testfile.txt"
        self.repo_shortcode_master_cherry_file_no_ext = "bit-store/testfiles+doxx/testfile"
        self.repo_shortcode_branch_cherry_file = "bit-store/testfiles:v1.1+doxx/testfile.txt"
        self.repo_shortcode_branch_cherry_file_no_ext = "bit-store/testfiles:v1.1+doxx/testfile"
        
        # remove any previous testing directories
        if dir_exists(os.path.join(self.test_dir, 'testfiles')):
            shutil.rmtree(os.path.join(self.test_dir, 'testfiles-master'))
            
        if dir_exists(os.path.join(self.test_dir, 'testfiles-1.1')):
            shutil.rmtree(os.path.join(self.test_dir, 'testfiles-1.1'))
            
        if dir_exists(os.path.join(self.test_dir, "doxx")):
            shutil.rmtree(os.path.join(self.test_dir, "doxx"))
        
    def test_doxx_github_shortcode_master(self):
        try:
            os.chdir(self.test_dir)
            run_pull(self.repo_shortcode_master)
            self.assertTrue(dir_exists("testfiles-master"))
            self.assertTrue(dir_exists("testfiles-master/doxx"))
            self.assertTrue(dir_exists("testfiles-master/doxx/templates"))
            self.assertTrue(file_exists("testfiles-master/doxx/testfile"))
            self.assertTrue(file_exists("testfiles-master/doxx/testfile.txt"))
            
            # execute the command a second time and confirm that the repository overwrites the testfiles directory without exception
            run_pull(self.repo_shortcode_master)
            
            # cleanup
            shutil.rmtree("testfiles-master")

            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
        
    def test_doxx_github_shortcode_branch(self):
        try:
            os.chdir(self.test_dir)
            run_pull(self.repo_shortcode_version)
            self.assertTrue(dir_exists("testfiles-1.1"))
            self.assertTrue(dir_exists("testfiles-1.1/doxx"))
            self.assertTrue(dir_exists("testfiles-1.1/doxx/templates"))
            self.assertTrue(file_exists("testfiles-1.1/doxx/testfile"))
            self.assertTrue(file_exists("testfiles-1.1/doxx/testfile.txt"))
            
            # execute the command again and confirm that it overwrites the directory with same name
            run_pull(self.repo_shortcode_version)
            
            #cleanup
            shutil.rmtree("testfiles-1.1")
            
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
    
    def test_doxx_github_shortcode_master_cherrypick_files(self):
        try:
            os.chdir(self.test_dir)
            
            # FILE with file extension
            run_pull(self.repo_shortcode_master_cherry_file)
            self.assertTrue(file_exists("doxx/testfile.txt"))
            fr_tft = FileReader("doxx/testfile.txt")
            text_tft = fr_tft.read()
            self.assertEqual(u"testfile.txt\n", text_tft)
            
            # execute the command again and confirm that overwrite does not occur, adds -new to the filename
            run_pull(self.repo_shortcode_master_cherry_file)
            self.assertTrue(file_exists("doxx/testfile.txt"))
            self.assertTrue(file_exists("doxx/testfile-new.txt"))
            fr_tftn = FileReader("doxx/testfile-new.txt")
            text_tftn = fr_tftn.read()
            self.assertEqual(u"testfile.txt\n", text_tftn)
            
            #cleanup
            shutil.rmtree("doxx")
            
            # FILE without file extension
            run_pull(self.repo_shortcode_master_cherry_file_no_ext)
            self.assertTrue(file_exists("doxx/testfile"))
            fr_tf = FileReader("doxx/testfile")
            text_tf = fr_tf.read()
            self.assertEqual(u"testfile\n", text_tf)
            
            # execute the command again and confirm that overwrite does not occur, adds -new to the filename
            run_pull(self.repo_shortcode_master_cherry_file_no_ext)
            self.assertTrue(file_exists("doxx/testfile"))
            self.assertTrue(file_exists("doxx/testfile-new"))
            fr_tfn = FileReader("doxx/testfile-new")
            text_tfn = fr_tfn.read()
            self.assertEqual(u"testfile\n", text_tfn)              
            
            #cleanup
            shutil.rmtree("doxx")
            
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
        
    def test_doxx_github_shortcode_branch_cherrypick_files(self):
        try:
            os.chdir(self.test_dir)
            
            # FILE with file extension
            run_pull(self.repo_shortcode_branch_cherry_file)
            self.assertTrue(file_exists("doxx/testfile.txt"))
            fr_tft = FileReader("doxx/testfile.txt")
            text_tft = fr_tft.read()
            self.assertEqual(u"testfile.txt branch v1.1\n", text_tft)
            
            # execute the command again and confirm that overwrite does not occur, adds -new to the filename
            run_pull(self.repo_shortcode_branch_cherry_file)
            self.assertTrue(file_exists("doxx/testfile.txt"))
            self.assertTrue(file_exists("doxx/testfile-new.txt"))
            fr_tftn = FileReader("doxx/testfile-new.txt")
            text_tftn = fr_tftn.read()
            self.assertEqual(u"testfile.txt branch v1.1\n", text_tftn)
            
            #cleanup
            shutil.rmtree("doxx")                        
        
            # FILE without file extension
            run_pull(self.repo_shortcode_branch_cherry_file_no_ext)
            self.assertTrue(file_exists("doxx/testfile"))
            fr_tf = FileReader("doxx/testfile")
            text_tf = fr_tf.read()
            self.assertEqual(u"testfile branch v1.1\n", text_tf)
            
            # execute the command again and confirm that overwrite does not occur, adds -new to the filename
            run_pull(self.repo_shortcode_branch_cherry_file_no_ext)
            self.assertTrue(file_exists("doxx/testfile"))
            self.assertTrue(file_exists("doxx/testfile-new"))
            fr_tfn = FileReader("doxx/testfile-new")
            text_tfn = fr_tfn.read()
            self.assertEqual(u"testfile branch v1.1\n", text_tfn)              
            
            #cleanup
            shutil.rmtree("doxx")
            
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
        
    def test_doxx_github_shortcode_errors(self):
        pass
    