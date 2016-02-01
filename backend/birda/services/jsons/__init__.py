#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import re
import colander
import json
import pprint

import birda.utils.generic as utils 

# ============================================================================ #

def check_uri(required=True):

	def check(node, value):
		if not value:
			if required:
				raise colander.Invalid(node,
					'URI required')
			else:
				return None

		if not utils.is_uri(value):
			raise colander.Invalid(node,
				'URI "%(value)s" doesn\'t match validation rules' % vars())
		else:
			return None

	return check

# ---------------------------------------------------------------------------- #

def check_iso_lang(required=True):

	# Stolen from Django
	lang_regex = re.compile(
        r'^[a-zA-Z]{2}$',
		re.IGNORECASE)

	def check(node, value):
		if not value:
			if required:
				raise colander.Invalid(node,
					'Language required')
			else:
				return None

		if not re.match(lang_regex, value):
			raise colander.Invalid(node,
				'Lang "%(value)s" doesn\'t match validation rules', vars())
		else:
			return None

	return check

# ---------------------------------------------------------------------------- #

def test_json_validation(colander_schema, test_json, dump=True):
	if type(test_json)== type(""):
		json_test_j = json.loads(test_json, strict=False)
	else:
		json_test_j = test_json
	schema_multi = colander_schema()
	deserialized = schema_multi.deserialize(json_test_j)
	if dump:
		pprint.pprint(deserialized)
		print