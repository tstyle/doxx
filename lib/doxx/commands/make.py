#!/usr/bin/env python
# encoding: utf-8

from Naked.toolshed.file import FileWriter

# the generic key template
key_template = """
---

outfile_extension:

---

# Enter the key to your template in YAML syntax below:
"""

class Maker(object):
    def __init__(self):
        pass
    
    def make_key(self, outpath):
        fw = FileWriter(outpath)
        fw.write(key_template)
        

    
    
