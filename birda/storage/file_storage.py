#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import rdflib
import storage
import pprint

# State if a birda instances without a corresponding repo instances will create an empty repo
CREATE_EMPTY_REPOS = True

class FileStorage(storage.Storage):
	"""
	Storage based on files
	"""

	# Dictionary "ontology_id" -> dictionary with keys:
	#	'birda': birda instance file
	#   'repos': ontology instances file
	ontologies = {}

	# ----------------------------------------------------------------------- #

	def __init__(self, prj_path):
		self.prj_path = prj_path
		self.catalog_path = os.path.abspath( self.prj_path + os.path.sep + 'catalog' )
		self.birda_catalog_path = self.catalog_path + os.sep + 'birda'
		self.repos_catalog_path = self.catalog_path + os.sep + 'ontologies'

		# Initialize catalog
		self.reload_available_ontologies_catalog()

	# ----------------------------------------------------------------------- #

	def reload_available_ontologies_catalog(self):

		def get_basename(file_path):
			return os.path.splitext( os.path.basename(file_path) )[0]

		def get_extension(file_path):
			return os.path.splitext( os.path.basename(file_path) )[1]

		self.ontologies = {}

		birda_files = os.listdir(self.birda_catalog_path)
		repos_files = os.listdir(self.repos_catalog_path)
		for birda_file in birda_files:
			onto_id = get_basename(birda_file)

			repos_file = ''
			for r_file in repos_files:
				if get_basename(r_file) == onto_id:
					repos_file = r_file
					break

			if CREATE_EMPTY_REPOS:
				if not repos_file:
					repos_file = onto_id + get_extension(birda_file)
					repos_file_path = self.catalog_path + os.sep + 'ontologies' + os.sep + repos_file
					print "Creating %(repos_file_path)s" % vars()
					f = open(repos_file_path,'w')
					f.close()

			if repos_file:
				self.ontologies[onto_id] = {
					'birda': self.catalog_path + os.sep + 'birda' + os.sep + birda_file,
					'repos': self.catalog_path + os.sep + 'ontologies' + os.sep + repos_file,
				}

		print pprint.pformat( self.ontologies )

	# ----------------------------------------------------------------------- #

	def get_birda_instances(self):
		instances = {}

		for onto_id in self.ontologies.keys():
			rdf = rdflib.Graph()
			instances[onto_id] = rdf.load(self.ontologies[onto_id]['birda'])

		return instances

# ================================================================================================ #

if __name__ == '__main__':
	prj_path = os.path.dirname( os.path.realpath(__file__) ) + "/../.."
	storage = FileStorage(prj_path)
	print storage.get_birda_instances()