#!/usr/bin/env python
# encoding: utf-8

from Naked.toolshed.file import FileReader
from Naked.toolshed.system import file_exists, stderr
from yaml import load_all
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    
class DoxxKey(object):
    def __init__(self, inpath):
        self.meta_data = {}      # holds key meta data
        self.key_data = {}       # holds key data
        self._read_yaml(inpath)  # define self.meta_data & self.key_data with the yaml key file
        self._cast_values_to_string()  # cast non-string values to strings (necessary for the Ink Renderer class)
    # PRIVATE METHODS
    
    def _read_yaml(self, inpath):
        """local YAML key file reader (private method)"""
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
        """cast non-string key values to strings (private method)"""
        key_list = self.key_data.keys()
        for key in key_list:
            if isinstance(self.key_data[key], str):
                pass
            else:
                self.key_data[key] = str(self.key_data[key])
    
    def _parse_yaml_for_errors(self):
        pass