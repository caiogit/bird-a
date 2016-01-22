'use strict';

/**
 * Created by caio on 14/01/16.
 */

angular.module('birdaApp')
	.controller('EditController', ['$routeParams', 'FormService', 'IndividualsFactory',
		function ($routeParams, FormService, IndividualsFactory) {
			var self = this;

			self.form_uri = '';
			self.form = {};

			self.individual_uri = '';
			self.individual = {};

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
					self.individual_uri = $routeParams.individual;
					self.individual = IndividualService.getIndividual();
					IndividualService.retrieveIndividual(self.individual_uri, self.form_uri);
				}
			}

			/* ========================================= */



			/* ========================================= */

			init();

		}]);
