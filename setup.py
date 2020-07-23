#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='metal-test',
    version='0.1',
    description='A C/C++ toolset for bare metal & embedded developments',
    author='Klemens Morgenstern',
    url='http://pypi.python.org/pypi/metal_test',
    packages=['metal'],
    install_requires=['argparse', 'pcpp', 'pyelftools', 'cxxfilt'],
    entry_points={
        'console_scripts': ['metal-serial-generate=metal.serial.generate.main',
                            'metal-serial-interpret=metal.serial.interpret.main',
                            'metal-flags:metal.flags.print_flags']
    },
    license='APACHE',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
)