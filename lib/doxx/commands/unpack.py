#!/usr/bin/env python
# encoding: utf-8

import tarfile
from os import remove
from Naked.toolshed.system import stderr, file_exists

def unpack_compressed_archive_file(targz_file_path):
    try:
        tar = tarfile.open(targz_file_path, "r:*")
        tar.extractall()
        tar.close()
    except Exception as e:
        stderr("[!] doxx: Unable to unpack the file '" + targz_file_path + "'. Error: " + str(e))
        

def remove_compressed_archive_file(targz_file_path):
    if file_exists(targz_file_path):
        remove(targz_file_path)
    else:
        pass  # could not find the compressed archive file, raise no error message and abort attempt
    