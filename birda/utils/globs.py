# -*- coding: utf-8 -*-

'''
Created on 19/nov/2014

@author: caio
'''


"""
Modulo che contiene la dichiarazione di "globs", oggetto che accentra le informazioni
globali del programma e le procedure che le richiedono
"""

import os
import sys
import cgi
import ascii_utils
import generic



# ============================================================================ #

class GlobsError(Exception):
	def __init__(self,msg):
		self.msg = msg
	def __str__(self):
		return str(self.msg)

# ---------------------------------------------------------------------------- #

class Globs:
	
	# States if the execution is a test execution by command line or not
	test = False
	
	# Environ dictionary from the wsgi script plus computed environ keys
	environ = {}
	
	# Dictionary containing bird-a.conf keys
	config = {}
	
	# Dictionary containing get and post parameters from the http request
	input = {}
	
	# Dictionary containing app defined variables
	vars = {}
	
	# User who made the request (None = Anonymous)
	user = None
	
	# Current status to be returned via http response (200 Ok, 404 Not Found, 500 Internal Error)
	#status = 200
	
	# Object designated to produce the html output
	Formatter = None
	
	
	
	def __init__(self, environ):
		"""
		environ:
			Environ object from the wsgi script
		"""
		
		if not environ:
			self.test = True
			
		self.environ = self._get_environ_(environ)
		self.input = self._get_input_from_env_(environ)
		self.config = self._get_config_()
		
		# ---------------------------------------- #
		
		
	
	# =================================================================== #
	
	def close(self):
		pass
	
	# =================================================================== #
	# =================================================================== #
	# =================================================================== #
	
	def __str__(self):
		s = "\n"
		
		s += "Environ variables:\n"
		s += ascii_utils.text_diz(self.environ, k_order=[], k_funz_vis={}, evidenz=False, formatta=True, alpha_key_order=True)
		s += "\n\n"
		
		s += "Input variables:\n"
		s += ascii_utils.text_diz(self.input, k_order=[], k_funz_vis={}, evidenz=False, formatta=True, alpha_key_order=True)
		s += "\n\n"
			
		s += "Config variables:\n"
		s += ascii_utils.text_diz(self.config, k_order=[], k_funz_vis={}, evidenz=False, formatta=True, alpha_key_order=True)
		s += "\n\n"
			
		s += "Application's variables:\n"
		s += ascii_utils.text_diz(self.vars, k_order=[], k_funz_vis={}, evidenz=False, formatta=True, alpha_key_order=True)
		s += "\n"
		
		return s

	
	# =================================================================== #
	# =================================================================== #
	# =================================================================== #
	
	def _get_environ_(self, environ):
		
		if environ:
			env = dict(environ)
		else:
			env = {'CONTEXT_DOCUMENT_ROOT': '/home/caio/Desktop/workspace/bird-a/static'}
		
		env['PROJECT_DIR'] = os.path.abspath( os.path.split(env['CONTEXT_DOCUMENT_ROOT'])[0] )
		env['CONFIG_DIR'] = env['PROJECT_DIR'] + os.path.sep + 'config'
		env['BIN_DIR'] = env['PROJECT_DIR'] + os.path.sep + 'bin'
		
		return env
	
	# ------------------------------ #
	
	def _get_config_(self):
		config = generic.import_file(self.environ['CONFIG_DIR'] + os.path.sep + 'config.py', dryrun=True)
		
		conf_dict = vars(config)
		for k in conf_dict.keys():
			if k.startswith('__'):
				del conf_dict[k]
		
		return conf_dict
	
	# ------------------------------ #
	
	def _get_input_from_env_(self,environ):
		if self.test:
			return {}
		else:
			env = environ.copy()
			fields = cgi.FieldStorage(
				fp = environ['wsgi.input'],
				environ = env,
				keep_blank_values = True
			)
			
			d = {}
			for k in fields:
				d[str(k)] = fields.getvalue(k)
			
			return d

# ============================================================================ #
# ============================================================================ #
# ============================================================================ #

if __name__ == '__main__':
	globs = Globs(None)
	print globs
	globs.close()
	
	
