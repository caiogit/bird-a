# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

from pyramid.security import (
	Allow,
	Everyone,
	Authenticated
)

# ---------------------------------------------------------------------------- #

class RootFactory(object):
	__acl__ = [
		(Allow, Everyone, 'view'),
		(Allow, Authenticated, 'post')
	]

	def __init__(self, request):
		pass  # pragma: no cover
