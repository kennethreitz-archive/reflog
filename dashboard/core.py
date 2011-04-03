# -*- coding: utf-8 -*-

"""
dashboard.core
~~~~~~~~~~~~~~

This module contains all of the Dashboard's core.

"""


from flask import (
    request, session, redirect, url_for,
    abort, render_template, flash, Flask
)

app = Flask(__name__)


GH_CHANGELOG_URL = 'https://github.com/changelog.atom'

import requests
from lxml import objectify, etree


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/changelog')
def show_changelog():

    r = requests.get(GH_CHANGELOG_URL)
    feed = objectify.fromstring(r.content)

    collector = []

    for commit in feed.entry:
        collector.append(dict(
            email=commit.author.email,
            title=commit.title,
            link=commit.link.attrib.get('href', None)
        ))

    return '<br />'.join([str(c['title']) for c in collector])