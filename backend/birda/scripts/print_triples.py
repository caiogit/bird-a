#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import sys
import os
import rdflib
import argparse
import tempfile

SUPPORTED_INPUT_TYPES = ['xml', 'pretty-xml', 'nt', 'n3', 'turtle']
SUPPORTED_OUTPUT_TYPES = ['triples', 'xml', 'n3', 'turtle', 'nt', 'pretty-xml']

# ============================================================================ #

def load_ontology(input_file):

	for type in SUPPORTED_INPUT_TYPES:
		try:
			print "Trying %(type)s: " % vars(),
			rdf = rdflib.Graph()
			rdf.load(input_file, format=type)
			print\
				"Ok"
			print
			return rdf
		except Exception, e:
			print "Fail"
			pass


def print_ontology(format, rdf):

	if format == 'triples':
		for s,p,o in rdf:
			if s.find('#') >= 0:
				continue
			print repr(s)
			print repr(p)
			print repr(o)
			print

	else:
		tmp_f = tempfile.NamedTemporaryFile(delete=True)
		rdf.serialize(tmp_f.name,format=format)

		lines = open(tmp_f.name).readlines()

		for l in lines:
			print l,

# -------------------------------------------------------------------- #

def arg_parse():
	parser = argparse.ArgumentParser(
		description="""Takes an input RDF file (in whatever format) and displays it in various formats""",
		epilog='',
	)

	parser.add_argument(
		dest='format',
		type=str,
		choices=SUPPORTED_OUTPUT_TYPES,
		help="Display format (%s)" % ', '.join(SUPPORTED_OUTPUT_TYPES))

	parser.add_argument(
		dest='input_file',
		type=str,
		help="Input rdf file"
	)

	args = parser.parse_args()

	if not os.path.isfile(args.input_file):
		print "\nFile \"%s\" doesn't exist\n" % args.input_file
		sys.exit(1)

	return args

# -------------------------------------------------------------------- #

if __name__ == '__main__':
	args = arg_parse()
	rdf = load_ontology(args.input_file)
	print_ontology(args.format, rdf)