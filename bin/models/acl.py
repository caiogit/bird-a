# -*- coding: utf-8 -*-

from pyramid.security import (
	Allow,
	Everyone,
	Authenticated
)

class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'post')
    ]

    def __init__(self, request):
        pass  # pragma: no cover
