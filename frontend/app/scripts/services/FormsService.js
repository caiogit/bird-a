'use strict';

/**
 * Created by caio on 28/12/15.
 */

angular.module('birdaApp')
	.service('FormsService', ['$resource', '$q', '$timeout', 'ConfigService', 'UIService',
		function($resource, $q, $timeout, ConfigService, UIService) {

			var self = this;
			var config = ConfigService.getConf();

			//var query = null;
			var forms = {};

			var Forms = $resource(config.buildApiUri('/forms'),{
				lang: '@lang'
			});

			/* ----------------------------------------- */

			function init() {
				self.retrieveForms();
			}

			/* ========================================= */

			self.getForms = function() {
				console.log('Forms',forms);
				return forms;
			};

			/* ----------------------------------------- */

			self.retrieveForms = function() {
				if (config.dummyData) {
					clearObject(forms);
					var defer = $q.defer();

					// simulated async function
					$timeout(function() {
						angular.extend(forms, getDummyForms(config));
						defer.resolve(forms);
					}, config.dummyWaitTime);

					return defer.promise;

				} else {
					//forms = Forms.get();
					clearAndSetObject(forms, Forms.get({
						lang:config.lang
					}));

					forms.$promise.then(
						function(response) {
							clearAndSetObject(forms, response);
							console.log(response);
						},
						UIService.notifyError);

					return forms.$promise;
				}

			};

			function getDummyForms() {
				return dummy_jsons.forms_test_1;
			}

			/* ----------------------------------------- */

			self.getFormByUri = function(formUri) {
				var ret = null;

				angular.forEach(forms.forms, function(form, key) {
					if (formUri === form.uri) {
						ret = form;
					}
				});

				return ret;
			};

			/* ========================================= */

			init();
		}]);
