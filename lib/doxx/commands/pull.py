#!/usr/bin/env python
# encoding: utf-8

from os import remove
from Naked.toolshed.network import HTTP
from Naked.toolshed.file import FileWriter
from Naked.toolshed.system import stderr, stdout, stdout_xnl, file_exists
from doxx.commands.unpack import unpack_compressed_archive_file


def pull_binary_file(url):
    # confirm that it is a properly formatted URL
    if url[0:7] == "http://" or url[0:8] == "https://":
        pass
    else:
        stderr("[!] doxx: Your URL is not properly formatted.  Please include the 'http://' or 'https://' protocol at the beginning of the requested URL.", exit=1)
    
    # if passes above test, find the archive name from the URL
    split_url = url.split('/')
    archive_file_name = split_url[-1]  # last string should contain the filename
    
    # test for presence of a filename, some URL may not include the filename in the URL string (e.g. test.com/compress/)
    if len(archive_file_name) == 0:
        archive_file_name = "doxx-project.tar.gz"
    
    # pull the binary file data
    stdout("[*] doxx: Pulling package...")
    http = HTTP(url)
    binary_data = http.get_bin()
    
    # write binary data to disk
    fw = FileWriter(archive_file_name)
    fw.write_bin(binary_data)  
    
    # unpack the file to the current working directory
    stdout("[*] doxx: Unpacking...")
    unpack_compressed_archive_file(archive_file_name)
    
    # remove the compressed archive file that was pulled
    if file_exists(archive_file_name):
        remove(archive_file_name)
    
    
