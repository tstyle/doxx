#!/usr/bin/env python
# encoding: utf-8

import sys
from os.path import dirname
from multiprocessing import Process, Lock
from doxx.datatypes.template import DoxxTemplate, RemoteDoxxTemplate
from Naked.toolshed.file import FileWriter
from Naked.toolshed.system import dir_exists, file_exists, make_dirs, stderr, stdout
from Naked.toolshed.ink import Renderer as InkRenderer
from Naked.toolshed.ink import Template as InkTemplate

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
            # notify user of build completion
            stdout("[*] doxx: Build complete.")
            
        except Exception as e:
            stderr("[!] doxx: Error Message: " + str(e), exit=1)
        
    
    def single_template_run(self, template_path):
        """Render replacements using a single template file as defined in a doxx key file (public method)"""
        #----------------------------------------------------------------------------
        # NOTE : changes in this method require the same changes to multi_process_run
        #----------------------------------------------------------------------------
        if len(template_path) > 6 and (template_path[0:7] == "http://" or template_path[0:8] == "https://"):
            template = RemoteDoxxTemplate(template_path)
        elif file_exists(template_path):
            template = DoxxTemplate(template_path)
        else:
            stderr("[!] doxx: Unable to find the requested template file " + template_path, exit=1)  # print error message and halt execution of application
            
        # have kept the following out of the constructor in order to isolate I/O and stdout/stderr writes for multiprocessing runs, need to run each instance method from the calling func/method
        template.load_data()
        template.split_data()
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
    
        ####
        # TESTING
        ####
        print(template.outfile)
        print(" ")
        print(rendered_text)
        sys.exit(0)
        # print(rendered_text)
        # print(template.outfile)
        fw = FileWriter(template.outfile)
        fw.write(rendered_text)        
            
    def multi_process_run(self, template_path, iolock, outputlock):
        """Render replacements over multiple template files as defined in doxx key file using multiple processes (public method)"""
        #-------------------------------------------------------------------------------
        # NOTE : changes in this method require the same changes to single_template_run
        #-------------------------------------------------------------------------------
        if len(template_path) > 6 and (template_path[0:7] == "http://" or template_path[0:8] == "https://"):
            template = RemoteDoxxTemplate(template_path)
            template.load_data()  # load remote data from each file (overloaded method in RemoteDoxxTemplate)
        elif file_exists(template_path):
            template = DoxxTemplate(template_path)
            
            iolock.acquire()  # acquire the IO lock for template file read
            template.load_data()  # load local data
            iolock.release()  # release the IO lock for template file read
        else:
            outputlock.acquire()  # acquire the stderr lock
            stdout("[!] doxx: Unable to find the requested template file " + template_path)  # print error message in standard output, multi-file run so do not end execution of application       
            outputlock.release()  # release the stderr lock

        template.split_data()  # split the data sections
    
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
        


        