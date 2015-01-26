#!/usr/bin/env python
# encoding: utf-8

import tarfile
from Naked.toolshed.system import stderr

def unpack_targz_file(targz_file_path):
    try:
        tar = tarfile.open(targz_file_path, "r:gz")
        tar.extractall()
        tar.close()
    except Exception as e:
        stderr("[!] doxx: Unable to unpack the file '" + targz_file_path + "'. Error: " + str(e))
    