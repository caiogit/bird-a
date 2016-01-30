#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import rdflib

RDF =   rdflib.namespace.RDF
RDFS =  rdflib.namespace.RDFS
XSD =   rdflib.namespace.XSD
FOAF =  rdflib.namespace.FOAF
SKOS =  rdflib.namespace.SKOS
CO =    rdflib.Namespace("http://purl.org/co/")
BIRDA = rdflib.Namespace("http://w3id.org/ontologies/bird-a/")
BINST = rdflib.Namespace("http://pippo.it/birda-data/")
TINST = rdflib.Namespace("http://pippo.it/target-data/")

NAMESPACES = {
	'rdf':   RDF,
	'rdfs':  RDFS,
	'xsd':   XSD,
	'foaf':  FOAF,
	'skos':  SKOS,
	'co':    CO,
	'birda': BIRDA,
	'binst': BINST,
	'tinst': TINST
}

_NAMESPACES_ORDERED_KEYS = sorted(NAMESPACES.keys(), (lambda x,y: len(x)-len(y)), reverse=True )

B_HAS_BASE_NAME_LIST = BIRDA.hasBaseNameList

# ============================================================================ #

if __name__ == '__main__':
	pass
