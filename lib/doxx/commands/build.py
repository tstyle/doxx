#!/usr/bin/env python
# encoding: utf-8

from Naked.toolshed.file import FileReader, FileWriter
from yaml import load_all
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    
class Builder(object):
    def __init__(self):
        pass
    
    def single_key_run(self, key):
        print(key.meta_data)
        print(key.key_data)
    
    def multi_key_run(self, template_key_dict):
        pass



    # PRIVATE METHODS
