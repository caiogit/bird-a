'use strict';

/**
 * Created by caio on 28/12/15.
 */

angular.module('birdaApp')
	.service('IndividualsSearchService', ['ConfigService',
		function(ConfigService) {

			var self = this;
			var params = null;
			var results = null;

			function init() {
				self.clean();
			}

			/* ========================================= */

			self.clean = function() {
				params = {
					'properties': [],
					'filters': [],
					'order-by': []
				};
				results = null;
			};

			/* ----------------------------------------- */

			self.addProperty = function(property) {
				if (results) {
					console.log('IndividualsSearchService: Warning: altering params in a not cleaned status');
				}
				if ( (typeof property !== 'object') || (property === null)  ) {
					throw 'IndividualsSearchService: "property" should be a not null object';
				}
				if ( ! ('uri' in property) ) {
					throw 'IndividualsSearchService: "property" should have a "uri" property';
				}

				params.properties.push(property);
			};

			self.addFilter = function(filter) {
				if (results) {
					console.log('IndividualsSearchService: Warning: altering params in a not cleaned status');
				}
				if ( (typeof filter !== 'object') || (filter === null)  ) {
					throw 'IndividualsSearchService: "filter" should be a not null object';
				}
				if ( ! ('property' in filter) ) {
					throw 'IndividualsSearchService: "filter" should have a "property" property';
				}
				if ( ! ('value' in filter) ) {
					throw 'IndividualsSearchService: "filter" should have a "value" property';
				}
				if ( ! ('match' in filter) ) {
					throw 'IndividualsSearchService: "filter" should have a "match" property';
				}

				params.filters.push(filter);
			};

			self.addOrderBy = function(orderBy) {
				if (results) {
					console.log('IndividualsSearchService: Warning: altering params in a not cleaned status');
				}
				if ( (typeof orderBy !== 'object') || (orderBy === null)  ) {
					throw 'IndividualsSearchService: "orderBy" should be a not null object';
				}
				if ( ! ('property' in orderBy) ) {
					throw 'IndividualsSearchService: "orderBy" should have a "property" property';
				}
				if ( ! ('order' in orderBy) ) {
					throw 'IndividualsSearchService: "orderBy" should have a "order" property';
				}

				params.order_by.push(orderBy);
			};

			/* ----------------------------------------- */

			self.search = function() {

				/** TODO: Remove debug code here **/

				if ( (params.properties.length === 0) &&
					 (params.filters[0].property === RDF_TYPE) &&
					 (params.filters[0].value === 'http://xmlns.com/foaf/0.1/Person') ) {

					results = self.test_personResults;
					return;
				}

				if ( (params.properties.length === 0) &&
					 (params.filters[0].property === RDF_TYPE) &&
					 (params.filters[0].value === 'http://www.birda.it/fuff') ) {

					results = self.test_fuffResults;
					return;
				}

				throw "Azz";
			};

			self.getResults = function() {
				return results;
			};

			/* ========================================= */

			self.test_personResults = {
				'individuals': [
					{
						'uri': 'http://ex.com/john-max-smith-01',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-02',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-03',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-04',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-05',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-06',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-07',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-08',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-09',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-10',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-11',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-12',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-13',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-14',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-15',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-16',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-17',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-18',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					},
					{
						'uri': 'http://ex.com/john-max-smith-19',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'description': 'Famous actor'
					}
				]
			};

			self.test_fuffResults = {
				'individuals': [
					{
						'uri': 'http://ex.com/1111',
						'type': 'http://xmlns.com/foaf/0.1/Fuff',
						'label': 'Pippo',
						'Description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae nisl rutrum, placerat nisl ac.',
						'properties': []
					},
					{
						'uri': 'http://ex.com/2222',
						'type': 'http://xmlns.com/foaf/0.1/Fuff',
						'label': 'Pippo',
						'Description': 'Suspendisse non sapien tempus, cursus nisi at, lacinia justo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.',
						'properties': []
					}
				]
			};

			/* ========================================= */

			init();

		}]);
