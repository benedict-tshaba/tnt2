#!/usr/bin/env python

from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(name='tnt2',
      scripts=['bin/tnt2'],
      version='1.2.7',
      description='A simple note taking program with advanced encryption',
      long_description = readme,
      long_description_content_type="text/markdown",
      author='Tshaba Phomolo Benedict',
      author_email='benedicttshaba@gmail.com',
      url='https://github.com/benedict-tshaba/tnt2',
      packages=['tnt'],
      license = license,
     )
