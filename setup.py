#!/usr/bin/env python

"""Setup file for Multi-Task Multi-Stage library.
"""

__author__    = "Mark Santcroos"
__email__     = "mark.santcroos@rutgers.edu"
__copyright__ = "Copyright 2014, The RADICAL Project at Rutgers"
__license__   = "MIT"


""" Setup script. Used by easy_install and pip. """

import os
import sys
import subprocess

from setuptools import setup, find_packages, Command


#-----------------------------------------------------------------------------
#
def get_version():

    short_version = None
    long_version  = None

    try:
        import subprocess as sp
        import re

        srcroot       = os.path.dirname (os.path.abspath (__file__))
        VERSION_MATCH = re.compile (r'(([\d\.]+)\D.*)')

        # attempt to get version information from git
        p   = sp.Popen ('cd %s && git describe --tags --always' % srcroot,
                        stdout=sp.PIPE, stderr=sp.STDOUT, shell=True)
        out = p.communicate()[0]


        if  p.returncode != 0 or not out :

            # the git check failed -- its likely that we are called from
            # a tarball, so use ./VERSION instead
            out=open ("%s/VERSION" % srcroot, 'r').read().strip()


        # from the full string, extract short and long versions
        v = VERSION_MATCH.search (out)
        if v:
            long_version  = v.groups ()[0]
            short_version = v.groups ()[1]


        # sanity check if we got *something*
        if  not short_version or not long_version :
            sys.stderr.write ("Cannot determine version from git or ./VERSION\n")
            import sys
            sys.exit (-1)


        # make sure the version files exist for the runtime version inspection
        open ('%s/VERSION' % srcroot, 'w').write (long_version+"\n")
        open ('%s/src/radical/ensemblemd/mtms/VERSION' % srcroot, 'w').write (long_version+"\n")


    except Exception as e :
        print 'Could not extract/set version: %s' % e
        import sys
        sys.exit (-1)

    return short_version, long_version


short_version, long_version = get_version ()

#-----------------------------------------------------------------------------
# check python version. we need > 2.5, <3.x
if  sys.hexversion < 0x02050000 or sys.hexversion >= 0x03000000:
    raise RuntimeError("MTMS requires Python 2.x (2.5 or higher)")

#-----------------------------------------------------------------------------
#
def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

#-----------------------------------------------------------------------------
setup_args = {
    'name'             : 'radical.ensemblemd.mtms',
    'version'          : short_version,
    'description'      : "MTMS is a library for executing many pipelines.",
    'long_description' : (read('README.md') + '\n\n' + read('CHANGES.md')),
    'author'           : 'RADICAL Group at Rutgers University',
    'author_email'     : 'mark.santcroos@rutgers.edu',
    'maintainer'       : "Mark Santcroos", 
    'maintainer_email' : 'mark.santcroos@rutgers.edu',
    'url'              : 'https://github.com/radical-cybertools',
    'license'          : 'MIT',
    'keywords'         : "molecular dynamics workflow",
    'classifiers'      :  [
        'Development Status   :: 5 - Production/Stable',
        'Intended Audience    :: Developers',
        'Environment          :: Console',
        'License              :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic                :: Utilities',
        'Topic                :: System :: Distributed Computing',
        'Operating System     :: MacOS :: MacOS X',
        'Operating System     :: POSIX',
        'Operating System     :: Unix'
    ],

    #'entry_points': {
    #    'console_scripts': 
    #},

    #'dependency_links': ['https://github.com/saga-project/saga-pilot/tarball/master#egg=sagapilot'],

    'namespace_packages': ['radical', 'radical.ensemblemd'],
    'packages'    : find_packages('src'),
    'package_dir' : {'': 'src'},  

    'package_data'     : {'': ['*.sh', 'VERSION', 'VERSION.git', ]},
    'install_requires' : ['setuptools>=1',
                          'radical.pilot'
                         ],

    'zip_safe'         : False,
    'test_suite' :    'tests'
}

#-----------------------------------------------------------------------------

setup (**setup_args)

#-----------------------------------------------------------------------------
