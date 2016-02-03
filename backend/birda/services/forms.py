#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import cornice
from __init__ import ServiceError
from jsons.forms import FormsSimple, FormsFull

# ============================================================================ #

forms = cornice.Service(
		name='forms',
		path='/api/forms',
		description="Forms list")

formsV1 = cornice.Service(
		name='formsV1',
		path='/api/v1/forms',
		description="Forms list")

# ---------------------------------------------------------------------------- #

@forms.get()
@formsV1.get()
def forms_get(request):
	
	lang = request.GET.get('lang','en').lower()
	
	form_factory = request.find_service(name='FormsFactory')
	j = form_factory.get_forms_JSON(lang)
	
	# Try to deserialize the json in order to test its correctness
	deserialized = FormsSimple().deserialize(j)
	
	return deserialized

# ============================================================================ #

form = cornice.Service(
		name='form',
		path='/api/forms/*form_uri',
		description="Form full infos")

formV1 = cornice.Service(
		name='formV1',
		path='/api/v1/forms/*form_uri',
		description="Form full infos")

# ---------------------------------------------------------------------------- #

@form.get()
@formV1.get()
def form_get(request):
	
	if not request.matchdict['form_uri']:
		# With only a trailing slash, it's probably been invoked the forms_get...
		return forms_get(request)
	
	u = request.matchdict['form_uri']
	form_uri = u[0] + '//' + '/'.join(u[1:])
	lang = request.GET.get('lang','en').lower()
	
	form_factory = request.find_service(name='FormsFactory')
	
	form = form_factory.get_form(form_uri)
	
	if not form:
		raise ServiceError(status=404, msg="Form '%(form_uri)s' not found" % vars(), connections=[])
	
	j = form.getJSON(lang)
	
	# Try to deserialize the json in order to test its correctness
	deserialized = FormsFull().deserialize(j)
	
	return deserialized

# ============================================================================ #