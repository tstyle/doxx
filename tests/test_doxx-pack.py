#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import unittest

from Naked.toolshed.system import file_exists

from doxx.commands.pack import tar_gzip_package_directory
from doxx.commands.unpack import unpack_run, remove_compressed_archive_file

class DoxxPackTests(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        self.pack_main_dir = "pack-unpack-tests"
        self.pack_dir = "pack-unpack-tests/pack"
        self.unpack_dir = "pack-unpack-tests/unpack"
        
        # remove the test tar.gz file from the pack directory if present
        if file_exists("pack-unpack-tests/pack/packed.tar.gz"):
            os.remove("pack-unpack-tests/pack/packed.tar.gz")
            self.assertFalse(file_exists("pack-unpack-tests/pack/packed.tar.gz"))
            
        if file_exists('pack-unpack-tests/unpack/key.yaml'):
            os.remove('pack-unpack-tests/unpack/key.yaml')
            self.assertFalse(file_exists('pack-unpack-tests/unpack/key.yaml'))
            
        if file_exists('pack-unpack-tests/unpack/test.doxt'):
            os.remove('pack-unpack-tests/unpack/test.doxt')
            self.assertFalse(file_exists('pack-unpack-tests/unpack/test.doxt'))
            
        if file_exists('pack-unpack-tests/unpack/test2.doxt'):
            os.remove('pack-unpack-tests/unpack/test2.doxt')
            self.assertFalse(file_exists('pack-unpack-tests/unpack/test2.doxt'))
            
        if not file_exists('pack-unpack-tests/unpack/unpack.tar.gz'):
            os.chdir('pack-unpack-tests')  # change to the pack/unpack test dir in order to create the new file
            tar_gzip_package_directory('unpack', 'pack')
            self.assertTrue(file_exists('unpack.tar.gz'))
            os.rename('unpack.tar.gz', 'unpack/unpack.tar.gz')  # move it into the proper directory
            self.assertTrue(file_exists('unpack/unpack.tar.gz'))
            os.chdir(self.cwd)
            
        
    # test the pack command
    def test_doxx_pack_directory(self):
        try:
            os.chdir(self.pack_main_dir)
            tar_gzip_package_directory("packed", "pack")
            self.assertTrue(file_exists('packed.tar.gz'))
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e
        
    # test the unpack command
    def test_doxx_unpack_package(self):
        try:
            os.chdir(self.unpack_dir)
            unpack_run('unpack.tar.gz')
            self.assertTrue(file_exists('key.yaml'))
            self.assertTrue(file_exists('test.doxt'))
            self.assertTrue(file_exists('test2.doxt'))
            self.assertTrue(file_exists('unpack.tar.gz'))
            remove_compressed_archive_file('unpack.tar.gz')
            self.assertFalse(file_exists('unpack.tar.gz'))
            os.chdir(self.cwd)
        except Exception as e:
            os.chdir(self.cwd)
            raise e