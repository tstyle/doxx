#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# Application Name
#------------------------------------------------------------------------------
app_name = 'doxx'

#------------------------------------------------------------------------------
# Version Number
#------------------------------------------------------------------------------
major_version = "0"
minor_version = "9"
patch_version = "0"

#------------------------------------------------------------------------------
# Debug Flag (switch to False for production release code)
#------------------------------------------------------------------------------
debug = False

#------------------------------------------------------------------------------
# Usage String
#------------------------------------------------------------------------------
usage = """
doxx [command] <options> <argument>

commands : [build | make]

Use 'doxx --help' for additional information
"""

#------------------------------------------------------------------------------
# Help String
#------------------------------------------------------------------------------
help = """
----------------------------------------------------------
 doxx
 A simple, flexible text file templating system
 Copyright 2015 Christopher Simpkins
 MIT license
 Source: http://github.com/chrissimpkins/doxx
 Docs:   http://chrissimpkins.github.io/doxx
----------------------------------------------------------

doxx is a generic text file templating system that can be used to create reusable templates for projects with any combination of text file mime types and directory structure.

USAGE
  doxx [command] <options> <argument>
  
COMMANDS
  build    render text replacements & write files locally
  make     generate a key or template stub file

BUILD COMMAND USE
  doxx build <argument>
  
Use the build command without an argument if your key file is named `key.yaml` and is located in the working directory.  Use the key file path as an argument if you modify the name or directory path of the key file.

MAKE COMMAND USE
  doxx make [key | template]
  
Use `key` or `template` as a secondary command to generate the respective stub.

OPTIONS
  -h | --help      view application help
       --usage     view application usage
  -v | --version   view installed application version
"""

