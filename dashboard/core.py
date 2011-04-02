# -*- coding: utf-8 -*-

"""
dashboard.core
~~~~~~~~~~~~~~

This module contains all of the Dashboard's core.

"""


from flask import Flask
app = Flask(__name__)


GH_CHANGELOG_URL = 'https://github.com/changelog.atom'

import requests
from lxml import objectify, etree


@app.route('/')
def index():
    return 'Hello, from flask!'


@app.route('/changelog')
def show_changelog():

    r = requests.get(GH_CHANGELOG_URL)
    tree = objectify.fromstring(r.content)

    collector = []

    for commit in tree.xpath('//entry'):
        collector.append(commit.title)

    return '\n'.join(collector)