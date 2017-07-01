#!/usr/bin/env python

from distutils.core import setup

with open('README') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(name='tnt2',
      scripts=['bin/tnt2'],
      version='1.2.6',
      description='A simple note taking program',
      long_description = readme,
      author='Tshaba Phomolo Benedict',
      author_email='benedicttshaba@gmail.com',
      url='https://github.com/benedict-tshaba/tnt2/tree/v126',
      packages=['tnt'],
      license = license,
     )
