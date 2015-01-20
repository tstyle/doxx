#!/usr/bin/env python
# encoding: utf-8

from doxx.datatypes.template import DoxxTemplate, RemoteDoxxTemplate

dt = DoxxTemplate('/Users/ces/Desktop/code/doxx/tests/templates/ascii_template.doxt')
dt.load_data()
dt.split_data()
dt.parse_template_for_errors()
dt.parse_template_text()
print('done')
