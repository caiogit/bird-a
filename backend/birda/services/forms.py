#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import cornice
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
	
	lang = request.GET.get('lang','en')
	
	form_factory = request.find_service(name='FormFactory')
	j = form_factory.get_forms_JSON(lang)
	
	# Try to deserialize the json in order to test its correctness
	deserialized = FormsSimple().deserialize(j)
	
	return deserialized

# ============================================================================ #