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
	
	def search(self, iConn, in_json):
		"""
		Warning!
		
		The implementation of this feature is in "dummy" state.
		At the moment, this function only scan the input json properties
		in search of rdf:type property, search instances with this type
		ordering them by uri and then returns vanilla Individual jsons.
		"""
		
		"""
		{
			"properties": [
				{
					"uri": "http://xmlns.com/foaf/0.1/givenName"
				},
				{
					"uri": "http://xmlns.com/foaf/0.1/familyName"
				}
			],
			"filters":[
				{
					"property": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
					"value": "http://xmlns.com/foaf/0.1/Person",
					"match": "exact"
				},
				{
					"property": "http://xmlns.com/foaf/0.1/familyName",
					"value": "Pippo",
					"match": "starts_with"
				}
			],
			"order_by":[
				{
					"property": "http://xmlns.com/foaf/0.1/familyName",
					"order": "desc"
				}
			],
			"limit": 0,
			"offset": 0
		}
		"""
		
		# Search with SPARQL
		in_json['']
		
		iConn.query("""
		SELECT ?s
		WHERE {{
			?s rdf:type <{type_uri}> .
		}}
		""".format(**vars()))
		
		# Create list of individuals
		
		# Create jsons list
		
	
	# --------------------------------- #

# ============================================================================ #

if __name__ == '__main__':
	pass