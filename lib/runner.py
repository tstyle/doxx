#!/usr/bin/env python
# encoding: utf-8

from doxx.datatypes.package import OfficialPackage

test = OfficialPackage().get_package_key_url('license-apache')
print(test)


    