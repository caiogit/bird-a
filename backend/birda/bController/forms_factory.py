#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Reference: https://pypi.python.org/pypi/pyramid_services/0.1.1

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals

str = unicode
# -------------------------------------- #

import zope.interface
from birda.storage import Storage, FAKE_SETTINGS
from birda.bModel import BINST
from birda.bModel.widget import Widget

# ============================================================================ #

class IFormsFactory(zope.interface.Interface):
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

class FormsFactory(object):
	
	settings = None
	
	# Cache containing Form and SubForm widget objects
	form_cache = {}
	
	# --------------------------------- #
	
	def __init__(self, settings):
		"""
		:param settings: Dictionary of configuration keys as retrieved from
			Pyramid configuration file
		"""
		
		self.settings = settings
		self._load_forms()
	
	# --------------------------------- #
	
	def _load_forms(self):
		"""
		Retrieves forms and subforms, convert them in the relative widget
		objects and recreate the form_cache dictionary
		
		:return: None
		"""
		
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
		"""
		Reload the internal forms and subforms cache
		
		:return: None
		"""
		self._load_forms()
	
	# --------------------------------- #
	
	def get_forms(self):
		"""
		Get the URIs of the forms currently in cache
		
		:return: List of strings representing form URIs
		"""
		
		l = []
		for form,w_form in self.form_cache.items():
			if w_form.type_name == 'Form':
				l += [ form ]
		return l
	
	# --------------------------------- #
		
	def get_form(self, uri):
		"""
		Get a form or a subform from the cache
		
		:param uri: URI of the form
		:return: Widget Object containing the Form
		"""
		
		uri = str(uri)
		if self.form_cache.has_key(uri):			
			return self.form_cache[uri]
		else:
			return None
	
	# --------------------------------- #
	
	def get_forms_JSON(self, lang):
		"""
		Returns the list of forms in FormsSimple JSON format
		
		:param lang: texts preferred language
		:return: FormsSimple JSON
		"""
	    
		forms = self.get_forms()
    
		j = {}
		j['forms'] = []
		
		for form,w_form in self.form_cache.items():
			if w_form.type_name == 'Form':
				d = {}
				d['uri'] = form
				d['type'] = w_form.get_mapped_type()
				d['label'] = str(w_form.get_label(lang))
				d['description'] = str(w_form.get_description(lang))
				
				j['forms'] += [ d ]
				
# 				print
# 				print '#'*80
# 				print '#'*80
# 				print w_form
# 				print '#'*80
# 				print '#'*80
# 				print
		
		return j

# ---------------------------------------------------------------------------- #

# ============================================================================ #

if __name__ == '__main__':
	#bConn = Storage.connect(FAKE_SETTINGS, dataset='birda', verbose=True)
	#iConn = Storage.connect(FAKE_SETTINGS, dataset='indiv', verbose=True)
	
	ff = FormsFactory(FAKE_SETTINGS)
	print ff.get_forms()
	print ff.get_form(getattr(BINST, 'PersonNormal-Form'))
	