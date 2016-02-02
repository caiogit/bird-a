#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals

str = unicode
# -------------------------------------- #

import rdflib
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

class SubFormWidget(Widget):
	
	def __init__(self, conn, rdfw=None, uri=''):
		super(SubFormWidget, self).__init__(
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
		a['reference_form'] = get_property(self.conn, self.uri, BIRDA.hasReferenceForm, rdfw=self.rdfw, lexical=True, single=True)
		
		return a
	
	# --------------------------------- #
	
	def to_rdf(self, value, lang=None):
		"""
		See Widget.to_rdf declaration 
		"""
		if value != None:
			return rdflib.term.URIRef(value)
		else:
			return rdflib.term.URIRef('')
	
	# --------------------------------- #
	
	def getJSON(self, lang):
		"""
		Inherited from Widget 
		"""
		
		j = super(SubFormWidget, self).getJSON(lang)
		fields = j.pop('fields')
		
		j['maps_type'] = self.attributes['maps_type']
		j['reference_form'] = self.attributes['reference_form']
		
		j['fields'] = fields
		return j

# ---------------------------------------------------------------------------- #

# ============================================================================ #

if __name__ == '__main__':
	pass