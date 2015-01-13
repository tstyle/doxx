#!/usr/bin/env python
# encoding: utf-8

import sys
from os.path import basename, splitext, dirname
from multiprocessing import Process, Lock, active_children
from Naked.toolshed.file import FileReader, FileWriter
from Naked.toolshed.system import file_exists, make_path, stderr, stdout
from Naked.toolshed.ink import Renderer as InkRenderer
from Naked.toolshed.ink import Template as InkTemplate
from yaml import load_all
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    

def multi_process_build(key):
    processes = []   # list of spawned processes
    iolock = Lock()  # file read / write lock
    outputlock = Lock()  # stdout / stderr writes lock
    
    # create worker processes
    for template in key.meta_data['templates']:
        p = Process(target=single_process_runner, args=(template, key, iolock, outputlock))
        p.start()
        processes.append(p)
    # join worker processes upon completion or with 60 second timeout
    for process in processes:
        process.join(timeout=60)
    
    # zombie process finder for testing
    # active_child_processes = active_children()
    
    # if len(active_child_processes) > 0:
        # print("active children detected")
    # else:
        # print("no active children detected")

def single_process_runner(template_path, key, iolock, outputlock):
    b = Builder()
    b.set_key_data(key)
    b.multi_process_run(template_path, iolock, outputlock)


class Builder(object):
    """The Builder class renders doxx templates from user provided keys"""
    def __init__(self):
        self.key_data = {}
    
    def set_key_data(self, key):
        """used to set the key data in multi process, multi template file renders"""
        self.key_data = key.key_data
    
    def run(self, key):
        # detect single vs multiple keys in the template and execute replacements with every requested template
        # TODO: add multiprocessing capabilities to multi-template processing
        self.key_data = key.key_data  # assign key data from the doxx Key
        if key.multi_template_key == True:
            # for template in key.meta_data['templates']:
                # self.single_template_run(template, key.key_data)
            multi_process_build(key)
        else:
            self.single_template_run(key.meta_data['template']) # process single template file
        
    def single_template_run(self, template_path):
        """Render replacements using a single template file as defined in a doxx Key file (public method)"""
        # NOTE : changes in this method require the same changes to multi_process_run
        if file_exists(template_path):
            template = DoxxTemplate(template_path)
            template.parse_template_text()
            
            # template meta data is in template.meta_data
            # template text is in template.text
            ink_template = InkTemplate(template.text)
            ink_renderer = InkRenderer(ink_template, self.key_data)
            rendered_text = ink_renderer.render()
            
            print(rendered_text)
            print(template.outfile)
        else:
            stderr("Unable to find the requested template file " + template_path, exit=1)  # print error message and halt execution of application
            
    def multi_process_run(self, template_path, iolock, outputlock):
        """Render replacements over multiple template files as defined in doxx Key file using multiple processes (public method)"""
        # NOTE: changes in this method require the same changes in single_template_run
        if file_exists(template_path):
            template = DoxxTemplate(template_path)
            
            # parse the template text with read of the input template file
            iolock.acquire()  # acquire the IO lock for template file read
            template.parse_template_text()
            iolock.release()  # release the IO lock for template file read
    
            # template meta data is in template.meta_data
            # template text is in template.text
            ink_template = InkTemplate(template.text)
            ink_renderer = InkRenderer(ink_template, self.key_data)
            rendered_text = ink_renderer.render()
            
            outputlock.acquire()  # acquire the stdout lock
            print(rendered_text)
            print(template.outfile)
            outputlock.release()  # release the stdout lock
        else:
            outputlock.acquire()  # acquire the stderr lock
            stdout("Unable to find the requested template file " + template_path)  # print error message in standard output, multi-file run so do not end execution of application       
            outputlock.release()  # release the stderr lock

class DoxxTemplate(object):
    """A doxx template class that maintains state of user designed templates during the rendering process"""
    def __init__(self, inpath):
        self.text = ""
        self.meta_data = {}
        self.inpath = inpath
        self.extension = ""     # stored in the format '.txt'
        self.basename = ""      # base filename for the out write file path
        self.outfile = ""
        
    def parse_template_text(self):
        """parses doxx template meta data YAML and main body text and defines instance variables for the DoxxTemplate (public method)"""
        fr = FileReader(self.inpath)
        the_text = fr.read()
        the_yaml = load_all(the_text, Loader=Loader)
        i = 0
        # parse meta data and the text from the template file
        for the_text_block in the_yaml:
            if i == 0:
                self.meta_data = the_text_block
            elif i == 1:
                self.text = the_text_block
            i += 1
        # parse file extension type, base file name, and directory path
        if self.meta_data['extension'] == None:
            stderr("Please enter a file extension type in the template file " + self.inpath, exit=1)
        else:
            the_extension = self.meta_data['extension']
            if the_extension[0] == ".":
                self.extension = the_extension
            else:
                self.extension = "." + the_extension  # add a period if the user did not include it
            
            self.basename = splitext(basename(self.inpath))[0]
            file_name = self.basename + self.extension
            directory_path = dirname(self.inpath)
            # make the outfile path to be used for the rendered file write
            if len(directory_path) > 0:
                self.outfile = make_path(directory_path, file_name)
            else:
                self.outfile = file_name 
        
    
    

