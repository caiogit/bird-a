'use strict';

/**
 * Created by caio on 11/01/16.
 */

/* -------------------------------------------------------------------------- */

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
		size: 'md'
	});
}

/* -------------------------------------------------------------------------- */

/**
 * Clear the given object
 * @param obj
 */
function clearObject(obj) {
	if (angular.isArray(obj)) {
		/* Arrays */
		while (obj.pop(0)) {}

	} else if (angular.isObject(obj)) {
		/* Objects */
		for (var member in obj) {
			delete obj[member];
		}
	} else {

		throw Error('Object "'+obj+'" not implemented');
	}
}

/* -------------------------------------------------------------------------- */

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

/* -------------------------------------------------------------------------- */

/**
 * Search "individual" for the specified property occurrence
 * in properties and returns it
 *
 * @param individual Individual object returned by the IndividualService
 * @param propertyUri String containing property uri
 */
function getIndividualProperty($q, individual, propertyUri) {
	var defer = $q.defer();

	individual.$promise.then(
		function (response) {
			var propertyObj = null;

			angular.forEach(individual.properties,
				function (value, key) {
					if (value.uri === propertyUri) {
						propertyObj = value;
					}
				});
			//console.log("Property "+propertyUri, propertyObj);

			/* If property was not found, then creates it */
			if (!(propertyObj)) {
				//throw new Error('Property "' + propertyUri + '" not found!');
				console.log('Waring: property "' + propertyUri + '" not found. Creating it.');
				propertyObj = {
					'uri': propertyUri,
					'values': []
				};
				individual.properties.push(propertyObj);
			}

			defer.resolve(propertyObj);

		}, null);

	//console.log('Property premise',defer.promise);
	return defer.promise;
}

/* -------------------------------------------------------------------------- */

/**
 * Simple assert implementation
 *
 * @param condition
 * @param message
 */
function assert(condition, message) {
	if (!condition) {
		message = message || "Assertion failed";
		if (typeof Error !== "undefined") {
			throw new Error(message);
		}
		throw message; // Fallback
	}
}

/* -------------------------------------------------------------------------- */

function FieldController($scope, $element, $attrs, $transclude, $q) {
	var self = $scope;
	self.property = {};

	/* Default value when filling values */
	self.defaultValue = '';

	/* ----------------------------------------- */

	self.init = function() {
		// Get the property values
		getIndividualProperty($q, self.individual, self.field.property)
			.then(function(response) {
				self.property = response;
				self.fillValues();
			});
	};

	/* ========================================= */

	/**
	 * Set the default value
	 *
	 * @param value
	 */
	self.setDefaultValue = function(value) {
		self.defaultValue = value;
	};

	/* ----------------------------------------- */

	/**
	 * Fill "values" with self.emptyValue values in order
	 * to honor field.at_least
	 *
	 * Warning: function with implicit parameter (self.emptyValue)
	 */
	self.fillValues = function() {
		for (var i = self.property.values.length;
			 i < Math.max(1, self.field.at_least);
			 i++) {

			self.property.values.push(self.defaultValue);
		}
	};

	/* ----------------------------------------- */

	/**
	 *
	 * @param index
	 * @param value
	 */
	self.addValue = function(index, value) {
		if (typeof value === 'undefined') {
			value = self.defaultValue;
		}

		if (typeof index === 'undefined') {
			self.property.values.push(value);
		} else {
			// TODO
			throw Error('Not implemented');
		}
	};

	/* ----------------------------------------- */

	/**
	 * Delete the value at "index" position in "values" array
	 *
	 * @param index {integer}
	 */
	self.delValue = function(index) {
		self.property.values.splice(index,1);
		self.fillValues();
	};

	/* ----------------------------------------- */

	/**
	 * Reset "values"
	 */
	self.delAllValues = function() {
		self.property.values = [];
		self.fillValues();
	};

	/* ----------------------------------------- */

	/**
	 * States if the field admits multiple values
	 *
	 * @returns {boolean}
	 */
	self.hasMultipleValues = function() {
		if (self.field.at_most !== 1) {
			return true;
		} else {
			return false;
		}

	};

	/* ========================================= */

	/* Should be called once the controller has been configurated */
	//init();

	return self;
}
