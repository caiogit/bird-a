#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals

str = unicode
# -------------------------------------- #

import zope.interface
from birda.bModel.individual import Individual

# ============================================================================ #

class IIndividualsFactory(zope.interface.Interface):
	def reload_forms():
		pass
	
	def reload_forms(self):
		pass
		
	def get_forms(self):
		pass
		
	def get_form(self, form_uri):
		pass
	
	def get_forms_JSON(self, lang):
		pass

# ============================================================================ #

class IndividualsFactory(object):
	
	settings = None
	forms_factory = None
	
	# --------------------------------- #
	
	def __init__(self, settings, forms_factory):
		"""
		:param settings: Dictionary of configuration keys as retrieved from
			Pyramid configuration file
		"""
		
		self.settings = settings
		self.forms_factory = forms_factory
	
	# --------------------------------- #
	
	def get_individual(self, iConn, individual_uri, form_uri):
		w_form = self.forms_factory.get_form(form_uri)
		assert w_form
		
		return Individual(iConn, individual_uri=individual_uri, w_form=w_form)
	
	# --------------------------------- #

# ============================================================================ #

if __name__ == '__main__':
	pass