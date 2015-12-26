'use strict';

/**
 * @ngdoc function
 * @name birdaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the birdaApp
 */
angular.module('birdaApp')
	.controller('MainController', ['$location',
		function ($location) {
			this.isCurrentPage = function(page) {
				return $location.path() === page;
			};
		}]);

