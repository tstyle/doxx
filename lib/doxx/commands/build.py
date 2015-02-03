#!/usr/bin/env python
# encoding: utf-8

import sys
from os.path import dirname
from multiprocessing import Process, Lock
from doxx.datatypes.template import DoxxTemplate, RemoteDoxxTemplate
from Naked.toolshed.file import FileWriter
from Naked.toolshed.system import dir_exists, file_exists, make_dirs, stderr, stdout
from Naked.toolshed.python import is_py2

# need a different template for Python 2 & 3
if is_py2():    
    from doxx.renderer.inkpy2 import Template as InkTemplate
    from doxx.renderer.inkpy2 import Renderer as InkRenderer
else:
    from doxx.renderer.inkpy3 import Template as InkTemplate
    from doxx.renderer.inkpy3 import Renderer as InkRenderer

def multi_process_build(key):
    processes = []       # list of spawned processes
    iolock = Lock()      # file read / write lock
    outputlock = Lock()  # stdout / stderr writes lock
    
    
    # ## SINGLE PROCESS
    # for template in key.meta_data['templates']:
        # b = Builder()
        # b.set_key_data(key)
        # b.single_template_run(template)
    
    ## MULTI-PROCESS    
    # create worker processes
    for template in key.meta_data['templates']:
        p = Process(target=single_process_runner, args=(template, key, iolock, outputlock))
        p.start()
        processes.append(p)
    # join worker processes upon completion or with 60 second timeout
    for process in processes:
        process.join(timeout=60)
    
    # ## zombie process finder for testing
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
    
    def run(self, key):
        # detect single vs multiple keys in the template and execute replacements with every requested template
        self.set_key_data(key)  # assign key data from the doxx Key
        
        try:
            if key.multi_template_key == True:
                multi_process_build(key)
            else:
                self.single_template_run(key.meta_data['template']) # process single template file
            # notify user of build completion
            stdout("[*] doxx: Build complete.")   
        except Exception as e:
            stderr("[!] doxx: Error: " + str(e), exit=1)
            
    
    def set_key_data(self, key):
        """used to set the key data in multi process, multi template file renders"""
        self.key_data = key.key_data    
        
    
    def single_template_run(self, template_path):
        """Render replacements using a single template file as defined in a doxx key file (public method)"""
        #----------------------------------------------------------------------------
        # NOTE : changes in this method require the same changes to multi_process_run
        #----------------------------------------------------------------------------       
        ## Load the data
        # remote templates
        if len(template_path) > 6 and (template_path[0:7] == "http://" or template_path[0:8] == "https://"):
            template = RemoteDoxxTemplate(template_path)
            try:
                result = template.load_data()
                if result[0] == False:  # if the method responds False, then HTTP data load did not work
                    stderr(result[1], exit=1)  # write out the returned error message in result[1] position of the tuple
                    # halt execution if unsuccessful
            except Exception as e:
                stderr("[!] doxx: Unable to load the remote template file '" + template_path + "'. Error message: " + str(e), exit=1)
        # local templates        
        elif file_exists(template_path):
            template = DoxxTemplate(template_path)
            try:
                template.load_data()
            except Exception as e:
                stderr("[!] doxx: Unable to read the local template file '" + template_path + "'. Error message: " + str(e), exit=1)
        else:
            stderr("[!] doxx: Unable to find the requested template file " + template_path, exit=1)  # print error message and halt execution of application
         
        ## Split the data  
        try:
            template.split_data()
        except Exception as e:
            stderr("[!] doxx: Unable to parse the template data.  Please verify the template syntax and try again.  Error message: " + str(e), exit=1)
        
        ## Parse data for errors
        error_parse_result = template.parse_template_for_errors()
        
        if error_parse_result[0] == True:          # if there was a parsing error
            stderr(error_parse_result[1], exit=1)  # print the returned error message to stderr and exit application
        
        ## Then parse the template text and load instance attributes for the text replacement with Ink below
        try:
            template.parse_template_text()
        except Exception as e:
            stderr("[!] doxx: An error occurred while parsing your template file. Error message: " + str(e), exit=1)
    
        # determine whether this is a verbatim text file (no replacements) or if requires text replacements
        if template.verbatim == True:
            # write template.text out verbatim
            try:
                fw = FileWriter(template.outfile)
                fw.write(template.text)
                stdout("[+] doxx: '" + template.outfile + "' build... check")
            except Exception as e:
                stderr("[!] doxx: There was a file write error. Error message: " + str(e), exit=1)        
        else:
            # template meta data is in template.meta_data
            # template text is in template.text
            # perform the text replacements:         
            try:
                ink_template = InkTemplate(template.text)
                ink_renderer = InkRenderer(ink_template, self.key_data)
                rendered_text = ink_renderer.render()
            except Exception as e:
                stderr("[!] doxx: An error occurred during the text replacement attempt.  Error message: " + str(e), exit=1)
        
            # if the requested destination directory path does not exist, make it
            if dirname(template.outfile) == "":
                pass  # do nothing, it is the current working directory
            elif not dir_exists(dirname(template.outfile)):
                make_dirs(dirname(template.outfile))
    
            # write rendered file to disk
            try:
                fw = FileWriter(template.outfile)
                fw.write(rendered_text)
                stdout("[+] doxx: -- " + template.outfile + " ... check")
            except Exception as e:
                stderr("[!] doxx: There was an error with the rendered file write. Error message: " + str(e), exit=1)
            
    def multi_process_run(self, template_path, iolock, outputlock):
        """Render replacements over multiple template files as defined in doxx key file using multiple processes (public method)"""
        #-------------------------------------------------------------------------------
        # NOTE : changes in this method require the same changes to single_template_run
        #-------------------------------------------------------------------------------
        ## Load the data
        if len(template_path) > 6 and (template_path[0:7] == "http://" or template_path[0:8] == "https://"):
            template = RemoteDoxxTemplate(template_path)
            try:
                result = template.load_data()  # load remote template file through HTTP or HTTPS protocol
                if result[0] == False:  # if the method responds False, then HTTP data load was not successful
                    outputlock.acquire()
                    stderr(result[1], exit=1)  # write out the returned error message in result[1] position of the tuple
                    outputlock.release()
            except Exception as e:
                outputlock.acquire()
                stderr("[!] doxx: Unable to load the remote template file '" + template_path + "'. Error message: " + str(e), exit=1)
                outputlock.release()
        elif file_exists(template_path):
            template = DoxxTemplate(template_path)
            
            iolock.acquire()  # acquire the IO lock for template file read
            try:
                template.load_data()  # load local data
            except Exception as e:
                outputlock.acquire()
                stderr("[!] doxx: Unable to read the local template file '" + template_path + "'. Error message: " + str(e), exit=1)
                outputlock.release()
            iolock.release()  # release the IO lock for template file read
        else:
            outputlock.acquire()  # acquire the stderr lock
            stdout("[!] doxx: Unable to find the requested template file " + template_path)  # print error message in standard output, multi-file run so do not end execution of application       
            outputlock.release()  # release the stderr lock

        ## Split the data
        try:
            template.split_data()  # split the data sections
        except Exception as e:
            outputlock.acquire()
            stderr("[!] doxx: Unable to parse the template data.  Please verify the template syntax and try again.  Error message: " + str(e), exit=1)
            outputlock.release()
            
        ## Parse the data for errors
        error_parse_result = template.parse_template_for_errors()
        
        if error_parse_result[0] == True:          # if there was a parsing error
            outputlock.acquire()
            stderr(error_parse_result[1], exit=1)  # print the returned error message to stderr and exit application
            outputlock.release()
    
        ## Parse the template text
        try:
            template.parse_template_text()
        except Exception as e:
            outputlock.acquire()
            stderr("[!] doxx: An error occurred while parsing your template file. Error message: " + str(e), exit=1)
            outputlock.release()
        
        # determine whether this is a verbatim text file (no replacements) or if requires text replacements
        if template.verbatim == True:
            # write template.text out verbatim
            try:
                # if the requested destination directory path does not exist, make it
                iolock.acquire()
                if dirname(template.outfile) == "":
                    pass  # do nothing, it is the current working directory
                elif not dir_exists(dirname(template.outfile)):
                    make_dirs(dirname(template.outfile))
                # then write the file out verbatim
                fw = FileWriter(template.outfile)
                fw.write(template.text)
                iolock.release()
                
                outputlock.acquire()
                stdout("[+] doxx: -- " + template.outfile + " ... check")
                outputlock.release()
            except Exception as e:
                outputlock.acquire()
                stderr("[!] doxx: There was a file write error with '" + template_path + "'. Error message: " + str(e), exit=1)
                outputlock.release()
        else:
            # template meta data is in template.meta_data
            # template text is in template.text
            # perform the text replacements:
            try:
                ink_template = InkTemplate(template.text)
                ink_renderer = InkRenderer(ink_template, self.key_data)
                rendered_text = ink_renderer.render()
            except Exception as e:
                outputlock.acquire()
                stderr("[!] doxx: An error occurred during the text replacement attempt.  Error message: " + str(e), exit=1)            
                outputlock.release()        
        
            iolock.acquire()
            # if the requested destination directory path does not exist, make it
            if dirname(template.outfile) == "":
                pass  # do nothing, it is the current working directory
            elif not dir_exists(dirname(template.outfile)):
                make_dirs(dirname(template.outfile))          
            fw = FileWriter(template.outfile)
            fw.write(rendered_text)
            iolock.release()
            
            outputlock.acquire()
            stdout("[+] doxx: -- " + template.outfile + " ... check")
            outputlock.release()
        

        