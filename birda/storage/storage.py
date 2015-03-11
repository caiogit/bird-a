# -*- coding: utf-8 -*-

class Storage(object):

	def __init__(self):
		pass

	def get_ontologies(self):
		"""
		Get a list all all available ontologies

		:return: List of dictionaries in the form {'id':'...', 'title':'...', 'description':'...'}
		"""
		pass

	def get_instances(self, onto_id):
		"""
		Get a list of all instances of a given ontology

		:param onto_id: Ontology ID
		:return: List of dictionaries (keys: 'id', 'title')
		"""
		pass

	def get_ontology_iri(self, onto_id):
		"""
		Get the ontology IRI

		:param onto_id: (string) Ontology ID
		:return: (string) IRI of the ontology
		"""
		pass