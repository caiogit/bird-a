#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 09/01/16.
"""

import cornice
import json
import jsons.forms

forms = cornice.Service(
		name='forms', path='/api/forms',
		description="Forms list")
formsV1 = cornice.Service(
		name='formsV1', path='/api/v1/forms',
		description="Forms list")

@forms.get()
@formsV1.get()
def forms_get(request):

    # xxx.get_forms_list()

    return jsons.forms.FormSimple_example