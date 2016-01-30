#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals

str = unicode
# -------------------------------------- #

import collections
from birda.bModel.widget import Widget


from birda.bModel import BIRDA

from birda.storage.utils import (
	get_types,
	get_property,
	prettify,
	get_co_list, 
	get_by_lang
)

# Consts ...

# ============================================================================ #

class FormWidget(Widget):
	
	def __init__(self, conn, rdfw=None, uri=''):
		super(FormWidget, self).__init__(
				conn, rdfw=rdfw, uri=uri,
				actionable=True, hierarchical=True)
		
		self.attributes.update( self._get_specific_attributes() )
		
	# --------------------------------- #
	
	def _get_specific_attributes(self):
		"""
		Get the attributes specific for this type of widget
		
		:return: Dictionary containing widget properties
		"""
		
		a = collections.OrderedDict()
		a['maps_type'] = get_property(self.conn, self.uri, BIRDA.mapsType, rdfw=self.rdfw, lexical=True, single=True)
		a['base_uri'] = get_property(self.conn, self.uri, BIRDA.hasBaseIRI, rdfw=self.rdfw, lexical=True, single=True)
		
		a['label_property'] = get_property(self.conn, self.uri, BIRDA.usesPropertyForLabel, rdfw=self.rdfw, lexical=True, single=True)
		a['descr_property'] = get_property(self.conn, self.uri, BIRDA.usesPropertyForDescription, rdfw=self.rdfw, lexical=True, single=True)
		
		def fields2list(fields):
			if fields:
				return [ str(f).strip() for f in str(fields).split(',') ]
			else:
				return []
		
		a['local_name'] = {}
		a['local_name']['fields'] = fields2list( get_property(self.conn, self.uri, BIRDA.hasLocalNameFields, rdfw=self.rdfw, lexical=True, single=True) )
		a['local_name']['separator'] = get_property(self.conn, self.uri, BIRDA.hasLocalNameSeparator, rdfw=self.rdfw, lexical=True, single=True)
		a['local_name']['tokenSeparator'] = get_property(self.conn, self.uri, BIRDA.hasLocalNameTokenSeparator, rdfw=self.rdfw, lexical=True, single=True)
		a['local_name']['renderer'] = get_property(self.conn, self.uri, BIRDA.hasLocalNameRenderer, rdfw=self.rdfw, lexical=True, single=True)
		
		return a
	
	# --------------------------------- #
	
	def getJSON(self, lang):
		"""
		Inherited from Widget 
		
		(pop and re-add fields for a better readability of output json)
		"""
		
		j = super(FormWidget, self).getJSON(lang)
		fields = j.pop('fields')
		
		j.pop('w_type')
		uri = j.pop('widget_uri')
		j['form_uri'] = uri
		
		j['maps_type'] = self.attributes['maps_type']
		j['base_uri'] = self.attributes['base_uri']
		
		j['label_property'] = self.attributes['label_property']
		j['descr_property'] = self.attributes['descr_property']
		
		if self.attributes['local_name']['fields']:
			j['local_name'] = self.attributes['local_name']
		else:
			# Will be created by the schema
			#j['local_name'] = {}
			pass
		
		j['fields'] = fields
		return j

# ---------------------------------------------------------------------------- #

# ============================================================================ #

if __name__ == '__main__':
	pass