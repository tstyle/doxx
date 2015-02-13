#!/usr/bin/env python
# encoding: utf-8

from Naked.toolshed.file import FileReader

class OfficialPackage(object):
    def __init__(self):
        self.binary_package_url_prefix = "https://github.com/doxx-repo/bin/raw/master/"
        self.package_key_file_url_prefix = "https://raw.githubusercontent.com/doxx-repo/"
        self.package_key_file_url_postfix = "/master/pkey.yaml"
        self.master_package_list_text_url = "http://doxx-repo.github.io/master/repository-list/list.txt"
    
    # Getter methods
    
    def get_package_targz_url(self, package_name):
        normalized_package_name = package_name.lower().strip()
        return self.binary_package_url_prefix + normalized_package_name + '.tar.gz'
    
    def get_package_zip_url(self, package_name):
        normalized_package_name = package_name.lower().strip()
        return self.binary_package_url_prefix + normalized_package_name + '.zip'        
    
    def get_package_key_url(self, package_name):
        normalized_package_name = package_name.lower().strip()
        return self.package_key_file_url_prefix + normalized_package_name + self.package_key_file_url_postfix
    
    def get_master_package_list_url(self):
        return self.master_package_list_text_url
    

    
    