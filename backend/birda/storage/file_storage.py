#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import rdflib
import pprint

import __init__ as storage

# ============================================================================ #

class FileConnection(storage.Connection):
	
	rdf = None
	settings = {}
	dataset = ''
	namespaces = {}
	
	verbose = False
	
	def __init__(self, settings, dataset='', namespaces={}, verbose=False):
		assert dataset in ('birda','indiv')
		
		self.settings = settings
		self.dataset = dataset
		self.namespaces = namespaces
		
		self.verbose = verbose
		
		self.rdf = rdflib.Graph()
		
		if dataset == 'birda':
			db_file = settings['birda_storage_file_birda_db']
			db_format = db_file.split('.')[-1]
			self.rdf.load(db_file, format=db_format)
		elif dataset == 'indiv':
			db_file = settings['birda_storage_file_indiv_db']
			db_format = db_file.split('.')[-1]
			self.rdf.load(db_file, format=db_format)
		else:
			raise NotImplementedError("")

	# ----------------------------------------------------------------------- #
	
	def query(self, query):
		"""
		Exectutes a read-only sparql query

		:return: Result object
		"""
		
		start_time = time.time()
		results = self.rdf.query(query, initNs=self.namespaces)
		elapsed_time = time.time() - start_time
		
		bResults = storage.Results(query, results, elapsed_time, namespaces=self.namespaces)
		
		if self.verbose:
			bResults.printQueryResults()
		
		return bResults
		
	# ----------------------------------------------------------------------- #

	def update(self, query):
		"""
		Exectutes a write-only sparql query

		:return: ???
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	def close(self):
		"""
		Close the connection

		:return: None
		"""
		raise NotImplementedError("This method should be implemented by subclasses")

# ================================================================================================ #

if __name__ == '__main__':
	bConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='birda', verbose=True)
	results = bConn.query("""
	select ?s ?p ?o
	where {
		?s ?p ?o
	}
	""")