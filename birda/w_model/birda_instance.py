#!/usr/bin/env python
# -*- coding: utf-8 -*-

class BirdaInstance(object):
	"""
	Python representation of a bird-a instance
	"""
	
	# List of w_model.Widget not descending from any other widget (root widgets)
	widgets = []
	
	def __init__(self):
		pass

	def parse(self,rdf):
		"""
		Initializes the object by parsing a rdf birda instance

		:param rdf: (rdflib.Graph) RDF object containing the birda instance
		:return: None
		"""
		pass


if __name__ == '__main__':
	pass