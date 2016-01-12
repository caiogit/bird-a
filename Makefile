# ================================ #

BASE_DIR := $(PWD)
GRUNT := ./node_modules/grunt

# Set VENV if not already set
ifndef VENV
	VENV := /usr
	SUDO := sudo
else:
	SUDO :=
endif


# Ask the user if prod or devel
reply := $(shell read -p 'Production or Development? (p/D) ' reply; echo $$reply)
PROD := $(shell echo "$(reply)" | grep "^[pP]$$" | tr '[:lower:]' '[:upper:]')

# Variables setting
ifeq ($(PROD), "P")
	BE_SETUP_TARGET := install
	BE_CONF := production.ini
else
	BE_SETUP_TARGET := develop
	BE_CONF := development.ini
endif


.PHONY: all make-be run-be make-fe run-fe make-fuseki run-fuseki \
        clean-be clean-fe clean-fuseki clean lines-of-code

# -------------------------------- #

all:
	#@echo "Prod: \"$(PROD)\" (reply: \"$(reply)\")"
	@echo
	@echo "make make-be"
	@echo "make run-be"
	@echo "make clean-be"
	@echo "     Make, run and clean the backend"
	@echo
	@echo "make make-fe"
	@echo "make run-fe"
	@echo "make clean-fe"
	@echo "     Make, run and clean the frontend"
	@echo
	@echo "make clean"
	@echo "     Clean backend, frontend and fuseki"
	@echo
	@echo "make lines-of-code"
	@echo "     Display actual Source Lines of Codes (SLOC)"
	@echo

# ================================ #

# Make Backend
make-be:
	cd $(BASE_DIR)/backend ; \
#	export PYTHON_PATH=$(BASE_DIR)/backend:$(BASE_DIR)/backend/birda:$PYTHON_PATH ; \
	$(SUDO) $(VENV)/bin/python setup.py $(BE_SETUP_TARGET)
	# TODO: Initialization scripts

# -------------------------------- #

# Run Backend
run-be:
	cd $(BASE_DIR)/backend ; $(VENV)/bin/pserve $(BE_CONF) --reload

# ================================ #

# Make Frontend
make-fe:
	cd $(BASE_DIR)/frontend; npm install
	cd $(BASE_DIR)/frontend; ./node_modules/grunt --force

# -------------------------------- #

# Run Frontend
run-fe:
	cd $(BASE_DIR)/frontend ; grunt serve --force

# ================================ #

# Make Fuseki
make-fuseki:
	wget http://mirrors.muzzy.it/apache/jena/binaries/apache-jena-fuseki-2.3.1.tar.gz
	tar xzf apache-jena-fuseki-*.tar.gz
	rm -vf apache-jena-fuseki-*.tar.gz
	# TODO: Make Fuseki
	# 1) packet wget
	# 2) untar
	# 3) rm packet
	# 4) installation?

# -------------------------------- #

# Run Frontend
run-fuseki:
	# TODO: Run Fuseki

# ================================ #

clean-be:
	cd $(BASE_DIR)/backend;  $(VENV)/bin/python setup.py clean
	#cd $(BASE_DIR)/backend;  $(SUDO) rm -rvf backend.egg-info
	cd $(BASE_DIR)/backend;  find . -name "*.pyc" -exec rm -vf '{}' \;

# -------------------------------- #

clean-fe:
	cd $(BASE_DIR)/frontend; grunt clean

# -------------------------------- #

clean-fuseki:
	# TODO: Clean Fuseki

# -------------------------------- #

clean: clean-be clean-fe clean-fuseki

# -------------------------------- #

lines-of-code:
#	( \
#	find $(BASE_DIR)/backend -iname "*.py" ; \
#	find $(BASE_DIR)/frontend/app -iname "*.js" ; \
#	find $(BASE_DIR)/frontend/app -iname "*.html" ; \
#	find $(BASE_DIR)/frontend/app -iname "*.css" ; \
#	echo $(BASE_DIR)/Makefile ) | \
#	grep -v 'ascii_utils' | \
#	xargs wc

	cloc --exclude-dir=node_modules,bower_components --not-match-f=ascii_utils --by-file-by-lang backend/birda frontend/app/

# ================================ #
