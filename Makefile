# ================================ #

BASE_DIR := $(PWD)
#GRUNT := $(PWD)/frontend/node_modules/.bin/grunt
#BOWER := $(PWD)/frontend/node_modules/.bin/bower
EXPORT_PATH_FE = export PATH=$(BASE_DIR)/frontend/node_modules/.bin:$(BASE_DIR)/frontend/gems_packages/bin:$(BASE_DIR)/frontend/node/n/versions/node/5.4.1/bin:$(PATH)

# Set VENV if not already set
ifndef VENV
	VENV := /usr
	SUDO := sudo -E
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
	BE_RELOAD := 
else
	BE_SETUP_TARGET := develop
	BE_CONF := development.ini
	BE_RELOAD := --reload
endif


.PHONY: all make-be run-be make-fe run-fe make-fuseki run-fuseki \
        clean-be clean-fe clean-fuseki clean lines-of-code

# -------------------------------- #

# Functions

# intestation2(string)
define intestation2 =
@$(VENV)/bin/python -c 'print "\n"; print "="*80; print "$1".center(80); print "="*80; print'
endef

# test_ok()
define test_ok =
$(call intestation2,All tests successfully finished)
endef

# Function test_be_api(method, service_name, service_full_uri)
define test_be_api =
$(call intestation2,$(1) $(2))
cd $(BASE_DIR)/backend ; ./birda/scripts/test_service.sh $(VENV) $(BE_CONF) $(1) "$(3)"
endef

# ================================ #

all:
	#@echo "Prod: \"$(PROD)\" (reply: \"$(reply)\")"
	@echo
	@echo "make make-be"
	@echo "make run-be"
	@echo "make test-be"
	@echo "make clean-be"
	@echo "     Make, run, test and clean the backend"
	@echo
	@echo "make make-fe"
	@echo "make run-fe"
	@echo "make test-fe"
	@echo "make clean-fe"
	@echo "     Make, run, test and clean the frontend"
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
	
	# Just to make sure...
	$(SUDO) $(VENV)/bin/easy_install -UZ cryptacular
	$(SUDO) $(VENV)/bin/pip install --upgrade rdflib
	
	# TODO: Initialization scripts
	@echo
	@echo "========================"
	@echo " Initialize users db"
	@echo "========================"
	cd $(BASE_DIR)/backend ; $(VENV)/bin/birda_init_db $(BE_CONF)

# -------------------------------- #

# Run Backend
run-be:
	cd $(BASE_DIR)/backend ; $(VENV)/bin/pserve $(BE_CONF) $(BE_RELOAD)
	
# -------------------------------- #

# Test Backend
test-be:
	
	$(call intestation2,bModel/widget.py)
	cd $(BASE_DIR)/backend ; $(VENV)/bin/python birda/bModel/widget.py
	
	$(call intestation2,bModel/individual.py)
	cd $(BASE_DIR)/backend ; $(VENV)/bin/python birda/bModel/individual.py
	
	$(call intestation2,storage/file_storage.py)
	cd $(BASE_DIR)/backend ; $(VENV)/bin/python birda/storage/file_storage.py

	$(call intestation2,storage/utils.py)
	cd $(BASE_DIR)/backend ; $(VENV)/bin/python birda/storage/utils.py
	
	$(call intestation2,scripts/create_test_instance.py)
	cd $(BASE_DIR)/backend ; $(VENV)/bin/python birda/scripts/create_test_ontologies.py
	
	$(call intestation2,birda/services/jsons/forms.py)
	cd $(BASE_DIR)/backend ; $(VENV)/bin/python birda/services/jsons/forms.py
	
	$(call intestation2,birda/services/jsons/individuals.py)
	cd $(BASE_DIR)/backend ; $(VENV)/bin/python birda/services/jsons/individuals.py
	
	$(call test_be_api,GET,/api/v1/forms,/api/v1/forms)
	
	$(call test_be_api,GET,/api/v1/forms/{form_uri},/api/v1/forms/http://pippo.it/birda-data/PersonNormal-Form)
	
	$(call test_be_api,GET,/api/v1/individuals/{uri},/api/v1/individuals/http://pippo.it/target-data/pierluigi-mariuolo?form_uri=http://pippo.it/birda-data/PersonNormal-Form&lang=it)
	
	$(call test_be_api,GET,/api/v1/individuals/{uri},/api/v1/individuals/http://pippo.it/target-data/pierluigi-mariuolo?form_uri=http://pippo.it/birda-data/PersonNormal-Form&lang=us)
	
	$(call test_ok)
	
# ================================ #

# Make Frontend
make-fe:
	cd $(BASE_DIR)/frontend; npm install npm
	cd $(BASE_DIR)/frontend; gem install compass --install-dir gems_packages
	$(EXPORT_PATH_FE); cd $(BASE_DIR)/frontend; export N_PREFIX=node ; n 5.4.1
	$(EXPORT_PATH_FE); cd $(BASE_DIR)/frontend; npm install
	$(EXPORT_PATH_FE); cd $(BASE_DIR)/frontend; bower install
	$(EXPORT_PATH_FE); cd $(BASE_DIR)/frontend; grunt --force

# -------------------------------- #

# Run Frontend
run-fe:
	$(EXPORT_PATH_FE); cd $(BASE_DIR)/frontend ; grunt serve --force
	
# -------------------------------- #

# Test Frontend
test-fe:
	# TODO

# ================================ #

# Make Fuseki
make-fuseki:
	rm -rf fuseki
	wget -c http://it.apache.contactlab.it/jena/binaries/jena-fuseki1-1.3.1-distribution.tar.gz
	tar xzf jena-fuseki*.tar.gz
	mv -vi jena-fuseki*/ fuseki
	rm -vf jena-fuseki*.tar.gz

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

	cloc --exclude-dir=node_modules,bower_components --not-match-f='(ascii_utils|dummy_jsons)' --by-file-by-lang backend/birda frontend/app/

# ================================ #
