#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import storage

class FileStorage(storage.Storage):
	"""
	Storage based on files
	"""

	# Dictionary "ontology_id" -> dictionary with keys:
	#	'title': ontology name
	#	'birda': birda instance file
	#   'ontology': ontology instances file
	ontologies = []

	# ----------------------------------------------------------------------- #

	def __init__(self, prj_path):
		self.prj_path = prj_path
		self.catalog_path = self.prj_path + os.path.sep + 'catalog'
		self.birda_catalog_path = self.catalog_path + os.path.sep + 'birda'
		self.ontologies_catalog_path = self.catalog_path + os.path.sep + 'birda'

		# Initialize catalog
		self.load_available_ontologies_catalog()

	# ----------------------------------------------------------------------- #

	def load_available_ontologies_catalog(self):
		ontos = os.listdir(self.ontologies_catalog_path)
		ontos = [os.path.basename(onto) for onto in ontos]
		print ontos

	# ----------------------------------------------------------------------- #

	def get_ontologies(self):
		ontos = os.listdir(self.ontologies_catalog_path)
		ontos = [os.path.basename(onto) for onto in ontos]
		print ontos

# ================================================================================================ #

if __name__ == '__main__':
	prj_path = os.path.dirname( os.path.realpath(__file__) ) + "/../.."
	storage = FileStorage(prj_path)
	storage.get_ontologies()