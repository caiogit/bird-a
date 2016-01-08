#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 08/01/16.
"""

from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home.jinja2')
def my_view(request):
    return {}