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
					var self = $scope;
					self.property = {};

					/* Default value when filling values */
					self.emptyValue = '';

					/* ----------------------------------------- */

					function init() {
						// Get the property values
						getIndividualProperty($q, self.individual, self.field.property)
							.then(function(response) {
								self.property = response;
								self.fillValues();
							});
					}

					/* ========================================= */

					/**
					 * Fill "values" with self.emptyValue values in order
					 * to honor field.at_least
					 *
					 * Warning: function with implicit parameter (self.emptyValue)
					 */
					self.fillValues = function() {
						for (var i = self.property.values.length;
							 i < Math.max(1, self.field.at_least);
							 i++) {

							self.property.values.push(self.emptyValue);
						}
					};

					/* ----------------------------------------- */

					/**
					 *
					 * @param index
					 * @param value
					 */
					self.addValue = function(index, value) {
						if (typeof value === 'undefined') {
							value = '';
						}

						if (typeof index === 'undefined') {
							self.property.values.push(value);
						} else {

						}
					};

					/* ----------------------------------------- */

					/**
					 * Delete the value at "index" position in "values" array
					 *
					 * @param index {integer}
					 */
					self.delValue = function(index) {
						self.property.values.splice(index,1);
						self.fillValues();
					};

					/* ----------------------------------------- */

					/**
					 * Reset "values"
					 */
					self.delAllValues = function() {
						self.property.values = [];
						self.fillValues();
					};

					/* ----------------------------------------- */

					/**
					 * States if the field admits multiple values
					 *
					 * @returns {boolean}
					 */
					self.hasMultipleValues = function() {
						if (self.field.at_most != 1) {
							return true;
						} else {
							return false;
						}

					};

					/* ========================================= */

					init();

				}
			],
			controllerAs: 'cField'
		};
});
