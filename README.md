# Bird-A

Builder of Interfaces for RDF Data Authoring (BIRD-A) Ontology.

<blockquote>
  <p><img src="https://upload.wikimedia.org/wikipedia/commons/2/24/Warning_icon.svg" alt="warning" width="20" heigth="20" /> &nbsp;<b>Warning</b></p>
  
  <p>This project is part of Francesco Caliumi bachelor degree thesis
     and it's intended to be completed by one or more additional theses in 
     Web Technologies field of Bologna Computer Science Degree.</p>
     
  <p>Even though the software is fully working, there are some unimplemented
     features that should be implemented in future versions.</p>
</blockquote>

## Requirements

- Python 2.7
- Python SQLite3 bindings (debian packages: build-essential, libsqlite3-dev).
- virtualenv (optional)
- npm
- Java Runtime Environment (required by Fuseki)

In a debian system:

- sudo apt-get install git virtualenv python2.7 python-dev python3-dev python-setuptools nodejs nodejs-legacy npm virtualenv build-essential libsqlite3-dev ruby ruby-dev
- sudo gem update --system
- sudo gem install compass
- sudo npm install -g bower grunt

## Installing and Running

Configure virtual env:

	virtualenv env27
	cd env27
	export VENV=${PWD}

Get Bird-A:

	git clone https://github.com/caiogit/bird-a.git
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

### Cryptacular

If `make make-be` ends with this error::

	cryptacular/bcrypt/_bcrypt.c:26:20: fatal error: Python.h: No such file or directory

then try (source [[https://github.com/eventray/horus/issues/38]]):

	sudo apt-get install python-dev python3-dev
	sudo easy_install -UZ cryptacular

### Rdflib

If some scripts raise this error:

	Traceback (most recent call last):
	  File "...", line XXX, in <...>
		from rdflib.namespace import RDF
	ImportError: No module named namespace

try:

	sudo pip install --upgrade rdflib

### Unibo CS department only

In department machines npm is not in path. To bypass this:

	echo -e '\nexport PATH=$PATH:/usr/local/node/bin\n' >> ~/.bashrc

