# -*- coding: utf-8 -*-

"""
dashboard.core
~~~~~~~~~~~~~~

This module contains all of the Dashboard's core.

"""


import requests
from jsonpickle import encode as json_encode
from jsonpickle import decode as json_decode

from redis import Redis
from lxml import objectify, etree
from flask import (
    request, session, redirect, url_for,
    abort, render_template, flash, Flask, g
)


# Redis autoconfig for ep.io

def redis_connect():
    try:
        from bundle_config import config
        r = Redis(
            host = config['redis']['host'],
            port = int(config['redis']['port']),
            password = config['redis']['password'],
        )
    except ImportError:
        # use local settings (env?)
        r = Redis(host='localhost', port=6379, db=0)

    return r


app = Flask(__name__)

app.debug = True

@app.before_request
def before_request():
    if not getattr(g, 'r', None):
        g.r = redis_connect()


GH_CHANGELOG_URL = 'https://github.com/changelog.atom'


def cached_or_not_url(url, expires=600):
    """Returns cached content, else caches results and stores."""

    content = g.r.get(url)

    if content is not None:
        return json_decode(content)
    else:

        r = requests.get(url)

        g.r.set(url, json_encode(r.content))
        g.r.expire(url, expires)

        return r.content


def cached_or_not(key, callback, expires=60, *args):
    """Cacher"""

    value = g.r.get(key)

    if value is not None:
        return json_decode(value)
    else:
        value = callback(*args)

        g.r.set(key, json_encode(value))
        g.r.expire(key, expires)

        return value


def fetch_github_commits():

    r = requests.get(GH_CHANGELOG_URL).content

    feed = objectify.fromstring(r)

    commits = []

    for commit in feed.entry:
        commits.append(dict(
            author=unicode(commit.author.name),
            email=str(commit.author.email),
            message=unicode(commit.title),
            link=str(commit.link.attrib.get('href', None))
        ))

    return commits



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/changelog')
def show_changelog():

    commits = g.r.lrange('dashboard:github:commits', 0, -1)

    for i, c in enumerate(commits):
        commits[i] = json_decode(c)

    return render_template('github-commits.html', commits=commits)



@app.route('/get/changelog')
def grab_changelog():

    stored_commits = g.r.lrange('dashboard:github:commits', 0, -1)
    added_count = 0

    for i, c in enumerate(stored_commits):
        stored_commits[i] = json_decode(c)

    for commit in reversed(fetch_github_commits()):

        if commit not in stored_commits:
            g.r.lpush('dashboard:github:commits', json_encode(commit))
            added_count += 1
        # g.r.set('dashboard:github:commits:latest', commit.get('link'))



    return '{0} commits added.'.format(added_count)