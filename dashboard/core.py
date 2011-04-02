# -*- coding: utf-8 -*-

"""
dashboard.core
~~~~~~~~~~~~~~

This module contains all of the Dashboard's core.

"""


from flask import Flask
app = Flask(__name__)



@app.route('/')
def index():
    return 'Hello, from flask!'
