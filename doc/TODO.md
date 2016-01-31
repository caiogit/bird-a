# Todo

## Backend
 
 - `create_test_ontologies`: 
    - Migrate utility functions to storage.utilies
    - Add local_name management
        -  Create an example
    - Add Forms and fields
    - Make the script run with pyramid configuration
    - Make write the files in /db

 - Make `scripts/initialize_db.py` running
 
## Frontend

 - Portare tutti i dummy JSON in un unico file
    - Rimuovere questo file dal conteggio delle linee di codice 


## Generic

 - Ontology:
    - Check '/' instead of '#'
    - Add "hasBaseURI"
    - Add "hasLocalName"
        - Add child "hasLocalNameFields"
            - Comma separated URIs
        - Add child "hasLocalNameSeparator"
        - Add child "hasLocalNameTokenSeparator"
        - Add child "hasLocalNameRenderer"
	- Add "hasReferenceForm"
	    - Only for SubForms
	    - States what is the preferred form for inserting elements
    

## Low Priority

 - Align development.ini and production.ini
 - Link config files in config/
 - Create test ontologies
 - make run-fe Production
 
## Maybe next steps
 
 - Authentication
 - Authorization
 - Multilanguage
 - Individuals authors
 - Individuals modified time
 - Other output formats besides json (e.g. turtle, nt, etc.)
 - Storage on other databases besides files

 - Validation of produced individuals
 - Facilitated creation of birda widgets
 - Unittests
 