#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import *


CMD_TEMPLATE = '{0}'


def _run(cmd):
    local(CMD_TEMPLATE.format(cmd))


def prod():
    global CMD_TEMPLATE

    CMD_TEMPLATE = 'epio run_command {0}'


def deploy():
    """Deploys the application"""

    local('epio upload')
    local('epio run_command ./manage.py migrate')


def migrate():
    """Runs migrate script."""

    _run('./manage.py migrate')


def clear_db():
    _run('./manage.py clear_db')


