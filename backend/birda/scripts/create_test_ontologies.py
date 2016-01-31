#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import os
import rdflib
import birda.bModel.ontology as ontology

from rdflib.namespace import RDF, RDFS, XSD, FOAF, SKOS
from rdflib import Namespace, Literal, URIRef
from birda.bModel import NAMESPACES, CO, BIRDA, BINST, TINST

DIR_PATH = os.path.dirname( os.path.realpath(__file__) )
SUPPORTED_OUTPUT_TYPES = ['triples', 'xml', 'n3', 'turtle', 'nt', 'pretty-xml']

# ---------------------------------------------------------------------------- #

def create_birda_instace():
	rdf = ontology.new_rdf_Graph()

	# --------------------------------------------------------------- #

	# FOAF Name
	input_givenName = ontology.create_widget(
		rdf, type=BIRDA.TextInput, namespace=BINST, name='GivenName',
		maps_property=FOAF.givenName, at_least=1, labels={
			'en': "Name",
			'it': "Nome"
		})
	
	# ----------------------- #
	
	# FOAF Family Name
	input_FamilyName = ontology.create_widget(
		rdf, type=BIRDA.TextInput, namespace=BINST, name='FamilyName',
		maps_property=FOAF.familyName, at_least=1, labels={
			'en': "Family Name",
			'it': "Cognome"
		})
	
	# ----------------------- #
	
	# FOAF Gender
	input_Gender = ontology.create_widget(
		rdf, type=BIRDA.TextInput, namespace=BINST, name='Gender',
		maps_property=FOAF.gender, at_least=0, at_most=1, labels={
			'en': "Gender",
			'it': "Sesso"
		})
	ontology.set_widget_options(input_Gender, {
		'en': ["Male", "Female", "Unknown"],
		'it': ["Maschio", "Femmina", "Sconosciuto"]
	})
	
	# --------------------------------------------------------------- #

	# FOAF Form Light
	form_PersonLight = ontology.create_form_widget(
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
	
	ontology.make_co_list(rdf, form_PersonLight, [input_givenName, input_FamilyName, input_Gender])
	
	# ----------------------- #
	
	# FOAF SubForm knows
	subform_Knows = ontology.create_widget(
		rdf, type=BIRDA.SubForm, namespace=BINST, name='PersonKnowsSubForm',
		maps_type=FOAF.Person, maps_property=FOAF.knows, labels={
			'en': "Gender",
			'it': "Sesso"
		})
	
	ontology.make_co_list(rdf, subform_Knows, [input_givenName, input_FamilyName])
	ontology.set_reference_form(rdf, subform_Knows, form_PersonLight)
	
	# ----------------------- #
	
	# FOAF Form Extended
	form_PersonNormal = ontology.create_form_widget(
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

	ontology.make_co_list(rdf, form_PersonNormal, [input_givenName, input_FamilyName, input_Gender, subform_Knows])
	ontology.add_local_name_list(rdf, form_PersonNormal, [input_givenName, input_FamilyName])

	return rdf

# ============================================================================ #

def create_target_instace():
	rdf = ontology.new_rdf_Graph()

	p1 = getattr(TINST, ontology.create_random_id())
	rdf.add((p1, RDF.type, FOAF.Person))
	rdf.add((p1, SKOS.prefLabel, Literal('Mario Rossi',lang='it')))
	rdf.add((p1, RDFS.comment, Literal('Il ben noto Mario',lang='it')))
	rdf.add((p1, FOAF.givenName, Literal('Mario',lang='it')))
	rdf.add((p1, FOAF.familyName, Literal('Rossi',lang='it')))
	rdf.add((p1, FOAF.gender, Literal('Maschio',lang='it')))
	
	p2 = getattr(TINST, ontology.create_random_id())
	rdf.add((p2, RDF.type, FOAF.Person))
	rdf.add((p2, SKOS.prefLabel, Literal('Anselmo Edoardo Verdi',lang='it')))
	rdf.add((p2, RDFS.comment, Literal('Sempre il solito Anselmo',lang='it')))
	rdf.add((p2, FOAF.givenName, Literal('Anselmo',lang='it')))
	rdf.add((p2, FOAF.givenName, Literal('Edoardo',lang='it')))
	rdf.add((p2, FOAF.familyName, Literal('Verdi',lang='it')))

	p3 = getattr(TINST,'pierluigi-mariuolo')
	rdf.add((p3, RDF.type, FOAF.Person))
	rdf.add((p3, SKOS.prefLabel, Literal('Dr. Pierluigi Mariuolo',lang='it')))
	rdf.add((p3, RDFS.comment, Literal('Grande primario di tetratricologia',lang='it')))
	rdf.add((p3, FOAF.givenName, Literal('Pierluigi',lang='it')))
	rdf.add((p3, FOAF.familyName, Literal('Mariuolo',lang='it')))
	rdf.add((p3, FOAF.gender, Literal('Maschio',lang='it')))
	rdf.add((p3, FOAF.knows, p1))
	rdf.add((p3, FOAF.knows, p2))

	p4 = getattr(TINST,'maria-grazia-rivera')
	rdf.add((p4, RDF.type, FOAF.Person))
	rdf.add((p4, SKOS.prefLabel, Literal('Maria Grazia Rivera',lang='it')))
	rdf.add((p4, RDFS.comment, Literal('La mitica Mary G',lang='it')))
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

	binst = create_birda_instace()
	
	output(
		binst, output_format='turtle', file_name='birda', 
		print_triples=False, print_file=True)

	print '\n'+ '#'*80 + '\n' + '#'*80 + '\n'

	tinst = create_target_instace()
	
	output(
		tinst, output_format='turtle', file_name='indiv',
		print_triples=False, print_file=True)
	