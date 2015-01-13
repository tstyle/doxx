#!/usr/bin/env python
# encoding: utf-8

from Naked.toolshed.file import FileReader
from Naked.toolshed.system import directory, make_path
from Naked.toolshed.system import file_exists, stderr
from yaml import load_all
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    
class DoxxKey(object):
    def __init__(self, inpath):
        # instance variables
        self.meta_data = {}      # holds key meta data
        self.key_data = {}       # holds key data
        self.multi_template_key = False  # changed to True in the _generate_dir_paths method if method detects multiple requested templates
        
        # define methods
        self._read_yaml(inpath)  # define self.meta_data & self.key_data with the yaml key file
        self._cast_values_to_string()  # cast non-string values to strings (necessary for the Ink Renderer class)
        self._generate_dir_path(inpath)      # join the directory path to the template files specified in the key (for keys executed from outside of containing directory)
        
    
    def _read_yaml(self, inpath):
        """local YAML doxx key file reader (private method)"""
        if file_exists(inpath):
            fr = FileReader(inpath)
            the_yaml = fr.read()
            the_data = load_all(the_yaml, Loader=Loader)
            i = 0
            for x in the_data:
                if i == 0:
                    # first section of the YAML is meta data
                    self.meta_data = x
                elif i == 1:
                    # second section of the YAML includes the key data
                    self.key_data = x
                else:
                    pass  # ignore any other sections that are included
        
                i += 1
        else:
            stderr("Unable to load the requested key " + inpath + ". Please check the path and try again.", exit=1)
    
    def _cast_values_to_string(self):
        """cast non-string doxx key values to strings (private method)"""
        key_list = self.key_data.keys()
        for key in key_list:
            if isinstance(self.key_data[key], str):
                pass
            else:
                self.key_data[key] = str(self.key_data[key])
                
                
    def _generate_dir_path(self, inpath):
        """joins the directory path from the current working directory to the template file paths specified in the doxx key meta data (private method)"""
        meta_keys = self.meta_data.keys()
        dir_path = directory(inpath)
        if 'template' in meta_keys:     # single template file request
            pre_file_path = self.meta_data['template']
            self.meta_data['template'] = make_path(dir_path, pre_file_path)
        elif 'templates' in meta_keys:  # multi-template file request
            self.multi_template_key = True  # used to detect whether there is a need to process multiple templates with this key
            i = 0
            for template in self.meta_data['templates']:  # iterate through template files and join the directory path to the specified template path
                pre_file_path = template
                self.meta_data['templates'][i] = make_path(dir_path, pre_file_path)
                i += 1
        else:
            stderr("Unable to read the template file path(s) from your doxx key file.  Did you include one or more template file paths in the meta data section?", exit=1)
    
    def _parse_yaml_for_errors(self):
        pass
        # confirm that there is some key data
        # confirm that the meta data is complete