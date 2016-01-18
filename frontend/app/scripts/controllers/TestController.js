'use strict';

/**
 * Created by caio on 16/01/16.
 */

angular.module('birdaApp')
	.controller('TestController', ['$scope', '$q', '$resource', 'ConfigService',
		function ($scope, $q, $resource, ConfigService) {
			var self = this;
			var config = ConfigService.getConf();

			/* ----------------------------------------- */

			function init() {

			}

			/* ========================================= */

			self.testResource = function() {
				var Resource = $resource(
					config.getBackendUri()+'/test/resource/echo/:echoId',
					{echoId:'@id'});

				var getRes = Resource.get({echoId:10, pippo:1, pluto:2});
				//console.log(res);
				getRes.$promise.then(
					function(response) {
						console.log('Get Ok',response);
					},
					function(error) {
						console.log('Get Ko',error);
					}
				);

				var payload = {};
				payload.a = 'a';
				payload.b = 'b';
				var postRes = Resource.save({echoId:10, pippo:1, pluto:2}, payload);
				//console.log(res);
				postRes.$promise.then(
					function(response) {
						console.log('Post Ok',response);
					},
					function(error) {
						console.log('Post Ko',error);
					}
				);
			};

			/* ========================================= */

			init();

		}]);
