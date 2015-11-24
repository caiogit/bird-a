#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import hashlib
import rdflib
import random
import string
import math
from rdflib.namespace import RDF, RDFS, XSD, FOAF, SKOS
from rdflib import Namespace, Literal, URIRef

import birda

DIR_PATH = os.path.dirname( os.path.realpath(__file__) )
SUPPORTED_OUTPUT_TYPES = ['triples', 'xml', 'n3', 'turtle', 'nt', 'pretty-xml']

BIRDA = Namespace("http://w3id.org/ontologies/bird-a/")
CO = Namespace("http://purl.org/co/")

BINST = Namespace("http://pippo.it/birda-data/")
TINST = Namespace("http://pippo.it/target-data/")

B_HAS_BASE_NAME_LIST = BIRDA.hasBaseNameList

# ============================================================================ #

def int2base(n, base):
	chr_list = string.digits + string.lowercase + string.uppercase
	l = [ chr_list[(n/base**i)%base] for i in xrange(int(math.log(n, base)), -1, -1) ]
	return ''.join(l)

def	get_id(s, length=6):
	h = hashlib.md5()
	h.update(str(s))
	return h.hexdigest()[:length]

def	get_random_id(length=6):
	chr_range = string.digits + string.lowercase
	base = len(chr_range)
	rand = random.randint(1, base**length)
	return int2base(rand,base)

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

	str_type = type.replace(str(BIRDA),'')

	if name:
		widget = URIRef(namespace+name+'-'+str_type)
	else:
		widget = URIRef(namespace+str_type+'-'+get_random_id())

	rdf.add((widget, RDF.type, type))

	if maps_type:
		rdf.add((widget, BIRDA.mapsType, maps_type))
	if maps_property:
		rdf.add((widget, BIRDA.mapsProperty, maps_property))

	if at_least:
		rdf.add((widget, BIRDA.atLeast, Literal(at_least, datatype=XSD.integer)))
	if at_most:
		rdf.add((widget, BIRDA.atMost, Literal(at_most, datatype=XSD.integer)))

	add_string_property(rdf, widget, BIRDA.hasLabel, labels)
	add_string_property(rdf, widget, BIRDA.hasDescription, descriptions)

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
		rdf, type=BIRDA.Form,
		namespace=namespace, name=name,
		maps_type=maps_type, maps_property=maps_property,
		labels=labels, descriptions=descriptions)

	# Dubbio: Va bene qui Literal anyURI o usare URIRef?
	rdf.add((form, BIRDA.hasBaseIRI, Literal(base_iri, datatype=XSD.anyURI)))
	rdf.add((form, BIRDA.hasTokenSeparator, Literal(token_separator)))
	rdf.add((form, BIRDA.usesPropertyForLabel, target_label_property))
	rdf.add((form, BIRDA.usesPropertyForDescription, target_descr_property))

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
		rdf.add((widget, BIRDA.hasOptions, Literal(opts_literal, lang=lang)))

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
			actual_list_element = URIRef(list_element+'-'+'list'+'-'+get_random_id())

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


# ---------------------------------------------------------------------------- #

def create_birda_instace():
	rdf = rdflib.Graph()

	# --------------------------------------------------------------- #

	# FOAF Name
	input_givenName = create_widget(
		rdf, type=BIRDA.TextInput, namespace=BINST, name='GivenName',
		maps_property=FOAF.givenName, at_least=1, labels={
			'en': "Name",
			'it': "Nome"
		})

	# FOAF Family Name
	input_FamilyName = create_widget(
		rdf, type=BIRDA.TextInput, namespace=BINST, name='FamilyName',
		maps_property=FOAF.familyName, at_least=1, labels={
			'en': "Family Name",
			'it': "Cognome"
		})

	# FOAF Gender
	input_Gender = create_widget(
		rdf, type=BIRDA.TextInput, namespace=BINST, name='Gender',
		maps_property=FOAF.gender, at_least=0, at_most=1, labels={
			'en': "Gender",
			'it': "Sesso"
		})
	set_widget_options(input_Gender, {
		'en': ["Male", "Female", "Unknown"],
		'it': ["Maschio", "Femmina", "Sconosciuto"]
	})

	# FOAF knows
	subform_Knows = create_widget(
		rdf, type=BIRDA.SubForm, namespace=BINST, name='PersonKnowsSubForm',
		maps_type=FOAF.Person, maps_property=FOAF.knows, labels={
			'en': "Gender",
			'it': "Sesso"
		})
	make_co_list(rdf, subform_Knows, [input_givenName, input_FamilyName])


	# --------------------------------------------------------------- #

	# FOAF Form Light
	form_PersonLight = create_form_widget(
		rdf, namespace=BINST, name='PersonLight',
		maps_type=FOAF.Person, maps_property=None,
		base_iri=URIRef(TINST), token_separator='-',
		target_label_property=SKOS.prefLabel,  target_descr_property=RDFS.comment,
		labels={
			'en': "FOAF:Person Light",
			'it': "FOAF:Person Minimale",
		},
		descriptions={
			'en': "Used to insert only the minimal FOAF:Person attributes",
			'it': "Utilizzato per inserire solo gli attributi minimali di FOAF:Person",
		})

	make_co_list(rdf, form_PersonLight, [input_givenName, input_FamilyName, input_Gender])

	# FOAF Form Extended
	form_PersonNormal = create_form_widget(
		rdf, namespace=BINST, name='PersonNormal',
		maps_type=FOAF.Person, maps_property=None,
		base_iri=URIRef(TINST), token_separator='-',
		target_label_property=SKOS.prefLabel,  target_descr_property=RDFS.comment,
		labels={
			'en': "FOAF:Person",
			'it': "FOAF:Person",
		},
		descriptions={
			'en': "Used to insert FOAF:Person attributes",
			'it': "Utilizzato per inserire attributi di FOAF:Person",
		})

	make_co_list(rdf, form_PersonNormal, [input_givenName, input_FamilyName, input_Gender, subform_Knows])
	add_local_name_list(rdf, form_PersonNormal, [input_givenName, input_FamilyName])

	return rdf

# ============================================================================ #

def create_target_instace():
	rdf = rdflib.Graph()

	p1 = getattr(TINST,get_random_id())
	rdf.add((p1, RDF.type, FOAF.Person))
	rdf.add((p1, FOAF.givenName, Literal('Mario',lang='it')))
	rdf.add((p1, FOAF.familyName, Literal('Rossi',lang='it')))
	rdf.add((p1, FOAF.gender, Literal('Maschio',lang='it')))

	p2 = getattr(TINST,get_random_id())
	rdf.add((p2, RDF.type, FOAF.Person))
	rdf.add((p2, FOAF.givenName, Literal('Anselmo',lang='it')))
	rdf.add((p2, FOAF.givenName, Literal('Edoardo',lang='it')))
	rdf.add((p2, FOAF.familyName, Literal('Verdi',lang='it')))

	p3 = getattr(TINST,'pierluigi-mariuolo')
	rdf.add((p3, RDF.type, FOAF.Person))
	rdf.add((p3, FOAF.givenName, Literal('Pierluigi',lang='it')))
	rdf.add((p3, FOAF.familyName, Literal('Mariuolo',lang='it')))
	rdf.add((p3, FOAF.gender, Literal('Maschio',lang='it')))
	rdf.add((p3, FOAF.knows, p1))
	rdf.add((p3, FOAF.knows, p2))

	p4 = getattr(TINST,'maria-grazia-rivera')
	rdf.add((p4, RDF.type, FOAF.Person))
	rdf.add((p4, FOAF.givenName, Literal('Maria',lang='it')))
	rdf.add((p4, FOAF.givenName, Literal('Grazia',lang='it')))
	rdf.add((p4, FOAF.familyName, Literal('Rivera',lang='it')))
	rdf.add((p4, FOAF.gender, Literal('Femmina',lang='it')))
	rdf.add((p4, FOAF.knows, p1))
	rdf.add((p4, FOAF.knows, p3))

	return rdf

# ============================================================================ #

def output(rdf, output_format='nt', file_name='', print_triples=False, print_file=False):
	if file_name:
		rdf.serialize("%(DIR_PATH)s/%%(file_name)s.%%(output_format)s" % globals() % vars(), format=output_format)

	if print_file:
		print rdf.serialize(format=output_format)

	if print_triples:
		print '\n'+ '='*60 + '\n'
		for s,p,o in rdf:
			print "%(s)r,\n%(p)r,\n%(o)r\n" % vars()
		print '\n'+ '='*60 + '\n'

# ============================================================================ #

if __name__ == '__main__':
	#simple = create_simple_birda_instance()
	#output(simple, output_format='turtle', file_name='', print_triples=True, print_file=True)
	#print '\n'+ '#'*80 + '\n' + '#'*80 + '\n'

	binst = create_birda_instace()
	output(binst, output_format='turtle', file_name='birda-example', print_triples=False, print_file=True)

	print '\n'+ '#'*80 + '\n' + '#'*80 + '\n'

	tinst = create_target_instace()
	output(tinst, output_format='turtle', file_name='target-instance-example', print_triples=False, print_file=True)
