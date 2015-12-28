## Controllers

- Main: general infos
- FormsList

## Services

- Forms:
 - (D) Forms: list of all forms
  - from /api/v1/forms
 - (F) getForms: retrive forms list from server
 
- IndividualsSearch:
 - (D) Params: 
  - from /api/v1/individuals/search
 - (D) Results:
  - form /api/v1/individuals/search
  
 - (F) clean(): clean Params and Results
 - (F) addProperty(property)
 - (F) addFilter(filter)
 - (F) addOrderBy(orderBy)
 - (F) search(): Uses Params and produce Results

## Factories

- Form (form_uri, individual_uri):
 - (D) form_uri
 - (D) form: data necessary in order to render the form
  - from /api/v1/forms/{form_uri}
 - (D) individual_uri
 - (D) individual: data rendered in the form
  - from /api/v1/individuals/{individual_uri}?form={form}
 - (F) getForm(): get form from the server
 - (F) getIndividual(): get individual from the server
 - (F) putIndividual(): put individual to the server
 - (F) postIndividual(): post individual to the server
