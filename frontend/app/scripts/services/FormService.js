'use strict';

/**
 * Created by caio on 15/01/16.
 */

angular.module('birdaApp')
	.service('FormService', ['$resource', '$q', '$timeout', 'ConfigService', 'UIService',
		function($resource, $q, $timeout, ConfigService, UIService) {

			var self = this;
			var config = ConfigService.getConf();

			//var query = null;
			var form = null;

			var Form = $resource(config.buildApiUri('/forms/:formUri'), {formUri:'@form_uri'});

			/* ----------------------------------------- */

			function init() {

			}

			/* ========================================= */

			self.getForm = function() {
				console.log('Forms',form);
				return form;
			};

			/* ----------------------------------------- */

			self.retrieveForm = function(formUri) {

				if (config.dummyData) {
					clearObject(form);
					var defer = $q.defer();

					// simulated async function
					$timeout(function() {
						angular.extend(form, getDummyForm(config));
						defer.resolve(form);
					}, config.dummyWaitTime);

					return defer.promise;

				} else {

					form = Form.get({formUri:formUri});

					form.$promise.then(
						function(response) {
							console.log(response);
						},
						UIService.notifyError);

					return form.$promise;
				}

			};

			function getDummyForm() {
				return self.form_Test1;
			}

			/* ========================================= */

			self.form_Test1 = {
				// TODO
			};

			/* ========================================= */

			init();
		}]);
