# -*- coding: utf-8 -*-

"""
dashboard.core
~~~~~~~~~~~~~~

This module contains all of the Dashboard's core.

"""

import redi
import requests

from lxml import objectify, etree

from flask import (
    request, session, redirect, url_for,
    abort, render_template, flash, Flask, g
)

app = Flask(__name__)
app.debug = True


from .db import redis_connect
from .views import index, gh_commits, topsy

app.register_module(index)
app.register_module(gh_commits, url_prefix='/github/commits')
app.register_module(topsy, url_prefix='/topsy')



@app.before_request
def before_request():

    # redis connect
    if not getattr(g, 'r', None):
        g.r = redis_connect()

        redi.config.init(r=g.r)
