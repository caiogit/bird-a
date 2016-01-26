#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import time
import rdflib
import birda.utils.lock

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
	
	writed = False
	
	# ----------------------------------------------------------------------- #
	
	def __init__(self, settings, dataset='', namespaces={}, verbose=False):
		assert dataset in ('birda','indiv')
		
		self.settings = settings
		self.dataset = dataset
		self.namespaces = namespaces
		
		self.verbose = verbose
		
		self.rdf = rdflib.Graph()
		
		# Determines the database file name and format
		if dataset == 'birda':
			self.db_file = settings['birda_storage_file_birda_db']
		elif dataset == 'indiv':
			self.db_file = settings['birda_storage_file_indiv_db']
		else:
			raise NotImplementedError("")
		
		self.db_format = self.db_file.split('.')[-1]
		
		# Acquires the lock
		self.lock = birda.utils.lock.wait_for_lock(self.db_file, max_sleep=0.2)
		
		# Load the file
		self.rdf.load(self.db_file, format=self.db_format)

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
		
		self.writed = True
		
		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #
	
	def commit(self):
		"""
		Commits updates and deletes to db

		:return: None
		"""
		
		# Write changes (if any) to file
		if self.writed:
			rdf.serialize(self.db_file, format=self.db_format)
	
	# ----------------------------------------------------------------------- #
	
	def rollback(self):
		"""
		Rollback updates and deletes and restore the initial status

		:return: None
		"""
		
		# Reload the file
		self.rdf.load(db_file, format=self.db_format)
	
	# ----------------------------------------------------------------------- #
	
	def close(self):
		"""
		Close the connection

		:return: None
		"""
		
		# The changes are automatically discarded, so rollback is not necessary 
		#self.rollback()
		
		# Release the acquired lock on the file
		birda.utils.lock.release_lock(self.lock)
		self.lock = None
		

# ================================================================================================ #

if __name__ == '__main__':
	bConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='birda', verbose=True)
	results = bConn.query("""
	select ?s ?p ?o
	where {
		?s ?p ?o
	}
	""")
	time.sleep(20)
	bConn.close()
	