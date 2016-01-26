#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import rdflib
import __init__ as storage
from rdflib.namespace import RDF, RDFS, XSD

# ============================================================================ #

def rdf2py(value):
	"""
	Convert the passed rdflib object in a classic python value.
	Refers to this tab: http://rdflib.readthedocs.org/en/latest/rdf_terms.html#python-support
	
	:param value: rdflib object
	:return: python object
	"""
	
	# URIRef
	if type(value) == type(rdflib.term.URIRef(u'')):
		return unicode(value)
	
	if type(value) == type(rdflib.term.Literal(1)):
		# String
		if (value.datatype == None or
		    value.datatype == XSD.string):
			return unicode(value)
		
		# Long
		if (value.datatype == XSD.integer or
		    value.datatype == XSD.int):
			return long(value)
		
		raise ValueError('Datatype "%s" not supported!' % value.datatype)
	
	if type(value) in ( type(''), type(u'') ):
		return value
	
	raise ValueError('Object "%s" not supported!' % type(value))

# ---------------------------------------------------------------------------- #

def py2rdf(value):
	"""
	Convert the passed python object in the relative rdf counterpart.
	Refers to this tab: http://rdflib.readthedocs.org/en/latest/rdf_terms.html#python-support
	
	:param value: python object
	:return: rfdlib object
	"""
	
	if type(value) in [type(rdflib.term.URIRef(u'')), type(rdflib.term.Literal(u''))]:
		return value
	
	return rdflib.term.Literal(value)
	
# ---------------------------------------------------------------------------- #

def prettify(element, 
			 namespaces=storage.NAMESPACES, 
			 namespaces_ordered_keys=storage._NAMESPACES_ORDERED_KEYS):
	"""
	Prettify an RDF element for human readability
	
	:param element: RDF element or uri string to process
	:param namespaces: optional namespaces list
	:param namespaces_ordered_keys: namespaces keys ordered by priority in evaluation
	:return: prettified string
	"""
	
	if type(element) == type(rdflib.term.URIRef('')):
		uri = str(element)
		
		# Namespaces substitution
		for ns in namespaces_ordered_keys:
			if uri.startswith(str(namespaces[ns])):
				uri = uri.replace(str(namespaces[ns]), ns+':')
				break
		
		return '<'+uri+'>'
	
	else:
		if element.datatype:
			datatype = str(element.datatype).split('#')[-1]
			return "%s^^%s" % (element.value, datatype)
		else:
			if element.language:
				return '"%s"@%s' % (element.value, element.language)
			else:
				return '"%s"' % (element.value)

# --------------------------------- #

def test_prettify(element):
	print "%r -> %s" % (element,prettify(element))

# ============================================================================ #

def get_types(conn, subject_uri, lexical=False):
	"""
	Get individual classes (related with rdf:type)
	
	:param conn: 
	:param subject_uri: 
	:param lexical: If true the original rdflib object is returned, otherwise
		the best python object that fits the type is returned
	:return: List of URIRef
	"""

	values = get_property(conn, subject_uri, getattr(storage.RDF,'type'), lexical=lexical)
	
	if lexical:
		return values
	else:
		return [ rdf2py(v) for v in values ]

# ---------------------------------------------------------------------------- #

def get_property(conn, subject_uri, property_uri, lexical=False):
	"""
	Get property value for the given subject
	
	:param conn: 
	:param subject_uri: 
	:param property_uri:
	:param lexical: If true the original rdflib object is returned, otherwise
		the best python object that fits the type is returned
	:return: List of values relative to this property
	"""
	
	results = conn.query("""
	select ?value
	where {{
		<{subject_uri}> <{property_uri}> ?value
	}}
	""".format(**vars()))
	
	dlist = results.getDictList()
	
	if lexical:
		return [ d['value'] for d in dlist ]
	else:
		return [ rdf2py(d['value']) for d in dlist ]
	

# ---------------------------------------------------------------------------- #

def test_classes():
	
	class A(object):
		a = 1
		c = 1
		def get_a(self):
			print self.a
		def get_c(self):
			print self.c
		def set_c(self):
			print "A.set_c"
			self.c = c*10
	
	class B(A):
		b = 2
		c = 3
		def get_b(self):
			print self.b
		def set_c(self):
			print "B.set_c"
			self.c = self.c*100
			#super(A,self).c = super(A,self).c*100
	
	b = B()
	b.get_a()
	b.get_b()
	print dir(b)
	b.a = 4
	b.get_a()
	print dir(b)
	b.get_c()
	b.set_c()
	b.get_c()
	print dir(super(A,b))
	super(A,b).get_c()
	super(A,b).set_c()
	super(A,b).get_c()

# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
	bConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='birda', verbose=True)
	iConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='indiv', verbose=True)
	
	print '-------------------------------------'
	test_prettify(rdflib.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'))
	test_prettify(rdflib.term.URIRef(u'http://w3id.org/ontologies/bird-a/atLeast'))
	test_prettify(rdflib.term.Literal(u'-'))
	test_prettify(rdflib.term.Literal(u'Used to insert FOAF:Person attributes', lang=u'en'))
	test_prettify(rdflib.term.Literal(u'http://pippo.it/target-data/', datatype=rdflib.term.URIRef(u'http://www.w3.org/2001/XMLSchema#anyURI')))
	test_prettify(rdflib.term.Literal(u'1', datatype=rdflib.term.URIRef(u'http://www.w3.org/2001/XMLSchema#integer')))
	print '-------------------------------------'
	print
	
	values = get_property(bConn, getattr(storage.BINST,'PersonLight-Form'), getattr(storage.RDF,'type'), lexical=True)
	print '-------------------------------------'
	print values
	print '-------------------------------------'
	print
	
	types = get_types(bConn, getattr(storage.BINST,'PersonLight-Form'), lexical=True)
	print '-------------------------------------'
	print types
	print '-------------------------------------'
	print
	
	test_classes()

	