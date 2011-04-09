# -*- coding: utf-8 -*-

"""
dashboard.views.github
~~~~~~~~~~~~~~~~~~~~~~

This module contains all of the GitHub Dashboard capabilities.

"""

import requests
import redi

from lxml import objectify

from flask import Module, g, render_template


__all__ = ('commits',)


GH_CHANGELOG_URL = 'https://github.com/changelog.atom'
NAMESPACE = ('dashboard', 'github', 'commits')


gh_commits = Module(__name__)



def fetch_github_commits():
    """Returns a list of GitHub commit dicts from the feed."""

    r = requests.get(GH_CHANGELOG_URL).content

    feed = objectify.fromstring(r)

    for commit in reversed([c for c in feed.entry]):
        yield dict(
            author=unicode(commit.author.name),
            email=str(commit.author.email),
            message=unicode(commit.title),
            link=str(commit.link.attrib.get('href', None))
        )



@gh_commits.route('/')
def show_changelog():

    commits = redi.list(NAMESPACE, r=g.r)
    return render_template('github-commits.html', commits=commits)



@gh_commits.route('/get')
def grab_changelog():

    commits = redi.list(NAMESPACE, r=g.r)
    added_count = 0

    for commit in fetch_github_commits():

        if commit not in commits:
            commits.lpush(commit)
            added_count += 1

    return '{0} commits added.'.format(added_count)