'use strict';

/**
 * Created by caio on 28/12/15.
 */

angular.module('birdaApp')
	.service('ConfigService', ['$http', '$uibModal',
		function ($http, $uibModal) {

			var self = this;
			var config = CONFIG;

			/* ----------------------------------------- */

			function init() {
				self.loadConf();
			}

			/* ========================================= */

			self.loadConf = function() {
				/*
				$http.get('config.json').then(

					function success(response) {
						self.config = response.data;
						console.log('Configuration: ',self.config);
					},

					function error(response) {
						self.config = null;
						modalXhrError($uibModal, response);
					}
				);
				*/
			};

			self.getConf = function() {
				return config;
			};

			/* ========================================= */

			init();

		}]);
