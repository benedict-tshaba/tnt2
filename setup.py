#!/usr/bin/env python

from distutils.core import setup

setup(name='tnt2',
      scripts=['bin/tnt2'],
      version='1.0.3',
      description='A simple note taking program',
      author='Tshaba Phomolo B3n3dict',
      author_email='benedicttshaba@gmail.com',
      url='http://www.benedict.heliohost.org/',
      packages=['lib','tnt'],
      include_package_data = True,
      license = "GPLv3",
     )
