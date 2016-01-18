# Prefix
```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX birda: <http://w3id.org/ontologies/bird-a/>
PREFIX birda-d: <http://pippo.it/birda-data/>
``

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
``
