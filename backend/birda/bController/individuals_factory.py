#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals

str = unicode
# -------------------------------------- #

import zope.interface
from birda.bModel.individual import Individual

from rdflib.namespace import RDF

# ============================================================================ #

class IIndividualsFactory(zope.interface.Interface):
	
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
	
	def search(self, iConn, in_json, w_form, lang, limit, offset):
		"""
		Warning!
		The implementation of this feature is incomplete. It relies on a form
		in order to operate (constraint that should be removed in future releases),
		and ignores the "properties" selection. The reason behind this choice is
		to ease the recognition of correct type of values and to have a handy
		generation of the output json.
		Correct implementation should independently look for correct widget to
		manage each "filter" and each "property" and use it to validate input,
		generate sparql and render the result.
		
		Update: for simplicity, all values in sparql queries have been handled
		as strings. This could affect performances, so it probably need some
		enhancements in future versions
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
		
		# Normalize fields
		
		sparql_type = ''
		sparql_filters = []
		
		for filter in in_json['filters']:
			property = filter['property']
			print filter
			
			if str(property) == str(RDF.type):
				sparql_type = '?ind rdf:type <{value}> .'.format(value=filter['value'])
			
			else:
				sparql_filter = []
				value = filter['value']
				value_name = '?value%s' % (len(sparql_filters)+1)
				
				sparql_filter += ['?ind <{property}> {value_name} .'.format(**vars()) ]
				sparql_filter += ['FILTER (langMatches(lang({value_name}), "{lang}")) .'.format(**vars()) ]
				"""
				?ind foaf:givenName ?prop1 .
				FILTER (strstarts(lcase(?prop1), "m")) .
				FILTER (langMatches(lang(?prop1), "it")) .
				"""
				
				# For normal properties we should look for the widget that maps it 
				# in order to use the correct sparql syntax
				#if not w_form.descendants_per_property.has_key(property):
				#	raise ValueError('Property <%s> not defined in form <%s>' % (property,w_form.uri))
				#value = w_form.descendants_per_property.has_key[property]\
				#	.to_rdf(filter['value'].lower(), lang=lang)
				
				if filter['match'] == 'exact':
					sparql_filter += [ 'FILTER (lcase(str({value_name})), "{value}")) .'.format(**vars()) ]
				elif filter['match'] == 'starts_with':
					sparql_filter += [ 'FILTER (strstarts(lcase({value_name}), "{value}")) .'.format(**vars()) ]
				else:
					raise NotImplementedError('match: %(match)s' % filter)
				
				sparql_filters += ['\n'.join(sparql_filter)]
		
		# TODO
		# To be used the json order-by indications
		order_by = "?ind"
		
		# TODO
		# To be used the limit and offset indications
		
		iConn.verbose = True
		
		# SPARQL query building
		results = iConn.query("""
		SELECT ?ind
		WHERE {{
			{type}
			
			{filters}
		}}
		ORDER BY {order_by}
		""".format(
			type = sparql_type,
			filters = '\n\n'.join(sparql_filters),
			order_by = order_by
		))
		
		# Create list of individuals
		individuals = []
		for res in results.getDictList():
			individuals += [
				Individual(iConn, individual_uri=res['ind'], w_form=w_form)
			 ]
		
		# Create jsons list
		j = {
			'individuals':[
				ind.get_json(lang) for ind in individuals
			]
		}
		
		return j
	
	# --------------------------------- #

# ============================================================================ #

if __name__ == '__main__':
	pass