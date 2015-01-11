import pyramid.config
import pyramid.authentication
import pyramid.authorization
import pyramid.session

import sqlalchemy

import birda.models
import birda.models.acl
import birda.routes

def main(global_config, **settings):
	"""
	This function returns a Pyramid WSGI application.
	"""
	engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
	birda.models.DBSession.configure(bind=engine)

	session_factory = pyramid.session.UnencryptedCookieSessionFactoryConfig(
		settings['session.secret']
	)

	authn_policy = pyramid.authentication.SessionAuthenticationPolicy()
	authz_policy = pyramid.authorization.ACLAuthorizationPolicy()

	config = pyramid.config.Configurator(
		settings=settings,
		root_factory=birda.models.acl.RootFactory,
		authentication_policy=authn_policy,
		authorization_policy=authz_policy,
		session_factory=session_factory
	)

	# Add a static view routed on "/static" for the directory "bird-a/static"
	config.add_static_view('static', 'static')

	# Add all the routes of birda
	config.include(birda.routes.addroutes)

	# Scan modules for views (i.e. @view_config decorators)
	config.scan()

	# Import all birda.models modules (necessary?)
	config.scan('birda.models')

	return config.make_wsgi_app()


