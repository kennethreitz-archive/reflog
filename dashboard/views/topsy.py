# -*- coding: utf-8 -*-

"""
dashboard.views.topsy
~~~~~~~~~~~~~~~~~~~~~

This module contains all of the Topsy Dashboard capabilities.

"""

import otter
import redi     # \o/
import requests


from flask import Module, g, render_template


__all__ = ('commits',)


SEARCH_TERM = 'github.com/'

WINDOW_MAP = {
    'day': 'd',
    '3day': 'd3',
    'week': 'w',
    'month': 'm',
    'year': 'y',
}

topsy = Module(__name__)


@topsy.before_request
def configure_redi():
    redi.config.redis = g.r


def get_by_window(term, n, pages=3):

    for page in range(pages):

        r = otter.Resource('search')
        r(q=term, window=n, offset=page*10)

        for link in r.response.list:
            yield dict(
                title=link.title,
                url=link.url,
                hits=link.hits
            )


def show_window(window):
    """  """
    links = redi.s.dashboard.topsy._(window, 'list')

    return links.sorted_by('hits', reverse=True)


def get_window(window, w):
    """  """

    links = redi.s.dashboard.topsy._(window, 'list')
    added_count = 0
    updated_count = 0


    for new_link in get_by_window(SEARCH_TERM, window):

        if not new_link['url'] in [l['url'] for l in links]:
            links.lpush(new_link)
            added_count += 1
        else:
            for link in links:
                if link['url'] == new_link['url']:
                    link['hits'] = new_link['hits']
                    updated_count += 1

    return dict(updated_count=updated_count, added_count=added_count)


@topsy.route('/')
def show_topsy():
    return ''.join(WINDOW_MAP.keys())


@topsy.route('/<window>')
def show_window_url(window):

    if window in WINDOW_MAP:

        links = show_window(window)

        if not len(links):
            get_window(WINDOW_MAP[window], window)

        return render_template('topsy.html', links=links, window=window)
    else:
        pass


@topsy.route('/<window>/get')
def get_window_url(window):

    r = get_window(WINDOW_MAP[window], window)

    return '{0} links added.\n{1} links updated.'.format(r['added_count'], r['updated_count'])

