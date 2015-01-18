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
    from Naked.toolshed.system import stdout, stderr
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
            key_path = c.arg1
        else:
            key_path = "key.yaml"
        stdout("[*] doxx: Starting your build with the key file '" + key_path + "'...")
        doxxkey = DoxxKey(key_path)
        b = Builder()
        b.run(doxxkey)
    elif c.cmd == "make":
        if c.argc > 1:
            if c.cmd2 == "key":            
                m = Maker()
                if c.argc > 2:
                    m.make_key(c.arg1)
                else:
                    m.make_key("key.yaml")
            elif c.cmd2 == "template":
                m = Maker()
                if c.argc > 2:
                    m.make_template(c.arg1)
                else:
                    m.make_template("stub.doxt")  # default name is 'stub.doxt' for new template if not specified by user
            else:
                stderr("Usage: doxx make [key | template]", exit=1)
        else:
            stderr("[!] doxx: Please include the secondary command 'key' or 'template' with the 'make' command.", exit=1)

    #------------------------------------------------------------------------------------------
    # [ DEFAULT MESSAGE FOR MATCH FAILURE ]
    #  Message to provide to the user when all above conditional logic fails to meet a true condition
    #------------------------------------------------------------------------------------------
    else:
        stderr("[!] doxx: Could not complete the command that you entered.  Please try again.")
        sys.exit(1) #exit

if __name__ == '__main__':
    main()
    
    