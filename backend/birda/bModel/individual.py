#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals

str = unicode
# -------------------------------------- #

import json
import collections
import rdflib

import birda.storage as storage
import birda.bModel as bModel

from rdflib.namespace import RDF, RDFS
from birda.bModel import BINST

from birda.bController.forms_factory import FormsFactory
from birda.storage.utils import (
	get_types,
	get_property,
	prettify,
	get_co_list, 
	get_by_lang,
	get_by_lang_mul,
	py2rdf
)

# Consts ...

# ============================================================================ #

class Individual(object):
	
	conn = None
	rdfw = None
	
	individual_uri = ''
	w_form = None
	
	type = None
	label_property = RDFS.label
	descr_property = RDFS.comment
	
	# Stores data retrieved by DB (readonly data)
	data_orig = {}
	
	# Stores current data (read/write data)
	data_current = {}
	# Indicates the language currently loaded in data_current
	lang_current = ''
	
	# -------------------------------------- #
	
	def __init__(self, conn, individual_uri='', w_form=None):
		"""
		
		:param individual_uri: URI of the individual
		:param w_form: Widget object representing a form or a subform.
			It is necessary in order to know which properties to retrieve
		:return: Individual object
		"""
		
		assert individual_uri
		assert w_form
		assert w_form.type_name in ('Form', 'SubForm')
		
		self.conn = conn
		self.rdfw = storage.RDFWrapper()
		
		self.individual_uri = individual_uri
		self.w_form = w_form
		
		# Gather Form Widget infos
		self.type = self.w_form.attributes['maps_type']
		self.only_properties = w_form.get_managed_properties()
		if self.w_form.attributes['label_property']:
			self.label_property = self.w_form.attributes['label_property']
		if self.w_form.attributes['descr_property']:
			self.descr_property = self.w_form.attributes['descr_property']
		
	# -------------------------------------- #
	
	def __str__(self):
		s = []
		s += ['-'*50]
		s += [(prettify(self.individual_uri)).center(50)]
		s += ['-'*50]
		s += [' + Type: %s' % prettify(self.type)]
		for k in ['labels', 'descriptions']:
			for val in self.data_current[k]:
				s += [' + %s: %s' % (k,prettify(val))]
		for property, val_list in self.data_current['properties'].items():
			for val in val_list:
				s += [' > %s: %s' % (prettify(property),prettify(val))]
		
		return '\n'.join(s)
	
	# -------------------------------------- #
	
	def is_present_at_db(self):
		"""
		Tell if this individual is present at db
		
		:return: True if present, False otherwise
		"""
	
	# -------------------------------------- #
	
	def load_from_db(self):
		
		d = collections.OrderedDict()
		
		types = get_types(self.conn, self.individual_uri, rdfw=self.rdfw, lexical=True)
		for type in types:
			if type == self.type:
				d['type'] = type
				break
		else:
			d['type'] = None
		
		d['labels'] = get_property(self.conn, self.individual_uri, self.label_property, rdfw=self.rdfw, lexical=True)
		d['descriptions'] = get_property(self.conn, self.individual_uri, self.descr_property, rdfw=self.rdfw, lexical=True)
		
		# a['authors'] = ...
		# a['modified_time'] = ...
		
		d['properties'] = collections.OrderedDict()
		for property in self.w_form.get_managed_properties():
			d['properties'][property] = get_property(self.conn, self.individual_uri, property, rdfw=self.rdfw, lexical=True)
		
		self.data_orig = d
		self.data_current = d.copy()
		self.lang_current = ''
		
	# -------------------------------------- #
	
	def load_json(self, in_json):
		"""
		Load an Individual JSON in data_current
		
		:param in_json: Individual JSON
		:return: None
		"""
		
		d = collections.OrderedDict()
		d['type'] = in_json['type']
		d['labels'] = [ rdflib.term.Literal(in_json['label'],lang=in_json['lang']) ]
		d['descriptions'] = [ rdflib.term.Literal(in_json['description'],lang=in_json['lang']) ]
		
		# d['authors'] = ...
		# d['modified_time'] = ...
		
		d['properties'] = collections.OrderedDict()
		for prop in in_json['properties']:
			# FIXME
			# Warning: matching uri-like strings and assign them a URIRef type is not
			# correct. Some method should be used to discern URIRef from datatype anyUri
			d['properties'][prop['uri']] = [
				py2rdf(val) for val in prop['values']
			]
		
		self.data_current = d
		self.lang_current = in_json['lang']
	
	# -------------------------------------- #
	
	def update_db(self):
		"""
		Compare current data vs the original data retrieved from db and
		delete or delete/insert in order to make the letter be equal to
		the former
		
		:return: None
		"""
		
		# Label
		# get_by_lang(,self.lang_current)
		
	
	# -------------------------------------- #
	
	def get_json(self, lang):
		
		j = collections.OrderedDict()
		j['uri'] = self.individual_uri
		j['type'] = self.type
		j['lang'] = lang
		j['label'] = get_by_lang(self.data_current['labels'], lang)
		j['description'] = get_by_lang(self.data_current['descriptions'], lang)
		# j['last_modified'] = ...
		# j['authors'] = ...
		
		j['properties'] = []
		for property in self.data_current['properties']:
			d = collections.OrderedDict()
			d['uri'] = property
			d['values'] = get_by_lang_mul(self.data_current['properties'][property], lang)
			j['properties'] += [ d ]
		
		return j
	
# ---------------------------------------------------------------------------- #

def test_individual_1(iConn, form_factory, individual, form_uri):
	
	ind = Individual(iConn, individual_uri=individual, w_form=form_factory.get_form(form_uri))
	ind.load_from_db()
	print
	print ind
	print
	print json.dumps(ind.get_json('it'), indent=4)
	print
	print json.dumps(ind.get_json('en'), indent=4)
	print

# ---------------------------------------------------------------------------- #

def test_individual_2(iConn, form_factory, individual, form_uri):
	
	ind = Individual(iConn, individual_uri=individual, w_form=form_factory.get_form(form_uri))
	ind.load_from_db()
	j = ind.get_json('it')
	ind.load_json(j)
	print json.dumps(ind.data_orig, indent=4)
	print json.dumps(ind.data_current, indent=4)

# ============================================================================ #

if __name__ == '__main__':
	ff = FormsFactory(storage.FAKE_SETTINGS)
	iConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='indiv', verbose=False)
	
	#test_individual_2(iConn, ff, getattr(bModel.TINST, 'pierluigi-mariuolo'), getattr(BINST, 'PersonLight-Form'))
	test_individual_2(iConn, ff, getattr(bModel.TINST, 'pierluigi-mariuolo'), getattr(BINST, 'PersonNormal-Form'))