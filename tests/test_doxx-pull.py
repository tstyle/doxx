#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import unittest

from Naked.toolshed.system import file_exists, dir_exists

from doxx.commands.pull import get_file_name, is_gzip_file, is_url, is_tar_gz_archive, is_zip_archive, run_pull


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
    
    
    