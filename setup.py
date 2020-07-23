#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='metal-test',
    version='0.1',
    description='A C/C++ toolset for bare metal & embedded developments',
    author='Klemens Morgenstern',
    url='http://pypi.python.org/pypi/metal_test',
    packages=['metal'],
    entry_points={
        'console_scripts': [ 'metal-serial-generate=metal.serial.generate', 'metal-serial-interpret=metal.serial.interpret' ]
    },
    license='APACHE',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Test Tools',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python :: 3',
    ],
)