#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import os
import time
import rdflib
import birda.utils.lock

import birda.bModel.ontology as ontology
import __init__ as storage

# ============================================================================ #

class FileConnection(storage.Connection):
	
	rdf = None
	settings = {}
	dataset = ''
	namespaces = {}
	
	verbose = False
	
	db_file = ''
	db_format = ''
	lock = None
	
	written = False
	
	# ----------------------------------------------------------------------- #
	
	def __init__(self, settings, dataset='', namespaces={}, verbose=False):
		assert dataset in ('birda','indiv','test')
		
		self.settings = settings
		self.dataset = dataset
		self.namespaces = namespaces
		
		self.verbose = verbose
		
		self.rdf = ontology.new_rdf_Graph()
				
		# Determines the database file name and format
		if dataset == 'birda':
			self.db_file = settings['birda.storage_file_birda_db']
		elif dataset == 'indiv':
			self.db_file = settings['birda.storage_file_indiv_db']
		elif dataset == 'test':
			self.db_file = settings['birda.storage_file_test_db']
		else:
			raise NotImplementedError("")
		
		self.db_format = self.db_file.split('.')[-1]
		
		# Acquires the lock
		self.lock = birda.utils.lock.wait_for_lock(self.db_file, max_sleep=0.2)
		
		# Creates the file if it doesn't exist
		if not os.path.isfile(self.db_file):
			f = open(self.db_file,'w')
			f.close()
		
		# Load the file
		self.rdf.load(self.db_file, format=self.db_format)

	# ----------------------------------------------------------------------- #
	
	def query(self, query):
		"""
		Exectutes a read-only sparql query

		:return: Result object
		"""
		
		if self.verbose:
			storage.Results.printQuery(query)
		
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
		
		self.written = True
		
		if self.verbose:
			storage.Results.printQuery(query)
		
		start_time = time.time()
		results = self.rdf.update(query, initNs=self.namespaces)
		elapsed_time = time.time() - start_time
		
		bResults = storage.Results(query, results, elapsed_time, namespaces=self.namespaces)
		
		if self.verbose:
			bResults.printQueryResults()
		
	# ----------------------------------------------------------------------- #
	
	def commit(self):
		"""
		Commits updates and deletes to db

		:return: None
		"""
		
		# Write changes (if any) to file
		if self.written:
			self.rdf.serialize(self.db_file, format=self.db_format)
			self.written = False
	
	# ----------------------------------------------------------------------- #
	
	def rollback(self):
		"""
		Rollback updates and deletes and restore the initial status

		:return: None
		"""
		
		# Reload the file
		self.rdf = ontology.new_rdf_Graph()
		self.rdf.load(self.db_file, format=self.db_format)
		self.written = False
	
	# ----------------------------------------------------------------------- #
	
	def close(self):
		"""
		Close the connection

		:return: None
		"""
		
		# The changes are automatically discarded, so explicit rollback is not necessary 
		#self.rollback()
		
		# Release the acquired lock on the file
		birda.utils.lock.release_lock(self.lock)
		self.lock = None
		

# ================================================================================================ #

if __name__ == '__main__':
	tConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='test', verbose=True)
	tConn.update("""
	INSERT DATA {
		<birda:pippetto> birda:hasLabel "foo"@it .
	}
	""")
	tConn.update("""
	INSERT DATA {
		<birda:pippetto> birda:hasLabel "foo" .
	}
	""")
	tConn.update("""
	DELETE DATA {
		<birda:pippetto> birda:hasLabel "foo"@it .
	}
	""")
	tConn.commit()
	results = tConn.query("select ?s ?p ?o where { ?s ?p ?o }")
	tConn.close()