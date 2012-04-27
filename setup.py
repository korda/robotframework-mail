from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='RobotMail',
      version=version,
      description="Mail related keywords for robotframework.",
      long_description="""\
Library providing mail related keywords to use with robotframework.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mail robotframework',
      author='Adrian Adamski',
      author_email='maidy.adr@gmail.com',
      url='http://github.com/korda/robotframework-mail',
      license='Apache License, Version 2.0',
      #packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      packages=['robotmail', 'robotmail.keywords'],
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'beautifulsoup4 >= 4.0.4'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
