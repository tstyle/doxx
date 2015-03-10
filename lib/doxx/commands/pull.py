#!/usr/bin/env python
# encoding: utf-8

import gzip
import shutil
from os import remove, rename, makedirs
from os.path import join, dirname, basename
from Naked.toolshed.network import HTTP
from Naked.toolshed.file import FileWriter
from Naked.toolshed.system import stderr, stdout, file_exists, dir_exists
from Naked.toolshed.python import is_py3
from doxx.commands.unpack import unpack_run


def run_pull(url):
    # URL pulls for project archive packages, gzip files, text files
    if is_url(url):
        file_name = get_file_name(url)
        if len(file_name) == 0:
            file_name = "pullfile"
        
        # begin file pull
        stdout("[*] doxx: Pulling file...")
            
        if is_tar_gz_archive(file_name):
            root_dir = None
            try:
                pull_binary_file(url, file_name)      # pull remote file
            except Exception as e:
                stderr("[!] doxx: Unable to pull the tar.gz project. Error: " + str(e), exit=1)
            stdout("[*] doxx: Unpacking...")
            try:
                root_dir = unpack_archive(file_name)             # unpack archive and define the root directory
            except Exception as e:
                stderr("[!] doxx: Unable to unpack the compressed project file. Error: " + str(e), exit=1)
            if file_exists(file_name):
                remove_file(file_name)                # remove the archive file
            if file_exists('pkey.yaml'):
                if not file_exists('key.yaml'):
                    rename('pkey.yaml', 'key.yaml')   # change name of pkey.yaml to key.yaml if there is not already a key.yaml file
            return root_dir                           # return the root directory path for calling code that needs it
        elif is_zip_archive(file_name):
            root_dir = None
            try:
                pull_binary_file(url, file_name)      # pull remote file
            except Exception as e:
                stderr("[!] doxx: Unable to pull the .zip project. Error: " + str(e), exit=1)
            stdout("[*] doxx: Unpacking...")
            try:
                root_dir = unpack_archive(file_name)             # unpack archive and define the root directory
            except Exception as e:
                stderr("[!] doxx: Unable to unpack the compressed project file. Error: " + str(e), exit=1)
            if file_exists(file_name):
                remove_file(file_name)                # remove the arhcive file
            if file_exists('pkey.yaml'):
                if not file_exists('key.yaml'):
                    rename('pkey.yaml', 'key.yaml')   # change name of pkey.yaml to key.yaml if there is not already a key.yaml file      
            return root_dir                           # return the root directory path for calling code that needs it
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
        # SHORT CODE PULL REQUESTS for Github repository, CDNJS, etc
        if "/" in url:
            short_code = url
            
            if short_code.startswith('cdnjs:'):
                pass  # add code for cdnjs pulls (syntax: 'cdnjs:/project')
            else:
                # default to Github repositories
                keep_a_file_or_dir = False    # indicator for user request to maintain single file or dir from repository
                
                # parse the file or directory path keep request
                if "+" in short_code:    # user requested single directory or file from the repository
                    short_code_keep = short_code.split("+")
                    short_code = short_code_keep[0]  # split on the + char and eliminate it from the request argument at this point
                    keep_path = short_code_keep[1]   # the file or dir path to keep
                    keep_a_file_or_dir = True        # switch the indicator
    
                short_code_parts = short_code.split('/')
                if len(short_code_parts) == 2:
                    if ":" in short_code_parts[1]:
                        # contains a request for a specific branch of the Github repository
                        user = short_code_parts[0]
                        if ":" in user:
                            stderr("[!] doxx: the short code for a Github repository does not have the proper format")
                            stderr("[!] doxx: the syntax is user/repository[:branch][+keepath]", exit=1)
                        repo_parts = short_code_parts[1].split(':')
                        repo = repo_parts[0]
                        branch = repo_parts[1]
                        targz_filename = repo + "-" + branch + ".tar.gz"
                        url = "https://github.com/{{user}}/{{repository}}/archive/{{branch}}.tar.gz"
                        url = url.replace("{{user}}", user)
                        url = url.replace("{{repository}}", repo)
                        url = url.replace("{{branch}}", branch)
                        user_message = "[*] doxx: Pulling branch '" + branch + "' of Github repository '" + user + "/" + repo + "'..."
                    else:
                        # default to the master Github repository branch
                        user = short_code_parts[0]
                        if ":" in user:
                            stderr("[!] doxx: the short code for Github repositories does not have a proper format")
                            stderr("[!] doxx: the syntax is user/repository[:branch][+keeppath]", exit=1)                        
                        repo = short_code_parts[1]
                        targz_filename = repo + "-master.tar.gz"
                        url = "https://github.com/{{user}}/{{repository}}/archive/master.tar.gz"
                        url = url.replace("{{user}}", user)
                        url = url.replace("{{repository}}", repo)
                        user_message = "[*] doxx: Pulling master branch of Github repository '" + user + "/" + repo + "'..."
                     
                    # notify user of the pull   
                    stdout(user_message)
                        
                    try:
                        pull_binary_file(url, targz_filename)  # pull the archive file
                    except Exception as e:
                        stderr("[!] doxx: Unable to pull the Github repository.  Error: " + str(e), exit=1)
                        
                    if file_exists(targz_filename):
                        try:
                            # Unpack and remove the archive file
                            targz_basename = unpack_archive(targz_filename)  # unpack the archive locally
                            remove(targz_filename)                           # remove the archive file
                        except Exception as e:
                            stderr("[!] doxx: Unable to unpack the pulled Github repository. Error: " + str(e), exit=1)                        
                            
                        try:
                            # Did user request keep of a specific file or directory path?
                            if keep_a_file_or_dir is True:
                                # is this a multilevel path request?
                                # if so, make OS dependent file path from the user argument (keep path argument syntax uses POSIX path style on all platforms)
                                if "/" in keep_path:
                                    keep_path_parts = keep_path.split('/')
                                    keep_path_depth = len(keep_path_parts)
                                    if keep_path_depth > 3:
                                        stderr("[!] doxx: doxx supports up to 3 levels of depth in the keep shortcode. Your request exceeded that level of depth and the requested file or directory was not retrieved from the repository.", exit=1)
                                    
                                    # make the OS dependent paths
                                    if keep_path_depth == 2:
                                        path_part_one = keep_path_parts[0]
                                        path_part_two = keep_path_parts[1]
                                        keep_path = join(path_part_one, path_part_two)
                                    elif keep_path_depth == 3:
                                        path_part_one = keep_path_parts[0]
                                        path_part_two = keep_path_parts[1]
                                        path_part_three = keep_path_parts[2]
                                        keep_path = join(path_part_one, path_part_two, path_part_three)
                                else:
                                    keep_path_depth = 1  # need to have a definition of depth of file/dir keep for mkdirs code below
                                    
                                joined_keep_path = join(targz_basename, keep_path)  # the path to the local version of the file or directory following pull
                                
                                if dir_exists(joined_keep_path):
                                    stdout("[*] doxx: keeping the directory '" + keep_path + "'")
                                    if dir_exists(keep_path):
                                        shutil.rmtree(targz_basename)  # remove the pulled repository file prior to raising the error message
                                        stderr("[!] doxx: the directory path " + keep_path + "' already exists and the requested write did not occur. Please remove it and repeat your pull request.", exit=1)
                                    shutil.copytree(joined_keep_path, keep_path)
                                    shutil.rmtree(targz_basename)
                                elif file_exists(joined_keep_path):
                                    stdout("[*] doxx: keeping the file '" + keep_path + "'")
                                    if keep_path_depth > 1:
                                        if dir_exists(dirname(keep_path)):
                                            pass  # do nothing if the path already exists
                                        else:
                                            makedirs(dirname(keep_path))       # make the necessary directory path to the file in the root directory for the pull
                                    ##TODO## : keep file overwrite by default or remove it?
                                    shutil.copy2(joined_keep_path, keep_path)  # write the file relative to the top level pull directory
                                    shutil.rmtree(targz_basename)              # remove the rest of the repository that was pulled
                                else:
                                    stderr("[!] doxx: '" + joined_keep_path + "' does not appear to be a file or directory in the requested repository.")
                        except Exception as e:
                            stderr("[!] doxx: Unable to process the requested keep file or directory path. Error" + str(e), exit=1)
                    
                    else:  # archive file not found locally
                        stderr("[!] doxx: The Github repository pull did not complete successfully.  Please try again.")
                else:  # length of short_code_parts > 2
                    stderr("[!] doxx: short code syntax for Github repository pulls:", exit=0)
                    stderr("    $ doxx pull user/repository")
                    stderr("[!] doxx: with an optional branch or release:")
                    stderr("    $ doxx pull user/repository:branch")
                    stderr("[!] doxx: with an optional branch or release AND optional keep file or directory path:")
                    stderr("    $ doxx pull user/repository:branch+path", exit=1)
            
        # PROJECT PACKAGES - official repository package pulls
        else:  
            from doxx.datatypes.package import OfficialPackage
            package_name = url
            package = OfficialPackage()
            package_url = package.get_package_targz_url(package_name)
            package_archive_name = package_name + ".tar.gz"
            root_dir = None
            # pull the package archive file
            stdout("[*] doxx: Pulling package '" + package_name + "'...")
            try:
                pull_binary_file(package_url, package_archive_name)
            except Exception as e:
                stderr("[!] doxx: Unable to pull the doxx repository package.  Error: " + str(e), exit=1)
            # unpack the archive file
            stdout("[*] doxx: Unpacking...")
            try:
                root_dir = unpack_archive(package_archive_name)             # unpack archive and define the root directory
            except Exception as e:
                stderr("[!] doxx: Unable to unpack the project package. Error: " + str(e), exit=1)            
            # remove the archive file
            if file_exists(package_archive_name):
                remove_file(package_archive_name)                # remove the archive file
            if file_exists('pkey.yaml'):
                if not file_exists('key.yaml'):
                    rename('pkey.yaml', 'key.yaml')              # change name of pkey.yaml to key.yaml if there is not already a key.yaml file            
            return root_dir                                      # return the root directory path for calling code that needs it            


def is_url(url):
    """test for HTTP and HTTPS protocol in the string"""
    if len(url) > 6 and (url[0:7] == "http://" or url[0:8] == "https://"):
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
            if fail_status_code == 404:
                stderr("[!] doxx: Unable to pull the file because it does not appear to exist. (HTTP status code: " + str(fail_status_code) + ")", exit=1)
            else:
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
    root_dir = unpack_run(archive_file_name)  # root directory of unpacked archive returned from the unpack function, returned from this function if calling code needs it
    return root_dir


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
        