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
				console.log(self);
				console.log(self.forms);
			}

			/* ========================================= */

			self.retrieveForms = function() {
				formsService.retrieveForms();
				self.forms = formsService.getForms();
			};

			/* ========================================= */

			init();

		}]);

