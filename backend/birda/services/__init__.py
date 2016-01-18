#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 05/01/16.
"""

import os
import glob

# Allow "import services.models.*"
services = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in services]

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