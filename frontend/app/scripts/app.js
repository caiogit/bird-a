'use strict';

/**
 * @ngdoc overview
 * @name birdaApp
 * @description
 * # birdaApp
 *
 * Main module of the application.
 */
angular
	.module('birdaApp', [
		'ngAnimate',
		'ngCookies',
		'ngResource',
		'ngRoute',
		'ngSanitize',
		'ngTouch'
	])
	.config(function ($routeProvider, $locationProvider) {
		$routeProvider
			.when('/', {
				templateUrl: 'views/main.html',
				controller: 'MainCtrl',
				controllerAs: 'main'
			})
			.when('/contact', {
				templateUrl: 'views/contact.html',
			})
			.otherwise({
				redirectTo: '/'
			});

		$locationProvider.html5Mode({
			enabled: true,
			requireBase: false
		});
	});
