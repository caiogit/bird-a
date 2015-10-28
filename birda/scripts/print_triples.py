#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import rdflib
import argparse
import tempfile

SUPPORTED_TYPES = ['triples', 'xml', 'n3', 'turtle', 'nt', 'pretty-xml']

def print_ontology(format, input_file):
	rdf = rdflib.Graph()
	rdf.load(input_file)

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
		choices=SUPPORTED_TYPES,
		help="Display format (%s)" % ', '.join(SUPPORTED_TYPES))

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
	print_ontology(args.format, args.input_file)