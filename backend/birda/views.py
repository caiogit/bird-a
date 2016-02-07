#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

from pyramid.view import view_config

# ============================================================================ #

def add_routes(config):
	config.add_route('home', '/')
	config.add_route('proxy', '/proxy.html')

# ============================================================================ #

# "home" view with a simple greeting message
@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
	print "Ok"
	return {}

# ---------------------------------------------------------------------------- #

# "proxy.html" view needed by xdomain (https://github.com/jpillora/xdomain)
@view_config(route_name='proxy', renderer='templates/proxy.jinja2')
def proxy(request):
	return {'frontend_uri':request.registry.settings['birda.frontend']}

# ============================================================================ #
