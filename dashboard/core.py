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
from .views import commits

app.register_module(commits, url_prefix='/changelog')


@app.before_request
def before_request():
    if not getattr(g, 'r', None):
        g.r = redis_connect()



@app.route('/')
def index():
    return render_template('index.html')



    