#!/usr/bin/env python

import os
import sys
import codecs

from setuptools import setup

import workshopper


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'workshopper',
]

requires = []

with codecs.open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with codecs.open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='workshopper',
    version=workshopper.__version__,
    description=workshopper.__doc__.strip(),
    long_description=readme + '\n\n' + history,
    url='http://pyschool.github.io',
    download_url='https://github.com/pyschool/workshopper',
    author=workshopper.__author__,
    license=workshopper.__licence__,
    packages=packages,
    package_data={'': ['LICENSE', '*.rst']},
    package_dir={'workshopper': 'workshopper'},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Console'
    ),
)
