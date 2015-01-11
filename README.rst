Bird-A
======

Builder of Interfaces for RDF Data Authoring (BIRD-A) Ontology.

Library Requirements
--------------------

Bird-A requires a SQLite3 bindings.

On a Debian system, these imply: build-essentials, libsqlite3-dev.

Installing and Running
----------------------

Python 2.6 or 2.7 is required.

- virtualenv --no-site-packages env

- cd env

- . bin/activate

- git clone git@github.com:caiogit/bird-a

- cd bird-a

- python setup.py develop

- initialize_birda_db config/development.ini

- pserve config/development.ini

Troubleshooting
---------------

If setup.py terminates with this error::

	cryptacular/bcrypt/_bcrypt.c:26:20: fatal error: Python.h: No such file or directory

then try (source https://github.com/eventray/horus/issues/38) ::

	sudo apt-get install python-dev python3-dev
	easy_install -UZ cryptacular

