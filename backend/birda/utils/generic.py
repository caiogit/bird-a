# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import os
import sys
import re

# ============================================================================ #

def import_file(full_path_to_module, dryrun=False):
	'''
	Import a module located at a given filepath and returns it.
	
	dryrun:
		If True, the module will not be really added to globals() 
	'''
	
	try:
		module_dir, module_file = os.path.split(full_path_to_module)
		module_name, module_ext = os.path.splitext(module_file)
		
		old_sys_path = sys.path
		sys.path = [ module_dir ]
		
		module_obj = __import__(module_name)
		module_obj.__file__ = full_path_to_module
		
		sys.path = old_sys_path
		
		if not dryrun:
			globals()[module_name] = module_obj
		
		return module_obj
		
	except:
		raise #ImportError('Unable to import %(full_path_to_module)s' % vars())

# -------------------------------------------------------------------- #

def is_uri(s):
	"""
	Tell if input string matches the uri syntax
	
	:param s: Input string
	:return: True string matches uri syntax, False otherwise
	"""
	
	# Stolen from Django (and slightly enhanced to handle "...#resource_fragment")
	uri_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]|#?\S+)$',
		re.IGNORECASE)
	
	return re.match(uri_regex, s)
	
# -------------------------------------------------------------------- #

if __name__ == '__main__':
	pass