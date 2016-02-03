#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import json
import rdflib
import birda.bModel as bModel
import __init__ as storage

from rdflib.namespace import RDF, RDFS, XSD
from birda.bModel import CO, BIRDA, BINST, TINST

from birda.utils.generic import is_uri

# ============================================================================ #

def rdf2py(value):
	"""
	Convert the passed rdflib object in a classic python value.
	Refers to this tab: http://rdflib.readthedocs.org/en/latest/rdf_terms.html#python-support
	
	:param value: rdflib object
	:return: python object
	"""
	
	if type(value) == type(rdflib.term.URIRef(u'')):
		# URIRef
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

def rdf2sparql(element, lang=None):
	
	if type(element) == type(rdflib.term.URIRef('')):
		return "<%s>" % element
		
	if type(element) != type(rdflib.term.Literal('')):
		element = rdflib.term.Literal(element, lang=lang)
		
	if element.datatype:
		datatype = str(element.datatype).split('#')[-1]
		return '"%s"^^xsd:%s' % (element.value, datatype)
	else:
		if element.language:
			return '"%s"@%s' % (element.value, element.language)
		else:
			return '"%s"' % (element.value)
	
# ---------------------------------------------------------------------------- #

def py2rdf(value, force='', lang=None):
	"""
	Convert the passed python object in the relative rdf counterpart.
	Refers to this tab: http://rdflib.readthedocs.org/en/latest/rdf_terms.html#python-support
	
	:param value: python object
	:param force: force interpretation to specified type.
		Allowed types: 'uri'
	:param lang: 
	:return: rfdlib object
	"""
	
	assert (not force) or (force in ['uri', 'any_uri'])
	
	if type(value) in [type(rdflib.term.URIRef(u'')), type(rdflib.term.Literal(u''))]:
		return value
	
	if force == 'any_uri':
		return rdflib.term.Literal(value,datatype=XSD.anyURI)
	
	if force == 'uri' or is_uri(value):
		return rdflib.term.URIRef(value)
	
	return rdflib.term.Literal(value, lang=lang)
	
# ---------------------------------------------------------------------------- #

def prettify(element, 
			 namespaces=bModel.NAMESPACES, 
			 namespaces_ordered_keys=bModel._NAMESPACES_ORDERED_KEYS):
	"""
	Prettify an RDF element for human readability
	
	:param element: RDF element or uri string to process
	:param namespaces: optional namespaces list
	:param namespaces_ordered_keys: namespaces keys ordered by priority in evaluation
	:return: prettified string
	"""
	
	if type(element) in [ type(''), type(u''), type(rdflib.term.URIRef('')) ]:
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

def get_types(conn, subject_uri, lexical=False, rdfw=None):
	"""
	Get individual classes (related with rdf:type)
	
	:param conn: 
	:param subject_uri: 
	:param lexical: If true the original rdflib object is returned, otherwise
		the best python object that fits the type is returned
	:return: List of URIRef
	"""

	values = get_property(conn, subject_uri, getattr(RDF,'type'), lexical=lexical, rdfw=rdfw)
	
	if lexical:
		return values
	else:
		return [ rdf2py(v) for v in values ]

# ---------------------------------------------------------------------------- #

def get_property(conn, subject_uri, property_uri, lexical=False, rdfw=None, single=False):
	"""
	Get property value for the given subject
	
	:param conn: RDF connection
	:param subject_uri: 
	:param property_uri: 
	:param lexical: If true the original rdflib object is returned, otherwise
		the best python object that fits the type is returned
	:param rdfw: RDFWrapper object
	:param single: if True returns a single value or None if not present, if False an array
	:return: List of values relative to this property
	"""
	
	results = conn.query("""
	select ?value
	where {{
		<{subject_uri}> <{property_uri}> ?value
	}}
	""".format(**vars()))
	
	dlist = results.getDictList()
	
	if rdfw:
		for d in dlist:
			rdfw.add(subject_uri, property_uri, d['value'])
	
	if lexical:
		ret = [ d['value'] for d in dlist ]
	else:
		ret = [ rdf2py(d['value']) for d in dlist ]
	
	if single:
		if len(ret) > 1:
			raise Exception('Error! Found more than one value (vars: %s)' % vars())
		if ret:
			ret = ret[0]
		else:
			ret = None
	
	return ret

# ---------------------------------------------------------------------------- #

def get_all_properties(conn, subject_uri, lexical=False, rdfw=None):
	"""
	Get all properties relative to a subject
	
	:param conn: RDF connection
	:param subject_uri: 
	:param lexical: If true the original rdflib object is returned, otherwise
		the best python object that fits the type is returned
	:param rdfw: RDFWrapper object
	:return: Dictionary property -> list of values
	"""
	
	results = conn.query("""
	select ?property ?value
	where {{
		<{subject_uri}> ?property ?value
	}}
	""".format(**vars()))
	
	dlist = results.getDictList()
	
	if rdfw:
		for d in dlist:
			rdfw.add(subject_uri, d['property'], d['value'])
	
	# Build property dictionary
	p_dict = {}
	for d in dlist:
		if lexical:
			key = d['property']
			value = d['value']
		else:
			key = rdf2py(d['property'])
			value = rdf2py(d['value'])
		
		if not p_dict.has_key(key):
			p_dict[key] = []
		
		p_dict[key] += [ value ]
		
	
	return p_dict

# ---------------------------------------------------------------------------- #

def get_co_list(conn, list_node, rdfw=None):
	"""
	Get uri elements of a co:List
	
	:param conn: RDF connection
	:param list_node: URI of the co:List element
	:param rdfw: Object RDFWrapper
	
	:return: List of string URIs
	"""
	
	el_list = []
	
	current_element = get_property(conn, list_node, CO.firstItem, rdfw=rdfw, single=True)
	
	while current_element != None:
		elem = get_property(conn, current_element, CO.itemContent, rdfw=rdfw, single=True)
		if not elem:
			raise ValueError('Elemento non trovato! (%s)' % vars())
		el_list += [elem]
		
		current_element = get_property(conn, current_element, CO.nextItem, rdfw=rdfw, single=True)
			
	# Not useful, it onlty populates rdfw
	if rdfw:
		current_element = get_property(conn, list_node, CO.item, rdfw=rdfw)
	
	return el_list

# ============================================================================ #

# Refer to: http://stackoverflow.com/questions/19502398/sparql-update-example-for-updating-more-than-one-triple-in-a-single-query

def insert_triple(conn, subject_uri, property_uri, value, lang=None):
	
	value = rdf2sparql(value, lang=lang)
	
	conn.update("""
	INSERT DATA {{
		<{subject_uri}> <{property_uri}> {value} .
	}}
	""".format(**vars()))

# ---------------------------------------------------------------------------- #

def delete_triple(conn, subject_uri, property_uri, value, lang=None):
	
	value = rdf2sparql(value, lang=lang)
	
	conn.update("""
	DELETE DATA {{
		<{subject_uri}> <{property_uri}> {value} .
	}}
	""".format(**vars()))

# ---------------------------------------------------------------------------- #

def update_triple(conn, subject_uri, property_uri, old_value, new_value, lang=None):
	delete_triple(conn, subject_uri, property_uri, old_value, lang=lang)
	insert_triple(conn, subject_uri, property_uri, new_value, lang=lang)

# ---------------------------------------------------------------------------- #

def delete_all_triples(conn, subject_uri):
	
	conn.update("""
	DELETE  {{
		<{subject_uri}> ?p ?o
	}}
	WHERE {{ 
		<{subject_uri}> ?p ?o. 
	}}
	""".format(**vars()))

	
# ============================================================================ #

def get_by_lang(lit_list, lang, loose=False):
	"""
	Finds the occurrence of <lang> in the specified literals list
	
	:param lit_list: Literals list
	:param lang: Language in 2 chars iso format
	:param loose: tell the function to try to search for something else if
		it doesn't find the input lang
	:return: Found Literal, a default Literal or Literal('') if no literals were present
	"""
	
	if not lit_list:
		# If there is nothing to return, returns ''
		return rdflib.term.Literal('')
	
	default1 = None
	default2 = None
	for l in lit_list:
		assert type(l) == type(rdflib.term.Literal(''))
		
		if l.language == lang:
			# If lang was found, returns it
			return l
		elif l.language == 'en':
			default1 = l
		elif l.language == None:
			default2 = l
	
	if loose:
		if default1:
			# If lang was not found, return english
			return default1
		elif default2:
			# If lang was not found, return the literal without language informations
			return default2
		else:
			# If even english was not found, return the first available
			return lit_list[0]
	else:
		return rdflib.term.Literal('')

# ---------------------------------------------------------------------------- #

def get_by_lang_mul(lit_list, lang):
	"""
	Finds the occurrences of <lang> in the specified Literal or URIRef list
	
	:param lit_list: Literals or URIRef list
	:param lang: Language in 2 chars iso format
	:return: List of found Literals with specified language or, if no one match
		that language, a list of literals without any language information
	"""
	
	lang_list = []
	neutral_list = []

	for l in lit_list:
		assert type(l) in [ type(rdflib.term.Literal('')), type(rdflib.term.URIRef('')) ]
		
		if (type(l) == type(rdflib.term.Literal(''))) and (l.language == lang):
			lang_list += [ l ]
		
		if (type(l) == type(rdflib.term.URIRef(''))) or (l.language == None):
			neutral_list += [ l ]
	
	if lang_list:
		return lang_list
	else:
		return neutral_list

# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
	bConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='birda', verbose=True)
	iConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='indiv', verbose=True)
	tConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='test', verbose=True)
	
# 	print '-------------------------------------'
# 	test_prettify(rdflib.URIRef(u'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'))
# 	test_prettify(rdflib.term.URIRef(u'http://w3id.org/ontologies/bird-a/atLeast'))
# 	test_prettify(rdflib.term.Literal(u'-'))
# 	test_prettify(rdflib.term.Literal(u'Used to insert FOAF:Person attributes', lang=u'en'))
# 	test_prettify(rdflib.term.Literal(u'http://pippo.it/target-data/', datatype=rdflib.term.URIRef(u'http://www.w3.org/2001/XMLSchema#anyURI')))
# 	test_prettify(rdflib.term.Literal(u'1', datatype=rdflib.term.URIRef(u'http://www.w3.org/2001/XMLSchema#integer')))
# 	print '-------------------------------------'
# 	print
# 	
# 	values = get_property(bConn, getattr(BINST,'PersonLight-Form'), getattr(rdflib.namespace.RDF,'type'), lexical=True)
# 	print '-------------------------------------'
# 	print values
# 	print '-------------------------------------'
# 	print
# 	
# 	types = get_types(bConn, getattr(BINST,'PersonLight-Form'), lexical=True)
# 	print '-------------------------------------'
# 	print types
# 	print '-------------------------------------'
# 	print
# 	
# 	properties = get_all_properties(iConn, getattr(TINST, 'pierluigi-mariuolo'), lexical=False, rdfw=None)
# 	print '-------------------------------------'
# 	print json.dumps(properties, indent=4)
# 	print '-------------------------------------'
# 	print
# 	
# 	el_list = get_co_list(bConn, getattr(BINST,'PersonLight-Form'), rdfw=None)
# 	print '-------------------------------------'
# 	for el in el_list: print el
# 	print '-------------------------------------'
# 	print
	
	insert_triple(tConn, TINST.provolo, BIRDA.hasLabel, 'asd', lang='it')
	update_triple(tConn, TINST.provolo, BIRDA.hasLabel, 'asd', 'masd', lang='it')
	delete_triple(tConn, TINST.provolo, BIRDA.hasLabel, 'asd', lang='it')
	tConn.commit()
	tConn.close()
	
	