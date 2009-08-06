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
def test():
    env.host_string = '38.118.71.92'
    env.user = 'webdev'
    output = run('ls -l')
    return output


print test()