#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import colander
import cornice
import jsons.individuals

import birda.storage as storage

from __init__ import ServiceError
from jsons.individuals import IndividualsInfos, SearchQuery

# ============================================================================ #

individual = cornice.Service(
		name='individuals',
		path='/api/v1/individuals/*individual_uri',
		description="Individuals get, insert and update")

individualV1 = cornice.Service(
		name='individuals',
		path='/api/v1/individuals/*individual_uri',
		description="Individuals get, insert and update")

# ---------------------------------------------------------------------------- #

@individual.get()
@individualV1.get()
def individual_get(request):
		
	u = request.matchdict['individual_uri']
	individual_uri = u[0] + '//' + '/'.join(u[1:])
	form_uri = request.GET.get('form_uri','')
	lang = request.GET.get('lang','en')
	
	if not form_uri:
		raise ServiceError(status=400, msg="Querystring parameter 'form_uri' is mandatory" % vars())
	
	forms_factory = request.find_service(name='FormsFactory')
	individuals_factory = request.find_service(name='IndividualsFactory')
	
	w_form = forms_factory.get_form(form_uri)
	if not w_form:
		raise ServiceError(status=404, msg="Form '%(form_uri)s' not found" % vars()) 
	
	iConn = storage.Storage.connect(request.registry.settings, dataset='indiv', verbose=False)
	ind = individuals_factory.get_individual(iConn, individual_uri, form_uri)
	
	j = ind.get_json(lang)
	j = {
		"individuals": [ j ] 
	}
	
	try:
		deserialized = IndividualsInfos().deserialize(j)
	except colander.Invalid as e:
		raise ServiceError(status=500, msg="JSON validation error", additional=e.asdict())
	
	return deserialized

# ============================================================================ #