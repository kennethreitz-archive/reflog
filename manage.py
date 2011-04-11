#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

dashboard manager
~~~~~~~~~~~~~~~~~

This module contains the management functionality.

"""

import os

from clint.textui import puts, indent, colored
from flaskext.script import Manager

from dashboard import app, g, redis_connect
from dashboard.views.gh_commits import grab_changelog
from dashboard.views.topsy import get_window_url, WINDOW_MAP


manager = Manager(app)

app.test_request_context('/').push()



@manager.command
def hello():
    print 'hello'

@manager.command
def clear_db():

    KEYS = ['dashboard:github:commits',]

    puts('Clearing Database...')

    with indent(4):

        r = redis_connect()

        for key in KEYS:
            if r.delete(key):
                puts('{0} deleted.'.format(colored.red(key)))


@manager.command
def migrate():
    os.system('./migrate.py')


@manager.command
def sync():
    puts('Grabbing GitHub Commits...')
    with indent(2):
        puts(grab_changelog())

    puts('Grabbing Topsy Links...')
    with indent(2):
        for w in WINDOW_MAP.keys():
            puts(get_window_url(w))


if __name__ == '__main__':
    manager.run()