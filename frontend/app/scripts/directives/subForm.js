'use strict';

/**
 * Created by caio on 23/01/16.
 */

angular.module('birdaApp')
	.directive('bTextInput', function() {
		return {
			restrict: 'E',
			replace: 'true',
			templateUrl: '/views/directives/text-input.html',
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
					if (typeof cField.field.default === 'undefined') {
						defaultValue = '';
					} else {
						defaultValue = cField.field.default;
					}
					cField.setDefaultValue(defaultValue);

					/* Initialize controller */
					cField.init();
				}
			],
			controllerAs: 'cField'
		};
});
