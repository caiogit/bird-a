#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 09/01/16.
"""

import cornice
import json
import jsons.forms

forms = cornice.Service(
		name='forms', path='/forms',
		description="Forms list")

@forms.get()
def forms_get(request):

    # xxx.get_forms_list()

    return jsons.forms.FormSimple_example