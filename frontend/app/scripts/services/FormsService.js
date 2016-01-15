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

			var Forms = $resource(config.buildApiUri('/forms'));

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
					forms = Forms.get();

					forms.$promise.then(
						function(response) {
							console.log(response);
						},
						UIService.notifyError);

					return forms.$promise;
				}

			};

			function getDummyForms() {
				return self.forms_Test1;
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

			self.forms_Test1 = {
				'forms': [
					{
						'uri': 'http://www.birda.it/form-person-1',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'FOAF Person Light',
						'description': 'Form for editing idividuals in the FOAF Ontology.\nLight version.'
					},
					{
						'uri': 'http://www.birda.it/form-person-2',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'FOAF Person Extended',
						'description': 'Form for editing idividuals in the FOAF Ontology.\nExtended version'
					},
					{
						'uri': 'http://www.birda.it/fuff',
						'type': 'http://xmlns.com/foaf/0.1/Fuff',
						'label': 'FUFF Object',
						'description': 'Nothing much here'
					}
				]
			};

			/* ========================================= */

			init();
		}]);
