# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import os
import sys

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

def add_to_dict(d, key, val, init_value):
	"""
	
	:param d: 
	:param key: 
	:param val: 
	:param item_type: 
	:return: 
	"""
	
	if not d.has_key(key):
		d[key] = init_value

	if type(init_value) in [ type([]) ]:
		d[key] += [ val ]
	
	raise ValueError('Unknown init_value type "%s"' % type(init_value))
	
	
	
	
	
	
# -------------------------------------------------------------------- #

if __name__ == '__main__':
	pass