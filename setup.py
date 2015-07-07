#!/usr/bin/env python

import codecs

from setuptools import find_packages, setup

import story


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        readme = f.read()
    with codecs.open('HISTORY.rst', encoding='utf8') as f:
        history = f.read()
    return readme + history


setup(
    name='story',
    version=story.__version__,
    description=story.__doc__.strip(),
    long_description=long_description(),
    url='http://pyschool.github.io',
    download_url='https://github.com/pyschool/story',
    author=story.__author__,
    license=story.__licence__,
    packages=find_packages(),
    install_requires=[
        'pygments',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Console'
    ]
)
