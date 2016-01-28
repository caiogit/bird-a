'use strict';

/**
 * Created by caio on 23/01/16.
 */

angular.module('birdaApp')
	.directive('bDateInput', function() {
		return {
			restrict: 'E',
			replace: 'true',
			templateUrl: '/views/directives/date-input.html',
			scope: {
				field: '=formField',
				individual: '='
			},
			controller: [ '$scope', '$element', '$attrs', '$transclude', '$q',
				function($scope, $element, $attrs, $transclude, $q) {
					/* Instantiate the prototype controller */
					var cField = new FieldController($scope, $element, $attrs, $transclude, $q);

					/* Set the default value */
					var defaultValue;
					if (typeof cField.field.default === 'undefined' || cField.field.default === '') {
						defaultValue = new Date();
					} else {
						defaultValue = new Date(cField.field.default);
					}
					cField.setDefaultValue(defaultValue);

					// TODO: Retrieve next configuration from ontology

					/* Set Datepicker options */
					$scope.dateOptions = {
						formatYear: 'yy',
						startingDay: 1
					};

					/* Set Min and Max Date */
					cField.minDate = null;
					cField.maxDate = null;

					/* Set the date format */
					cField.format = 'dd/MM/yyyy';

					/* Rules for disabling specific days */
					cField.disabled = function(date, mode) {
						// Ex: disable weekend selection:
						//return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
						return false;
					};

					/* Set the popup initial state and the function for altering it */
					cField.datePopup = {
						opened: false
					};

					cField.openPopup = function() {
						cField.datePopup.opened = true;
					};

					/* Initialize controller */
					cField.init();
				}
			],
			controllerAs: 'cField'
		};
});
