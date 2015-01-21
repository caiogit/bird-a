# -*- coding: utf-8 -*-

import pyramid.view
import pyramid.security
import pyramid.httpexceptions
import birda.models.users

#_ = TranslationStringFactory('bird-a')

def addroutes(config):
	"""
	Map uri patterns with associated views
	"""

	# Show available ontologies
	config.add_route('main', '/')
	# Let the user log in
	#config.add_route('login', '/login')
	# Let the user log out
	#config.add_route('logout', '/logout')

	# List all available ontologies
	#config.add_route('show_instances', '/list')
	# Show all the instances of an ontology
	#config.add_route('show_instances', '/{onto_id}/')
	# Add an instance to an ontology
	#config.add_route('add_instance', '/{onto_id}/add')
	# Show an instance of an ontology
	#config.add_route('show_instance', '/{onto_id}/{inst_id}')
	# Show an instance of an ontology
	#config.add_route('edit_instance', '/{onto_id}/{inst_id}/edit')
	# Delete an instance of an ontology
	#config.add_route('delete_instance', '/{onto_id}/{inst_id}/delete')

	# Returns via JSON all the instances
	#config.add_route('search_instances', '/{onto_id}/search')

# ================================================================================================ #

class WikiViews(object):
	def __init__(self, request):
		self.request = request
		#renderer = get_renderer("templates/layout.pt")
		#self.layout = renderer.implementation().macros['layout']
		self.logged_in = pyramid.security.authenticated_userid(request)

	# ----------------------------------------------------------------------------- #

	@pyramid.view.view_config(route_name='main', permission='view',
						 renderer='templates/main.jinja2')
	def main(self):
		return {}

	# ----------------------------------------------------------------------------- #

	# @pyramid.view.view_config(route_name='login', permission='view',
	# 						  renderer='templates/login.jinja2')
	# @pyramid.view.forbidden_view_config(renderer='templates/login.jinja2')
	# def login(self):
	#
	# 	message, login, password = '', '', ''
	# 	if self.request.referer == self.request.route_url('login'):
	# 		self.request.referer = '/'  # never use login form itself as came_from
	# 	came_from = self.request.params.get('came_from', self.request.referer)
	#
	# 	if 'form.submitted' in self.request.params:
	# 		login = self.request.params['login']
	# 		password = self.request.params['password']
	# 		if birda.models.users.User.check_password(login, password):
	# 			headers = pyramid.security.remember(self.request, login)
	# 			return pyramid.httpexceptions.HTTPFound(
	# 											location=came_from,
	# 											headers=headers)
	# 		message = 'Failed login'
	#
	# 	return dict(
	# 		title='Login',
	# 		message=message,
	# 		url=self.request.application_url + '/login',
	# 		came_from=came_from,
	# 		login=login,
	# 		password=password,
	# 	)
	#
	# # ----------------------------------------------------------------------------- #
	#
	# @pyramid.view.view_config(route_name='logout')
	# def logout(self):
	# 	headers = pyramid.security.forget(self.request)
	# 	url = self.request.route_url('wiki_view')
	# 	return pyramid.httpexceptions.HTTPFound(location=url,
	# 					 headers=headers)