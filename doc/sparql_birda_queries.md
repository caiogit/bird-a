# Prefix

```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX birda: <http://w3id.org/ontologies/bird-a/>
PREFIX birda-d: <http://pippo.it/birda-data/>
```

# First Tests

## Query all

```
SELECT ?s ?p ?o
WHERE {
    ?s ?p ?o .
}
```

# Forms

## List all forms

```
SELECT ?form ?property ?value
WHERE {
	VALUES ?property
	{
		birda:mapsType
		birda:hasLabel
		birda:hasDescription
	}
    ?form rdf:type birda:Form .
    ?form ?property ?value .
}
```


With "DESCRIBE":
```
DESCRIBE ?form
WHERE {
    ?form rdf:type birda:Form .
}
```

'''Warning!''': This query gives the cartesian product of the values relative to the form
```
SELECT ?form ?type ?label ?description
WHERE {
    ?form rdf:type birda:Form .
    ?form birda:mapsType ?type .
    OPTIONAL { ?form birda:hasLabel ?label . }
    OPTIONAL { ?form birda:hasDescription ?description . }
}
```

```
SELECT ?form ?type ?label ?description
WHERE {
    ?form rdf:type birda:Form .
    ?form birda:mapsType ?type .
    OPTIONAL { ?form birda:hasLabel ?label . }
    OPTIONAL { ?form birda:hasDescription ?description . }
}
```

```
SELECT ?form ?label
WHERE {
	?form rdf:type birda:Form .
	?form birda:hasLabel ?label .
	FILTER (langMatches(lang(?label), "EN")) .
}
```


```
SELECT ?form ?property ?value
WHERE {
	VALUES ?property
	{
	   birda:mapsType
	   birda:hasLabel
	   birda:hasDescription
	}
    ?form rdf:type birda:Form .
    ?form ?property ?value .
}
ORDER BY ?form ?property
```

# Individuals

```
SELECT ?ind ?name
WHERE { 
	?ind rdf:type foaf:Person ;
		 foaf:givenName ?name .
	FILTER (langMatches(lang(?name), "EN")) .
}
```

```
SELECT ?ind ?prop1 ?prop2
WHERE { 
	?ind rdf:type foaf:Person .
	
	?ind foaf:givenName ?prop1 .
	FILTER (lcase(str(?prop1)) = "mario") .
	FILTER (langMatches(lang(?prop1), "it")) .

	?ind foaf:familyName ?prop2 .
	FILTER (strstarts(lcase(?prop2), "ro")) .
	FILTER (langMatches(lang(?prop2), "it")) .
}
```