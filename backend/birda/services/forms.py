#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import cornice
import jsons.forms

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

    # xxx.get_forms_list()

    return jsons.forms.FormSimple_example

# ============================================================================ #