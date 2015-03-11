#!/usr/bin/python
# -*- coding: utf-8 -*-

import rdflib
from rdflib.namespace import RDF
from rdflib import Namespace, Literal, URIRef

rdf = rdflib.Graph()

# rdf.load("test_foaf_instance.rdf")
# rdf.serialize("test_foaf_instance_2.n3",format="n3")

# for s,p,o in rdf:
#   print "%(s)r,\n%(p)r,\n%(o)r\n" % vars()

BIRDA = Namespace("http://www.semanticweb.org/ontologies/bird-a-ontology/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

B_DATA = Namespace("http://www.francescocaliumi.it/bird-a/test/data/")

formPerson = B_DATA.Form
rdf.add((formPerson, RDF.type, BIRDA.Form))
rdf.add((formPerson, BIRDA.hasLabel, Literal("Persona")))
rdf.add((formPerson, BIRDA.mapsResource, URIRef(B_DATA)))
rdf.add((formPerson, BIRDA.mapsType, FOAF.Person))

inputGivenName = B_DATA.GivenName
rdf.add((inputGivenName, RDF.type, BIRDA.TextInput))
rdf.add((formPerson, BIRDA.hasFirstWidget, inputGivenName))
rdf.add((inputGivenName, BIRDA.ifPartOf, formPerson))
rdf.add((inputGivenName, BIRDA.hasLabel, Literal("Name")))
rdf.add((inputGivenName, BIRDA.mapsType, FOAF.givenName))

inputFamilyName = B_DATA.FamilyName
rdf.add((inputFamilyName, RDF.type, BIRDA.TextInput))
rdf.add((inputGivenName, BIRDA.hasNextWidget, inputFamilyName))
rdf.add((inputFamilyName, BIRDA.ifPartOf, formPerson))
rdf.add((inputFamilyName, BIRDA.hasLabel, Literal("Family Name")))
rdf.add((inputFamilyName, BIRDA.mapsType, FOAF.familyName))

# hasFirstWidget
# hasPart ...
# hasDescription
# hasLabel
# mapsResource

# Usiamo una proprietà (object property) da definire, che colleghi qualsiasi 
# widget a una certa risorsa RDF. Io userei una generica “mapsResource”, e 
# una sua sottoproprità come “mapsType” in modo da poter gestire al meglio 
# le casistiche relative ai HierarchicalWidget. Può andare?


print rdf.serialize(format="turtle")

for s,p,o in rdf: 
  print "%(s)r,\n%(p)r,\n%(o)r\n" % vars()

rdf.serialize("test_birda.turtle",format="turtle")
