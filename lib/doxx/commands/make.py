#!/usr/bin/env python
# encoding: utf-8

from Naked.toolshed.file import FileWriter
from Naked.toolshed.system import stderr

#############
# KEY STUB - changes to this stub require changes to the datatypes.key._parse_yaml_for_errors method
#############

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
    """doxx key and template stub generator class"""
    def __init__(self):
        pass
    
    def make_key(self, outpath):
        try:
            fw = FileWriter(outpath)
            fw.write(key_stub)
        except Exception as e:
            stderr("[!] doxx: Unable to write the key stub to disk.  Error: " + str(e), exit=1)
        
    def make_template(self, outpath):
        try:
            fw = FileWriter(outpath)
            fw.write(template_stub)
        except Exception as e:
            stderr("[!] doxx: Unable to write the template stub to disk. Error: " + str(e), exit=1)

    
    
