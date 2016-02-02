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
	py2rdf,
	insert_triple,
	delete_triple,
	update_triple,
	delete_all_triples
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
		self.type = self.w_form.get_mapped_type()
		self.only_properties = w_form.get_managed_properties()
		if self.w_form.attributes['label_property']:
			self.label_property = self.w_form.attributes['label_property']
		if self.w_form.attributes['descr_property']:
			self.descr_property = self.w_form.attributes['descr_property']
		
		# Load from db, if he istance exists
		self.load_from_db()
		
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
		
		return self.data_current['type'] != None
	
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
	
	# -------------------------------------- #
	
	def update_db(self, verbose=False):
		"""
		Compare current data vs the original data retrieved from db and
		delete or delete/insert in order to make the letter be equal to
		the former
		
		:return: True database was changed, False otherwise
		"""
		
		modified = False
		
		if verbose: print "Update..."
		
		# ----------------------------- #
		
		# Type #
		
		if self.data_current['type'] != self.data_orig['type']:
			if self.data_orig['type'] == None:
				if verbose: print "Added type: %s" % (prettify(self.data_current['type']))
				insert_triple(self.conn, self.individual_uri, RDF.type, self.data_current['type'])
				modified = True
			else:
				raise Exception('RDF Types mismatch! new: %s, orig: %s' % 
						(prettify(self.data_current['type']), prettify(self.data_orig['type'])))
		
		# ----------------------------- #
		
		# Label and Description #
		
		def update_single_field(d_orig, d_curr, field, property, lang):
			"""Utility function"""
			
			old_value = get_by_lang(d_orig[field], lang)
			new_value = get_by_lang(d_curr[field], lang)
			print repr(old_value)
			assert (not old_value and old_value.language == None) or (old_value.language == new_value.language), \
				"old language %r differ from new language %r" % (old_value.language, new_value.language)
			
			if old_value != new_value:
				if verbose: print "%(field)s (%(property)s): %(old_value)r -> %(new_value)r" % vars()
				update_triple(self.conn, self.individual_uri, property, old_value, new_value)
				return True
			else:
				return False
		
		modified |= update_single_field(self.data_orig, self.data_current, 'labels', self.label_property, self.lang_current)
		modified |= update_single_field(self.data_orig, self.data_current, 'descriptions', self.descr_property, self.lang_current)
		
		# ----------------------------- #
		
		# Authors #
		# ...
		
		# Modified time #
		# ...
		
		# ----------------------------- #
		
		# Other properties #
		for widget in self.w_form.get_descendants():
			
			property = widget.get_mapped_property()
			values_orig = get_by_lang_mul(
				self.data_orig['properties'].get(property,[]),
				lang=widget.get_language(self.lang_current))
			values_current = get_by_lang_mul(
				self.data_current['properties'].get(property,[]),
				lang=widget.get_language(self.lang_current))
			
			only_in_orig = set(values_orig) - set(values_current)
			only_in_curr = set(values_current) - set(values_orig)
			#in_both = set(values_current) & set(values_orig)
			
			for val in only_in_orig:
				if verbose: print "Delete %s: %s" % (prettify(property), prettify(val))
				delete_triple(
					self.conn, self.individual_uri, property,
					widget.to_rdf(val, lang=self.lang_current))
				modified = True
				
			for val in only_in_curr:
				if verbose: print "Insert %s: %s" % (prettify(property), prettify(val))
				insert_triple(
					self.conn, self.individual_uri, property,
					widget.to_rdf(val, lang=self.lang_current))
				modified = True
		
		if verbose: print "Modified: %s" % modified
		
		# After an update, data_orig and data_current should be reset
		if modified:
			self.load_from_db()
		else:
			self.data_current = self.data_orig.copy()
		
		return modified
		
	# -------------------------------------- #
	
	def delete(self):
		delete_all_triples(self.conn, self.individual_uri)
		self.load_from_db()
			
# ============================================================================ #

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
	
	iConn.verbose = True
	
	# Test Update #
	
	#ind.data_current['type'] = BINST.pippo
	ind.data_current['labels'] = [ rdflib.term.Literal('Mariottide',lang='it') ]
	#ind.data_current['descriptions'] = [ rdflib.term.Literal('Maranello',lang='en') ]
	ind.data_current['descriptions'] = [ rdflib.term.Literal('Maranello',lang='it') ]
	ind.data_current['properties']['http://xmlns.com/foaf/0.1/givenName'] \
		+= [ rdflib.term.Literal('Maria',lang='it') ]
	ind.data_current['properties']['http://xmlns.com/foaf/0.1/familyName'] \
		= [ rdflib.term.Literal('Mistificio',lang='it') ]
	ind.data_current['properties']['http://xmlns.com/foaf/0.1/knows'] \
		.pop(0)
	print
	ind.update_db(verbose=True)
	print
	
	iConn.rollback()

# ---------------------------------------------------------------------------- #

def test_individual_3(iConn, form_factory, individual, form_uri):
	
	ind = Individual(iConn, individual_uri=individual, w_form=form_factory.get_form(form_uri))
	ind.load_from_db()
	j = ind.get_json('it')
	
	new_ind = Individual(iConn, individual_uri=individual+'-bis', w_form=form_factory.get_form(form_uri))
	new_ind.load_from_db()
	new_ind.load_json(j)
	print json.dumps(new_ind.data_orig, indent=4)
	print json.dumps(new_ind.data_current, indent=4)
	
	iConn.verbose = True
	
	# Test Insert #
	
	print
	new_ind.update_db(verbose=True)
	print
	
	print json.dumps(new_ind.data_orig, indent=4)
	
	iConn.rollback()
	
# ============================================================================ #

if __name__ == '__main__':
	ff = FormsFactory(storage.FAKE_SETTINGS)
	iConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='indiv', verbose=False)
	
	#test_individual_2(iConn, ff, getattr(bModel.TINST, 'pierluigi-mariuolo'), getattr(BINST, 'PersonLight-Form'))
	test_individual_2(iConn, ff, getattr(bModel.TINST, 'pierluigi-mariuolo'), getattr(BINST, 'PersonNormal-Form'))
	test_individual_3(iConn, ff, getattr(bModel.TINST, 'pierluigi-mariuolo'), getattr(BINST, 'PersonNormal-Form'))
	