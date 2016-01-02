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
    - **(D)P formService**: FormService created through FormFactory
    - **(D) form**:
        - from `formService.form`
    - **(D)P individualService**: IndividualService created through IndividualFactory
    - **(D) individual**:
        - from `individualService.form`
 
    - **(F)P initFormService()**: instantiates _formService_
    - **(F)P initIndividualService()**: instantiates _individualService_

    - **(F) save()**:
        - put or post instance to the server
        - put or post subForm instances to the server
- 

## Directives

- TextInput
- DateInput
- SubForm


## Services

- Forms:
    - **(D)P forms**: list of all forms
        - from `/api/v1/forms`
    - **(F) getForms**: get _forms_
    - **(F) retrieveForms**: retrieve forms list from server


- IndividualsSearch:
    - **(D)P params**: 
        - from `/api/v1/individuals/search`
    - **(D)P results**:
        - form `/api/v1/individuals/search`
  
    - **(F) clean()**: clean _params_ and _results_
    - **(F) addProperty(property)**: add _property_ to the properties array in _params_
    - **(F) addFilter(filter)** add _filter_ to the filters array in _params_
    - **(F) addOrderBy(orderBy)** add _orderBy_ to the order by array in _params_
    - **(F) search()**: Using _params_ retrieves _results_ from server
    - **(F) getResults()**: get _results_

## Factories

- Individual(individualUri='', formUri=''):
    - **(D)P individualUri**: not required
    - **(D)P formUri**: not required
    - **(D)P individual**: data
        - from `/api/v1/individuals/{individual_uri}?form={form}`

    - **(F) retrieveIndividual()**: retrieve _individual_ from server
    - **(F) putIndividual()**: put _individual_ to the server
        - updates _individual_ e _individualUri_
    - **(F) postIndividual()**: post individual to the server
        - updates _individual_ e _individualUri_
    - **(F) getIndividual**: get _individual_


- Form (formUri):
    - **(D)P formUri**: required
    - **(D)P form**: data necessary in order to render the form
        - from `/api/v1/forms/{form_uri}`
  
    - **(F) retrieveForm()**: get form from the server
    - **(F) getForm()**: get _form_


- PropertyDropdown(propertyUri, subjectType=''):
    - **(D)P propertyUri**: required
    - **(D)P subjectType**: not required
    - **(D)P values**: values retrieved from server
    
    - **(F) retrieveValues()**: get _values_ from server
    - **(F) getValues()**: get _values_