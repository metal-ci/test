#!/usr/bin/env python
import os

from setuptools import setup, find_packages

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

setup(
    name='metal-test',
    version='0.1.2',
    description='A C/C++ toolset for bare metal & embedded developments',
    author='Klemens Morgenstern',
    author_email='klemens@metal.ci',
    url='http://pypi.python.org/pypi/metal_test',
    packages=['metal', 'metal.gdb', 'metal.serial'],
    package_data={'metal': package_files('src') + package_files('include')},
    install_requires=['argparse', 'pcpp', 'pyelftools', 'cxxfilt'],
    entry_points={
        'console_scripts': ['metal-serial-generate=metal.serial.generate:main',
                            'metal-serial-interpret=metal.serial.interpret:main',
                            'metal-flags=metal.flags:print_flags']
    },
    license='APACHE',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
)