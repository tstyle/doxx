#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from os.path import basename, splitext, dirname
from multiprocessing import Process, Lock, active_children
from Naked.toolshed.file import FileReader, FileWriter
from Naked.toolshed.system import dir_exists, file_exists, make_dirs, make_path, stderr, stdout
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
        
        try:
            if key.multi_template_key == True:
                multi_process_build(key)
            else:
                self.single_template_run(key.meta_data['template']) # process single template file
        except Exception as e:
            stderr("Error: Unable to run the build command. ", exit=0)
            stderr("Error Message: " + str(e), exit=1)
        
    
    def single_template_run(self, template_path):
        """Render replacements using a single template file as defined in a doxx key file (public method)"""
        #----------------------------------------------------------------------------
        # NOTE : changes in this method require the same changes to multi_process_run
        #----------------------------------------------------------------------------
        if file_exists(template_path):
            template = DoxxTemplate(template_path)
            template.parse_template_for_errors()
            template.parse_template_text()
            
            # template meta data is in template.meta_data
            # template text is in template.text
            ink_template = InkTemplate(template.text)
            ink_renderer = InkRenderer(ink_template, self.key_data)
            rendered_text = ink_renderer.render()
            
            # if the requested destination directory path does not exist, make it
            if not dir_exists(dirname(template.outfile)):
                make_dirs(dirname(template.outfile))
            
            
            # print(rendered_text)
            # print(template.outfile)
            fw = FileWriter(template.outfile)
            fw.write(rendered_text)
        else:
            stderr("Unable to find the requested template file " + template_path, exit=1)  # print error message and halt execution of application
            
    def multi_process_run(self, template_path, iolock, outputlock):
        """Render replacements over multiple template files as defined in doxx key file using multiple processes (public method)"""
        #-------------------------------------------------------------------------------
        # NOTE : changes in this method require the same changes to single_template_run
        #-------------------------------------------------------------------------------
        if file_exists(template_path):
            iolock.acquire()  # acquire the IO lock for template file read
            template = DoxxTemplate(template_path)
            iolock.release()  # release the IO lock for template file read
            
            outputlock.acquire()  # acquire stderr lock
            template.parse_template_for_errors()
            outputlock.release()  # release stderr lock
            
            # parse the template text
            template.parse_template_text()
            
    
            # template meta data is in template.meta_data
            # template text is in template.text
            ink_template = InkTemplate(template.text)
            ink_renderer = InkRenderer(ink_template, self.key_data)
            rendered_text = ink_renderer.render()            
            
            iolock.acquire()
            # if the requested destination directory path does not exist, make it
            if not dir_exists(dirname(template.outfile)):
                make_dirs(dirname(template.outfile))            
            fw = FileWriter(template.outfile)
            fw.write(rendered_text)
            iolock.release()
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
        self.outfile = ""       # write file path for use by calling code
        
        fr = FileReader(inpath)
        self.raw_text = fr.read()
        
        parsed_text = self.raw_text.split("---doxx---")
        
        if len(parsed_text) == 3:  # should split into three sections (0 = before first ---doxx---, 1 = meta data, 2 = template text data after second ---doxx---)
            self.meta_data = load(parsed_text[1], Loader=Loader)
            self.text = parsed_text[2][1:]  # define self.text with the template data from the file, the [1:] slice removes /n at end of the delimiter        
        else:
            self.meta_data = {}
            self.text = ""
        
    def parse_template_text(self):
        """parses doxx template meta data YAML and main body text and defines instance variables for the DoxxTemplate (public method)"""
        
        meta_keys = self.meta_data.keys()
        
        # if user did not enter an extension type, use .doxr as the default
        if not 'extension' in meta_keys or self.meta_data['extension'] == None:
            self.meta_data['extension'] = ".doxr"
        
        # define rendered file destination directory relative to current working directory
        if not 'destination_directory' in meta_keys or self.meta_data['destination_directory'] == None:
            dest_dir = ""
        else:
            dest_dir = self.meta_data['destination_directory']
            
        # define rendered file extension
        the_extension = self.meta_data['extension']
        if the_extension[0] == ".":
            self.extension = the_extension
        else:
            self.extension = "." + the_extension  # add a period if the user did not include it
            
        # define rendered file base file name
        if not 'basename' in meta_keys or self.meta_data['basename'] == None:
            self.basename = splitext(basename(self.inpath))[0]
        else:
            self.basename = self.meta_data['basename']
        
        file_name = self.basename + self.extension  # local temp file_name variable, modified below to final write path
        
        # make the outfile path to be used for the rendered file write
        if len(dest_dir) > 0:
            self.outfile = make_path(dest_dir, file_name)
        else:
            self.outfile = file_name
            
        print(self.outfile)
        sys.exit(0)
        
    
    def parse_template_for_errors(self):
        # confirm meta data contains data
        if self.meta_data == None or len(self.meta_data) == 0:
            stderr("The template file '" + self.inpath + "' is not properly formatted.  Please include the required meta data block between '---doxx---' delimiters at the top of your file.", exit=1)
        # confirm that there is template text
        if self.text == None or len(self.text) < 5:  # if self.text not defined or length of the string < 5 chars (because {{x}} == 5 so must not include any replacement tags)
            stderr("Unable to parse template text from the template file '" + self.inpath + "'. Please include a template in order to render this file.", exit=1)
                
        