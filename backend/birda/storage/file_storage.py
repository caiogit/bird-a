#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import rdflib
import storage
import pprint

# ============================================================================ #

class FileConnection(object):

	def __init__(self, settings, dataset='', namespaces={}):
		pass

	def sparql_query(self, query):
		"""
		Exectutes a read-only sparql query

		:return: Result object
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	def sparql_update(self, query):
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
	prj_path = os.path.dirname( os.path.realpath(__file__) ) + "/../.."
	storage = FileStorage(prj_path)
	print storage.get_birda_instances()