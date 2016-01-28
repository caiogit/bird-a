# Todo

## Backend
 
 - `create_test_ontologies`: 
    - Migrate utility functions to storage.utilies
    - Add local_name management
        -  Create an example
    - Add Forms and fields
    - Make the script run with pyramid configuration
    - Make write the files in /db


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
    

## Low Priority

 - Align development.ini and production.ini
 - Link config files in config/
 - Create test ontologies
 - make run-fe Production