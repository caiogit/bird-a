'use strict';

/**
 * Created by caio on 28/12/15.
 */

angular.module('birdaApp')
	.service('FormsService', ['$resource', 'ConfigService', 'UIService',
		function($resource, ConfigService, UIService) {

			var self = this;
			var config = ConfigService.getConf();

			//var query = null;
			var forms = null;

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
					forms = getDummyForms(config);
				} else {
					// TODO
					forms = Forms.get();

					forms.$promise.then(
						function(response) {
							console.log(response);
						},
						UIService.notifyError);
					//forms.$promise.then(null,function(error) {console.log("Error!!",error);});
				}

			};

			function getDummyForms() {
				return self.forms_Test1;
			}

			function getRealForms(config) {
				return $http.get('config.json').then(

					function success(response) {
						console.log('Configuration: ',self.config);
						return response.data;
					},

					function error(response) {
						modalXhrError($uibModal, response);
						return $q.reject(response.data);
					}
				);
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
