#!/usr/bin/env python
# encoding: utf-8

import os
from Naked.toolshed.file import FileWriter
from Naked.toolshed.system import stdout, stderr, file_exists, dir_exists

###############
# KEY.YAML STUB - changes to this stub require changes to the datatypes.key._parse_yaml_for_errors method
###############

key_stub = """
---

# enter a template path (template), multiple template paths (templates), OR a project archive
# path (projects) relative to this key file, then remove or comment out the other fields with # character:

template: ***.doxt
templates: [***.doxt, 'http://***/***.doxt']
project: ***.tar.gz

---

# Enter the key to your template in YAML syntax below:
"""

#### END KEY STUB


###################
# PROJECT.YAML STUB - changes to this stub require changes to the datatypes.key._parse_yaml_for_errors method
###################

project_yaml_stub = """
---

# enter a template path (template) or multiple template paths (templates)
# then remove or comment out the other field with # character:

template: ***.doxt
templates: [***.doxt, 'http://***/***.doxt']

---
"""

##################
# TEMPLATE STUB
##################

template_stub = """
---doxx---

# (REQUIRED) enter the file extension for files generated from this template or leave blank for no extension
#  the use of a '.' in the extension definition is optional (e.g. you can use '.txt' or 'txt')
extension:

# (OPTIONAL) enter a base file name for files generated from this template:
#  default: absent or undefined = use the template base file name for the generated file
basename:

# (OPTIONAL) enter a directory path relative to this file for files generated from this template:
#  default : absent or undefined = write to current working directory where your build command was executed
destination-directory:

# (OPTIONAL): change to 'true' for templates that contain text that should write to disk verbatim (i.e. no replacements)
#  default: false or absent = attempt text replacements in this template file
verbatim: false

---doxx---

"""

### END TEMPLATE STUB


class Maker(object):
    """doxx key, template, and project stub generator class"""
    def __init__(self):
        pass
    
    def make_key(self, outpath):
        try:
            fw = FileWriter(outpath)
            fw.write(key_stub)
            if file_exists(outpath):
                stdout("[+] doxx: The key stub '" + outpath + "' is available in the current directory.")
        except Exception as e:
            stderr("[!] doxx: Unable to write the key stub to disk.  Error: " + str(e), exit=1)
        
    def make_template(self, outpath):
        try:
            fw = FileWriter(outpath)
            fw.write(template_stub)
            if file_exists(outpath):
                stdout("[+] doxx: The template stub '" + outpath + "' is available in the current directory.")
        except Exception as e:
            stderr("[!] doxx: Unable to write the template stub to disk. Error: " + str(e), exit=1)
            
    def make_project(self):
        try:
            # project.yaml file write
            fw_projyaml = FileWriter('project.yaml')
            fw_projyaml.write(project_yaml_stub)
            
            # pkey.yaml file write
            fw_pkey = FileWriter('pkey.yaml')
            fw_pkey.write(key_stub)
            
            # templates directory write
            if not dir_exists('templates'):
                os.mkdir('templates')
                
            # template.doxt file in templates directory
            fw_template = FileWriter('templates/stub.doxt')
            fw_template.write(template_stub)
            
            # confirm for user
            if file_exists('project.yaml'):
                stdout("[+] doxx: 'project.yaml' ... check")
            else:
                stderr("[!] doxx: There was an error writing the 'project.yaml' key file to your project directory")
                
            if file_exists('pkey.yaml'):
                stdout("[+] doxx: 'pkey.yaml' ... check")
            else:
                stderr("[!] doxx: There was an error writing the 'pkey.yaml' key file to your project directory")
                
            if file_exists('templates/stub.doxt'):
                stdout("[+] doxx: 'templates/stub.doxt' ... check")
            else:
                stderr("[!] doxx: There was an error writing the 'templates/stub.doxt' template file to your project directory")
                
            
        except Exception as e:
            stderr("[!] doxx: Unable to write project files to disk.  Error: " + str(e), exit=1)
            
            
    

    
    
