#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import json
import colander
import cornice

import jsons.individuals
import birda.storage as storage

from __init__ import ServiceError, is_verbose, do_commit
from jsons.individuals import IndividualsInfos, SearchQuery

# ============================================================================ #

individual = cornice.Service(
		name='individual',
		path='/api/v1/individuals*individual_uri',
		description="Individuals CRUD operations")

individualV1 = cornice.Service(
		name='individual',
		path='/api/v1/individuals*individual_uri',
		description="Individuals CRUD operations")

# ---------------------------------------------------------------------------- #

def individual_initialization(request):
	u = request.matchdict['individual_uri']
	print u
	if request.method in ('GET','POST','DELETE') and not u:
		raise ServiceError(status=400, msg="Individual URI is mandatory in method %s" % request.method)
		
	individual_uri = u[0] + '//' + '/'.join(u[1:])
	form_uri = request.GET.get('form_uri','')
	lang = request.GET.get('lang','en').lower()
	
	if not form_uri:
		raise ServiceError(status=400, msg="Querystring parameter 'form_uri' is mandatory" % vars())
	
	forms_factory = request.find_service(name='FormsFactory')
	individuals_factory = request.find_service(name='IndividualsFactory')
	
	w_form = forms_factory.get_form(form_uri)
	if not w_form:
		raise ServiceError(status=404, msg="Form '%(form_uri)s' not found" % vars()) 
	
	iConn = storage.Storage.connect(request.registry.settings, dataset='indiv', verbose=False)
	ind = individuals_factory.get_individual(iConn, individual_uri, form_uri)
	
	return iConn, lang, ind

# ---------------------------------------------------------------------------- #

@individual.get()
@individualV1.get()
def individual_get(request):
	
	iConn, lang, ind = individual_initialization(request)
	
	if not ind.is_present_at_db():
		raise ServiceError(status=404, msg="Individual '%s' not found" % ind.individual_uri)
	
	j = ind.get_json(lang)
	j = {
		"individuals": [ j ] 
	}
	
	try:
		deserialized = IndividualsInfos().deserialize(j)
	except colander.Invalid as e:
		raise ServiceError(status=500, msg="JSON validation error", additional=e.asdict())
	
	iConn.close()
	
	return deserialized

# ---------------------------------------------------------------------------- #

@individual.post()
@individualV1.post()
def individual_post(request):
	
	iConn, lang, ind = individual_initialization(request)
	
	if not ind.is_present_at_db():
		raise ServiceError(status=404, msg="Individual '%s' not found" % ind.individual_uri)
	
	try:
		j = IndividualsInfos().deserialize(request.json_body)
	except colander.Invalid as e:
		raise ServiceError(status=400, msg="JSON validation error", additional=e.asdict())
	
	if len(j['individuals']) != 1:
		raise ServiceError(status=400, msg="There should be only one individual in POST JSON")
	
	issues = ind.load_json(j['individuals'][0])
	
	if issues:
		raise ServiceError(status=500, msg="JSON validation error", additional=issues)
	
	modified = ind.update_db(verbose=is_verbose(request))
	
	j = ind.get_json(lang)
	j = {
		"individuals": [ j ] 
	}
	
	try:
		deserialized = IndividualsInfos().deserialize(j)
	except colander.Invalid as e:
		raise ServiceError(status=500, msg="JSON validation error", additional=e.asdict())
	
	if modified and do_commit(request):
		iConn.commit()
	iConn.close()
	
	return deserialized

# ---------------------------------------------------------------------------- #

@individual.delete()
@individualV1.delete()
def individual_delete(request):
	
	iConn, lang, ind = individual_initialization(request)
	
	if not ind.is_present_at_db():
		#raise ServiceError(status=404, msg="JSON validation error", additional=e.asdict())
		request.response.status = 202
		if is_verbose(request): print "Not found"
	else:
		ind.delete()
		request.response.status = 204
		if is_verbose(request): print "Deleted!!"
	
	if do_commit(request):
		iConn.commit()
	iConn.close()
	
	return {}

# ============================================================================ #
