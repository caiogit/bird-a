'use strict';

/**
 * @ngdoc function
 * @name birdaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the birdaApp
 */
angular.module('birdaApp')
	.controller('FormsListController', ['$scope', 'formsService',
		function ($scope, formsService) {
			var self = this;
			self.forms = null;

			self.retrieveForms = function() {
				formsService.retrieveForms();
				self.forms = formsService.forms;
			};

			/* ========================================= */

			// Initialization
			(function init() {

            	self.retrieveForms();
				console.log(self);
				console.log(self.forms);

			})();
		}]);

