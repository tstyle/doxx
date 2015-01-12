#!/usr/bin/env python
# encoding: utf-8

from Naked.toolshed.file import FileReader, FileWriter
from yaml import load_all
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    
class DoxxKey(object):
    def __init__(self, args):
        pass
    
    