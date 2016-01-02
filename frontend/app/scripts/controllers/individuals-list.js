'use strict';

/**
 * @ngdoc function
 * @name birdaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the birdaApp
 */
angular.module('birdaApp')
	.controller('IndividualsListController', ['$scope', '$location',
		function ($scope, $location) {
			var self = this;

			self.individuals = null;
			self.found = false;
			self.valid = false;

			/* ----------------------------------------- */

			function init() {

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
					},
				]
			};

			self.setTestData = function(form) {
				this.valid = true;

				switch (form) {
					case 'http://www.birda.it/form-person-1':
						this.individuals = this.testData_person1;
						break;
					case 'http://www.birda.it/form-person-2':
						this.individuals = this.testData_person2;
						break;
					case 'http://www.birda.it/fuff':
						this.individuals = this.testData_fuff;
						break;
					default:
						console.log('Error! No such form: ' + form);
						this.individuals = null;
				}
			};

			/* ========================================= */

			init();

		}]);

