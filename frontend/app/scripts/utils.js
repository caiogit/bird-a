'use strict';

/**
 * Created by caio on 11/01/16.
 */

/**
 * Creates a modal with the XHR Error infos
 * @param $uibModal
 * @param response
 */
function modalXhrError($uibModal, response) {
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
}
