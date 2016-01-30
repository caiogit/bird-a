#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals

str = unicode
# -------------------------------------- #

import os
import hashlib
import rdflib
import random
import string
import math

from rdflib import Literal, URIRef

import __init__ as bModel
from __init__ import NAMESPACES, RDF, RDFS, XSD, CO, B_HAS_BASE_NAME_LIST

# ============================================================================ #

def int2base(n, base):
	chr_list = string.digits + string.lowercase + string.uppercase
	l = [ chr_list[(n/base**i)%base] for i in xrange(int(math.log(n, base)), -1, -1) ]
	return ''.join(l)

def	create_id(s, length=6):
	h = hashlib.md5()
	h.update(str(s))
	return h.hexdigest()[:length]

def	create_random_id(length=6):
	chr_range = string.digits + string.lowercase
	base = len(chr_range)
	rand = random.randint(1, base**length)
	return int2base(rand,base)

# ---------------------------------------------------------------------------- #

def new_rdf_Graph():
	"""
	Creates a new rdflib Graph and bind to it all birda defined namespaces
	
	:return: rdflib.Graph
	"""
	
	rdf = rdflib.Graph()
	
	for ns in NAMESPACES.keys():
		rdf.bind(ns,NAMESPACES[ns])
		
	return rdf

# ---------------------------------------------------------------------------- #

def add_string_property(rdf, element, property, strings):
	"""
	Adds all translations of a specified string property to an element

	:param rdf: the RDF Graph
	:param element: the subject element
	:param property: the property used for "labeling"
	:param strings: dictionary of labels to attach to the widget.
		Keys are languages, values are the labels in those languages.
		Es: {'en':"Foo", 'it':"Pippo"}

	:return: None
	"""

	for lang,s in strings.items():
		rdf.add((element, property, Literal(s, lang=lang)))

# ---------------------------------------------------------------------------- #

def create_widget(
		rdf, type='', namespace='', name='',
		maps_type=None, maps_property=None,
		at_least=0, at_most=0,
		labels={}, descriptions={}):
	"""
	Creates a bird-a Widget and add it to the rdf graph

	:param rdf: the RDF Graph
	:param type: rdf.type of the widget
	:param namespace: namespace of the widget
	:param name: name of the widget (if empty, a random one will be chosen)
	:param maps_type: type mapped by the widget
	:param maps_property: property mapped by the widget
	:param at_least: min number of occurrences of the widget (zero for default value)
	:param at_most: max number of occurrences of the widget (zero for default value)
	:param labels: dictionary of labels to attach to the widget.
		Keys are languages, values are the labels in those languages.
		Es: {'en':"Foo", 'it':"Pippo"}
	:param labels: dictionary of descriptions to attach to the widget.
		Keys are languages, values are the labels in those languages.
		Es: {'en':"Foo", 'it':"Pippo"}

	:return: created element URIRef
	"""

	assert at_least >= 0
	assert at_most >= 0

	str_type = type.replace(str(bModel.BIRDA),'')

	if name:
		widget = URIRef(namespace+name+'-'+str_type)
	else:
		widget = URIRef(namespace + str_type +'-' + create_random_id())

	rdf.add((widget, RDF.type, type))

	if maps_type:
		rdf.add((widget, bModel.BIRDA.mapsType, maps_type))
	if maps_property:
		rdf.add((widget, bModel.BIRDA.mapsProperty, maps_property))

	if at_least:
		rdf.add((widget, bModel.BIRDA.atLeast, Literal(at_least, datatype=XSD.integer)))
	if at_most:
		rdf.add((widget, bModel.BIRDA.atMost, Literal(at_most, datatype=XSD.integer)))

	add_string_property(rdf, widget, bModel.BIRDA.hasLabel, labels)
	add_string_property(rdf, widget, bModel.BIRDA.hasDescription, descriptions)

	return widget

# ---------------------------------------------------------------------------- #

def create_form_widget(
		rdf, namespace='', name='',
		maps_type=None, maps_property=None,
		base_iri='', token_separator='-',
		target_label_property=RDFS.label,  target_descr_property=RDFS.comment,
		labels={}, descriptions={}):
	"""
	Creates a form widget

	:param rdf: the RDF Graph
	:param namespace: namespace of the widget
	:param name: name of the widget
	:param maps_property: type mapped by the widget
	:param maps_type: property mapped by the widget
	:param base_iri: ...
	:param token_separator: ...
	:param target_label_property: ...
	:param target_descr_property: ...
	:param labels: dictionary of labels to attach to the widget.
		Keys are languages, values are the labels in those languages.
		Es: {'en':"Foo", 'it':"Pippo"}
	:param labels: dictionary of descriptions to attach to the widget.
		Keys are languages, values are the labels in those languages.
		Es: {'en':"Foo", 'it':"Pippo"}

	:return: created element URIRef
	"""

	form = create_widget(
		rdf, type=bModel.BIRDA.Form,
		namespace=namespace, name=name,
		maps_type=maps_type, maps_property=maps_property,
		labels=labels, descriptions=descriptions)

	# Dubbio: Va bene qui Literal anyURI o usare URIRef?
	rdf.add((form, bModel.BIRDA.hasBaseIRI, Literal(base_iri, datatype=XSD.anyURI)))
	rdf.add((form, bModel.BIRDA.hasTokenSeparator, Literal(token_separator)))
	rdf.add((form, bModel.BIRDA.usesPropertyForLabel, target_label_property))
	rdf.add((form, bModel.BIRDA.usesPropertyForDescription, target_descr_property))

	return form

# ---------------------------------------------------------------------------- #

def set_widget_options(rdf, widget, options={}):
	"""
	Set options for a widget

	:param rdf: the RDF Graph
	:param widget: target widget
	:param options: dictionary in the form:
		{'en': ["value1","value2",...], 'it': ["value1","value2",...]}

	:return: None
	"""

	for lang,opts in options:
		opts_literal = ', '.join( [repr(o) for o in opts] )
		rdf.add((widget, bModel.BIRDA.hasOptions, Literal(opts_literal, lang=lang)))

# ---------------------------------------------------------------------------- #

def make_co_list(rdf, list_element, elements, detached_list_property=None, detached_list_name=''):
	"""
	:param rdf: graph to which attach the list
	:param list_element: element owning the list
	:param elements: list of rdf elements
	:param detached_list_property: states that the actual list element should be
		detached from "list_element" and "list_element" should refer to the actual
		list element with property "detached_list_property"
	:param detached_list_name: define the suffix to add at the end of "list_element"
		name for naming the list element
	:return: None
	"""

	if not detached_list_property:
		actual_list_element = list_element

	else:
		if detached_list_name:
			actual_list_element = URIRef(list_element+'-'+str(detached_list_name))
		else:
			actual_list_element = URIRef(list_element +'-' +'list' +'-' + create_random_id())

		rdf.add((list_element, detached_list_property, actual_list_element))

	rdf.add((actual_list_element, RDF.type, CO.List))
	#rdf.add((list_element, CO.size, Literal(str(len(el)), datatype=XSD.nonNegativeInteger)))

	prev_el_ref = None

	for i,element in enumerate(elements):
		c = i + 1
		el_ref = URIRef(actual_list_element + '-el' + str(c))

		rdf.add((actual_list_element, CO.item, el_ref))
		rdf.add((el_ref, CO.itemContent, element))
		#rdf.add((el_ref, URIRef(CO+'index'), Literal(str(c), datatype=XSD.positiveInteger)))

		if prev_el_ref:
			rdf.add((prev_el_ref, CO.nextItem, el_ref))

		if c == 1:
			rdf.add((actual_list_element, CO.firstItem, el_ref))

		if c == len(elements):
			#rdf.add((list_element, CO.lastItem, el_ref))
			pass
		
		prev_el_ref = el_ref

# ---------------------------------------------------------------------------- #

def add_local_name_list(rdf, form, widget_list):
	"""
	Add local name list to a form or a subform

	:param rdf: the RDF graph
	:param form: form or subform URIRef
	:param widget_list: list of URIRef which values will compose the local name

	:return: the created list
	"""

	make_co_list(rdf, form, widget_list, detached_list_property=B_HAS_BASE_NAME_LIST, detached_list_name='local-name-list')

# ============================================================================ #

if __name__ == '__main__':
	pass