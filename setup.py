#!/usr/bin/env python

from setuptools import find_packages
from distutils.core import setup

setup(name='miura',
      version='0.1.3',
      description='a Jenkins job management tool',
      long_description=open('README.rst').read(),
      author='Yusuke Tsutsumi',
      author_email='yusuke@yusuketsutsumi.com',
      url='http://toumorokoshi.github.io/miura',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'jenkinsapi>=0.2.18',
          'docopt',
          'pyyaml',
          'jinja2 >= 2.7.2'
      ],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Topic :: System :: Software Distribution',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7'
      ],
      entry_points={
          'console_scripts': [
              'miura = miura:main'
          ]
      },
      tests_require=['mock>=1.0.1', 'nose>=1.3.0', 'httpretty==0.6.5'],
      test_suite='nose.collector'
)
