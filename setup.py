from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='Mopidy-Rstation',
    version=get_version('mopidy_rstation/__init__.py'),
    url='https://github.com/araczkowski/mopidy-rstation',
    license='Apache License, Version 2.0',
    author='Andrzej Raczkowski',
    author_email='araczkowski@gmail.com',
    description='Mopidy extension, Raspberry Station or Radio Station',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >=1.1.1',
        'Pykka >= 1.1',
        'pylirc2 >= 0.1',
    ],
    entry_points={
        'mopidy.ext': [
            'rstation = mopidy_rstation:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
