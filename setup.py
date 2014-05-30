from __future__ import unicode_literals

import re

from distutils.command.build import build
from setuptools import setup, find_packages


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']


class cffi_build(build):
    """This is a shameful hack to ensure that cffi is present when we specify
    ext_modules. We can't do this eagerly because setup_requires hasn't run
    yet.
    """
    def finalize_options(self):
        from bt_manager import ffi
        self.distribution.ext_modules = [ffi.verifier.get_extension()]
        build.finalize_options(self)


setup(
    name='BT-Manager',
    version=get_version('bt_manager/__init__.py'),
    url='https://github.com/liamw9534/bt-manager',
    license='Apache License, Version 2.0',
    author='Liam Wickins',
    author_email='liamw9534@gmail.com',
    description='Python-based Bluetooth Device Management',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    ext_package='rtpsbc',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'cffi >= 0.7',
    ],
    setup_requires=['cffi >= 0.7'],
    cmd_class={'build': cffi_build},
    test_suite='nose.collector',
    tests_require=[
        'nose',
        'mock >= 1.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Communications',
    ],
)
