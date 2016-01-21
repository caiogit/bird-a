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

/**
 * Clear the given object (doesn't handle arrays, at the moment)
 * @param obj
 */
function clearObject(obj) {
	for (var member in obj) {
		delete obj[member];
	}
}

/**
 * Set the "obj" with the content of "new_obj" without breaking references to "obj"
 * @param obj The existent object to be reset
 * @param newObj The source object
 * @param deepCopy (bool) Optional: make deep copy instead of copying reference
 */
function clearAndSetObject(obj, newObj, deepCopy) {
	clearObject(obj);
	//for (var member in newObj) {
	//	if (deepCopy) {
	//		obj[member] = angular.copy(newObj[member]);
	//	} else {
	//		obj[member] = newObj[member];
	//	}
	//}
	if (deepCopy) {
		angular.merge(obj, newObj);
	} else {
		angular.extend(obj, newObj);
	}
}
