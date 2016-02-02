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

class TextInputWidget(Widget):
	
	def __init__(self, conn, rdfw=None, uri=''):
		super(TextInputWidget, self).__init__(
				conn, rdfw=rdfw, uri=uri,
				actionable=True, hierarchical=False)
		
		self.attributes.update( self._get_specific_attributes() )
		
	# --------------------------------- #
	
	def _get_specific_attributes(self):
		"""
		Get the attributes specific for this type of widget
		
		:return: Dictionary containing widget properties
		"""
		
		a = collections.OrderedDict()
		a['defaults'] = get_property(self.conn, self.uri, BIRDA.hasDefaultValue, rdfw=self.rdfw, lexical=True)
		a['placeholders'] = get_property(self.conn, self.uri, BIRDA.hasPlaceholder, rdfw=self.rdfw, lexical=True)
		
		return a
	
	# --------------------------------- #
	
	def to_rdf(self, value, lang=None):
		"""
		See Widget.to_rdf declaration 
		"""
		
		return rdflib.term.Literal(str(value), lang=lang, datatype=None)
	
	# --------------------------------- #
	
	def getJSON(self, lang):
		"""
		Inherited from Widget 
		"""
		
		j = super(TextInputWidget, self).getJSON(lang)
		j['default'] = get_by_lang(self.attributes['defaults'], lang)
		j['placeholder'] = get_by_lang(self.attributes['placeholders'], lang)
		return j

# ---------------------------------------------------------------------------- #

# ============================================================================ #

if __name__ == '__main__':
	pass