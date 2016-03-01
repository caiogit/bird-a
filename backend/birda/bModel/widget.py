#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import time
import collections
import rdflib

from birda import storage

from __init__ import BIRDA, BINST

from birda.storage.utils import (
	get_types,
	get_property,
	prettify,
	get_co_list, 
	get_by_lang
)

# ============================================================================ #

class Widget(object):
	conn = None
	rdfw = None
	
	uri = ''
	instantiaton_time = None
	
	actionable = False
	hierarchical = False
	
	type = ''
	type_name = ''
	attributes = {}
	#core_attributes = {}
	descendants = []
	
	# Descendants organized per property
	descendants_per_property = {}
	
	# --------------------------------- #
	
	def __init__(self, conn, rdfw=None, uri='', actionable=False, hierarchical=False):
		assert uri, "Uri is mandatory"
		
		self.conn = conn
		if not rdfw:
			# Creates a new RDFWrapper if not given
			rdfw = storage.RDFWrapper()
		self.rdfw = rdfw
		
		self.uri = uri
		self.instantiaton_time = time.time()
		
		self.actionable = actionable
		self.hierarchical = hierarchical
		
		self.type = Widget.get_type(self.conn, self.uri, rdfw=self.rdfw)
		self.type_name = Widget.get_type_name(self.type)
		
		self.attributes = self._get_attributes()
		
		if self.hierarchical:
			self.descendants = self._get_descendants()
			for desc in self.descendants:
				self.descendants_per_property[desc.attributes['maps_property']] = desc
		
	# --------------------------------- #
	
	def _get_attributes(self):
		"""
		Get the attributes of the widget
		
		:return: Dictionary containing widget properties
		"""
		
		a = collections.OrderedDict()
		a['labels'] = get_property(self.conn, self.uri, BIRDA.hasLabel, rdfw=self.rdfw, lexical=True)
		a['descriptions'] = get_property(self.conn, self.uri, BIRDA.hasDescription, rdfw=self.rdfw, lexical=True)
		a['maps_property'] = get_property(self.conn, self.uri, BIRDA.mapsProperty, rdfw=self.rdfw, single=True)
		a['at_least'] = get_property(self.conn, self.uri, BIRDA.atLeast, rdfw=self.rdfw, single=True)
		a['at_most'] = get_property(self.conn, self.uri, BIRDA.atMost, rdfw=self.rdfw, single=True)
		
		return a
		
	# --------------------------------- #
	
	def _get_descendants(self):
		"""
		For hierarchical widgets, get descendant widgets
		
		:return: List of Widgets Objs 
		"""
		
		if not self.hierarchical:
			return []
		
		el_list = get_co_list(self.conn, self.uri, rdfw=self.rdfw)
		return [ Widget.create_instance(self.conn, uri, rdfw=self.rdfw) for uri in el_list ]
		
	# --------------------------------- #
	
	def __str__(self, indentation_level=0):
		import json
	
		indent = '    '*indentation_level
		s = []
		s += [indent + '-'*50]
		s += [indent + ' %s (%s)' % (self.type_name, prettify(self.uri))]
		s += [indent + '-'*50]
		
		for k in self.attributes.keys():
			if ( self.attributes[k] ) and ( type(self.attributes[k]) in [type([]), type(())] ):
				for v in self.attributes[k]:
					s += [indent + '    > %s: %s'%(k,v) ]
			
			else:
				s += [indent + '    > %s: %s'%(k,self.attributes[k]) ]
		
		for des in self.descendants:
			s += ['']
			s += [ des.__str__(indentation_level=indentation_level+1) ]
		
		return '\n'.join(s)
	
	# --------------------------------- #
	
	def to_rdf(self, value, lang=None):
		"""
		Converts input <value> in the correct rdflib object
		
		:param value: input value (string or whatever). If None, returns
			a representative object (e.g. "" for strings)
		:param lang: optional language specification (used only for strings)
		:return: The corresponding rdflib object
		"""
		
		raise NotImplementedError('This method should implemented in subclasses')
	
	# --------------------------------- #
	
	def get_language(self, lang=None):
		"""
		Returns <lang> if widget cares about language, None otherwise
		
		:param lang: language specification
		:return: <lang> or None
		"""
		
		rep_el = self.to_rdf(None, lang=lang)
		
		if type(rep_el) == type(rdflib.term.Literal('')):
			return rep_el.language
		else:
			return None
		
	# --------------------------------- #
	
	def validate_values(self, values):
		"""
		Take a list of values (even raw strings) and validate them accordingly to
		the widget settings
		
		:param values: List of input values
		:return: List of founded issues (empty list indicates a valid values list)
		"""
		
		issues = []
		
		if self.attributes['at_least']:
			if len(values) < int(self.attributes['at_least']):
				issues += ['Values length "%s" is less then the minium allowed of "%s"' % (len(values), self.attributes['at_least'])]
		
		if self.attributes['at_most']:
			if len(values) > int(self.attributes['at_most']):
				issues += ['Values length "%s" is more then the maxium allowed of "%s"' % (len(values), self.attributes['at_most'])]
		
		return issues 
	
	# --------------------------------- #
	
	def get_descendants(self):
		if self.hierarchical:
			return self.descendants
		else:
			raise ValueError("This method should be invoked only on hierarchical widgets")
	
	# --------------------------------- #
	
	def get_mapped_type(self):
		if self.attributes.has_key('maps_type'):
			return self.attributes['maps_type']
		else:
			raise TypeError('This widget doesn\'t maps any type')
	
	# --------------------------------- #
	
	def get_mapped_property(self):
		if self.attributes.has_key('maps_property'):
			return self.attributes['maps_property']
		else:
			raise TypeError('This widget doesn\'t maps any property')
	
	# --------------------------------- #
	
	def get_managed_properties(self):
		"""
		Returns properties managed by descendants or a hierarchical widget
		
		:return: List of URI strings representing properties
		"""
		
		assert self.hierarchical
		#assert self.type_name in ('Form', 'SubForm')
		
		properties = []
		for w in self.descendants:
			if w.attributes.has_key('maps_property'):
				properties += [ w.attributes['maps_property'] ]
		
		return properties
	
	# --------------------------------- #
	
	def get_label(self, lang):
		assert self.attributes.has_key('labels')
		
		return get_by_lang(self.attributes['labels'], lang)
		
	# --------------------------------- #
	
	def get_description(self, lang):
		assert self.attributes.has_key('descriptions')
		
		return get_by_lang(self.attributes['descriptions'], lang)
	
	# --------------------------------- #
	
	def get_allowed_values(self, lang):
		assert self.attributes.has_key('options')
		
		options = get_by_lang(self.attributes['options'], lang)
		if options:
			return [ ast.literal_eval(o.strip()) for o in options.split(',') ]
		else:
			return []
	
	# ================================= #
	
	def getJSON(self, lang):
		"""
		Build a JSON representation of the object
		
		:param lang: Language of the description fields
		:return: Dictionary containing the JSON keys
		"""
		
		j = collections.OrderedDict()
		j['widget_uri'] = self.uri
		j['w_type'] = self.type_name
		if self.attributes['maps_property']:
			j['property'] = self.attributes['maps_property']
		j['label'] = self.get_label(lang)
		j['description'] = self.get_description(lang)
		if self.attributes['at_least']:
			j['at_least'] = self.attributes['at_least']
		if self.attributes['at_most']:
			j['at_most'] = self.attributes['at_most']
		j['lang'] = lang
			
		if self.hierarchical:
			# Descends the tree if widget is not a leaf
			j['fields'] = [ desc.getJSON(lang) for desc in self.descendants ]
		
		return j
	
	# ================================= #
	
	@staticmethod
	def get_type(conn, uri, rdfw=None):
		"""
		Get the rdf type of the widget
		
		:param conn: RDF connection
		:param uri: Widget URI
		:param rdfw: Object RDFWrapper
		:return: String containing the uri (in the birda namespace)
		"""
		
		types = get_types(conn, uri, rdfw=rdfw)
		for type in types:
			if type.startswith(BIRDA):
				return type
		
		raise Exception("No type found")
	
	# --------------------------------- #
	
	@staticmethod
	def get_type_name(type_uri):
		"""
		Get the rdf type human name of the widget
		
		:param type_uri: RDF connection
		:return: String containing the friendly name of the type
		"""
		
		return type_uri.replace(BIRDA,'')
	
	# --------------------------------- #
	
	@staticmethod
	def create_instance(conn, uri, rdfw=None):
		"""
		Create the right Widget instance for the specified widget URI
		
		:param conn: RDF connection
		:param uri: Widget URI
		:param rdfw: Object RDFWrapper
		:return: *Widget Obj
		"""
		import widget_catalog
		
		type_name = Widget.get_type_name( Widget.get_type(conn, uri, rdfw=rdfw) )
		
		# TODO
		if type_name == 'Form':
			return widget_catalog.FormWidget(
				conn, rdfw=rdfw, uri=uri,
			)
		if type_name == 'SubForm':
			return widget_catalog.SubFormWidget(
				conn, rdfw=rdfw, uri=uri,
			)
		if type_name == 'TextInput':
			return widget_catalog.TextInputWidget(
				conn, rdfw=rdfw, uri=uri,
			)
		if type_name == 'CheckboxInput':
			return widget_catalog.CheckboxInputWidget(
				conn, rdfw=rdfw, uri=uri,
			)
		if type_name == 'RadioInput':
			return widget_catalog.RadioInputWidget(
				conn, rdfw=rdfw, uri=uri,
			)
		
		# raise ValueError('Type "%s" unknown' % type_name)
		return Widget(
			conn, rdfw=rdfw, uri=uri,
			actionable=True, hierarchical=True)

# ---------------------------------------------------------------------------- #


# ============================================================================ #

if __name__ == '__main__':
	bConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='birda', verbose=False)
	iConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='indiv', verbose=False)
		
# 	w = Widget(
# 			bConn, rdfw=storage.RDFWrapper(), uri=getattr(storage.BINST,'PersonLight-Form'),
# 			actionable=True, hierarchical=True)
	
	w = Widget.create_instance(bConn, getattr(BINST,'PersonNormal-Form'))
	
	print
	print w.rdfw.dumps('turtle')
	print
	print w
	print
	print
	import json
	print json.dumps(w.getJSON('en'), indent=4)
