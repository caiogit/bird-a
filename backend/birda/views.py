#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

from pyramid.view import view_config

# ============================================================================ #

@view_config(route_name='home', renderer='templates/home.jinja2')
def my_view(request):
    return {}