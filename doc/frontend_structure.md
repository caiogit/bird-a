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


- PropertyDropdown:
    - **(I) PropertyDropdownFactory**
    
    - **(D) values**: values retrieved from server
        - from `/api/v1/values/{property_uri}`
    - **(D) propertyDropdownService**: PropertyDropdownService created through PropertyDropdownFactory
    
    - **(F) setPropertyDropdownService()**: instantiates _propertyDropdownService_


- Edit:
    - **(I) FormFactory**
 
    - **(D) formUri**: required (retrieved from query string)
    - **(D) individualUri**: not required (retrieved from query string)
    - **(D) formService**: FormService created through FormFactory
 
    - **(F) setFormService()**: instantiates _formService_


## Directives

- TextInput
- DateInput
- SubForm


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

- Form (formUri, individualUri=''):
    - **(D)P formUri**: required
    - **(D) form**: data necessary in order to render the form
        - from `/api/v1/forms/{form_uri}`
    - **(D)P individualUri**: not required. If null the individual is intended to
 	  be a new individual
    - **(D) individual**: data rendered in the form
        - from `/api/v1/individuals/{individual_uri}?form={form}`
  
    - **(F) getForm()**: get form from the server
    - **(F) getIndividual()**: get individual from the server
    - **(F) putIndividual()**: put individual to the server
        - updates _individual_ e _individualUri_
    - **(F) postIndividual()**: post individual to the server
        - updates _individual_ e _individualUri_
        
        
- PropertyDropdown(propertyUri, subjectType=''):
    - **(D)P propertyUri**: required
    - **(D)P subjectType**: not required
    - **(D) values**: values retrieved from server
    
    - **(F) getValues()**: get _values_ from server