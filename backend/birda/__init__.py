#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import pyramid.config
import pyramid.authentication
import pyramid.authorization
import pyramid.session
import pyramid.events

import sqlalchemy

import birda.models
import birda.models.acl

from birda.bController.form_factory import FormFactory, IFormFactory

# ============================================================================ #

# Add CORS headers
def add_cors_headers_response_callback(event):
	CORS_HEADERS = {
		'Access-Control-Allow-Origin': '*',
		'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
		'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
		'Access-Control-Allow-Credentials': 'true',
		'Access-Control-Max-Age': '1728000',
	}
	
	# Patch for unicode strings (to be removed in Python3)
	CORS_HEADERS = __all__ = { k.encode('ascii'): CORS_HEADERS[k].encode('ascii') for k in CORS_HEADERS }
	
	def cors_headers(request, response):
		response.headers.update(CORS_HEADERS)
		
	event.request.add_response_callback(cors_headers)

# ============================================================================ #

def main(global_config, **settings):
	"""
	This function returns a Pyramid WSGI application.
	"""

	# Database
	engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
	birda.models.DBSession.configure(bind=engine)

	# Authentication / Authorization
	session_factory = pyramid.session.UnencryptedCookieSessionFactoryConfig(
		settings['session.secret']
	)

	authn_policy = pyramid.authentication.SessionAuthenticationPolicy()
	authz_policy = pyramid.authorization.ACLAuthorizationPolicy()

	# Config creation
	config = pyramid.config.Configurator(
		settings=settings,
		root_factory=birda.models.acl.RootFactory,
		authentication_policy=authn_policy,
		authorization_policy=authz_policy,
		session_factory=session_factory
	)

	# Disabling exception logger in order to avoid conflicts with cornice
	# (exc_logger will be removed in .ini sometime in the future...)
	config.add_settings(handle_exceptions=False)
	
	# Add pretty printing to jsons
	if settings.get('birda.pretty_json_output','false') == 'true':
		config.add_renderer('json', pyramid.renderers.JSON(indent=4))

	# Scan modules for cornice services
	#config.include("birda.services")
	config.include('cornice')
	config.scan("birda.services")

	# Add "home" view, with a simple greeting message
	config.add_route('home', '/')
	config.scan()

	# Import all birda.models modules (necessary?)
	#config.scan('birda.models')

	config.add_subscriber(add_cors_headers_response_callback, pyramid.events.NewRequest)
	
	# Activate and set application wide services (singletons)
	config.include('pyramid_services')
	config.register_service(FormFactory(settings), iface=IFormFactory, name='FormFactory')

	# Make and run the application
	return config.make_wsgi_app()


