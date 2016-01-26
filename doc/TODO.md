# Todo

## Backend
 
 - RDFContainer:
    - Oggetto che recepirà le triple lette con get_property e che in futuro potrà
      occuparsi di generare rdf in qualsiasi formato
 
 - get_property:
    - Input rdfc: istanza di RDFContainer
    - Popolare rdfc
    
 - FormFactory
    - Creare l'oggetto FormFactory con:
        - form_cache = {<uri>: FormWidget}
        - def getForm(uri): cerca nella cache altrimenti lo crea
        - def getAllFormsURIs()
        - def loadAllForms(): si avvale del metodo FormFactory.getAllForms
    - 
    - Connection:
        - Al termine della creazione dell'albero del form, la connessione deve
          essere chiusa (non verrà più usata né in lettura né in scrittura per tutto
          l'arco di vita dell'oggetto)s
      

## Frontend

 - Portare tutti i dummy JSON in un unico file
    - Rimuovere questo file dal conteggio delle linee di codice 


## Generic