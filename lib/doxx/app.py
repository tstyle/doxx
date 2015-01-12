#!/usr/bin/env python
# encoding: utf-8

#------------------------------------------------------------------------------
# doxx
# Copyright 2015 Christopher Simpkins
# MIT license
#------------------------------------------------------------------------------

# Application start
def main():
    import sys
    from Naked.commandline import Command
    from doxx.commands.build import Builder
    from doxx.commands.make import Maker
    from doxx.datatypes.key import DoxxKey

    #------------------------------------------------------------------------------------------
    # [ Instantiate command line object ]
    #   used for all subsequent conditional logic in the CLI application
    #------------------------------------------------------------------------------------------
    c = Command(sys.argv[0], sys.argv[1:])
    #------------------------------------------------------------------------------------------
    # [ Command Suite Validation ] - early validation of appropriate command syntax
    # Test that user entered at least one argument to the executable, print usage if not
    #------------------------------------------------------------------------------------------
    if not c.command_suite_validates():
        from doxx.settings import usage as doxx_usage
        print(doxx_usage)
        sys.exit(1)
    #------------------------------------------------------------------------------------------
    # [ NAKED FRAMEWORK COMMANDS ]
    # Naked framework provides default help, usage, and version commands for all applications
    #   --> settings for user messages are assigned in the lib/doxx/settings.py file
    #------------------------------------------------------------------------------------------
    if c.help():      # User requested doxx help information
        from doxx.settings import help as doxx_help
        print(doxx_help)
        sys.exit(0)
    elif c.usage():   # User requested doxx usage information
        from doxx.settings import usage as doxx_usage
        print(doxx_usage)
        sys.exit(0)
    elif c.version(): # User requested doxx version information
        from doxx.settings import app_name, major_version, minor_version, patch_version
        version_display_string = app_name + ' ' + major_version + '.' + minor_version + '.' + patch_version
        print(version_display_string)
        sys.exit(0)
    #------------------------------------------------------------------------------------------
    # [ PRIMARY COMMAND LOGIC ]
    #   Enter your command line parsing logic below
    #------------------------------------------------------------------------------------------
    elif c.cmd == "build":
        if c.argc > 1:
            key_path = c.arg1  # todo : add file_exists check on this user argument
        else:
            key_path = "key.yaml"
        doxxkey = DoxxKey(key_path)
        b = Builder()
        b.single_key_run(doxxkey)
    elif c.cmd == "key":
        m = Maker()
        if c.argc > 1:
            m.make_key(c.arg1)
        else:
            m.make_key("key.yaml")
        

    #------------------------------------------------------------------------------------------
    # [ DEFAULT MESSAGE FOR MATCH FAILURE ]
    #  Message to provide to the user when all above conditional logic fails to meet a true condition
    #------------------------------------------------------------------------------------------
    else:
        print("Could not complete the command that you entered.  Please try again.")
        sys.exit(1) #exit

if __name__ == '__main__':
    main()