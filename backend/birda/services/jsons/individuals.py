#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import json
import colander
import __init__ as jsons

# ============================================================================ #
#							INDIVIDUALS_INFOS
# ============================================================================ #


class IndividualsInfos(colander.MappingSchema):

	# Uncomment to enable the "scrict" validation
	# (i.e. raise an error if an unknown key is present)
	#
	# def schema_type(self, **kw):
	# 	return colander.Mapping(unknown='raise')

	@colander.instantiate(
		missing=colander.required,
		validator=colander.Length(min=1))
	class individuals(colander.SequenceSchema):

		@colander.instantiate()
		class row(colander.MappingSchema):

			uri = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=jsons.check_uri(required=True))

			type = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=jsons.check_uri(required=True))

			lang = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=jsons.check_iso_lang(required=True))

			label = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=None)

			description = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=None)

			last_modified = colander.SchemaNode(
				colander.DateTime(),
				missing=None,
				validator=None)

			# ------------------------------------------------------- #

			@colander.instantiate(
				missing=[],
				validator=colander.Length(min=0))
			class authors(colander.SequenceSchema):

				@colander.instantiate()
				class row(colander.MappingSchema):

					uri = colander.SchemaNode(
						colander.String(),
						missing=colander.required,
						validator=jsons.check_uri(required=True))

					label = colander.SchemaNode(
						colander.String(),
						missing=colander.required,
						validator=None)

			# ------------------------------------------------------- #

			@colander.instantiate(
				missing=colander.required,
				validator=colander.Length(min=0))
			class properties(colander.SequenceSchema):

				@colander.instantiate()
				class row(colander.MappingSchema):

					uri = colander.SchemaNode(
						colander.String(),
						missing=colander.required,
						validator=jsons.check_uri(required=True))

					@colander.instantiate(
						missing=colander.required,
						validator=colander.Length(min=0))
					class values(colander.SequenceSchema):

						value = colander.SchemaNode(
							colander.String(),
							missing=colander.required,
							validator=None)


	# ======================================================= #

	# Coherence check
	def deserialize(self,in_json):

		res = super(IndividualsInfos, self).deserialize(in_json)

		# ValueError if something is not ok

		return res

# ============================================================================ #

IndividualsInfos_example = json.loads("""
{
	"individuals": [
		{
			"uri": "http://ex.com/john-max-smith",
			"type": "http://xmlns.com/foaf/0.1/Person",
			"lang": "en",
			"label": "John Max Smith",
			"description": "Famous actor",
			"authors": [
				{
					"uri": "http://bigio-bagio.it#me",
					"label": "Bigio Bagio"
				}
			],
			"last_modified": "2015-11-25 14:33:01",
			"properties": [
				{
					"uri": "http://xmlns.com/foaf/0.1/givenName",
					"values": ["John", "Max"]
				},
				{
					"uri": "http://xmlns.com/foaf/0.1/familyName",
					"values": ["Smith"]
				}
			]
		}
	]
}
""", strict=False)

# ============================================================================ #
#								SEARCH QUERY
# ============================================================================ #


class SearchQuery(colander.MappingSchema):

	# Uncomment to enable the "scrict" validation
	# (i.e. raise an error if an unknown key is present)
	#
	# def schema_type(self, **kw):
	# 	return colander.Mapping(unknown='raise')

	@colander.instantiate(
		missing=colander.required,
		validator=colander.Length(min=0))
	class properties(colander.SequenceSchema):

		@colander.instantiate()
		class row(colander.MappingSchema):

			uri = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=jsons.check_uri(required=True))

	# ------------------------------------------------------- #

	@colander.instantiate(
		missing=colander.required,
		validator=colander.Length(min=1))
	class filters(colander.SequenceSchema):

		@colander.instantiate()
		class row(colander.MappingSchema):

			property = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=jsons.check_uri(required=True))

			value = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=None)

			match = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=colander.OneOf(['exact', 'starts_with']))

	# ------------------------------------------------------- #

	@colander.instantiate(
		missing=colander.required,
		validator=colander.Length(min=0))
	class order_by(colander.SequenceSchema):

		@colander.instantiate()
		class row(colander.MappingSchema):

			property = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=jsons.check_uri(required=True))

			order = colander.SchemaNode(
				colander.String(),
				missing=colander.required,
				validator=colander.OneOf(['asc', 'desc']))

	# ------------------------------------------------------- #

	limit = colander.SchemaNode(
		colander.Integer(),
		missing=0,
		validator=colander.Range(min=0))

	offset = colander.SchemaNode(
		colander.Integer(),
		missing=0,
		validator=colander.Range(min=0))

	# ======================================================= #

	# Coherence check
	def deserialize(self,in_json):

		res = super(SearchQuery, self).deserialize(in_json)

		# ValueError if something is not ok

		return res

# ============================================================================ #

SearchQuery_example = json.loads("""
{
	"properties": [
		{
			"uri": "http://xmlns.com/foaf/0.1/givenName"
		},
		{
			"uri": "http://xmlns.com/foaf/0.1/familyName"
		}
	],
	"filters":[
		{
			"property": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
			"value": "http://xmlns.com/foaf/0.1/Person",
			"match": "exact"
		},
		{
			"property": "http://xmlns.com/foaf/0.1/familyName",
			"value": "http://xmlns.com/foaf/0.1/Person",
			"match": "starts_with"
		}
	],
	"order_by":[
		{
			"property": "http://xmlns.com/foaf/0.1/familyName",
			"order": "desc"
		}
	],
	"offset": 0
}
""", strict=False)


# ==================================================================== #
# ==================================================================== #
# ==================================================================== #


if __name__ == '__main__':

	jsons.test_json_validation(SearchQuery, SearchQuery_example, dump=True)
	jsons.test_json_validation(IndividualsInfos, IndividualsInfos_example, dump=True)
