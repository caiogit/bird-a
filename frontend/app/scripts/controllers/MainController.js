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
			self.config = ConfigService.getConf();

			/* ----------------------------------------- */

			function init() {
			}

			/* ========================================= */

			self.isCurrentPage = function(page) {
				return $location.path() === page;
			};

			/* ========================================= */

			init();
		}]);

