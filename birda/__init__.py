import pyramid.config
import pyramid.authentication
import pyramid.authorization
import pyramid.session

import sqlalchemy

import birda.models

def main(global_config, **settings):  # pragma: no cover
	""" This function returns a Pyramid WSGI application.
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
		root_factory=birda.models.RootFactory,
		authentication_policy=authn_policy,
		authorization_policy=authz_policy,
		session_factory=session_factory
	)

	config.include('pyramid_chameleon')
	config.add_static_view('static', 'shootout:static')
	config.include(addroutes)
	config.scan()

	# Import all birda.models modules (necessary?)
	config.scan('birda.models')

	return config.make_wsgi_app()

def addroutes(config):
	# broken out of main() so it can be used by unit tests
	config.add_route('idea', '/ideas/{idea_id}')
	config.add_route('user', '/users/{username}')
	config.add_route('tag', '/tags/{tag_name}')
	config.add_route('idea_add', '/idea_add')
	config.add_route('idea_vote', '/idea_vote')
	config.add_route('register', '/register')
	config.add_route('login', '/login')
	config.add_route('logout', '/logout')
	config.add_route('about', '/about')
	config.add_route('main', '/')

