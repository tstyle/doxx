#!/usr/bin/env python
# encoding: utf-8

class GithubRepository(object):
    def __init__(self):
        self.user = ""
        self.repo = ""
        self.branch = ""
        self.is_partial_repo = False
        self.keep_paths_map = {}
        self.url_pull_template = "https://github.com/{{user}}/{{repository}}/archive/{{branch}}.tar.gz"
        self.url_pull = ""  # set in set_properties_with_shortcode method
        
    def set_properties_with_shortcode(self, shortcode, local_keep_path):
        # Syntax = user/repo:branch+keep-file_or_dir
        user_repo_branch_block = ""
        user_repo_block = ""
        
        # parse cherry picked file/dir data
        if '+' in shortcode:
            self.is_partial_repo = True
            shortcode_pluschar_split_parts = shortcode.split('+')         # split on the + char
            user_repo_branch_block = shortcode_pluschar_split_parts[0]    # first part is the user/repo:branch block
            remote_repo_keep_path = shortcode_pluschar_split_parts[1]     # second part is the path to cherry pick file or dir in the remote repo
            self.keep_paths_map[remote_repo_keep_path] = local_keep_path  # map ==>  remote_keep_path : local_keep_path
        else:
            user_repo_branch_block = shortcode                            # no cherry pick shortcode, just assign the shortcode to the string block
            
        # parse branch data
        if ':' in user_repo_branch_block:
            user_repo_block_parts = user_repo_branch_block.split(":")
            self.branch = user_repo_block_parts[1]
            user_repo_block = user_repo_block_parts[0]
        else:
            self.branch = "master"
            user_repo_block = user_repo_branch_block
        
        # parse user and repo data
        user_repo_parts = user_repo_block.split('/')
        self.user = user_repo_parts[0]
        self.repo = user_repo_parts[1]
        
        # define the pull URL for this repository
        self.url_pull = self.url_pull_template.replace("{{user}}", self.user)
        self.url_pull = self.url_pull.replace("{{repository}}", self.repo)
        self.url_pull = self.url_pull.replace("{{branch}}", self.branch)
            
            
    def add_another_keeppath_with_shortcode(self, shortcode):
        pass
    
    def get_pull_url(self):
        pass
    
    def is_partial_repo(self):
        return self.is_partial_repo




class GithubRepoPuller(object):
    def __init__(self):
        pass
    
    def pull_from_key_shortcode_dictionary(self, github_dictionary_from_key):
        # dictionary mapping is "local file or dir path" : "repository file or dir path"
        local_path_list = github_dictionary_from_key.keys()  # create list of local paths from dictionary keys
        
        github_repo_collection = []
        github_fullrepo_collection = []
        github_partialrepo_collection = []
        
        # create the Github repository objects for every path in the key file
        for local_file in local_path_list:
            gh_repo = GithubRepository()
            gh_repo.set_properties_with_shortcode(github_dictionary_from_key[local_file], local_file)
            github_repo_collection.append(gh_repo)

        # iterate through repositories and create collections by repository user/repo/branch
        for repo in github_repo_collection:
            if repo.is_partial_repo == False:
                github_fullrepo_collection.append(repo)
            else:
                if len(github_partialrepo_collection) > 0:
                    match_found = False
                    for test_repo in github_partialrepo_collection:
                        if self.is_same_repo(test_repo, repo):
                            test_repo.keep_paths_map.update(repo.keep_paths_map)  # maintain dictionary with updated paths for a repository
                            match_found = True
                    if match_found is False:
                        github_partialrepo_collection.append(repo)
                else:
                    github_partialrepo_collection.append(repo)
               
        # TESTING     
        for repo in github_partialrepo_collection:
            print(repo.keep_paths_map)
    
    def is_same_repo(self, first_repo, second_repo):
        if first_repo.user == second_repo.user and first_repo.repo == second_repo.repo and first_repo.branch == second_repo.branch:
            return True
        else:
            return False        