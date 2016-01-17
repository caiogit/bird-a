#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 14/01/16.
"""
import this

import cornice
import jsons.individuals

# ============================================================================ #

individual = cornice.Service(
		name='individuals',
		path='/api/v1/individuals/{individual_uri}',
		description="Individuals get, insert and update")

individualV1 = cornice.Service(
		name='individuals',
		path='/api/v1/individuals/{individual_uri}',
		description="Individuals get, insert and update")

# ---------------------------------------------------------------------------- #

@individual.get()
@individualV1.get()
def individual_get(request):

	# ...

	s = """

	"""

	return {'resp': s}

# ============================================================================ #