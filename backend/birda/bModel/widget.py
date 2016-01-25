# -*- coding: utf-8 -*-

import time
from birda.storage import CO
from birda.storage.utils import get_types, get_property

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
			self = self.get_descendants()
	
	# --------------------------------- #
	
	def _get_descendants(self):
		"""
		For hierarchical widgets, get descendant widgets
		:return: List of Widgets
		"""
		
		# Look if widget is a co:List, if not returns []
		types = get_types(self.conn, self.uri)
		
		if CO.List not in types:
			return []
		
		# Get first widget
		first_item = get_property(self.uri, CO.firstItem)
		
		if not first_item:
			return []
		
		pass
