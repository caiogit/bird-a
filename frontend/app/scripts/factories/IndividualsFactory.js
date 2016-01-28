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
					return self.test_individuals[individualUri].individuals[0];
				}

				/* ========================================= */

				self.test_individuals = {
					'http://ex.com/john-max-smith-01': {
						'individuals': [
							{
								'uri': 'http://ex.com/john-max-smith',
								'type': 'http://xmlns.com/foaf/0.1/Person',
								'lang': 'en',
								'label': 'John Max Smith',
								'description': 'Famous actor',
								'last_modified': '2015-11-25 14:33:01',
								'authors': [
									{
										'uri': 'http://bigio-bagio.it#me',
										'label': 'Bigio Bagio'
									}
								],
								'properties': [
									{
										'uri': 'http://xmlns.com/foaf/0.1/givenName',
										'values': ['John', 'Max']
									},
									{
										'uri': 'http://xmlns.com/foaf/0.1/familyName',
										'values': ['Smith']
									}
								]
							}
						]
					},

					'http://ex.com/john-max-smith-02': {
						'individuals': [
							{
								'uri': 'http://ex.com/john-max-smith-2',
								'type': 'http://xmlns.com/foaf/0.1/Person',
								'lang': 'en',
								'label': 'John Max Smith Senior',
								'description': 'Famous singer',
								'last_modified': '2010-01-25 08:33:01',
								'authors': [
									{
										'uri': 'http://bigio-bagio.it#me',
										'label': 'Bigio Bagio'
									}
								],
								'properties': [
									{
										'uri': 'http://xmlns.com/foaf/0.1/givenName',
										'values': ['John', 'Max', 'Senior']
									},
									{
										'uri': 'http://xmlns.com/foaf/0.1/familyName',
										'values': ['Smith']
									},
									{
										'uri': 'http://xmlns.com/foaf/0.1/birthDate',
										'values': []
									}
								]
							}
						]
					}
				};

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
