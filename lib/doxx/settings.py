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
doxx <option> [command] <argument>

Use 'doxx help' for additional information
"""

#------------------------------------------------------------------------------
# Help String
#------------------------------------------------------------------------------
help = """
----------------------------------------------------------
 doxx
 A simple, flexible text file project build system
 Copyright 2015 Christopher Simpkins
 MIT license
 Source: http://github.com/chrissimpkins/doxx
   Docs: http://doxx.org
----------------------------------------------------------

USAGE
  doxx <option> [command] <argument>
  
GENERAL COMMANDS
  build    render string replacements in template files and build project
  clean    remove doxx project files from a project directory
  make     generate key, template, or project file stubs
  pack     create a tar.gz or zip archive file for project distribution
  pull     pull a key, template, or project archive from a remote repository
  unpack   unpack a tar.gz or zip project archive

PACKAGE REPOSITORY COMMANDS
  pull     pull a project package from the doxx Package Repository
  pullkey  pull the key file from a doxx Package Repository project
  search   search the doxx Package Repository by keyword or project name
  whatis   get descriptions of Package Repository packages by project name

OPTIONS
  -h | --help      view application help
       --usage     view application usage
  -v | --version   view installed application version
"""

