#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BirdaInstance(object):
	"""
	Python representation of a bird-a instance
	"""
	
	# List of w_model.Widget not descending from any other widget (root widgets)
	widgets = []

	# ----------------------------------------------------------------------- #
	
	def __init__(self):
		pass

	# ----------------------------------------------------------------------- #

	def parse(self,rdf):
		"""
		Initializes the object by parsing a rdf birda instance

		:param rdf: (rdflib.Graph) RDF object containing the birda instance
		:return: None
		"""
		pass

# ================================================================================================ #

class BirdaInstances(object):
	"""
	Container for processed Birda instances
	"""

	# Dictionary: "ontology_id" -> birda_instance
	birda_instances = {}

	# ----------------------------------------------------------------------- #

	def __init__(self):
		pass

	# ----------------------------------------------------------------------- #

	def load_instances(self, rdf_dict):
		"""
		Load birda instances from a dictionary containing birda instances in rdf format

		:param rdf_dict: Dictionary "ontology_id" -> rdflib.Graph
		:return: None
		"""
		raise NotImplementedError()

# ================================================================================================ #

if __name__ == '__main__':
	pass