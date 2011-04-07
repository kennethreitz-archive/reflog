# -*- coding: utf-8 -*-

from flask import Module, g, render_template

index = Module(__name__)


__all__ = ('index',)

@index.route('/')
def get_index():
    return render_template('index.html')
