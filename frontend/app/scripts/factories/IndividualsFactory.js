'use strict';

/**
 * Created by caio on 16/01/16.
 */

angular.module('birdaApp')
	.factory('IndividualsFactory', ['$resource', '$q', '$timeout', 'ConfigService', 'UIService',
		function($resource, $q, $timeout, ConfigService, UIService) {
			var IndividualService = function() {
				var self = this;
				var config = ConfigService.getConf();

				var individual = {};

				var Individuals = $resource(config.buildApiUri(
					'/api/v1/individuals/:individualUri'),
					{individualUri: '@uri', formUri:'form_uri'});

				/* ----------------------------------------- */

				function init() {

				}

				/* ========================================= */

				self.getIndividual = function() {
					return individual;
				};

				/* ----------------------------------------- */

				self.createNew = function(type) {
					var defer = $q.defer();
					individual.$promise = defer.promise;

					angular.merge(individual, {
						'uri': '',
						'type': '',
						'lang': config.lang,
						'label': '',
						'description': '',
						'last_modified': null,
						'authors': [],
						'properties': []
					});

					defer.resolve(individual);
					return individual.$promise;
				};

				/* ----------------------------------------- */


				self.retrieveIndividual = function(individualUri, formUri) {

					if (config.dummyData) {
						clearObject(individual);
						var defer = $q.defer();
						individual.$promise = defer.promise;

						// simulated async function
						$timeout(function() {
							angular.merge(individual, getDummyIndividual(config, individualUri, formUri));
							defer.resolve(individual);
							console.log("Individual: ",individual);
						}, config.dummyWaitTime);

						return individual.$promise;

					} else {

						individual = Individuals.get({formUri:formUri});

						individual.$promise.then(
							function(response) {
								console.log(response);

								// In order to simplify following individual management,
								// we put in "individual" the first (and in this case
								// the only one) individual retrieved from the backend
								var tmpIndividual = angular.copy(individual.individuals[0]);
								clearAndSetObject(individual, tmpIndividual, true);
								console.log("Individual: ",individual);
							},
							UIService.notifyError);

						return individual.$promise;
					}

				};

				/* ----------------------------------------- */

				function getDummyIndividual(config, individualUri, formUri) {
					//console.log(individualUri);
					return dummy_jsons.test_individuals[individualUri].individuals[0];
				}

				/* ========================================= */

				init();
			};

			return {
				getInstance: function () {
					return new IndividualService();
				}
			};
		}
	]);
