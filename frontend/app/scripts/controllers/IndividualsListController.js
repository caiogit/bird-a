'use strict';

/**
 * @ngdoc function
 * @name birdaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the birdaApp
 */
angular.module('birdaApp')
	.controller('IndividualsListController', ['$location', 'FormsService', 'IndividualsSearchService',
		function ($location, formsService, individualsSearchService) {
			var self = this;

			self.individuals = null;
			self.formUri = null;
			self.form = null;

			self.found = false;
			self.valid = false;
			self.error = '';
			self.messages = [];

			/* ----------------------------------------- */

			function init() {
				var query = $location.search();

				if ('form' in query) {
					self.formUri = query.form;
					self.form = formsService.getFormByUri(self.formUri);
					if (! self.form) {
						self.error = 'Form "'+self.formUri+'" not found!';
						self.valid = false;
					} else {
						individualsSearchService.clean();
						individualsSearchService.addFilter({
							'property': RDF_TYPE,
							'value': self.form.type,
							'match': 'exact'
						});
						individualsSearchService.search();
						self.individuals = individualsSearchService.getResults().individuals;
						self.valid = true;
					}
				} else {
					self.valid = false;
					self.error = '"form" key not in query string';
				}
			}

			/* ========================================= */

			self.isValid = function() {
				return self.individuals !== null;
			};

			self.hasValues = function() {
				return self.individuals.length > 0;
			};

			self.renderInstList = function() {
				var query = $location.search();
				if (! ('form' in query) ) {
					self.individuals = null;
				} else {
					self.setTestData(query.form);
				}
			};

			self.addMessage = function(message) {
				var acceptedTypes = ['success', 'warning', 'error'];

				if ( (typeof message !== 'object') || (message === null)  ) {
					throw 'IndividualsListController: "message" should be a not null object';
				}
				if ( (! ('type' in message)) || (! (_.contains(acceptedTypes, message.type)) )) {
					throw 'IndividualsListController: "message" should have a "type" property (admitted values: '+acceptedTypes.join(', ')+')';
				}
				if ( ! ('message' in message) ) {
					throw 'IndividualsListController: "message" should have a "order" property';
				}

				self.messages.push(message);
			};

			/* ========================================= */

			self.newIndividual = function() {
				$location.path(
					'/edit?form='+self.form.uri
				);
			};

			self.editIndividual = function(individualUri) {
				$location.path(
					'/edit?form='+self.form.uri+'&individual='+individualUri
				);
			};

			self.deleteIndividual = function(individualUri) {
				var success = false;

				/* TODO: Remove debug code here */

				var removedIndividual;
				if (_.endsWith(individualUri,'1')) {
					removedIndividual = [];
				} else {
					removedIndividual = _.remove(self.individuals, {'uri': individualUri});
				}

				if (removedIndividual.length > 0) {
					success = true;
				}

				if (success) {
					self.addMessage({
						'type': 'success',
						'message': 'Instance "'+individualUri+'" deleted'
					});
				} else {
					self.addMessage({
						'type': 'error',
						'message': 'Failed to delete instance "'+individualUri+'"'
					});
				}
			};

			/* ========================================= */

			init();

		}]);

