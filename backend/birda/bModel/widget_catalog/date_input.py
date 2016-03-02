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

class DateInputWidget(Widget):
	
	def __init__(self, conn, rdfw=None, uri=''):
		super(DateInputWidget, self).__init__(
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
		
		return a
	
	# --------------------------------- #
	
	def to_rdf(self, value, lang=None):
		"""
		See Widget.to_rdf declaration 
		"""
		
		return rdflib.term.Literal(str(value), lang=lang, datatype=None)
	
	# --------------------------------- #
	
	def are_valid_values(self, values):
		"""
		See Widget.validate_values declaration 
		"""
		
		issues = super(DateInputWidget, self).validate_values(values)
		
		# TODO
		# ...
		
		return issues 
	
	# --------------------------------- #
	
	def getJSON(self, lang):
		"""
		Inherited from Widget 
		"""
		
		j = super(DateInputWidget, self).getJSON(lang)
		j['default'] = get_by_lang(self.attributes['defaults'], lang)
		return j

# ---------------------------------------------------------------------------- #

# ============================================================================ #

if __name__ == '__main__':
	pass