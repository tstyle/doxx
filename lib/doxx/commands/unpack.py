#!/usr/bin/env python
# encoding: utf-8

import tarfile
import zipfile
from os import remove
from Naked.toolshed.system import stderr, file_exists

def unpack_run(file_path):
    if tarfile.is_tarfile(file_path):
        unpack_targz_archive_file(file_path)
    elif zipfile.is_zipfile(file_path):
        unpack_zip_archive_file(file_path)
    else:
        stderr("[!] doxx: '" + file_path + "' does not appear to be a supported project archive type.  Please review the project archive documentation and try again.", exit=1)

def unpack_targz_archive_file(targz_file_path):
    try:
        tar = tarfile.open(targz_file_path, "r:*")
        tar.extractall()
        tar.close()
    except Exception as e:
        stderr("[!] doxx: Unable to unpack the file '" + targz_file_path + "'. Error: " + str(e))
        
def unpack_zip_archive_file(zip_file_path):
    try:
        zip_archive = zipfile.ZipFile(zip_file_path, 'r')
        zip_archive.extractall()
        zip_archive.close()
    except Exception as e:
        stderr("[!] doxx: Unable to unpack the file '" + zip_file_path + "'. Error: " + str(e))
        
def remove_compressed_archive_file(targz_file_path):
    if file_exists(targz_file_path):
        remove(targz_file_path)
    else:
        pass  # could not find the compressed archive file, raise no error message and abort attempt
    