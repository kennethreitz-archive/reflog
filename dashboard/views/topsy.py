# -*- coding: utf-8 -*-

"""
dashboard.views.topsy
~~~~~~~~~~~~~~~~~~~~~

This module contains all of the Topsy Dashboard capabilities.

"""

import otter
import redi     # \o/
import requests

from operator import itemgetter

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
    links = redi.list(('dashboard', 'topsy', window), r=g.r)

    return sorted(links, key=itemgetter('hits'), reverse=True)


def get_window(window, w):
    """  """

    links = redi.list(('dashboard', 'topsy', w), r=g.r)
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





# @topsy.route('/week')
# def show_week():

#     window = 'week'

#     links = show_window(window)

#     if not len(links):
#         get_window('w', 'week')

#     return render_template('topsy.html', links=links, window=window)



# @topsy.route('/week/get')
# def get_week():

#     r = get_window('w', 'week')

#     return '{0} links added.\n{1} links updated.'.format(r['added_count'], r['updated_count'])





# @topsy.route('/3day')
# def show_threeday():

#     window = '3day'

#     links = show_window(window)

#     if not len(links):
#         get_window('3d', '3day')

#     return render_template('topsy.html', links=links, window=window)



# @topsy.route('/day/3day')
# def get_threeday():

#     r = get_window('3d', '3day')

#     return '{0} links added.\n{1} links updated.'.format(r['added_count'], r['updated_count'])




# @topsy.route('/month')
# def show_month():

#     window = 'month'

#     links = show_window(window)

#     if not len(links):
#         get_window('m', 'month')

#     return render_template('topsy.html', links=links, window=window)



# @topsy.route('/month/get')
# def get_month():

#     r = get_window('m', 'month')

#     return '{0} links added.\n{1} links updated.'.format(r['added_count'], r['updated_count'])


