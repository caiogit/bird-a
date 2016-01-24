'use strict';

/**
 * Created by caio on 14/01/16.
 */

angular.module('birdaApp')
	.controller('EditController', ['$route', '$routeParams', 'FormService', 'IndividualsFactory',
		function ($route, $routeParams, FormService, IndividualsFactory) {
			var self = this;

			self.form_uri = '';
			self.form = {};

			self.individual_uri = '';
			self.individual = {};

			self.isNew = true;

			var IndividualService = IndividualsFactory.getInstance();

			/* ----------------------------------------- */

			function init() {
				console.log('Initialized!');

				/* Retrieve form */
				if (typeof $routeParams.form === 'undefined') {
					alert('Missing parameter: "form"');
					$window.history.back();
				}

				self.form_uri = $routeParams.form;
				self.form = FormService.getForm();
				FormService.retrieveForm(self.form_uri);

				/* Retrieve individual if existent */
				if (typeof $routeParams.individual !== 'undefined') {
					self.isNew = false;
					self.individual_uri = $routeParams.individual;
					self.individual = IndividualService.getIndividual();
					IndividualService.retrieveIndividual(self.individual_uri, self.form_uri);
				} else {
					self.isNew = true;
				}
			}

			/* ========================================= */

			self.saveIndividual = function() {
				alert('Saved');
			};

			/* ----------------------------------------- */

			self.discardChanges = function() {
				//window.history.back();
				//location.reload();
				$route.reload();
			};

			/* ----------------------------------------- */

			self.deleteIndividual = function() {
				alert('Deleted');
			};


			/* ----------------------------------------- */

			/**
			 * Search "individual" for the specified property occurrence
			 * in properties and returns it
			 *
			 * @param property String containing property uri
			 */
			//self.getIndividualProperty = function(property) {
			//	self.individual.$promise.then(
			//		function (response) {
			//			var propertyObj = null;
			//
			//			console.log("OOKE", self.individual);
			//
			//			angular.forEach(self.individual.properties,
			//				function (value, key) {
			//					console.log(value.uri);
			//					if (value.uri === property) {
			//						propertyObj = value;
			//					}
			//				});
			//			console.log("BOOKE", propertyObj);
			//
			//			if (!(propertyObj)) {
			//				throw new Error('Property "' + property + '" not found!');
			//			}
			//
			//			return propertyObj;
			//		}, null);
			//};

			/* ========================================= */

			init();

		}]);
