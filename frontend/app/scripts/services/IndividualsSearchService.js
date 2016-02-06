'use strict';

/**
 * Created by caio on 28/12/15.
 */

angular.module('birdaApp')
	.service('IndividualsSearchService', ['ConfigService',
		function(ConfigService) {

			var self = this;
			var config = ConfigService.getConf();

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

					results = dummy_jsons.test_individuals_search_person_results;
					return;
				}

				if ( (params.properties.length === 0) &&
					 (params.filters[0].property === RDF_TYPE) &&
					 (params.filters[0].value === 'http://www.birda.it/fuff') ) {

					results = dummy_jsons.test_individuals_search_fuff_results;
					return;
				}

				throw "Azz";
			};

			self.getResults = function() {
				return results;
			};

			/* ========================================= */

			init();

		}]);
