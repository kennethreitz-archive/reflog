# -*- coding: utf-8 -*-

"""
dashboard.core
~~~~~~~~~~~~~~

This module contains all of the Dashboard's core.

"""


import requests

from redis import Redis
from lxml import objectify, etree

from flask import (
    request, session, redirect, url_for,
    abort, render_template, flash, Flask, g
)

app = Flask(__name__)
app.debug = True


from .db import redis_connect
from .views import index, gh_commits

app.register_module(index)
app.register_module(gh_commits, url_prefix='/github/commits')



@app.before_request
def before_request():
    # redis connect
    if not getattr(g, 'r', None):
        g.r = redis_connect()
