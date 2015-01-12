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
    
    def run(self):
        the_yaml = self._read_text("doxx.yaml")
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
                pass

            i += 1

        if self.meta_data == None or self.key_data == None:
            print('error')  # handle incorrect key files

        print(self.meta_data)
        print(self.key_data)



    # PRIVATE METHODS

    def _read_text(self, inpath):
        fr = FileReader(inpath)
        return fr.read()

    def _parse_yaml_for_errors(self):
        pass    