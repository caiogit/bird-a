#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import hashlib
import rdflib
from rdflib.namespace import RDF, RDFS, XSD
from rdflib import Namespace, Literal, URIRef

DIR_PATH = os.path.dirname( os.path.realpath(__file__) )
SUPPORTED_OUTPUT_TYPES = ['triples', 'xml', 'n3', 'turtle', 'nt', 'pretty-xml']

BIRDA = Namespace("http://w3id.org/ontologies/bird-a/")
CO = Namespace("http://purl.org/co/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

BINST = Namespace("http://pippo.it/birda-data/")
TINST = Namespace("http://pippo.it/target-data/")

# ============================================================================ #

def create_simple_birda_instance():

	# hasFirstWidget
	# hasPart ...
	# hasDescription
	# hasLabel
	# mapsResource

	# Usiamo una proprietà (object property) da definire, che colleghi qualsiasi
	# widget a una certa risorsa RDF. Io userei una generica “mapsResource”, e
	# una sua sottoproprità come “mapsType” in modo da poter gestire al meglio
	# le casistiche relative ai HierarchicalWidget. Può andare?

	rdf = rdflib.Graph()

	B_DATA = Namespace("http://www.francescocaliumi.it/bird-a/person")
	B_DATAs = Namespace(B_DATA + '/')

	b_data = URIRef(B_DATA)
	rdf.add((b_data, RDFS.comment, Literal("Persone")))

	formPerson = B_DATAs.Form
	rdf.add((formPerson, RDF.type, BIRDA.Form))
	rdf.add((formPerson, BIRDA.hasLabel, Literal("Persona: inserimento dati", datatype=XSD.string, lang='en')))
	rdf.add((formPerson, BIRDA.mapsResource, URIRef(B_DATAs)))
	rdf.add((formPerson, BIRDA.mapsType, FOAF.Person))

	inputgivenName = B_DATAs.givenName
	rdf.add((inputgivenName, RDF.type, BIRDA.TextInput))
	rdf.add((formPerson, BIRDA.hasFirstWidget, inputgivenName))
	rdf.add((inputgivenName, BIRDA.ifPartOf, formPerson))
	rdf.add((inputgivenName, BIRDA.hasLabel, Literal("Name")))
	rdf.add((inputgivenName, BIRDA.mapsType, FOAF.givenName))

	inputFamilyName = B_DATAs.FamilyName
	rdf.add((inputFamilyName, RDF.type, BIRDA.TextInput))
	rdf.add((inputgivenName, BIRDA.hasNextWidget, inputFamilyName))
	rdf.add((inputFamilyName, BIRDA.ifPartOf, formPerson))
	rdf.add((inputFamilyName, BIRDA.hasLabel, Literal("Family Name")))
	rdf.add((inputFamilyName, BIRDA.mapsType, FOAF.familyName))

	return rdf

# ============================================================================ #

def	getID(s, length=6):
	h = hashlib.md5()
	h.update(str(s))
	return h.hexdigest()[:length]

# ---------------------------------------------------------------------------- #

def add_string_property(rdf, element, property, strings):
	"""
	Add all translations of a specified string property to an element

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

def create_widget(rdf, type='', namespace='', name='',
				maps_resource=None, maps_type=None, labels={},
				  label_property=BIRDA.hasLabel):
	"""
	Create a bird-a Widget and add it to the rdf graph

	:param rdf: the RDF Graph
	:param type: rdf.type of the widget
	:param namespace: namespace of the widget
	:param name: name of the widget
	:param maps_resource: resource mapped by the widget
	:param maps_type: type mapped by the widget
	:param labels: dictionary of labels to attach to the widget.
		Keys are languages, values are the labels in those languages.
		Es: {'en':"Foo", 'it':"Pippo"}

	:return: created element URIRef
	"""

	widget = URIRef(namespace+'-'+name+'-'+type)
	rdf.add((widget, RDF.type, type))
	rdf.add((widget, BIRDA.mapsResource, maps_resource))
	rdf.add((widget, BIRDA.mapsType, maps_type))

	add_string_property(rdf, widget, BIRDA.hasLabel, labels)

# ---------------------------------------------------------------------------- #

def make_co_list(rdf, widget, elements, widget_binding=BIRDA.hasWidgetList):
	"""
	:param rdf: Graph to which attach the list
	:param widget: Widget owning the list
	:param elements: list of rdf elements
	:return: None
	"""

	list_ref = URIRef( widget + '-List-' + getID(widget) )
	rdf.add((list_ref, RDF.type, CO.List))
	#rdf.add((list_ref, CO.size, Literal(str(len(el)), datatype=XSD.nonNegativeInteger)))

	if widget_binding:
		rdf.add((widget, widget_binding, list_ref))

	prev_el_ref = None

	for i,element in enumerate(elements):
		c = i + 1
		el_ref = URIRef(list_ref + '-' + str(c))

		rdf.add((list_ref, CO.item, el_ref))
		rdf.add((el_ref, CO.itemContent, element))
		#rdf.add((el_ref, URIRef(CO+'index'), Literal(str(c), datatype=XSD.positiveInteger)))

		if prev_el_ref:
			rdf.add((prev_el_ref, CO.nextItem, el_ref))

		if c == 1:
			rdf.add((list_ref, CO.firstItem, el_ref))

		if c == len(elements):
			#rdf.add((list_ref, CO.lastItem, el_ref))
			pass

# ---------------------------------------------------------------------------- #

def create_birda_instace():
	rdf = rdflib.Graph()

	# --------------------------------------------------------------- #

	# Form Light
	form_PersonLight = create_widget(
		rdf, type=BIRDA.Form,
		namespace=BINST, name='PersonLight',
		maps_resource=URIRef(TINST), maps_type=FOAF.Person,
		labels={
			'en': "FOAF:Person - Light data input",
			'it': "FOAF:Person - Inserimento dati ristretti",
		})
	add_string_property(rdf, form_PersonLight, BIRDA.hasGeneralLabel, {
		'en': "FOAF:Person Light",
		'it': "FOAF:Person Minimale",
	})
	add_string_property(rdf, form_PersonLight, BIRDA.hasGeneralDescription, {
		'en': "Used to insert only the minimal FOAF:Person attributes",
		'it': "Utilizzato per inserire solo gli attributi minimali di FOAF:Person",
	})
	# Dubbio: Va bene qui Literal anyURI o usare URIRef?
	rdf.add((form_PersonLight, BIRDA.hasBaseIRI, Literal("http://pippo.com/foaf-data#", datatype=XSD.anyURI)))
	rdf.add((form_PersonLight, BIRDA.hasTokenSeparator, Literal("-")))
	rdf.add((form_PersonLight, BIRDA.usesPropertyForLabel, SKOS.prefLabel))
	rdf.add((form_PersonLight, BIRDA.usesPropertyForDescription, RDFS.description))

	# FOAF Name
	input_givenName = BINST.givenName
	rdf.add((input_givenName, RDF.type, BIRDA.TextInput))
	rdf.add((input_givenName, BIRDA.mapsType, FOAF.givenName))
	#rdf.add((input_givenName, BIRDA.hasFirstWidget, input_givenName))
	#rdf.add((input_givenName, BIRDA.ifPartOf, formPerson))
	rdf.add((input_givenName, BIRDA.hasLabel, Literal(
		"Name", lang='en')))
	rdf.add((input_givenName, BIRDA.hasLabel, Literal(
		"Nome", lang='it')))

	# FOAF Family Name
	input_FamilyName = BINST.FamilyName
	rdf.add((input_FamilyName, RDF.type, BIRDA.TextInput))
	rdf.add((input_FamilyName, BIRDA.mapsType, FOAF.familyName))
	#rdf.add((input_givenName, BIRDA.hasNextWidget, input_FamilyName))
	#rdf.add((input_FamilyName, BIRDA.ifPartOf, formPerson))
	rdf.add((input_FamilyName, BIRDA.hasLabel, Literal(
		"Family Name", lang='en')))
	rdf.add((input_FamilyName, BIRDA.hasLabel, Literal(
		"Cognome", lang='it')))

	# FOAF Gender
	input_Gender = BINST.Gender
	rdf.add((input_Gender, RDF.type, BIRDA.RadioInput))
	rdf.add((input_Gender, BIRDA.mapsType, FOAF.gender))
	rdf.add((input_Gender, BIRDA.hasOptions, Literal(
		"male,female,unknown", lang='en')))
	rdf.add((input_Gender, BIRDA.hasOptions, Literal(
		"maschio,femmina,sconosciuto", lang='it')))

	# Form Light List
	# formList_PersonLight = BINST.PersonLightFormWList
	# formList_PersonLight_1 = BINST.PersonLightFormWListE1
	# formList_PersonLight_2 = BINST.PersonLightFormWListE2
	# formList_PersonLight_3 = BINST.PersonLightFormWListE3
	#
	# rdf.add((form_PersonLight, BIRDA.hasWidgetList, formList_PersonLight))
	#
	# rdf.add((formList_PersonLight, RDF.type, CO.List))
	# #rdf.add((formList_PersonLight, CO.size, Literal("3", datatype=XSD.nonNegativeInteger)))
	# rdf.add((formList_PersonLight, CO.firstItem, formList_PersonLight_1))
	# #rdf.add((formList_PersonLight, CO.lastItem, formList_PersonLight_2))
	#
	# rdf.add((formList_PersonLight_1, RDF.type, CO.ListItem))
	# rdf.add((formList_PersonLight, CO.item, formList_PersonLight_1))
	# #rdf.add((formList_PersonLight_2, URIRef(CO+'index'), Literal("1", datatype=XSD.positiveInteger)))
	# rdf.add((formList_PersonLight_1, CO.itemContent, input_givenName))
	# rdf.add((formList_PersonLight_1, CO.nextItem, formList_PersonLight_2))
	#
	# rdf.add((formList_PersonLight_2, RDF.type, CO.ListItem))
	# rdf.add((formList_PersonLight, CO.item, formList_PersonLight_2))
	# #rdf.add((formList_PersonLight_2, URIRef(CO+'index'), Literal("2", datatype=XSD.positiveInteger)))
	# rdf.add((formList_PersonLight_2, CO.itemContent, input_FamilyName))
	#
	# rdf.add((formList_PersonLight_3, RDF.type, CO.ListItem))
	# rdf.add((formList_PersonLight, CO.item, formList_PersonLight_3))
	# #rdf.add((formList_PersonLight_3, URIRef(CO+'index'), Literal("3", datatype=XSD.positiveInteger)))
	# rdf.add((formList_PersonLight_3, CO.itemContent, input_Gender))
	make_co_list(rdf, form_PersonLight, [input_givenName, input_FamilyName, input_Gender])

	# --------------------------------------------------------------- #

	# Form Extended
	form_PersonExt = BINST.PersonExtForm
	rdf.add((form_PersonExt, RDF.type, BIRDA.Form))
	rdf.add((form_PersonExt, BIRDA.mapsResource, URIRef(TINST)))
	rdf.add((form_PersonExt, BIRDA.mapsType, FOAF.Person))
	rdf.add((form_PersonExt, BIRDA.hasLabel, Literal(
		"FOAF:Person - Extended data input", lang='en')))
	rdf.add((form_PersonExt, BIRDA.hasLabel, Literal(
		"FOAF:Person - Inserimento dati estesi", lang='it')))

	# FOAF knows
	subform_Knows = BINST.PersonKnowsSubForm
	rdf.add((subform_Knows, BIRDA.mapsResource, URIRef(TINST)))
	rdf.add((subform_Knows, BIRDA.mapsType, FOAF.Person))
	make_co_list(rdf, subform_Knows, [input_givenName, input_FamilyName])



	# Form Ext List


	return rdf

# ---------------------------------------------------------------------------- #

def create_target_instace():
	rdf = rdflib.Graph()
	return rdf

# ============================================================================ #

def output(rdf, output_format='nt', file_name='', print_triples=False, print_file=False):
	if file_name:
		rdf.serialize("%(DIR_PATH)s/%(file_name)s.%(output_format)s" % vars(), format=output_format)

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
	output(binst, output_format='turtle', file_name='', print_triples=True, print_file=True)

	print '\n'+ '#'*80 + '\n' + '#'*80 + '\n'

	tinst = create_target_instace()
	output(tinst, output_format='turtle', file_name='', print_triples=True, print_file=True)
