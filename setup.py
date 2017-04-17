#!/usr/bin/env python

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Pygments'
]

test_requirements = [
]

setup(
    name='story',
    version='1.1.2',
    description='Story for pyschool.',
    long_description=readme + '\n\n' + history,
    author='PySchool',
    author_email='pyschool@sophilabs.com',
    url='https://github.com/pyschool/story',
    packages=[
        'story',
    ],
    package_dir={'story': 'story'},
    include_package_data=True,
    install_requires=requirements,
    license='MIT license',
    zip_safe=False,
    keywords='story',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
