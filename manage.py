#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

dashboard manager
~~~~~~~~~~~~~~~~~

This module contains the management functionality.

"""


from flaskext.script import Manager
from clint.textui import puts, indent, colored

from dashboard import app, g, redis_connect


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



if __name__ == '__main__':
    manager.run()