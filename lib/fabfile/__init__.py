
from fabric.api import cd, hide, settings, show, hosts, roles, runs_once, \
                        require, prompt, put, get, run, sudo, local, env, \
                        abort, warn
from fabric.contrib.console import confirm
from fabric.contrib.files import exists, first, upload_template, sed, uncomment, \
                        comment, contains, append
from fabric.contrib.project import rsync_project, upload_project


def install_lib():
    pass