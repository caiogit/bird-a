'use strict';

/**
 * Created by caio on 28/12/15.
 */

angular.module('birdaApp')
	.service('IndividualsSearchService', ['$q', '$timeout', '$resource', 'ConfigService',
		function($q, $timeout, $resource, ConfigService) {

			var self = this;
			var config = ConfigService.getConf();

			var params = null;
			var results = [];

			var IndividualsSearch = $resource(config.buildApiUri('/individuals-search'));

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
				clearObject(results);
			};

			/* ----------------------------------------- */

			self.addProperty = function(property) {
				if (results) {
					console.log('IndividualsSearchService: Warning: altering params in a not cleaned status');
				}
				if ( (typeof property !== 'object') || (property === null)  ) {
					throw Error('IndividualsSearchService: "property" should be a not null object');
				}
				if ( ! ('uri' in property) ) {
					throw Error('IndividualsSearchService: "property" should have a "uri" property');
				}

				params.properties.push(property);
			};

			self.addFilter = function(filter) {
				if (results) {
					console.log('IndividualsSearchService: Warning: altering params in a not cleaned status');
				}
				if ( (typeof filter !== 'object') || (filter === null)  ) {
					throw Error('IndividualsSearchService: "filter" should be a not null object');
				}
				if ( ! ('property' in filter) ) {
					throw Error('IndividualsSearchService: "filter" should have a "property" property');
				}
				if ( ! ('value' in filter) ) {
					throw Error('IndividualsSearchService: "filter" should have a "value" property');
				}
				if ( ! ('match' in filter) ) {
					throw Error('IndividualsSearchService: "filter" should have a "match" property');
				}

				params.filters.push(filter);
			};

			self.addOrderBy = function(orderBy) {
				if (results) {
					console.log('IndividualsSearchService: Warning: altering params in a not cleaned status');
				}
				if ( (typeof orderBy !== 'object') || (orderBy === null)  ) {
					throw Error('IndividualsSearchService: "orderBy" should be a not null object');
				}
				if ( ! ('property' in orderBy) ) {
					throw Error('IndividualsSearchService: "orderBy" should have a "property" property');
				}
				if ( ! ('order' in orderBy) ) {
					throw Error('IndividualsSearchService: "orderBy" should have a "order" property');
				}

				params.order_by.push(orderBy);
			};

			/* ----------------------------------------- */

			self.search = function(form_uri) {

				if (config.dummyData) {
					clearObject(results);
					var defer = $q.defer();

					// simulated async function
					$timeout(function() {
						angular.extend(results, getDummyResults());
						defer.resolve(results);
						console.log('Results: ', results);
					}, config.dummyWaitTime);

					return defer.promise;

				} else {

					results = IndividualsSearch.get({
						form:form_uri,
						lang:config.lang
					});

					console.log("Results: ",results);

					results.$promise.then(
						function(response) {
							console.log('Results: ', response);
						},
						UIService.notifyError);

					return results.$promise;
				}

			};

			/* ----------------------------------------- */

			self.getResults = function() {
				console.log(results);
				return results;
			};

			/* ----------------------------------------- */

			function getDummyResults() {
				assert(
					((params.properties.length === 0) &&
					 (params.filters[0].property === RDF_TYPE)));

				//console.log(dummy_jsons.test_individuals_search_results, 'value', params.filters[0].value);
				return dummy_jsons.test_individuals_search_results[params.filters[0].value];

			}

			/* ========================================= */

			init();

		}]);
