import pyramid.config
import pyramid.authentication
import pyramid.authorization
import pyramid.session

import sqlalchemy

import birda
import birda.models
import birda.models.acl
import birda.services

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

	# COnfig creation
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

	# Scan modules for cornice services
	#config.include("birda.services")
	#config.scan("birda:services")

	# Import all birda.models modules (necessary?)
	#config.scan('birda.models')

	return config.make_wsgi_app()


