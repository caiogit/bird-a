'use strict';

/**
 * @ngdoc function
 * @name birdaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the birdaApp
 */
angular.module('birdaApp')
	.controller('FormsListController', ['$scope',
		function ($scope) {
			this.forms = {
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
		}]);

