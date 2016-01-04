'use strict';

/**
 * @ngdoc function
 * @name birdaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the birdaApp
 */
angular.module('birdaApp')
	.controller('FormsListController', ['$scope', 'FormsService',
		function ($scope, formsService) {
			var self = this;
			self.forms = null;

			/* ----------------------------------------- */

			function init() {
				self.retrieveForms();
			}

			/* ========================================= */

			self.retrieveForms = function() {
				formsService.retrieveForms();
				self.forms = formsService.getForms();
			};

			/* ========================================= */

			init();

		}]);

