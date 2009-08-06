#!/usr/bin/env python

from fabric.api import *
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, first, upload_template, sed, uncomment, \
                        comment, contains, append
from fabric.contrib.project import rsync_project, upload_project

# We don't need extra output from fabric
from fabric.state import output
output.everything = False
env.warn_only=True
env.abort=False


def has_command(cmd):
    """
    Check if a command exists on a separate host
    """
    output = run('which %s' % cmd)
    return not output.failed


def install_package(install_cmd, package):
    """
    Install a package on a separate host
    """
    output = sudo("%s %s" % (install_cmd, package))
    return not output.failed


def test():
    env.host_string = '38.118.71.92'
    env.user = 'webdev'
    env.password = '' #put password here
    command_list = ('charlie', 'ls', 'python')
    for cmd in command_list:
        if has_command(cmd):
            print "Has %s" % cmd
        else:
            print "Needs %s" % cmd
    package_list = ('dumbthing', 'apache2.2-common',)
    for pkg in package_list:
        if install_package('apt-get install', pkg):
            print "Success installing: %s" % pkg
        else:
            print "Failure installing: %s." % pkg


test()