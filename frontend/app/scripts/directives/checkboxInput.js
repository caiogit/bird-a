'use strict';

/**
 * Created by caio on 23/01/16.
 */

angular.module('birdaApp')
	.directive('bCheckboxInput', function() {
		return {
			restrict: 'E',
			replace: 'true',
			templateUrl: '/views/directives/checkbox-input.html',
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
					if (typeof cField.field.default === 'undefined' ||
					    cField.field.default === '') {
						defaultValue = null;
					} else {
						defaultValue = cField.field.default;
					}
					cField.setDefaultValue(defaultValue);

					/* Initialize controller */
					cField.init();

					/* ----------------------------------------- */

					cField.is_in_values = function(value) {
						if (typeof cField.property.values !== 'undefined' &&
							cField.property.values.indexOf(value) > -1) {
							return true;
						} else {
							return false;
						}
					};

					/* ----------------------------------------- */

					cField.toggle_in_values = function(value) {

						if (cField.is_in_values(value)) {

							/* If in "values" remove "value" */
							for(var i in cField.property.values) {
								if (cField.property.values[i] === value) {
									cField.property.values.splice(i, 1);
									break;
								}
							}

						} else {

							/* If not in "values" add "value" */
							cField.property.values.push(value);
						}
					};
				}
			],
			controllerAs: 'cField'
		};
});
