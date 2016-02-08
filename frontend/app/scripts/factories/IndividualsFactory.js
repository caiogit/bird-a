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
				var formUri = '';

				var Individual = $resource(config.buildApiUri(
					'/individuals/:individual_uri'),
					{
						individual_uri: '@individual_uri',
						form_uri: '@form_uri',
						lang: '@lang'
					});

				/* ----------------------------------------- */

				function init() {

				}

				/* ========================================= */

				self.getIndividual = function() {
					return individual;
				};

				/* ----------------------------------------- */

				self.createNew = function(formUri) {

					self.formUri = formUri;

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

				self.retrieveIndividual = function(individualUri, form_uri) {
					formUri = form_uri;

					if (config.dummyData) {
						clearObject(individual);
						var defer = $q.defer();
						individual.$promise = defer.promise;

						// simulated async function
						$timeout(function() {
							angular.merge(individual, getDummyIndividual(config, individualUri, form_uri));
							defer.resolve(individual);
							console.log("Individual: ",individual);
						}, config.dummyWaitTime);

						return individual.$promise;

					} else {

						individual = Individual.get({
							individual_uri: individualUri,
							form_uri: form_uri,
							lang: config.lang
						});

						//var new_individual = Individual.get({
						//	individual_uri: individualUri,
						//	form_uri: form_uri,
						//	lang: config.lang
						//});
						//clearAndSetObject(individual, new_individual, true);

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

				/* ========================================= */

				self.save = function() {
					Individual.save({
							individual_uri: individual.uri,
							form_uri: formUri,
							lang: config.lang
						},
						{
							'individuals': [
								individual
							]
						},
						function(response) {
							//console.log(response);
							clearAndSetObject(individual, response.individuals[0]);
						},
						UIService.notifyError);
				};

				/* ----------------------------------------- */

				self.delete = function() {
					Individual.delete({
							individual_uri: individual.uri,
							form_uri: formUri,
							lang: config.lang
						},
						function(response) {
							//console.log(response);
							clearObject(individual);
						},
						UIService.notifyError);
				};

				/* ========================================= */

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
