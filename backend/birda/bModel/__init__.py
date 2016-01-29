#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

from rdflib.namespace import RDF, RDFS, XSD, FOAF, SKOS
from rdflib import Namespace

BIRDA = Namespace("http://w3id.org/ontologies/bird-a/")
CO = Namespace("http://purl.org/co/")

BINST = Namespace("http://pippo.it/birda-data/")
TINST = Namespace("http://pippo.it/target-data/")

B_HAS_BASE_NAME_LIST = BIRDA.hasBaseNameList

# ============================================================================ #

if __name__ == '__main__':
	pass
