'use strict';

/**
 * @ngdoc overview
 * @name birdaApp
 * @description
 * # birdaApp
 *
 * Main module of the application.
 */

/*
 * Constants declaration
 */
var RDF_TYPE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type';


/*
 * Angular initialization
 */
angular
	.module('birdaApp', [
		'ngAnimate',
		'ngCookies',
		'ngResource',
		'ngRoute',
		'ngSanitize',
		'ngTouch',
		'ui.bootstrap'
	])
	//.config(['$sceDelegateProvider',
	//	function($sceDelegateProvider) {
	//		$sceDelegateProvider.resourceUrlWhitelist([
	//			'self',
	//			'http://0.0.0.0:8000/**'
	//		]);
	//	}])
	.config(function ($routeProvider, $locationProvider) {
		$routeProvider
			.when('/', {
				templateUrl: 'views/home.html',
			})
			.when('/contact', {
				templateUrl: 'views/contact.html',
			})
			.when('/forms-list', {
				templateUrl: 'views/forms-list.html',
				//controller: 'FormsListController',
				//controllerAs: 'cFormsList',
			})
			.when('/individuals-list', {
				templateUrl: 'views/individuals-list.html',
			})
			.when('/contact', {
				templateUrl: 'views/contact.html',
			})
			.when('/edit', {
				templateUrl: 'views/edit.html',
			})

			.when('/test', {
				templateUrl: 'views/test.html',
			})
			.when('/404', {
				templateUrl: 'views/404.html',
				controller: [ '$location',
					function($location) {
						this.location = $location.url();
					}
				],
				controllerAs: 'c404',
			})
			.otherwise({
				redirectTo: '/404',
			});

		$locationProvider.html5Mode({
			enabled: true,
			requireBase: false
		});
	})
	.run(['$rootScope', 'ConfigService',
		function ($rootScope, ConfigService) {
			if (ConfigService.getConf().debug_logLocationChanges) {
				$rootScope.$on('$locationChangeStart', function (evt, absNewUrl, absOldUrl) {
					console.log('Location changed. Old: ', absOldUrl, ' New: ', absNewUrl, evt);
				});
			}
		}
	]);
