#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import os
import glob
import json
import webob

# Allow "import services.models.*"
services = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in services]

# Patch for unicode strings (to be removed in Python3)
__all__ = [n.encode('ascii') for n in __all__]

# ============================================================================ #

class ServiceError(webob.exc.HTTPError):
	def __init__(self, status=0, msg='', additional={}):
		body = {'status': status, 'message': msg, 'additional':additional}
		webob.Response.__init__(self, json.dumps(body))
		self.status = status
		self.content_type = 'application/json'

# ---------------------------------------------------------------------------- #

def is_verbose(request):
	return request.registry.settings['birda.verbose'] == 'true'

# ---------------------------------------------------------------------------- #

def request2dict(request, function, extended=False):
	ret = {}
	ret['function'] = function
	ret['method'] = request.method
	ret['matchdict'] = request.matchdict
	ret['GET'] = dict(request.GET)
	ret['path_qs'] = request.path_qs
	try:
		ret['json_body'] = request.json_body
	except:
		ret['POST'] = dict(request.POST)
	ret['content_type'] = request.content_type

	if extended:
		ret['scheme'] = request.scheme
		ret['body'] = request.body
		ret['urlvars'] = request.urlvars
		ret['host_url'] = request.host_url
		ret['path'] = request.path
		ret['info'] = request.info
		ret['url'] = request.url
		ret['query_string'] = request.query_string
		ret['locale_name'] = request.locale_name
		ret['content_type'] = request.content_type
		ret['locale_name'] = request.locale_name

	return ret