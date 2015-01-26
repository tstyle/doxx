#!/usr/bin/env python
# encoding: utf-8

import tarfile
from os import chdir, getcwd
from Naked.toolshed.system import stderr

def tar_gzip_package_directory(archive_name, root_dir):
    try:
        current_dir = getcwd()  
        archive_gz_name = archive_name + ".tar.gz"
        tar = tarfile.open(archive_gz_name, mode="w:gz", compresslevel=8)    # file writes to current working directory
        chdir(root_dir)  # navigate to the root directory to add the files to the archive
        tar.add(".")     # make tar.gz archive
        tar.close()
        chdir(current_dir)  # navigate back to user's current working directory
    except Exception as e:
        os.chdir(current_dir)  # if exception was raised, make sure that user is back in their current working directory before raising system exit
        stderr("[!] doxx: Unable to pack the directory '" + root_dir + "'. Error: " + str(e))
        