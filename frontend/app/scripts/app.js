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
			})
			.when('/contact', {
				templateUrl: 'views/contact.html',
			})
			.when('/forms-list', {
				templateUrl: 'views/forms.html',
			})
			.when('/individuals-list', {
				templateUrl: 'views/individuals.html',
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
