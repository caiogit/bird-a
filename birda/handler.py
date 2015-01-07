# -*- coding: utf-8 -*-

'''
Created on 11/nov/2014

@author: Francesco Caliumi

@copyright: 

'''

import sys
import os
from cStringIO import StringIO

sys.path += [ os.path.dirname(__file__) ]

import utils.globs

# ---------------------------------------------------------------------------- #

def application(environ, start_response):
	
	old_stdout = sys.stdout
	sys.stdout = mystdout = StringIO()
	
	status = '200 OK'
	
	Globs = utils.globs.Globs(environ)
	print Globs
	
	response_headers = [('Content-type', 'text/plain'),
						('Content-Length', str(len(mystdout.getvalue())))]
	start_response(status, response_headers)

	return [mystdout.getvalue()]

# ============================================================================ #

if __name__ == '__main__':
	old_stdout = sys.stdout
	sys.stdout = mystdout = StringIO()
	
	ret = application({}, (lambda x,y: None))
	
	sys.stdout = old_stdout
	print ret[0]