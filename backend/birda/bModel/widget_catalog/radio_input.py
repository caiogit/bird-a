#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals

str = unicode
# -------------------------------------- #

import ast
import rdflib
import collections
from birda.bModel.widget import Widget
from checkbox_input import CheckboxInputWidget


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

class RadioInputWidget(CheckboxInputWidget):
	
	def __init__(self, conn, rdfw=None, uri=''):
		super(RadioInputWidget, self).__init__(
				conn, rdfw=rdfw, uri=uri)
		
		self.attributes.update( self._get_specific_attributes() )
		

# ============================================================================ #

if __name__ == '__main__':
	pass