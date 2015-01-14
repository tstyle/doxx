#!/usr/bin/env python
# encoding: utf-8

import sys
from os.path import basename, splitext, dirname
from multiprocessing import Process, Lock, active_children
from Naked.toolshed.file import FileReader, FileWriter
from Naked.toolshed.system import file_exists, make_path, stderr, stdout
from Naked.toolshed.ink import Renderer as InkRenderer
from Naked.toolshed.ink import Template as InkTemplate
from yaml import load, load_all
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    

def multi_process_build(key):
    processes = []       # list of spawned processes
    iolock = Lock()      # file read / write lock
    outputlock = Lock()  # stdout / stderr writes lock
    
    # create worker processes
    for template in key.meta_data['templates']:
        p = Process(target=single_process_runner, args=(template, key, iolock, outputlock))
        p.start()
        processes.append(p)
    # join worker processes upon completion or with 60 second timeout
    for process in processes:
        process.join(timeout=60)
    
    ## zombie process finder for testing
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
        self.key_data = key.key_data  # assign key data from the doxx Key
        if key.multi_template_key == True:
            # for template in key.meta_data['templates']:
                # self.single_template_run(template, key.key_data)
            multi_process_build(key)
        else:
            self.single_template_run(key.meta_data['template']) # process single template file
        
    
    def single_template_run(self, template_path):
        """Render replacements using a single template file as defined in a doxx Key file (public method)"""
        #----------------------------------------------------------------------------
        # NOTE : changes in this method require the same changes to multi_process_run
        #----------------------------------------------------------------------------
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
            # fw = FileWriter(template.outfile)
            # fw.write(rendered_text)
        else:
            stderr("Unable to find the requested template file " + template_path, exit=1)  # print error message and halt execution of application
            
    def multi_process_run(self, template_path, iolock, outputlock):
        """Render replacements over multiple template files as defined in doxx Key file using multiple processes (public method)"""
        #-------------------------------------------------------------------------------
        # NOTE : changes in this method require the same changes to single_template_run
        #-------------------------------------------------------------------------------
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
        self.inpath = inpath
        self.extension = ""     # stored in the format '.txt'
        self.basename = ""      # base filename for the out write file path
        self.outfile = ""
        
        fr = FileReader(inpath)
        self.raw_text = fr.read()
        
        parsed_text = self.raw_text.split("---doxx---")
        
        # TODO: add try/catch block around the following:
        
        self.meta_data = load(parsed_text[1], Loader=Loader)
        self.text = parsed_text[2][1:]  # define self.text with the template data from the file, the [1:] slice removes /n at end of the delimiter        
        
    def parse_template_text(self):
        """parses doxx template meta data YAML and main body text and defines instance variables for the DoxxTemplate (public method)"""
        
        meta_keys = self.meta_data.keys()
        
        # if user did not enter an extension type, use .doxr as the default
        if not 'extension' in meta_keys or self.meta_data['extension'] == None:
            self.meta_data['extension'] = ".doxr"
        
        # the user specified destination directory for the rendered file
        if not 'destination_directory' in meta_keys or self.meta_data['destination_directory'] == None:
            dest_dir = ""
        else:
            dest_dir = self.meta_data['destination_directory']
        
        # the user specified file extension for the rendered file
        the_extension = self.meta_data['extension']
        if the_extension[0] == ".":
            self.extension = the_extension
        else:
            self.extension = "." + the_extension  # add a period if the user did not include it
        
        self.basename = splitext(basename(self.inpath))[0]
        file_name = self.basename + self.extension
        
        if len(dest_dir) > 0:  # confirm that a destination directory was specified
            directory_path = make_path(dirname(self.inpath), dest_dir)  # make path that includes user specified destination directory if present
        else:
            directory_path = dirname(self.inpath)  # otherwise just use the directory path to the template file
        
        # make the outfile path to be used for the rendered file write
        if len(directory_path) > 0:
            self.outfile = make_path(directory_path, file_name)
        else:
            self.outfile = file_name 
        
    
    def parse_template_for_errors(self):
        # confirm meta data contains data
        if len(self.meta_data) == 0:
            return (True, "The template file " + self.inpath + " does not include meta data.  Please include the required meta data in order to process this file.")
        
        # confirm that there is template text
        if len(self.text) == 0:
            return (True, "There is no template text in the template file " + self.inpath)

    
    def parse_template_for_errors_multiprocess(self, outputlock):
        pass
