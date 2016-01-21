'use strict';

/**
 * Created by caio on 16/01/16.
 */

angular.module('birdaApp')
	.controller('TestController', ['$scope', '$q', '$resource', 'ConfigService', 'IndividualsFactory',
		function ($scope, $q, $resource, ConfigService, IndividualsFactory) {
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

			/* ----------------------------------------- */

			self.indiv1 = {};
			self.indiv2 = {};
			self.testInstancesFactory_active = false;

			self.testInstancesFactory = function() {
				var indivSrv1 = IndividualsFactory.getInstance();
				var indivSrv2 = IndividualsFactory.getInstance();

				self.indiv1 = indivSrv1.getIndividual();
				self.indiv2 = indivSrv2.getIndividual();

				indivSrv1.retrieveIndividual('http://ex.com/john-max-smith','');
				indivSrv2.retrieveIndividual('http://ex.com/john-max-smith-2','');

				self.testInstancesFactory_active = true;
			};
			/* ========================================= */

			init();

		}]);
