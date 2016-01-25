#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from birda import storage

from birda.storage import CO
from birda.storage.utils import get_types, get_property

# ============================================================================ #

class Widget(object):
	conn = None
	
	uri = ''
	instantiaton_time = None
	
	actionable = False
	hierarchical = False
	
	descendants = []
	
	# --------------------------------- #
	
	def __init__(self, conn, uri, actionable=False, hierarchical=False):
		self.conn = conn
		
		self.uri = uri
		self.instantiaton_time = time.time()
		
		self.actionable = actionable
		self.hierarchical = hierarchical
		
		if self.hierarchical:
			self.descendants = self._get_descendants()
			print repr(self.descendants)
	
	# --------------------------------- #
	
	def _get_descendants(self):
		"""
		For hierarchical widgets, get descendant widgets
		
		:return: List of Widgets
		"""
		
		if not self.hierarchical:
			return []
		
		# Look if widget is a co:List, if not returns []
		types = get_types(self.conn, self.uri)
		
		if str(CO.List) not in types:
			return []
		
		# Get first widget
		first_item = get_property(self.conn, self.uri, CO.firstItem)
		
		if not first_item:
			return []
			
		elem_list = [ first_item ]
		

# ---------------------------------------------------------------------------- #

def get_co_list(conn,list_node):
	
	el_list = []
	current_element = get_property(conn, list_node, CO.firstItem)
	while current_element:
		el_list += [ current_element ]
		current_element = get_property(conn, current_element, CO.firstItem)
	
		
# ============================================================================ #

if __name__ == '__main__':
	bConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='birda', verbose=False)
	iConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='indiv', verbose=False)
	
	w = Widget(bConn, getattr(storage.BINST,'PersonLight-Form'), actionable=True, hierarchical=True)
			
