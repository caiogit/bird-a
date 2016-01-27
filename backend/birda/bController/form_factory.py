#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Reference: https://pypi.python.org/pypi/pyramid_services/0.1.1

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals

str = unicode
# -------------------------------------- #

import zope.interface
from birda.storage import Storage, FAKE_SETTINGS, BINST
from birda.bModel.widget import Widget

# ============================================================================ #

class IFormFactory(zope.interface.Interface):
	def reload_forms():
		pass
		
	def get_forms(self):
		pass
		
	def get_form(form_uri):
		pass

# ============================================================================ #

class FormFactory(object):
	
	settings = None
	
	# Cache containing Form and SubForm objects
	form_cache = {}
	
	# --------------------------------- #
	
	def __init__(self, settings):
		self.settings = settings
		self._load_forms()
	
	# --------------------------------- #
	
	def _load_forms(self):
		bConn = Storage.connect(self.settings, dataset='birda', verbose=False)
		
		# Retrieves all Form and SubForm
		results = bConn.query("""
		SELECT DISTINCT ?form
		WHERE {{
			?form rdf:type ?type .
			FILTER( EXISTS {{ ?form rdf:type birda:Form }} ||
			        EXISTS {{ ?form rdf:type birda:SubForm }} ) .
		}}
		""".format(**vars()))
		
		dlist = results.getDictList()
		
		# Recreate the cache
		self.form_cache = {}
		
		for form in dlist:
			form_uri = str(form['form'])
			self.form_cache[form_uri] = Widget.create_instance(bConn, form_uri)
		
		bConn.close()
	
	# --------------------------------- #
	
	def reload_forms(self):
		self._load_forms()
	
	# --------------------------------- #
	
	def get_forms(self):
		l = []
		for form,w_form in self.form_cache.items():
			print form, w_form.type_name
			if w_form.type_name == 'Form':
				l += [ form ]
		return l
	
	# --------------------------------- #
		
	def get_form(self, uri):
		uri = str(uri)
		if self.form_cache.has_key(uri):			
			return self.form_cache[uri]
		else:
			return None
	

# ---------------------------------------------------------------------------- #

# ============================================================================ #

if __name__ == '__main__':
	#bConn = Storage.connect(FAKE_SETTINGS, dataset='birda', verbose=True)
	#iConn = Storage.connect(FAKE_SETTINGS, dataset='indiv', verbose=True)
	
	ff = FormFactory(FAKE_SETTINGS)
	print ff.get_forms()
	print ff.get_form(getattr(BINST, 'PersonNormal-Form'))
	