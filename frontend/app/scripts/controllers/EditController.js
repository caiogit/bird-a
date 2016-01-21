'use strict';

/**
 * Created by caio on 14/01/16.
 */

angular.module('birdaApp')
	.controller('EditController', ['$scope', '$resource',
		function ($scope) {
			var self = this;
			self.forms = null;

			/* ----------------------------------------- */

			function init() {
				var Instance = $resource(config.buildApiUri('/api/v1/individuals/:instanceUri'), {formUri:'@form_uri'});
			}

			/* ========================================= */



			/* ========================================= */

			init();

		}]);
