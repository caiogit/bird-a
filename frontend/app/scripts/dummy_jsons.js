'use strict';

/**
 * Created by caio on 06/02/16.
 */

var dummy_jsons = {

	forms_test_1: {
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
	},

	form_test_1: {
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
				'w_type': 'TextInput',
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
				'w_type': 'TextInput',
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
				'w_type': 'RadioInput',
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
				'widget_uri': 'http://birda.com/person-birthdate-1',
				'w_type': 'DateInput',
				'property': 'http://xmlns.com/foaf/0.1/birthDate',
				'label': 'Data di nascita',
				'description': 'Quando è nata questa persona?',
				'placeholder': 'es. 19/05/1985',
				'at_least': 1,
				'at_most': 1,
				'validation': {
					'required': true
				}
			},
			{
				'widget_uri': 'http://birda.com/person-knows-1',
				'w_type': 'SubForm',
				'maps_property': 'http://xmlns.com/foaf/0.1/knows',
				'maps_type': 'http://xmlns.com/foaf/0.1/',
				'label': 'Persone conosciute',
				'description': '',
				'at_least': 0,
				'at_most':50,

				'fields': [
					{
						'widget_uri': 'http://birda.com/person-givenName-1',
						'w_type': 'TextInput',
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
						'w_type': 'TextInput',
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
	},

	test_individuals_search_person_results: {
		'individuals': [
			{
				'uri': 'http://ex.com/john-max-smith-01',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-02',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-03',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-04',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-05',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-06',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-07',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-08',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-09',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-10',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-11',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-12',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-13',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-14',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-15',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-16',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-17',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-18',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			},
			{
				'uri': 'http://ex.com/john-max-smith-19',
				'type': 'http://xmlns.com/foaf/0.1/Person',
				'label': 'John Max Smith',
				'description': 'Famous actor'
			}
		]
	},

	test_individuals_search_fuff_results: {
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
	},

	test_individuals: {
		'http://ex.com/john-max-smith-01': {
			'individuals': [
				{
					'uri': 'http://ex.com/john-max-smith',
					'type': 'http://xmlns.com/foaf/0.1/Person',
					'lang': 'en',
					'label': 'John Max Smith',
					'description': 'Famous actor',
					'last_modified': '2015-11-25 14:33:01',
					'authors': [
						{
							'uri': 'http://bigio-bagio.it#me',
							'label': 'Bigio Bagio'
						}
					],
					'properties': [
						{
							'uri': 'http://xmlns.com/foaf/0.1/givenName',
							'values': ['John', 'Max']
						},
						{
							'uri': 'http://xmlns.com/foaf/0.1/familyName',
							'values': ['Smith']
						}
					]
				}
			]
		},

		'http://ex.com/john-max-smith-02': {
			'individuals': [
				{
					'uri': 'http://ex.com/john-max-smith-2',
					'type': 'http://xmlns.com/foaf/0.1/Person',
					'lang': 'en',
					'label': 'John Max Smith Senior',
					'description': 'Famous singer',
					'last_modified': '2010-01-25 08:33:01',
					'authors': [
						{
							'uri': 'http://bigio-bagio.it#me',
							'label': 'Bigio Bagio'
						}
					],
					'properties': [
						{
							'uri': 'http://xmlns.com/foaf/0.1/givenName',
							'values': ['John', 'Max', 'Senior']
						},
						{
							'uri': 'http://xmlns.com/foaf/0.1/familyName',
							'values': ['Smith']
						},
						{
							'uri': 'http://xmlns.com/foaf/0.1/birthDate',
							'values': []
						}
					]
				}
			]
		}
	}

};
