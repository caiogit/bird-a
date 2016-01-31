#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals

str = unicode
# -------------------------------------- #

import json
import collections

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
	get_by_lang_mul
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
	
	from_db = {}
	from_json = {}
	
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
			for val in self.from_db[k]:
				s += [' + %s: %s' % (k,prettify(val))]
		for property, val_list in self.from_db['properties'].items():
			for val in val_list:
				s += [' > %s: %s' % (prettify(property),prettify(val))]
		
		return '\n'.join(s)
	
	# -------------------------------------- #
	
	def load_from_db(self):
		
		a = collections.OrderedDict()
		a['type'] = self.type
		a['labels'] = get_property(self.conn, self.individual_uri, self.label_property, rdfw=self.rdfw, lexical=True)
		a['descriptions'] = get_property(self.conn, self.individual_uri, self.descr_property, rdfw=self.rdfw, lexical=True)
		
		# a['authors'] = ...
		# a['modified_time'] = ...
		
		a['properties'] = collections.OrderedDict()
		for property in self.w_form.get_managed_properties():
			a['properties'][property] = get_property(self.conn, self.individual_uri, property, rdfw=self.rdfw, lexical=True)
		
		self.from_db = a
		
	# -------------------------------------- #
	
	def load_json(self, json):
		pass
	
	# -------------------------------------- #
	
	def get_json(self, lang):
		
		j = collections.OrderedDict()
		j['uri'] = self.individual_uri
		j['type'] = self.type
		j['lang'] = lang
		j['label'] = get_by_lang(self.from_db['labels'], lang)
		j['description'] = get_by_lang(self.from_db['descriptions'], lang)
		# j['last_modified'] = ...
		# j['authors'] = ...
		
		j['properties'] = []
		for property in self.from_db['properties']:
			d = collections.OrderedDict()
			d['uri'] = property
			d['values'] = get_by_lang_mul(self.from_db['properties'][property], lang)
			j['properties'] += [ d ]
		
		return j
	
	# -------------------------------------- #
	
	def update_db(self):
		pass
	
# ---------------------------------------------------------------------------- #

def test_individual(iConn, form_factory, individual, form_uri):
	
	ind = Individual(iConn, individual_uri=individual, w_form=form_factory.get_form(form_uri))
	ind.load_from_db()
	print
	print ind
	print
	print json.dumps(ind.get_json('it'), indent=4)
	print
	print json.dumps(ind.get_json('en'), indent=4)
	print
	
# ============================================================================ #

if __name__ == '__main__':
	ff = FormsFactory(storage.FAKE_SETTINGS)
	iConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='indiv', verbose=False)
	
	test_individual(iConn, ff, getattr(bModel.TINST, 'pierluigi-mariuolo'), getattr(BINST, 'PersonLight-Form'))
	test_individual(iConn, ff, getattr(bModel.TINST, 'pierluigi-mariuolo'), getattr(BINST, 'PersonNormal-Form'))