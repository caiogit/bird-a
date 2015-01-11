# -*- coding: utf-8 -*-


def addroutes(config):
	"""
	Map uri patterns with associated views
	"""

	# Show available ontologies
	config.add_route('main', '/')
	# Let the user log in
	config.add_route('login', '/login')
	# Let the user log out
	config.add_route('logout', '/logout')

	# Show all the instances of an ontology
	config.add_route('show_instances', '/{onto_id}/')
	# Add an instance to an ontology
	config.add_route('add_instance', '/{onto_id}/add')
	# Show an instance of an ontology
	config.add_route('show_instance', '/{onto_id}/{inst_id}')
	# Show an instance of an ontology
	config.add_route('edit_instance', '/{onto_id}/{inst_id}/edit')
	# Delete an instance of an ontology
	config.add_route('delete_instance', '/{onto_id}/{inst_id}/delete')

	# Returns via JSON all the instances
	config.add_route('search_instances', '/{onto_id}/search')


