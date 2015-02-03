#!/usr/bin/env python
# encoding: utf-8

import gzip
from os import remove
from Naked.toolshed.network import HTTP
from Naked.toolshed.file import FileWriter
from Naked.toolshed.system import stderr, stdout, stdout_xnl, file_exists
from Naked.toolshed.python import is_py3
from doxx.commands.unpack import unpack_run


def run_pull(url):
    # confirm that the argument is a URL
    if is_url(url):
        file_name = get_file_name(url)
        if len(file_name) == 0:
            file_name = "pullfile"
        
        # begin file pull
        stdout("[*] doxx: Pulling file...")
            
        if is_tar_gz_archive(file_name):
            try:
                pull_binary_file(url, file_name)      # pull remote file
            except Exception as e:
                stderr("[!] doxx: Unable to pull the tar.gz project. Error: " + str(e), exit=1)
            stdout("[*] doxx: Unpacking...")
            try:
                unpack_archive(file_name)             # unpack archive
            except Exception as e:
                stderr("[!] doxx: Unable to unpack the compressed project file. Error: " + str(e), exit=1)
            if file_exists(file_name):
                remove_file(file_name)                # remove the archive file
        elif is_zip_archive(file_name):
            try:
                pull_binary_file(url, file_name)      # pull remote file
            except Exception as e:
                stderr("[!] doxx: Unable to pull the .zip project. Error: " + str(e), exit=1)
            stdout("[*] doxx: Unpacking...")
            try:
                unpack_archive(file_name)             # unpack archive
            except Exception as e:
                stderr("[!] doxx: Unable to unpack the compressed project file. Error: " + str(e), exit=1)
            if file_exists(file_name):
                remove_file(file_name)                # remove the arhcive file
        elif is_gzip_file(file_name):
            try:
                pull_binary_file(url, file_name)      # pull the remote gzip file
            except Exception as e:
                stderr("[!] doxx: Unable to pull the compressed file. Error: " + str(e), exit=1)
            stdout("[!] doxx: Decompressing...")
            try:
                decompress_gzip(file_name)           # decompress the file text
            except Exception as e:
                stderr("[!] doxx: Unable to decompress the gzip file. Error: " + str(e), exit=1)
            if file_exists(file_name):
                remove_file(file_name)               # remove the gzip compressed file and leave the decompressed text file
        else:
            try:
                pull_text_file(url, file_name)       # it is assumed to be a plain text template or key file, pull the text
            except Exception as e:
                stderr("[!] doxx: Unable to pull the requested file. Error: " + str(e), exit=1)
    else:
        stderr("[!] doxx: Your URL is not properly formatted.  Please include the 'http://' or 'https://' protocol at the beginning of the requested URL.", exit=1)  


def is_url(url):
    """test for HTTP and HTTPS protocol in the string"""
    if url[0:7] == "http://" or url[0:8] == "https://":
        return True
    else:
        return False
    
def is_tar_gz_archive(file_name):
    """test for tar.gz file archive"""
    if file_name.lower().endswith('.tar.gz') or file_name.lower().endswith('.tar.gzip'):
        return True
    else:
        return False
    
def is_zip_archive(file_name):
    """test for zip file archive extension"""
    if file_name.lower().endswith('.zip'):
        return True
    else:
        return False
    
# must be tested AFTER tests for tar.gz archive because both will test true
def is_gzip_file(file_name):
    """test for gzip compressed file extension"""
    if file_name.lower().endswith('.gz') or file_name.lower().endswith('.gzip'):
        return True
    else:
        return False
    
def get_file_name(url):
    """returns the filename from a URL"""
    split_url = url.split('/')
    return split_url[-1]

def pull_binary_file(url, binary_file_name):
    """pulls a remote binary file and writes to disk"""
    # pull the binary file data
    http = HTTP(url)
    try:
        if http.get_status_ok():
            binary_data = http.res.content    
            # write binary data to disk
            try:
                fw = FileWriter(binary_file_name)
                fw.write_bin(binary_data)
            except Exception as e:
                stderr("[!] doxx: File write failed for '" + binary_file_name + "'.  Error: " + str(e), exit=1)
        else:
            fail_status_code = http.res.status_code
            stderr("[!] doxx: Unable to pull '" + url + "'. (HTTP status code: " + str(fail_status_code) + ")", exit=1)
    except Exception as e:
        stderr("[!] doxx: Unable to pull '" + url + "'. Error: " + str(e), exit=1)
    
def pull_text_file(url, text_file_name):
    """pulls a remote text file and writes to disk"""
    # pull the binary file data
    http = HTTP(url)
    try:
        if http.get_status_ok():
            text_data = http.res.text
            # write text data to disk
            try:
                fw = FileWriter(text_file_name)
                fw.write(text_data)
            except Exception as e:
                stderr("[!] doxx: File write failed for '" + text_file_name + "'.  Error: " + str(e), exit=1)
        else:
            fail_status_code = http.res.status_code
            stderr("[!] doxx: Unable to pull '" + url + "' (HTTP status code " + str(fail_status_code) + ")", exit=1)
    except Exception as e:
        stderr("[!] doxx: Unable to pull '" + url + "'. Error: " + str(e), exit=1)
    
def unpack_archive(archive_file_name):
    """unpacks a tar.gz or zip file archive and writes to local disk"""
    unpack_run(archive_file_name)
    
def decompress_gzip(gz_filename):
    """decompress gzip compressed file"""
    # decompress the gzip'd file
    f = gzip.open(gz_filename, 'rb')
    file_content = f.read()
    f.close()
    
    # monkeypatch for Python 3 byte string read issue
    if is_py3():
        file_content = str(file_content)
    
    # get the base file name for the decompressed file write
    filename_split = gz_filename.split('.')
    if len(filename_split) == 2:
        basename = filename_split[0]
    elif len(filename_split) > 2:
        basename = filename_split[0] + '.' + filename_split[1]  # concatenate first two parts of file name (e.g. example + '.' + 'tar' )
    else:
        basename = gz_filename
        
    # write the file locally
    fw = FileWriter(basename)
    fw.write(file_content)
    
def remove_file(file_name):
    """removes archive file that was pulled from a remote source"""
    if file_exists(file_name):
        remove(file_name)
    
    
