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

	def reload_available_binst_catalog(self):
		"""
		Reload the internal bird-a instances catalog

		:return: None
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	def get_binst_instances(self, binst_id):
		"""
		Get a list of all instances of a given bird-a instance

		:param binst_id: bird-a instance id
		:return: List of dictionaries (keys: 'id', 'title')
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	def get_binst_iri(self, binst_id):
		"""
		Get the bird-a instance IRI

		:param binst_id: (string) bird-a instance id
		:return: (string) IRI of the ontology
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	def get_all_binst(self):
		"""
		Return all bird-a instances in rdf format

		:return: Dictionary {"<binst_id>" -> rdflib.Graph}
		"""
		raise NotImplementedError("This method should be implemented by subclasses")

# ================================================================================================ #

if __name__ == '__main__':
	storage = Storage()
	storage.get_ontologies()