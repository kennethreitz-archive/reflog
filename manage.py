#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

dashboard manager
~~~~~~~~~~~~~~~~~

This module contains the management functionality.

"""



from flaskext.script import Manager

from dashboard import app

manager = Manager(app)


@manager.command
def hello():
    print 'hello'



if __name__ == '__main__':
    manager.run()