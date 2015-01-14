#!/usr/bin/env python
# encoding: utf-8

from Naked.toolshed.file import FileWriter

#############
# KEY STUB - changes to this stub require changes to the datatypes.key._parse_yaml_for_errors method
#############

key_stub = """
---

# enter a template path (template) OR multiple template paths (templates)
# relative to this key file, then remove or comment out the other field:

template: ***.doxt
templates: [***.doxt, ***.doxt]

destination-directory: build

---

# Enter the key to your template in YAML syntax below:
"""

#### END KEY STUB


##################
# TEMPLATE STUB
##################

template_stub = """
---doxx---

# enter the extension for files generated from this template below:

extension:

---doxx---

"""

### END TEMPLATE STUB


class Maker(object):
    """doxx key and template stub generator class"""
    def __init__(self):
        pass
    
    def make_key(self, outpath):
        fw = FileWriter(outpath)
        fw.write(key_stub)
        
    def make_template(self, outpath):
        fw = FileWriter(outpath)
        fw.write(template_stub)

    
    
