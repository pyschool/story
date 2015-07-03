#!/usr/bin/env python

import codecs

from setuptools import setup, find_packages

import workshopper


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        readme = f.read()
    with codecs.open('HISTORY.rst', encoding='utf8') as f:
        history = f.read()
    return readme + history


setup(
    name='workshopper',
    version=workshopper.__version__,
    description=workshopper.__doc__.strip(),
    long_description=long_description(),
    url='http://pyschool.github.io',
    download_url='https://github.com/pyschool/workshopper',
    author=workshopper.__author__,
    license=workshopper.__licence__,
    packages=find_packages(),
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
