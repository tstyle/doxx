#!/usr/bin/env python
# encoding: utf-8

from Naked.toolshed.file import FileWriter

#############
# KEY STUB
#############

key_stub = """
---

# enter a template path (template) OR multiple template paths (templates)
# relative to this key file, then remove or comment out the other field:

template: ***.doxt
templates: [***.doxt, ***.doxt]

---

# Enter the key to your template in YAML syntax below:
"""

#### END KEY STUB


##################
# TEMPLATE STUB
##################

template_stub = """
---

# enter the extension for files generated from this template below:

extension:

---

"""

### END TEMPLATE STUB


class Maker(object):
    def __init__(self):
        pass
    
    def make_key(self, outpath):
        fw = FileWriter(outpath)
        fw.write(key_stub)
        
    def make_template(self, outpath):
        fw = FileWriter(outpath)
        fw.write(template_stub)

    
    
