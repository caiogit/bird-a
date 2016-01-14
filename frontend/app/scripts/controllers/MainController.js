'use strict';

/**
 * @ngdoc function
 * @name birdaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the birdaApp
 */
angular.module('birdaApp')
	.controller('MainController', ['$location', 'ConfigService',
		function ($location, ConfigService) {
			var self = this;

			/* ----------------------------------------- */

			function init() {
				console.log(ConfigService.config);
			}

			/* ========================================= */

			self.isCurrentPage = function(page) {
				return $location.path() === page;
			};

			/* ========================================= */

			init();
		}]);

