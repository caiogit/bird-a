shootout
========

Shootout is a demo app for the Pyramid web framework.  The concepts
demonstrated in the code include:

- Url dispatch mechanism.

- Built-in authentication and authorization mechanism.

- Usage of built-in sessioning machinery.

- Integration with pyramid_simpleform for form handling.

- SQLAlchemy based models and transaction management via pyramid_tm.

Library Requirements
--------------------

shootout requires a SQLite3 bindings.

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

- initialize_birda_db development.ini

- pserve development.ini

Troubleshooting
---------------

If setup.py terminates with this error::

	cryptacular/bcrypt/_bcrypt.c:26:20: fatal error: Python.h: No such file or directory

then try (source https://github.com/eventray/horus/issues/38) ::

	sudo apt-get install python-dev python3-dev
	easy_install -UZ cryptacular

