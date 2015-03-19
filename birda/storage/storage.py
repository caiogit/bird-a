#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Storage(object):
	"""
	Storage abstract class

	"""

	# ----------------------------------------------------------------------- #

	def __init__(self):
		pass

	# ----------------------------------------------------------------------- #

	def load_available_ontologies_catalog(self):
		"""
		Load the internal ontologies catalog

		:return: None
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	def get_ontologies(self):
		"""
		Get a list all all available ontologies

		:return: List of dictionaries in the form {'id':'...', 'title':'...', 'description':'...'}
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	def get_instances(self, onto_id):
		"""
		Get a list of all instances of a given ontology

		:param onto_id: Ontology ID
		:return: List of dictionaries (keys: 'id', 'title')
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	def get_ontology_iri(self, onto_id):
		"""
		Get the ontology IRI

		:param onto_id: (string) Ontology ID
		:return: (string) IRI of the ontology
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	def get_birda_instances(self):
		"""
		Return all birda instances in rdf format

		:return: Dictionary "ontology_id" -> rdflib.Graph
		"""
		raise NotImplementedError("This method should be implemented by subclasses")

# ================================================================================================ #

if __name__ == '__main__':
	storage = Storage()
	storage.get_ontologies()