'use strict';

/**
 * Created by caio on 28/12/15.
 */

angular.module('birdaApp')
	.service('formsService', function() {
		this.query = null;
		this.forms = null;

		this.retrieveForms = function() {
			this.forms = this.forms_test1;
		};

		/* ========================================= */

		this.forms_test1 = {
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
	});
