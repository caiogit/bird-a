'use strict';

/**
 * Created by caio on 14/01/16.
 */

angular.module('birdaApp')
	.controller('EditController', ['$route', '$routeParams', '$location', 'FormService', 'IndividualsFactory',
		function ($route, $routeParams, $location, FormService, IndividualsFactory) {
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
				FormService.retrieveForm(self.form_uri).then(
					function (response) {
						/* Set type if individual is a new one */
						if (self.isNew) {
							self.individual.type = self.form.maps_type;
						}
					}
				);
				self.form = FormService.getForm();

				if (typeof $routeParams.individual !== 'undefined') {
					/* Retrieves individual */
					self.isNew = false;
					self.individual_uri = $routeParams.individual;
					IndividualService.retrieveIndividual(self.individual_uri, self.form_uri);
					self.individual = IndividualService.getIndividual();
				} else {
					/* Creates a brand new individual */
					self.isNew = true;
					self.individual_uri = '';
					IndividualService.createNew(self.form_uri);
					self.individual = IndividualService.getIndividual();
					if (self.form) {
						self.individual.type = self.form.maps_type;
					}
				}
			}

			/* ========================================= */

			self.saveIndividual = function() {
				// TODO: Form validation
				IndividualService.save();
			};

			/* ----------------------------------------- */

			self.discardChanges = function() {
				//window.history.back();
				//location.reload();
				$route.reload();
			};

			/* ----------------------------------------- */

			self.deleteIndividual = function() {
				// TODO: confirmation
				IndividualService.delete();
				$location.path('/individuals-list')
					.search('form', self.form_uri);
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
