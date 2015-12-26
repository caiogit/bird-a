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
				templateUrl: 'views/home.html',
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

			.when('/404', {
				templateUrl: 'views/404.html',
			})
			.otherwise({
				redirectTo: '/404',
			});

		$locationProvider.html5Mode({
			enabled: true,
			requireBase: false
		});
	});
