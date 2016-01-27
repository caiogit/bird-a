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
			var form = {};

			var Form = $resource(config.buildApiUri('/forms/:formUri'), {formUri:'@form_uri'});

			/* ----------------------------------------- */

			function init() {

			}

			/* ========================================= */

			self.getForm = function() {
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
						console.log('Form: ',form);
					}, config.dummyWaitTime);

					return defer.promise;

				} else {

					form = Form.get({formUri:formUri});

					form.$promise.then(
						function(response) {
							console.log(response);
							console.log('Form: ',response);
						},
						UIService.notifyError);

					return form.$promise;
				}

			};

			function getDummyForm(config) {
				return self.form_Test1;
			}

			/* ========================================= */

			self.form_Test1 = {
				'form_uri': 'http://birda.com/form-person-1',
				'maps_type': 'http://xmlns.com/foaf/0.1/',
				'base_uri': 'http://ex.com/',
				'label': 'FOAF:Person Light',
				'description': 'Insert people here',
				'label_property': 'http://www.w3.org/2004/02/skos/core#prefLabel',
				'descr_property': 'http://www.w3.org/2000/01/rdf-schema#comment',
				'lang': 'it',
				'fields': [
					{
						'widget_uri': 'http://birda.com/person-givenName-1',
						'w_type': 'text-input',
						'property': 'http://xmlns.com/foaf/0.1/givenName',
						'label': 'Nome',
						'description': 'Usare un campo diverso per ogni nome',
						'default': '',
						'placeholder': 'Nome della persona (ad es. "Pino")',
						'at_least': 1,
						'validation': {
							'max_length':25
						}
					},
					{
						'widget_uri': 'http://birda.com/person-familyName-1',
						'w_type': 'text-input',
						'property': 'http://xmlns.com/foaf/0.1/familyName',
						'label': 'Cognome',
						'description': 'Usare un campo diverso per ogni cognome',
						'default': 'Labislacco',
						'placeholder': 'Cognome della persona (ad es. "Rossi")',
						'at_least': 1,
						'at_most': 1,
						'validation': {
							'max_length':25
						}
					},
					{
						'widget_uri': 'http://birda.com/person-gender-1',
						'w_type': 'radio-input',
						'property': 'http://xmlns.com/foaf/0.1/gender',
						'label': 'Genere',
						'description': '',
						'placeholder': '',
						'at_least': 1,
						'choices': [
							{
								'label': 'Uomo',
								'description': '',
								'type': 'xsd:string',
								'value': 'http://w3id.com/gender-ontology/male'
							},
							{
								'label': 'Donna',
								'description': '',
								'type': 'xsd:string',
								'value': 'http://w3id.com/gender-ontology/female'
							},
							{
								'label': 'Non specificato',
								'description': '',
								'type': 'xsd:string',
								'value': 'http://w3id.com/gender-ontology/not-specified',
								'default': true
							}
						],
						'validation': {
							'required': true
						}
					},
					{
						'widget_uri': 'http://birda.com/person-knows-1',
						'w_type': 'subform',
						'maps_property': 'http://xmlns.com/foaf/0.1/knows',
						'maps_type': 'http://xmlns.com/foaf/0.1/',
						'label': 'Persone conosciute',
						'description': '',
						'at_least': 0,
						'at_most':50,

						'fields': [
							{
								'widget_uri': 'http://birda.com/person-givenName-1',
								'w_type': 'text-input',
								'property': 'http://xmlns.com/foaf/0.1/givenName',
								'label': 'Nome',
								'description': 'Usare un campo diverso per ogni nome',
								'default': '',
								'placeholder': 'Nome della persona (ad es. "Pino")',
								'at_least': 1,
								'validation': {
									'max_length':25
								}
							},
							{
								'widget_uri': 'http://birda.com/person-familyName-1',
								'w_type': 'text-input',
								'property': 'http://xmlns.com/foaf/0.1/familyName',
								'label': 'Cognome',
								'description': 'Usare un campo diverso per ogni cognome',
								'default': '',
								'placeholder': 'Cognome della persona (ad es. "Rossi")',
								'at_least': 1,
								'validation': {
									'max_length':25
								}
							}
						]
					}
				],
				'local_name':{
					'fields': ['givenName', 'familyMame'],
					'localNameSeparator': '_',
					'tokenSeparator': '(\\\.|\\\s|-)+',
					'localNameRenderer': 'lowercase'
				}
			};

			/* ========================================= */

			init();
		}]);
