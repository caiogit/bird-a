'use strict';

/**
 * @ngdoc function
 * @name birdaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the birdaApp
 */
angular.module('birdaApp')
	.controller('IndividualsListController', ['$location', 'FormsService', 'IndividualsSearchService',
		function ($location, formsService, individualsSearchService) {
			var self = this;

			self.individuals = null;
			self.formUri = null;
			self.form = null;

			self.found = false;
			self.valid = false;
			self.error = '';

			/* ----------------------------------------- */

			function init() {
				var query = $location.search();

				if ('form' in query) {
					self.formUri = query.form;
					self.form = formsService.getFormByUri(self.formUri);
					if (! self.form) {
						self.error = 'Form "'+self.formUri+'" not found!';
					} else {
						individualsSearchService.clean();
						individualsSearchService.addFilter({
							'property': RDF_TYPE,
							'value': self.form.type,
							'match': 'exact'
						});
						individualsSearchService.search();
						self.individuals = individualsSearchService.getResults().individuals;
					}
				} else {

				}
			}

			/* ========================================= */

			self.isValid = function() {
				return self.individuals !== null;
			};

			self.hasValues = function() {
				return self.individuals.individuals.length > 0;
			};

			self.renderInstList = function() {
				var query = $location.search();
				if (! ('form' in query) ) {
					self.individuals = null;
				} else {
					self.setTestData(query.form);
				}
			};

			/* ========================================= */

			/*
			self.testData_person1 = {
				'individuals': [
					{
						'uri': 'http://ex.com/john-max-smith',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'Description': 'Famous actor',
						'properties': []
					},
					{
						'uri': 'http://ex.com/john-max-smith',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'Description': 'Famous actor',
						'properties': []
					},
					{
						'uri': 'http://ex.com/john-max-smith',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'Description': 'Famous actor',
						'properties': []
					},
					{
						'uri': 'http://ex.com/john-max-smith',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'Description': 'Famous actor',
						'properties': []
					},
					{
						'uri': 'http://ex.com/john-max-smith',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'Description': 'Famous actor',
						'properties': []
					},
					{
						'uri': 'http://ex.com/john-max-smith',
						'type': 'http://xmlns.com/foaf/0.1/Person',
						'label': 'John Max Smith',
						'Description': 'Famous actor',
						'properties': []
					}
				]
			};

			self.testData_person2 = this.testData_person1;

			self.testData_fuff = {
				'individuals': [
					{
						'uri': 'http://ex.com/1111',
						'type': 'http://xmlns.com/foaf/0.1/Fuff',
						'label': 'Pippo',
						'Description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vitae nisl rutrum, placerat nisl ac.',
						'properties': []
					},
					{
						'uri': 'http://ex.com/2222',
						'type': 'http://xmlns.com/foaf/0.1/Fuff',
						'label': 'Pippo',
						'Description': 'Suspendisse non sapien tempus, cursus nisi at, lacinia justo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.',
						'properties': []
					}
				]
			};

			self.setTestData = function(form) {
				self.valid = true;

				switch (form) {
					case 'http://www.birda.it/form-person-1':
						self.individuals = self.testData_person1;
						break;
					case 'http://www.birda.it/form-person-2':
						self.individuals = self.testData_person2;
						break;
					case 'http://www.birda.it/fuff':
						self.individuals = self.testData_fuff;
						break;
					default:
						self.error = 'Form "'+self.formUri+'" unknown!';
						self.individuals = null;
				}
			};
			*/

			/* ========================================= */

			init();

		}]);

