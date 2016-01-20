#!/usr/bin/env python
# -*- coding: utf-8 -*-

# References:
# - Static and abstract methods: https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods
# - Singletons in Python: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python?rq=1
# - Lock acquisition with a decorator: http://stackoverflow.com/questions/489720/what-are-some-common-uses-for-python-decorators/490090#490090
# - Python thread synchronization guide: http://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/

import rdflib
import abc

NAMESPACES = {
	'rdf': rdflib.namespace.RDF,
	'rdfs': rdflib.namespace.RDFS,
	'xsd': rdflib.namespace.XSD,
	'foaf': rdflib.namespace.FOAF,
	'skos': rdflib.namespace.SKOS,
	'co': rdflib.Namespace("http://purl.org/co/"),
	'birda': rdflib.Namespace("http://w3id.org/ontologies/bird-a/"),
	'binst': rdflib.Namespace("http://pippo.it/birda-data/"),
	'tinst': rdflib.Namespace("http://pippo.it/target-data/")
}

# ============================================================================ #

class Results(object):
	"""
	Wrapper for sparql_results who provides some utility features
	"""

	query = ""
	sparql_results = []

	# ----------------------------------------------------------------------- #

	def __init__(self, query, sparql_results):
		self.query = query
		self.sparql_results = sparql_results

	# ----------------------------------------------------------------------- #

	def getDictList(self):
		"""
		Get a list of dictionaries which keys are strings and values are
		RDFLib object

		:return: List of dictionaries
		"""

		return self.sparql_results.bindings

	# ----------------------------------------------------------------------- #

	def getSimpleDictList(self):
		"""
		Get a list of dictionaries which keys are strings and values are
		strings, ints and dates

		:return: List of dictionaries
		"""

		# TODO
		pass

	# ----------------------------------------------------------------------- #

	def printQueryResults(self):
		"""
		Print query results in a MySQL ascii tab fashion

		:return: None
		"""

		# TODO

# ============================================================================ #

class Connection(object):
	__metaclass__  = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self, settings, dataset='', namespaces={}):
		pass

	@abc.abstractmethod
	def sparql_query(self, query):
		"""
		Exectutes a read-only sparql query

		:return: Result object
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	@abc.abstractmethod
	def sparql_update(self, query):
		"""
		Exectutes a write-only sparql query

		:return: ???
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	@abc.abstractmethod
	def close(self):
		"""
		Close the connection

		:return: None
		"""
		raise NotImplementedError("This method should be implemented by subclasses")

# ============================================================================ #

class Storage(object):
	"""
	Storage abstract class

	"""

	# ----------------------------------------------------------------------- #

	def __init__(self):
		pass

	# ----------------------------------------------------------------------- #

	@staticmethod
	def connect(settings, dataset='', namespaces=NAMESPACES):
		"""
		Creates a connection to a sparql endpoint using "setting" parameters

		:return: Connection object (sublass of storage.Connection)
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

# ================================================================================================ #

if __name__ == '__main__':
	storage = Storage()