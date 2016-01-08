#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 05/01/16.
"""

from cornice import Service

hello = Service(name='hello', path='/hello', description="Simplest app")

@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}