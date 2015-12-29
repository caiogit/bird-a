## Controllers

- Main: general infos
    - **isCurrentPage(page)**: true if "page" is the current page


- FormsList:
    - **(I) FormsService**
 

- IndividualsList:
    - **(I) FormsService**
    - **(I) IndividualsSearch**
 
    - **(D) type**: rdf type of individuals
    - **(D) individuals**: list of all individuals
 
    - **(F) setType(type)**: set _type_
    - **(F) getIndividuals()**: get _individuals_ from server
        - from `/api/v1/individuals/search`


- Edit:
    - **(I) FormFactory**
 
    - **(D) formUri**: required (retrieved from query string)
    - **(D) individualUri**: not required (retrieved from query string)
    - **(D) formService**
 
    - **(I) setFormService()**

## Services

- Forms:
    - **(D) forms**: list of all forms
        - from `/api/v1/forms`
    - **(F) getForms**: retrieve forms list from server


- IndividualsSearch:
    - **(D) params**: 
        - from `/api/v1/individuals/search`
    - **(D) results**:
        - form `/api/v1/individuals/search`
  
    - **(F) clean()**: clean _params_ and _results_
    - **(F) addProperty(property)**: add _property_ to the properties array in _params_
    - **(F) addFilter(filter)** add _filter_ to the filters array in _params_
    - **(F) addOrderBy(orderBy)** add _orderBy_ to the order by array in _params_
    - **(F) search()**: Using _params_ retrieves _results_ from server

## Factories

- Form (form_uri, individual_uri):
    - **(D)P form_uri**: required
    - **(D) form**: data necessary in order to render the form
        - from `/api/v1/forms/{form_uri}`
    - **(D)P individual_uri**: not required. If null the individual is intended to
 	  be a new individual
    - **(D) individual**: data rendered in the form
        - from `/api/v1/individuals/{individual_uri}?form={form}`
  
    - **(F) getForm()**: get form from the server
    - **(F) getIndividual()**: get individual from the server
    - **(F) putIndividual()**: put individual to the server
        - updates _individual_ e _individual_uri_
    - **(F) postIndividual()**: post individual to the server
        - updates _individual_ e _individual_uri_