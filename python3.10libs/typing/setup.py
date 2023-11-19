#!/usr/bin/env python
# coding: utf-8

import sys
from setuptools import setup

if sys.version_info < (2, 7, 0) or (3, 0, 0) <= sys.version_info < (3, 4, 0):
    sys.stderr.write('ERROR: You need Python 2.7 or 3.4+ '
                     'to install the typing package.\n')
    exit(1)

version = '3.7.4.3'
description = 'Type Hints for Python'
long_description = '''\
Typing -- Type Hints for Python

This is a backport of the standard library typing module to Python
versions older than 3.5.  (See note below for newer versions.)

Typing defines a standard notation for Python function and variable
type annotations. The notation can be used for documenting code in a
concise, standard format, and it has been designed to also be used by
static and runtime type checkers, static analyzers, IDEs and other
tools.

NOTE: in Python 3.5 and later, the typing module lives in the stdlib,
and installing this package has NO EFFECT, because stdlib takes higher
precedence than the installation directory. To get a newer version of
the typing module in Python 3.5 or later, you have to upgrade to a
newer Python (bugfix) version.  For example, typing in Python 3.6.0 is
missing the definition of 'Type' -- upgrading to 3.6.2 will fix this.

Also note that most improvements to the typing module in Python 3.7
will not be included in this package, since Python 3.7 has some
built-in support that is not present in older versions (See PEP 560.)

For package maintainers, it is preferred to use
``typing;python_version<"3.5"`` if your package requires it to support
earlier Python versions. This will avoid shadowing the stdlib typing
module when your package is installed via ``pip install -t .`` on
Python 3.5 or later.
'''

package_dir = {2: 'python2', 3: 'src'}[sys.version_info.major]

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Python Software Foundation License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Topic :: Software Development',
]

setup(name='typing',
      version=version,
      description=description,
      long_description=long_description,
      author='Guido van Rossum, Jukka Lehtosalo, Łukasz Langa, Ivan Levkivskyi',
      author_email='jukka.lehtosalo@iki.fi',
      url='https://docs.python.org/3/library/typing.html',
      project_urls={'Source': 'https://github.com/python/typing'},
      license='PSF',
      keywords='typing function annotations type hints hinting checking '
               'checker typehints typehinting typechecking backport',
      package_dir={'': package_dir},
      py_modules=['typing'],
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
      classifiers=classifiers)
