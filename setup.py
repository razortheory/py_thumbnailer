#!/usr/bin/env python

import os

from setuptools import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='py_thumbnailer',
    version='0.1',
    description='Documents Thumbnailer library',
    long_description=read('README.rst'),

    author='Roman Karpovich',
    author_email='fpm.th13f@gmail.com',
    url='https://github.com/razortheory/py_thumbnailer',
    license='BSD',
    packages=['py_thumbnailer', ],
    entry_points={
        'console_scripts': [
            'py-thumbnailer = py_thumbnailer.cli:main',
        ]
    },
    install_requires=[
        'pillow',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

