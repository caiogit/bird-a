# Bird-A


Builder of Interfaces for RDF Data Authoring (BIRD-A) Ontology.

## Requirements


- Python 2.7
- Python SQLite3 bindings (debian packages: build-essentials, libsqlite3-dev).
- npm
- bower
- grunt

In a debian system:

- apt-get install build-essentials libsqlite3-dev nodejs npm
- npm install -g bower grunt


## Installing and Running

Configure virtual env:

	virtualenv env27
	cd env27
	export VENV=${PWD}

Get Bird-A:

	git clone git@github.com:caiogit/bird-a
	cd bird-a

Make backend, frontend and fuseki:

	make make-be
	make make-fe
	make make-fuseki

Run backend, frondend and fuseki:

	make run-be
	make run-fe
	make run-fuseki

## Troubleshooting

If `make make-be` ends with this error::

	cryptacular/bcrypt/_bcrypt.c:26:20: fatal error: Python.h: No such file or directory

then try (source [[https://github.com/eventray/horus/issues/38]]):

	sudo apt-get install python-dev python3-dev
	sudo easy_install -UZ cryptacular


If some scripts raise this error:

	Traceback (most recent call last):
	  File "...", line XXX, in <...>
		from rdflib.namespace import RDF
	ImportError: No module named namespace

then try:

	sudo pip install --upgrade rdflib