#!/usr/bin/env python
# encoding: utf-8

from os.path import basename, splitext
from Naked.toolshed.file import FileReader
from Naked.toolshed.network import HTTP
from Naked.toolshed.system import make_path, stderr

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
    

class DoxxTemplate(object):
    """A doxx template class that maintains state of user designed templates during the rendering process"""
    def __init__(self, inpath):
        self.inpath = inpath
        self.raw_text = ""
        self.text = ""
        self.meta_data = {}     # holds meta data from the header of the file
        self.extension = ""     # stored in the format '.txt'
        self.basename = ""      # base filename for the out write file path
        self.outfile = ""       # write file path for use by calling code
    
    def load_data(self):
        try:
            fr = FileReader(self.inpath)
            self.raw_text = fr.read()
        except IOError as e:
            stderr("[!] doxx: Unable to find the requested template file '" + self.inpath + "'.", exit=1)

    def split_data(self):
        parsed_text = self.raw_text.split("---doxx---")

        if len(parsed_text) == 3:  # should split into three sections (0 = before first ---doxx---, 1 = meta data, 2 = template text data after second ---doxx---)
            self.meta_data = load(parsed_text[1], Loader=Loader)
            self.text = parsed_text[2][1:]  # define self.text with the template data from the file, the [1:] slice removes /n at end of the delimiter        
        else:
            self.meta_data = {}
            self.text = ""
    
    def parse_template_text(self):
        """parses doxx template meta data YAML and main body text and defines instance variables for the DoxxTemplate (public method)"""

        meta_keys = self.meta_data.keys()

        # if user did not enter an extension type, use .doxr as the default
        if not 'extension' in meta_keys or self.meta_data['extension'] == None:
            self.meta_data['extension'] = ".doxr"

        # define rendered file destination directory relative to current working directory
        if not 'destination_directory' in meta_keys or self.meta_data['destination_directory'] == None:
            dest_dir = ""
        else:
            dest_dir = self.meta_data['destination_directory']

        # define rendered file extension
        the_extension = self.meta_data['extension']
        if the_extension[0] == ".":
            self.extension = the_extension
        else:
            self.extension = "." + the_extension  # add a period if the user did not include it

        # define rendered file base file name (different approach for local vs. remote paths)
        if not 'basename' in meta_keys or self.meta_data['basename'] == None:
            # if it is a URL, split by '/' and obtain file path from the URL
            if len(self.inpath) > 6 and (self.inpath[0:7] == "http://" or self.inpath[0:8] == "https://"):
                url_path = self.inpath.split("/")
                filename_with_extension = splitext(url_path[-1])  # get the filename from the '/' split url :: url_path[-1] = URL filename, [0] index is the basename from that filename.extension
                self.basename = filename_with_extension[0]
            else:  # local files
                self.basename = splitext(basename(self.inpath))[0]
        else:
            self.basename = self.meta_data['basename']

        file_name = self.basename + self.extension  # local temp file_name variable, modified below to final write path

        # make the outfile path to be used for the rendered file write
        if len(dest_dir) > 0:
            self.outfile = make_path(dest_dir, file_name)
        else:
            self.outfile = file_name


    def parse_template_for_errors(self):
        # confirm meta data contains data
        if self.meta_data == None or len(self.meta_data) == 0:
            stderr("[!] doxx: The template file '" + self.inpath + "' is not properly formatted.  Please include the required meta data block between '---doxx---' delimiters at the top of your file.", exit=1)
        # confirm that there is template text
        if self.text == None or len(self.text) < 5:  # if self.text not defined or length of the string < 5 chars (because {{x}} == 5 so must not include any replacement tags)
            stderr("[!] doxx: Unable to parse template text from the template file '" + self.inpath + "'. Please include a template in order to render this file.", exit=1)



class RemoteDoxxTemplate(DoxxTemplate):
    def __init__(self, inpath):
        DoxxTemplate.__init__(self, inpath)

    def load_data(self):
        """overloaded load_data method that retrieves data from a remote file using HTTP or HTTPS protocol instead of a local file"""
        http = HTTP(self.inpath)
        
        ## TODO : add try/except block and catch timeout exceptions (does not get returned as non-200 status code)
        if http.get_status_ok():
            import unicodedata
            norm_text = unicodedata.normalize('NFKD', http.res.text)  # normalize unicode data to NFKD (like local file reads)
            self.raw_text = norm_text
        else:
            fail_status_code = http.res.status_code
            stderr("[!] doxx: Unable to pull the requested template file '" + self.inpath + "' (HTTP status code " + str(fail_status_code) + ")", exit=1)
        
        