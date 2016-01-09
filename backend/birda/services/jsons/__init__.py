#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 08/01/16.
"""

import re
import colander
import json
import pprint

def check_uri(required=True):

	# Stolen from Django
	uri_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$',
		re.IGNORECASE)

	def check(node, value):
		if not value:
			if required:
				raise colander.Invalid(node,
					'URI required')
			else:
				return None

		if not re.match(uri_regex, value):
			raise colander.Invalid(node,
				'URI "%(value)s" doesn\'t match validation rules', vars())
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