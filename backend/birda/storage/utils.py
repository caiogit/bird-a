#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 25/01/16.
"""

import rdflib
import __init__ as storage

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

# ---------------------------------------------------------------------------- #

def get_types(conn, subject_uri):
	"""
	Get individual classes (related with rdf:type)
	
	:param conn: 
	:param subject_uri: 
	:return: List of URIRef
	"""
	
	return []

# ---------------------------------------------------------------------------- #

def get_property(conn, subject_uri, property_uri):
	"""
	Get property value for the given subject
	
	:param conn: 
	:param subject_uri: 
	:param property_uri:
	:return: Property value or None if the property was not set for the subject
	"""
	
	return None

# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
	print '-------------------------------------'
	test_prettify(rdflib.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'))
	test_prettify(rdflib.term.URIRef(u'http://w3id.org/ontologies/bird-a/atLeast'))
	test_prettify(rdflib.term.Literal(u'-'))
	test_prettify(rdflib.term.Literal(u'Used to insert FOAF:Person attributes', lang=u'en'))
	test_prettify(rdflib.term.Literal(u'http://pippo.it/target-data/', datatype=rdflib.term.URIRef(u'http://www.w3.org/2001/XMLSchema#anyURI')))
	test_prettify(rdflib.term.Literal(u'1', datatype=rdflib.term.URIRef(u'http://www.w3.org/2001/XMLSchema#integer')))
	print '-------------------------------------'
	print
	print '-------------------------------------'
	print '-------------------------------------'
	