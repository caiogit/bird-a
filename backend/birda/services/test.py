#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created by caio on 05/01/16.
"""

import cornice
import cornice.resource
import pprint
import colander

import __init__ as services


# ============================================================================ #

hello = cornice.Service(name='hello', path='/test/hello', description="Simplest app")

@hello.get()
def get_info(request):
	"""Returns Hello in JSON."""
	return {'Hello': 'World'}

# ============================================================================ #

params_test = cornice.Service(
		name='params',
		path='/test/params/{param}',
		description="Cornice params test")

# ---------------------------------------------------------------------------- #

@params_test.get()
@params_test.post()
def params_test_f(request):

	ret = {}
	ret['matchdict'] = request.matchdict
	ret['GET'] = dict(request.GET)
	ret['POST'] = dict(request.POST)
	ret['path_qs'] = request.path_qs
	ret['scheme'] = request.scheme
	ret['method'] = request.method
	ret['body'] = request.body
	ret['urlvars'] = request.urlvars
	ret['content_type'] = request.content_type
	ret['host_url'] = request.host_url
	ret['path'] = request.path
	ret['info'] = request.info
	ret['url'] = request.url
	ret['query_string'] = request.query_string
	ret['locale_name'] = request.locale_name
	ret['content_type'] = request.content_type
	ret['locale_name'] = request.locale_name

	try:
		ret['json_body'] = request.json_body
	except:
		pass

	# ret['req'] = {}
	# for k in dir(request):
	# 	try:
	# 		el = getattr(request,k)
	# 		if type(el) in [type(0),type(0.0),type(""),type([]),type(()),type({})]:
	# 			ret['req'][k] = str(getattr(request,k))
	# 	except:
	# 		pass

	return ret

# ============================================================================ #

_ORDERS = {
	1: {'client':'pippo', 'items':5},
	2: {'client':'pluto', 'items':1},
	3: {'client':'pluto', 'items':3}
}

@cornice.resource.resource(collection_path='/test/resource/orders', path='/test/resource/orders/{id}')
class User(object):

	def __init__(self, request):
		self.request = request

	# ---------------------------- #

	class GetCollectionSchema(colander.MappingSchema):
		client = colander.SchemaNode(colander.String(), location="querystring", type='str')

	@cornice.resource.view(renderer='json',schema=GetCollectionSchema)
	def collection_get(self):
		l = []
		for o in _ORDERS.values():
			if o['client'] == self.request.GET['client']:
				l.append(o)
		return l

	# ---------------------------- #

	@cornice.resource.view(renderer='json')
	def get(self):
		return _ORDERS.get(int(self.request.matchdict['id']))

	# ---------------------------- #

	class PutCollectionSchema(colander.MappingSchema):
		def schema_type(self, **kw):
			return colander.Mapping(unknown='raise')

		client = colander.SchemaNode(colander.String(), location="body", type='str')
		items = colander.SchemaNode(colander.Integer(), location="body", type='int')
		desc = colander.SchemaNode(colander.String(), location="body", type='str', missing=colander.drop)

	@cornice.resource.view(renderer='json', accept='text/json', schema=PutCollectionSchema)
	def collection_put(self):
		print(self.request.json_body)
		new_id = len(_ORDERS) + 1
		_ORDERS[new_id] = self.request.json_body
		return {"new_id": new_id}

# ============================================================================ #
# ============================================================================ #

@cornice.resource.resource(collection_path='/test/resource/echo', path='/test/resource/echo/{id}')
class User(object):

	def __init__(self, request):
		self.request = request

	# ---------------------------- #

	@cornice.resource.view(renderer='json')
	def get(self):
		return services.request2dict(self.request, 'get')

	@cornice.resource.view(renderer='json')
	def put(self):
		return services.request2dict(self.request, 'put')

	@cornice.resource.view(renderer='json')
	def post(self):
		print vars()
		return services.request2dict(self.request, 'post')

	@cornice.resource.view(renderer='json')
	def delete(self):
		return services.request2dict(self.request, 'delete')

	# ---------------------------- #

	@cornice.resource.view(renderer='json')
	def collection_get(self):
		return services.request2dict(self.request, 'collection_get')

	@cornice.resource.view(renderer='json')
	def collection_put(self):
		return services.request2dict(self.request, 'collection_put')

	@cornice.resource.view(renderer='json')
	def collection_post(self):
		print vars(self)
		return services.request2dict(self.request, 'collection_post')

	@cornice.resource.view(renderer='json')
	def collection_delete(self):
		return services.request2dict(self.request, 'collection_delete')

# ============================================================================ #
# ============================================================================ #

import cornice.schemas

def get_mock_request(body, get=None):
	# Construct a mock request with the given request body
	class MockRegistry(object):
		def __init__(self):
			self.cornice_deserializers = {
				'application/json': cornice.util.extract_json_data
			}

	class MockRequest(object):
		def __init__(self, body, get):
			self.headers = {}
			self.matchdict = {}
			self.body = body
			self.GET = get or {}
			self.POST = {}
			self.validated = {}
			self.registry = MockRegistry()
			self.content_type = 'application/json'

	dummy_request = MockRequest(body, get)
	setattr(dummy_request, 'errors', cornice.errors.Errors(dummy_request))
	return dummy_request

# ---------------------------------------------------------------------------- #

PutCollectionSchema_mockReq = (
	'{"client":"asd", "items":3}',
	 {'egg.bar': 'GET'}
)
class PutCollectionSchema(colander.MappingSchema):
	client = colander.SchemaNode(colander.String(), location="body", type='str')
	items = colander.SchemaNode(colander.Integer(), location="body", type='int')
	desc = colander.SchemaNode(colander.String(), location="body", type='str', missing=colander.drop)

def test_colander_nested_schema(in_schema, mock_request):
	schema = cornice.schemas.CorniceSchema.from_colander(in_schema)

	dummy_request = get_mock_request(*mock_request)
	cornice.schemas.validate_colander_schema(schema, dummy_request)

	qs_fields = schema.get_attributes(location="querystring")
	print '>>> qs_fields <<<'
	print qs_fields
	print

	errors = dummy_request.errors
	print '>>> errors <<<'
	print pprint.pprint(errors)
	print

	expected = {'egg': {'bar': 'GET'},
				'ham': {'bar': 'POST'},
				}

	print '>>> validated <<<'
	print dummy_request.validated
	print

# ---------------------------------------------------------------------------- #

if __name__ == '__main__':
	test_colander_nested_schema(PutCollectionSchema, PutCollectionSchema_mockReq)