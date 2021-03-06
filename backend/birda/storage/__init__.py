#!/usr/bin/env python
# -*- coding: utf-8 -*-

# References:
# - Static and abstract methods: https://julien.danjou.info/blog/2013/guide-python-static-class-abstract-methods
# - Singletons in Python: http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python?rq=1
# - Lock acquisition with a decorator: http://stackoverflow.com/questions/489720/what-are-some-common-uses-for-python-decorators/490090#490090
# - Python thread synchronization guide: http://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import os
import abc
import rdflib
import birda.utils.ascii_utils
import utils

import birda.bModel as bModel
import birda.bModel.ontology as ontology

# --------------------------------- #

SUPPORTED_OUTPUT_TYPES = ['triples', 'xml', 'n3', 'turtle', 'nt', 'pretty-xml']

# "Fake settings" for testing purpose
FAKE_DB_PATH = os.path.dirname( os.path.realpath(__file__) ) + "/../../../db"
FAKE_SETTINGS = {
	'birda.storage_type': 'file',
	'birda.storage_file_birda_db': FAKE_DB_PATH + '/birda.turtle',
	'birda.storage_file_indiv_db': FAKE_DB_PATH + '/indiv.turtle',
	'birda.storage_file_test_db': FAKE_DB_PATH + '/test.turtle',
}

# ============================================================================ #

class Results(object):
	"""
	Wrapper for sparql_results who provides some utility features
	"""

	query = ""
	sparql_results = []
	elapsed_time = 0.0
	
	namespaces = {}

	# ----------------------------------------------------------------------- #

	def __init__(self, query, sparql_results, elapsed_time, namespaces={}):
		self.query = query
		self.sparql_results = sparql_results
		self.elapsed_time = elapsed_time
		self.namespaces = namespaces

	# ----------------------------------------------------------------------- #
	
	def getFields(self):
		return [str(k) for k in self.sparql_results.vars]
	
	# ----------------------------------------------------------------------- #
		
	def getDictList(self):
		"""
		Get a list of dictionaries which keys are strings and values are
		RDFLib object

		:return: List of dictionaries
		"""
		
		l = []
		for res in self.sparql_results.bindings:
			d = {}
			for k in self.getFields():
				d[str(k)] = res[k]
				
			l += [ d ]
		
		return l

	# ----------------------------------------------------------------------- #

	def getPrettyDictList(self):
		"""
		Get a list of dictionaries which keys are strings and values are
		pretty_urls, strings, ints and dates

		:return: List of dictionaries
		"""
		
		# Order namespaces from longest to shortest (in order to match first
		# full path instead of partial path) 
		namespaces_ordered_keys = sorted(self.namespaces.keys(), (lambda x,y: len(x)-len(y)), reverse=True )
		
		l = []
		for res in self.sparql_results.bindings:
			d = {}
			for k in self.getFields():
				d[str(k)] = utils.prettify(res[k], namespaces=self.namespaces, namespaces_ordered_keys=namespaces_ordered_keys)
				
			l += [ d ]
		
		return l

	# ----------------------------------------------------------------------- #

	def printQueryResults(self):
		"""
		Print query results in a MySQL ascii tab fashion

		:return: None
		"""
		
		if self.sparql_results != None:
			print birda.utils.ascii_utils.render_list_dict( self.getPrettyDictList(), map=self.getFields() ) ,
			print "%s rows in set (%s sec)" % ( len(self.getPrettyDictList()), birda.utils.ascii_utils.hhmmss(self.elapsed_time,tutto=False) )
		else:
			print "Updated (%s sec)" % birda.utils.ascii_utils.hhmmss(self.elapsed_time,tutto=False)
		print
	
	# ----------------------------------------------------------------------- #
	
	@staticmethod
	def printQuery(query, lines_number=False):
		query_rows = query.replace('\t','  ').split('\n')
		
		if lines_number:
			# Little ugly function of convenience
			def ln(s):
				ln.n += 1
				return "%2s   %s" % (ln.n, s)
			ln.n = 0
			
			query = "\n".join([ ln(r) for r in query_rows if r.strip() ])
		
		else:
			query = "\n".join([ r for r in query_rows if r.strip() ])
		
		print '===================================='
		print query
		print '===================================='
		
# ============================================================================ #

class Connection(object):
	"""
	Abstract object wrapping all functionalities relative to db interaction.
	"""

	__metaclass__  = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self, settings, dataset='', namespaces={}, verbose=False):
		pass

	@abc.abstractmethod
	def query(self, query):
		"""
		Exectutes a read-only sparql query

		:return: Result object
		"""

		raise NotImplementedError("This method should be implemented by subclasses")

	# ----------------------------------------------------------------------- #

	@abc.abstractmethod
	def update(self, query):
		"""
		Exectutes a write-only sparql query

		:return: ???
		"""

		raise NotImplementedError("This method should be implemented by subclasses")
	
	# ----------------------------------------------------------------------- #
	
	@abc.abstractmethod
	def commit(self):
		"""
		Commits updates and deletes to db

		:return: None
		"""
		
		raise NotImplementedError("This method should be implemented by subclasses")
	
	# ----------------------------------------------------------------------- #
	
	@abc.abstractmethod
	def rollback(self):
		"""
		Rollback updates and deletes and restore the initial status

		:return: None
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

class RDFWrapper(object):
	"""
	Object that wraps rdflib.Graph object.
	
	It is intended to accumulate rdf statements and dump them in several
	formats.
	"""
	
	rdf = None
	
	# ----------------------------------------------------------------------- #
	
	def __init__(self):
		self.rdf = ontology.new_rdf_Graph()
	
	# ----------------------------------------------------------------------- #
	
	def add(self, s, p, o):
		"""
		Add the rdf statement to the rdf container
		
		:param s: subject of the rdf statement
		:param p: predicate of the rdf statement
		:param o: object of the rdf statement
		:return: None
		"""
		
		assert type(s) in (type(''),type(u'')) or type(s) == type(rdflib.term.URIRef(''))
		assert type(p) in (type(''),type(u'')) or type(p) == type(rdflib.term.URIRef(''))
		
		if type(s) in (type(''),type(u'')):
			s = rdflib.term.URIRef(s)
		if type(p) in (type(''),type(u'')):
			p = rdflib.term.URIRef(p)
		
		o = utils.py2rdf(o)
		
		self.rdf.add((s,p,o))
		
	# ----------------------------------------------------------------------- #
	
	def dumps(self, output_format):
		"""
		Dump the rdf graph into a string
		
		:param output_format: Format of the dumped rdf
		:return: String rapresentation of the rdf graph
		"""
		
		assert output_format in SUPPORTED_OUTPUT_TYPES
		
		return self.rdf.serialize(format=output_format)
		

# ============================================================================ #

class Storage(object):
	"""
	Storage abstract class
	"""

	# ----------------------------------------------------------------------- #

	def __init__(self):
		raise NotImplementedError("Storage should not be instantiated")

	# ----------------------------------------------------------------------- #

	@staticmethod
	def connect(settings, dataset='', namespaces=bModel.NAMESPACES, verbose=False):
		"""
		Creates a connection to a sparql endpoint using "setting" parameters

		:return: Connection object (sublass of storage.Connection)
		"""

		if settings['birda.storage_type'] == 'file':
			import file_storage
			return file_storage.FileConnection(settings, dataset=dataset, namespaces=namespaces, verbose=verbose)
		else:
			raise NotImplementedError("Storage type unknown")

# ================================================================================================ #

if __name__ == '__main__':
	storage = Storage()