#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import os
import datetime
import rdflib
import birda.bModel.ontology as ontology

from rdflib.namespace import RDF, RDFS, XSD, FOAF, SKOS
from rdflib import Namespace, Literal, URIRef
from birda.bModel import NAMESPACES, CO, BIRDA, BINST, TINST

DIR_PATH = os.path.dirname( os.path.realpath(__file__) )
SUPPORTED_OUTPUT_TYPES = ['triples', 'xml', 'n3', 'turtle', 'nt', 'pretty-xml']

DUMMY = Namespace('http://dummy.com/onto-dummy')
DUMMY_INST = Namespace('http://dummy.com/onto-dummy/data#')

# ============================================================================ #

def create_birda_foaf_forms(rdf, widgets):

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
	
	# FOAF Height
	input_Height = ontology.create_widget(
		rdf, type=BIRDA.TextInput, namespace=BINST, name='Height',
		maps_property=FOAF.height, at_least=1, at_most=1, labels={
			'en': "Height",
			'it': "Altezza"
		})
	
	# ----------------------- #
	
	# FOAF Gender
	input_Gender = ontology.create_widget(
		rdf, type=BIRDA.CheckboxInput, namespace=BINST, name='Gender',
		maps_property=FOAF.gender, at_least=0, at_most=1, labels={
			'en': "Gender",
			'it': "Sesso"
		})
	ontology.set_widget_options(rdf, input_Gender, {
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
			'en': "Connections",
			'it': "Conoscenze"
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

	ontology.make_co_list(rdf, form_PersonNormal, [input_givenName, input_FamilyName, input_Gender, input_Height, subform_Knows])
	ontology.add_local_name_list(rdf, form_PersonNormal, [input_givenName, input_FamilyName])
	
	# --------------------------------------------------------------- #
	
	# Adding created widgets to widgets dict
	for k in set(vars().keys()) - set(['rdf','widgets']):
		assert not widgets.has_key(k), 'Error, name "%s" already assigned' % k
	widgets.update(vars())

# ---------------------------------------------------------------------------- #

def create_ontodummy(rdf, widgets):
	
	# Dummy Single Text
	dummy_text_inp_single = ontology.create_widget(
		rdf, type=BIRDA.TextInput, namespace=BINST, name='dummy-single-text',
		maps_property=DUMMY.SingleText, at_least=1, at_most=1, labels={
			'en': "Dummy single text",
			'it': "Singolo campo testuale"
		},
		descriptions={
			'en': "One and only one value",
			'it': "Uno ed un solo valore",
		})
	
	# ----------------------- #
	
	# Dummy Multiple Text
	dummy_text_inp_multi = ontology.create_widget(
		rdf, type=BIRDA.TextInput, namespace=BINST, name='dummy-multi-text',
		maps_property=DUMMY.MultiText, at_least=1, labels={
			'en': "Dummy multi text",
			'it': "Campo multiplo testuale"
		},
		descriptions={
			'en': "At least one value",
			'it': "Almeno un valore",
		})
	
	# ----------------------- #
	
	# Dummy Multiple Dates
	dummy_date_inp_multi = ontology.create_widget(
		rdf, type=BIRDA.DateInput, namespace=BINST, name='dummy-multi',
		maps_property=DUMMY.MultiDates, at_least=0, at_most=3, labels={
			'en': "Dummy multi dates",
			'it': "Date multiple"
		},
		descriptions={
			'en': "Min zero, max three dates",
			'it': "Minimo zero, massimo tre date",
		})
	
	# ----------------------- #
	
	# Dummy Checkbox
	dummy_check_inp = ontology.create_widget(
		rdf, type=BIRDA.CheckboxInput, namespace=BINST, name='dummy-checkbox',
		maps_property=DUMMY.Checkbox, at_least=1, at_most=1, labels={
			'en': "Checkbox",
			'it': "Checkbox"
		})
	ontology.set_widget_options(rdf, dummy_check_inp, {
		'en': ["One", 2, "3"],
		'it': ["Uno", 2, "3"]
	})
	
	# ----------------------- #
	
	# Dummy Radio
	dummy_radio_inp = ontology.create_widget(
		rdf, type=BIRDA.RadioInput, namespace=BINST, name='dummy-radio',
		maps_property=DUMMY.Radio, at_least=1, at_most=1, labels={
			'en': "Radio input",
			'it': "Radio input"
		})
	ontology.set_widget_options(rdf, dummy_radio_inp, {
		'en': ["One", 2, "3"],
		'it': ["Uno", 2, "3"]
	})
	
	# --------------------------------------------------------------- #
	
	# Dummy FOAF SubForm knows
	dummy_foaf_knows_subform = ontology.create_widget(
		rdf, type=BIRDA.SubForm, namespace=BINST, name='dummy-foaf-knows',
		maps_type=FOAF.Person, maps_property=FOAF.knows, at_least=0, at_most=3, labels={
			'en': "Dummy Connections",
			'it': "Conoscenze Dummy"
		},
		descriptions={
			'en': "Min zero, max three connections",
			'it': "Minimo zero, massimo tre conoscenze",
		})
	
	ontology.make_co_list(rdf, dummy_foaf_knows_subform, [widgets['input_givenName'], widgets['input_FamilyName']])
	ontology.set_reference_form(rdf, dummy_foaf_knows_subform, widgets['form_PersonLight'])
	
	# ----------------------- #
	
	# Dummy Dummy SubForm knows
	dummy_dummy_knows_subform = ontology.create_widget(
		rdf, type=BIRDA.SubForm, namespace=BINST, name='dummy-dummy-knows',
		maps_type=FOAF.DummyGuy, maps_property=DUMMY.knows, at_least=0, labels={
			'en': "Intenal Dummy Connections",
			'it': "Conoscenze Dummy interne"
		},
		descriptions={
			'en': "Min zero internal connections",
			'it': "Minimo zero conoscenze interne",
		})
	
	ontology.make_co_list(rdf, dummy_dummy_knows_subform, [
		dummy_text_inp_single, dummy_text_inp_multi, dummy_date_inp_multi, 
		dummy_check_inp, dummy_radio_inp, dummy_foaf_knows_subform
	])
	
	# ----------------------- #
	
	# FOAF Form Extended
	form_dummy = ontology.create_form_widget(
		rdf, namespace=BINST, name='dummy-guy',
		maps_type=FOAF.DummyGuy, maps_property=None,
		base_iri=URIRef(DUMMY_INST), token_separator='-',
		target_label_property=SKOS.prefLabel,  target_descr_property=RDFS.comment,
		labels={
			'en': "Dummy Form",
			'it': "Form Dummy",
		},
		descriptions={
			'en': "Dummy form with all available widgets",
			'it': "Dummy form con tutti i widget disponibili",
		})

	ontology.make_co_list(rdf, form_dummy, [
		dummy_text_inp_single, dummy_text_inp_multi, dummy_date_inp_multi, dummy_check_inp, 
		dummy_radio_inp, dummy_foaf_knows_subform, dummy_dummy_knows_subform
	])
	ontology.add_local_name_list(rdf, form_dummy, [dummy_text_inp_multi])
	
	# --------------------------------------------------------------- #
	
	ontology.set_reference_form(rdf, dummy_dummy_knows_subform, form_dummy)
	
	# --------------------------------------------------------------- #
	
	# Adding created widgets to widgets dict
	for k in set(vars().keys()) - set(['rdf','widgets']):
		assert not widgets.has_key(k), 'Error, name "%s" already assigned' % k
	widgets.update(vars())

# ---------------------------------------------------------------------------- #

def create_birda_instace():
	rdf = ontology.new_rdf_Graph()
	
	widgets = {}
	
	create_birda_foaf_forms(rdf, widgets)
	create_ontodummy(rdf, widgets)
	
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
	rdf.add((p3, SKOS.prefLabel, Literal('MD. Pierluigi Mariuolo',lang='en')))
	rdf.add((p3, RDFS.comment, Literal('Grande primario di tetratricologia',lang='it')))
	rdf.add((p3, RDFS.comment, Literal('Great head physician of tetratricology',lang='en')))
	rdf.add((p3, FOAF.givenName, Literal('Pierluigi',lang='it')))
	rdf.add((p3, FOAF.givenName, Literal('Pierluigi',lang='en')))
	rdf.add((p3, FOAF.familyName, Literal('Mariuolo',lang='it')))
	rdf.add((p3, FOAF.familyName, Literal('Mariuolo',lang='en')))
	rdf.add((p3, FOAF.gender, Literal('Maschio',lang='it')))
	rdf.add((p3, FOAF.gender, Literal('Male',lang='en')))
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
	