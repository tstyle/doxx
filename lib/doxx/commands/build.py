#!/usr/bin/env python
# encoding: utf-8

import sys
from Naked.toolshed.file import FileReader, FileWriter
from Naked.toolshed.system import file_exists, stderr, stdout
from Naked.toolshed.ink import Renderer as InkRenderer
from Naked.toolshed.ink import Template as InkTemplate
from yaml import load_all
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    
class Builder(object):
    def __init__(self):
        pass
    
    def single_key_run(self, key):
        template_path = key.meta_data['template']  # single template path
        template = DoxxTemplate(template_path)
        template.parse_template_text()
        
        print(key.key_data)
        # template meta data is in template.meta_data
        # template text is in template.text
        ink_template = InkTemplate(template.text)
        ink_renderer = InkRenderer(ink_template, key.key_data)
        rendered_text = ink_renderer.render()
        
        print(rendered_text)
        # print(key.key_data)
    
    def multi_key_run(self, key_list):
        for the_key in key_list:
            self.single_key_run(the_key)



class DoxxTemplate(object):
    def __init__(self, inpath):
        self.text = ""
        self.meta_data = {}
        self.inpath = inpath
        
    def parse_template_text(self):
        if file_exists(self.inpath):
            fr = FileReader(self.inpath)
            the_text = fr.read()
            the_yaml = load_all(the_text, Loader=Loader)
            i = 0
            for the_text_block in the_yaml:
                if i == 0:
                    self.meta_data = the_text_block
                elif i == 1:
                    self.text = the_text_block
                i += 1
        else:
            stderr("Unable to identify the requested template file " + self.inpath, exit=1)
        
    
    

