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


"""
Check server for requirements task
    checks for and installs services
    installs libraries

Check server has web site requirements
    checks for and installs services
    installs libraries

Install website (scm checkout)
    cd to folder
    checkout the repository
    run post-install script
    ?add to web server settings?

Update website (scm checkout)
    cd to folder
    run a "files to be updated" command
    update
"""

def set_env(*args, **kwargs):
    """
    A generic command to setup the environment
    """
    for key, value in kwargs.items():
        setattr(env, key, value)

def has_command(cmd):
    """
    Check if a command exists on a separate host
    """
    output = run('which %s' % cmd)
    return not output.failed


def has_package(list_pkg_cmd, package, **kwargs):
    """
    Check if the server has the package installed
    """
    set_env(**kwargs)
    pkgs = package.split(" ")
    final_output = []
    has_everything = True
    for item in pkgs:
        if "%(package)s" in list_pkg_cmd:
            output = sudo(list_pkg_cmd % {'package': item})
        elif "%s" in install_cmd:
            output = sudo(list_pkg_cmd % item)
        else:
            output = sudo("%s %s" % (list_pkg_cmd, item))
        final_output.append(output)
        has_everything = not output.failed
    return has_everything

def install_package(install_cmd, package, **kwargs):
    """
    Install a package on a separate host
    """
    set_env(**kwargs)
    if "%(package)s" in install_cmd:
        output = sudo(install_cmd % {'package': package})
    elif "%s" in install_cmd:
        output = sudo(install_cmd % package)
    else:
        output = sudo("%s %s" % (install_cmd, package))
    print output
    return not output.failed


def run_or_sudo(command, sudo, **kwargs):
    """
    Utility command to either issue a run command or a sudo command
    """
    set_env(**kwargs)
    if sudo:
        output = sudo(command)
    else:
        output = run(command)
    return not output.failed
    

def svn_to_update(path, sudo=False, **kwargs):
    """
    Find out what is going to be updated when you update from the repository
    """
    set_env(**kwargs)
    cmd = "cd %s;svn status -u | grep '*'" % path
    output = run_or_sudo(cmd, sudo)
    return not output.failed


def git_clone(path, url, sudo=False, **kwargs):
    """
    Clone a git repository
    """
    set_env(**kwargs)
    cmd = 'cd %s;git clone %s' % (path, url)
    output = run_or_sudo(cmd, sudo)
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


#test()