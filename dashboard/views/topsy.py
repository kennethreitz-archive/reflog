# -*- coding: utf-8 -*-

"""
dashboard.views.topsy
~~~~~~~~~~~~~~~~~~~~~

This module contains all of the Topsy Dashboard capabilities.

"""

import requests

from lxml import objectify
from jsonpickle import encode as json_encode
from jsonpickle import decode as json_decode

from flask import Module, g, render_template


__all__ = ('commits',)




topsy = Module(__name__)


@topsy.route('/')
def show_topsy():
    return'topsy!'
