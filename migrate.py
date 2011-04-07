#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clint.textui import puts, colored, progress, indent

from dashboard import app, g, redis_connect
app.test_request_context('/').push()


redis = redis_connect()


def main():
    print '\o/'


if __name__ == '__main__':
    main()