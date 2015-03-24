#!/usr/bin/env python
# encoding: utf-8

from os import remove, makedirs
import os.path
from multiprocessing import Process, Lock

from Naked.toolshed.system import stderr, stdout, file_exists, dir_exists
from doxx.commands.pull import pull_binary_file, pull_text_file
from doxx.commands.unpack import unpack_run


def pull_textfile_runner(text_url_dict):
    file_list = text_url_dict.keys()      # the local outfile names in a list    
    number_of_files = len(file_list)      # the number of files included in the list
    if number_of_files > 0:   
        if number_of_files > 1:  # multiple text file pull, each in separate process
            processes = []       # list of spawned processes
            outputlock = Lock()  # stdout / stderr writes lock
            iolock = Lock()      # input/output lock
            
            # iterate through requested files and execute pull in separate process for each one
            for file_path in file_list:
                p = Process(target=_pull_textfile_multiprocess, args=(file_path, text_url_dict[file_path], outputlock, iolock))
                p.start()
                processes.append(p)
                
            for process in processes:
                process.join(timeout=60)
                
        else:  # single text file pull
            file_path = file_list[0]
            _pull_textfile(file_path, text_url_dict[file_path])  # file_path is local path for write, dictionary value is the URL
    else:
        stderr("[!] doxx: Unable to find text files to pull in the key file", exit=0)

def pull_binaryfile_runner(binary_url_dict):
    file_list = binary_url_dict.keys()      # the local outfile names in a list    
    number_of_files = len(file_list)      # the number of files included in the list
    if number_of_files > 0:   
        if number_of_files > 1:  # multiple binary file pull, each in separate process
            processes = []       # list of spawned processes
            outputlock = Lock()  # stdout / stderr writes lock
            iolock = Lock()      # input/output lock
            
            # iterate through requested files and execute pull in separate process for each one
            for file_path in file_list:
                p = Process(target=_pull_binaryfile_multiprocess, args=(file_path, binary_url_dict[file_path], outputlock, iolock))
                p.start()
                processes.append(p)
                
            for process in processes:
                process.join(timeout=60)
                
        else:  # single text file pull
            file_path = file_list[0]
            _pull_binaryfile(file_path, binary_url_dict[file_path])  # file_path is local path for write, dictionary value is the URL
    else:
        stderr("[!] doxx: Unable to find binary files to pull in the key file", exit=0)

def pull_github_repo_runner(repo_url_dict):
    file_list = repo_url_dict.keys()      # the local outfile names in a list    
    number_of_files = len(file_list)      # the number of files included in the list
    if number_of_files > 0:   
        if number_of_files > 1:  # multiple binary file pull, each in separate process
            stdout("[*] doxx: Hang in there. Pulling " + str(number_of_files) + " entire repositories. This may take a bit of time...")
            processes = []       # list of spawned processes
            outputlock = Lock()  # stdout / stderr writes lock
            iolock = Lock()      # input/output lock
            
            # iterate through requested files and execute pull in separate process for each one
            for file_path in file_list:
                p = Process(target=_pull_github_repo_multiprocess, args=(file_path, repo_url_dict[file_path], outputlock, iolock))
                p.start()
                processes.append(p)
                
            for process in processes:
                process.join(timeout=120)
                
        else:  # single text file pull
            stdout("[*] doxx: Hang in there. Pulling an entire repository. This may take a bit of time...")
            file_path = file_list[0]
            _pull_github_repo(file_path, repo_url_dict[file_path])  # file_path is local path for write, dictionary value is the URL
    else:
        stderr("[!] doxx: Unable to find binary files to pull in the key file", exit=0)   

def _pull_textfile(file_path, url):
    # create OS dependent file path (if necessary)
    file_path = _make_os_dependent_path(file_path)
    # make directory structure if necessary for the file path
    if os.path.dirname(file_path) is not "":
        _create_pull_dirs(file_path)
    # pull the file and write to local filesystem
    try:
        pull_text_file(url, file_path)
    except Exception as e:
        stderr("[!] doxx: Unable to pull '" + file_path + "' from '" + url + "'. Error: " + str(e), exit=1)
        
    if file_exists(file_path):
        stdout("[+] doxx: '" + file_path + "' ...check!")
    else:
        stderr("[!] doxx: There was an error pulling '" + file_path + "'. Error: Unable to locate local file.", exit=1)    
    
def _pull_textfile_multiprocess(file_path, url, outputlock, iolock):
    # create OS dependent file path (if necessary)
    file_path = _make_os_dependent_path(file_path)
    # make directory structure if necessary for the file path
    if os.path.dirname(file_path) is not "":
        iolock.acquire()
        _create_pull_dirs(file_path)
        iolock.release()
    # pull the file and write to local filesystem
    try:
        pull_text_file(url, file_path)
    except Exception as e:
        outputlock.acquire()
        stderr("[!] doxx: Unable to pull '" + file_path + "' from '" + url + "'. Error: " + str(e), exit=0)
        outputlock.release()
    if file_exists(file_path):
        outputlock.acquire()
        stdout("[+] doxx: '" + file_path + "' ...check!")
        outputlock.release()
    else:
        outputlock.acquire()
        stderr("[!] doxx: There was an error pulling '" + file_path + "'. Error: Unable to locate local file", exit=0)
        outputlock.release()
    
def _pull_binaryfile(file_path, url):
    # create OS dependent file path (if necessary)
    file_path = _make_os_dependent_path(file_path)
    # make directory structure if necessary for the file path
    if os.path.dirname(file_path) is not "":
        _create_pull_dirs(file_path)
    # pull the file and write to local filesystem    
    try:
        pull_binary_file(url, file_path)
    except Exception as e:
        stderr("[!] doxx: Unable to pull '" + file_path + "' from '" + url + "'. Error: " + str(e), exit=0)
    if file_exists(file_path):
        stdout("[+] doxx: '" + file_path + "' ...check!")
    else:
        stderr("[!] doxx: There was an error pulling '" + file_path + "'. Error: Unable to locate local file.", exit=1) 
    
def _pull_binaryfile_multiprocess(file_path, url, outputlock):
    # create OS dependent file path (if necessary)
    file_path = _make_os_dependent_path(file_path)
    # make directory structure if necessary for the file path
    if os.path.dirname(file_path) is not "":
        iolock.acquire()
        _create_pull_dirs(file_path)
        iolock.release()
    # pull the file and write to local filesystem
    try:
        pull_binary_file(url, file_path)
    except Exception as e:
        outputlock.acquire()
        stderr("[!] doxx: Unable to pull '" + file_path + "' from '" + url + "'. Error: " + str(e), exit=0)
        outputlock.release()
    if file_exists(file_path):
        outputlock.acquire()
        stdout("[+] doxx: '" + file_path + "' ...check!")
        outputlock.release()
    else:
        outputlock.acquire()
        stderr("[!] doxx: There was an error pulling '" + file_path + "'. Error: Unable to locate local file", exit=0)
        outputlock.release()

def _pull_github_repo(file_path, url):
    # create OS dependent file path (if necessary)
    file_path = _make_os_dependent_path(file_path)
    # make directory structure if necessary for the file path
    if os.path.dirname(file_path) is not "":
        _create_pull_dirs(file_path)
    # pull the file and write to local filesystem    
    try:
        pull_binary_file(url, file_path)
    except Exception as e:
        stderr("[!] doxx: Unable to pull the archive file from the URL '" + url + "'. Error: " + str(e), exit=0)
    if file_exists(file_path):
        root_dir = unpack_run(file_path)
        remove(file_path)
        stdout("[+] doxx: '" + root_dir + "' ...check!")
    else:
        stderr("[!] doxx: There was an error pulling the repository file. Error: Unable to locate local archive file.", exit=1)

def _pull_github_repo_multiprocess(file_path, url, outputlock, iolock):
    # create OS dependent file path (if necessary)
    file_path = _make_os_dependent_path(file_path)
    # make directory structure if necessary for the file path
    if os.path.dirname(file_path) is not "":
        iolock.acquire()
        _create_pull_dirs(file_path)
        iolock.release()
    # pull the file and write to local filesystem    
    try:
        pull_binary_file(url, file_path)
    except Exception as e:
        outputlock.acquire()
        stderr("[!] doxx: Unable to pull the archive file from the URL '" + url + "'. Error: " + str(e), exit=0)
        outputlock.release()
    if file_exists(file_path):
        root_dir = unpack_run(file_path)
        remove(file_path)
        outputlock.acquire()
        stdout("[+] doxx: '" + root_dir + "' ...check!")
        outputlock.release()
    else:
        outputlock.acquire()
        stderr("[!] doxx: There was an error pulling the repository file. Error: Unable to locate local archive file.", exit=1)
        outputlock.release()

def _make_os_dependent_path(file_path):
    """Makes an OS dependent file path from a POSIX file path"""
    if "/" in file_path:
        path_list = file_path.split("/")
        os_file_path = os.path.join(*path_list)  # use splat operator to unpack list to tuple of path names
        return os_file_path                      # return the OS dependent path if there are path separators
    else:
        return file_path                         # else simply return file or dir name if there are no path separators

def _create_pull_dirs(file_path):
    """Creates a recursive directory path to the requested file name if it does not exist. [file_path] must have correct OS path separators as they are not checked in this function"""
    dir_path = os.path.dirname(file_path)
    if dir_exists(dir_path):
        pass
    else:
        makedirs(dir_path)


# class GithubRepository(object):
    # def __init__(self):
        # self.user = ""
        # self.repo = ""
        # self.branch = ""
        # self.is_partial_repo = False
        # self.keep_filepaths_map = {}
        # self.keep_dirpaths_map = {}
        # self.url_pull_archive_template = "https://github.com/{{user}}/{{repository}}/archive/{{branch}}.tar.gz"
        # self.url_pull_file_template = "https://raw.githubusercontent.com/{{user}}/{{repo}}/{{branch}}/"  # add repo path to this url
        # self.url_pull = ""  # set in set_properties_with_shortcode method
        
    # def set_properties_with_shortcode(self, shortcode, local_keep_path):
        # # Syntax = user/repo:branch+keep-file_or_dir
        # user_repo_branch_block = ""
        # user_repo_block = ""
        
        # # parse cherry picked file/dir data
        # if '+' in shortcode:
            # self.is_partial_repo = True
            # shortcode_pluschar_split_parts = shortcode.split('+')         # split on the + char
            # user_repo_branch_block = shortcode_pluschar_split_parts[0]    # first part is the user/repo:branch block
            # remote_repo_keep_path = shortcode_pluschar_split_parts[1]     # second part is the path to cherry pick file or dir in the remote repo
            # self.keep_paths_map[remote_repo_keep_path] = local_keep_path  # map ==>  remote_keep_path : local_keep_path
        # else:
            # user_repo_branch_block = shortcode                            # no cherry pick shortcode, just assign the shortcode to the string block
            
        # # parse branch data
        # if ':' in user_repo_branch_block:
            # user_repo_block_parts = user_repo_branch_block.split(":")
            # self.branch = user_repo_block_parts[1]
            # user_repo_block = user_repo_block_parts[0]
        # else:
            # self.branch = "master"
            # user_repo_block = user_repo_branch_block
        
        # # parse user and repo data
        # user_repo_parts = user_repo_block.split('/')
        # self.user = user_repo_parts[0]
        # self.repo = user_repo_parts[1]
        
        # # define the pull URL for this repository
        # self.url_pull = self.url_pull_archive_template.replace("{{user}}", self.user)
        # self.url_pull = self.url_pull.replace("{{repository}}", self.repo)
        # self.url_pull = self.url_pull.replace("{{branch}}", self.branch)
    
    # def get_pull_url(self):
        # return self.url_pull
    
    # def is_partial_repo(self):
        # return self.is_partial_repo


# class GithubRepoPuller(object):
    # def __init__(self):
        # pass
    
    # def pull_from_key_shortcode_dictionary(self, github_dictionary_from_key):
        # # dictionary mapping is "local file or dir path" : "repository file or dir path"
        # local_path_list = github_dictionary_from_key.keys()  # create list of local paths from dictionary keys
        
        # github_repo_collection = []
        # github_fullrepo_collection = []
        # github_partialrepo_collection = []
        
        # # create the Github repository objects for every path in the key file
        # for local_file in local_path_list:
            # gh_repo = GithubRepository()
            # gh_repo.set_properties_with_shortcode(github_dictionary_from_key[local_file], local_file)
            # github_repo_collection.append(gh_repo)

        # # iterate through repositories and create collections by repository user/repo/branch
        # for repo in github_repo_collection:
            # if repo.is_partial_repo == False:
                # github_fullrepo_collection.append(repo)
            # else:
                # if len(github_partialrepo_collection) > 0:
                    # match_found = False
                    # for test_repo in github_partialrepo_collection:
                        # if self.is_same_repo(test_repo, repo):
                            # test_repo.keep_paths_map.update(repo.keep_paths_map)  # maintain dictionary with updated paths for a repository
                            # match_found = True
                    # if match_found is False:
                        # github_partialrepo_collection.append(repo)
                # else:
                    # github_partialrepo_collection.append(repo)
               
        # # TESTING     
        # # Full Repo Pulls
        # if len(github_fullrepo_collection) > 0:
            # for repo in github_fullrepo_collection:
                # gh_repo_url = repo.get_pull_url()
                # targz_filename = repo.repo + "-" + repo.branch + ".tar.gz"  # the name of the pulled archive file
                # stdout("[*] doxx: Pulling '" + repo.branch + "' branch of '" + repo.user + "/" + repo.repo + "'")
                
                # # pull the github repo as a tar.gz archive
                # try:
                    # pull_binary_file(gh_repo_url, targz_filename)
                # except Exception as e:
                    # stderr("[!] doxx: Unable to pull the Github repository.  Error: " + str(e), exit=1)
                    
                # # unpack the archive
                # if file_exists(targz_filename):
                    # root_dir = unpack_run(targz_filename)
                    # remove(targz_filename)
                    # stdout("[+] doxx: Unpacked to '" + root_dir + "'")
                
        # # Cherry picked files and/or directory pulls
        # for repo in github_partialrepo_collection:
            # print(repo.keep_paths_map)
            # print(repo.get_pull_url())
    
    # def is_same_repo(self, first_repo, second_repo):
        # if first_repo.user == second_repo.user and first_repo.repo == second_repo.repo and first_repo.branch == second_repo.branch:
            # return True
        # else:
            # return False        