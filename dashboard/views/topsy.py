# -*- coding: utf-8 -*-

"""
dashboard.views.topsy
~~~~~~~~~~~~~~~~~~~~~

This module contains all of the Topsy Dashboard capabilities.

"""

import otter
import requests
from operator import itemgetter

from lxml import objectify
from jsonpickle import encode as json_encode
from jsonpickle import decode as json_decode

from flask import Module, g, render_template


__all__ = ('commits',)




topsy = Module(__name__)


def get_by_window(term, n):

    r = otter.Resource('search')
    r(q=term, window=n)

    for link in r.response.list:
        yield dict(
            title=link.title,
            url=link.url,
            hits=link.hits
        )


@topsy.route('/')
def show_topsy():
    return'topsy!'



@topsy.route('/week')
def show_week():

    links = g.r.lrange('dashboard:topsy:week', 0, -1)

    for i, l in enumerate(links):
        links[i] = json_decode(l)

    links = sorted(links, key=itemgetter('hits'), reverse=True)

    return render_template('topsy.html', links=links)

# Passing parameters to API:


@topsy.route('/week/get')
def get_week():

    stored_links = g.r.lrange('dashboard:topsy:week', 0, -1)
    added_count = 0

    for i, c in enumerate(stored_links):
        stored_links[i] = json_decode(c)['url']

    links = get_by_window('github.com/', 'w')

    for link in links:

        if not link['url'] in stored_links:
            g.r.lpush('dashboard:topsy:week', json_encode(link))
            added_count += 1
        else:
            pass
            # TODO: update it

    return '{0} links added.'.format(added_count)
