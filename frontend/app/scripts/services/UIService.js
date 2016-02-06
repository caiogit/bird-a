'use strict';

/**
 * Created by caio on 13/01/16.
 */

angular.module('birdaApp')
	.service('UIService', ['$uibModal',
		function ($uibModal) {

			var self = this;

			/* ----------------------------------------- */

			function init() {

			}

			/* ========================================= */

			self.notifyError = function(response) {
				if (response.status === -1) {
					console.log('Status -1. What happened?', response);
					response.status = '<?>';
					response.statusText = 'Server Error';
					response.data = 'Problems with the server. Is it up and running?';
				}
				var modalInstance = $uibModal.open({
					animation: true,
					templateUrl: '/templates/modal_xhr_error.html',
					controller: function($scope) {
						$scope.response = response;
						$scope.close = function() {
							modalInstance.dismiss();
						};
					},
					size: 'sm'
				});
			};

			/* ========================================= */

			init();

		}]);
