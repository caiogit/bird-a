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
			this.individuals = null;
			this.found = false;
			this.valid = false;

			this.testData_person1 = {
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

			this.testData_person2 = this.testData_person1;

			this.testData_fuff = {
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

			this.setTestData = function(form) {
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

			this.isValid = function() {
				return this.individuals !== null;
			};

			this.hasValues = function() {
				return this.individuals.individuals.length > 0;
			};

			this.renderInstList = function() {
				var query = $location.search();
				if (! ('form' in query) ) {
					this.individuals = null;
				} else {
					this.setTestData(query.form);
				}
			};
		}]);

