# ================================ #

BASE_DIR := $(PWD)

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


.PHONY: all make-be make-fe run-be run-fe

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

# ================================ #

# Make Backend
make-be:
	cd $(BASE_DIR)/backend ; \
#	export PYTHON_PATH=$(BASE_DIR)/backend:$(BASE_DIR)/backend/birda:$PYTHON_PATH ; \
	$(SUDO) $(VENV)/bin/python setup.py $(BE_SETUP_TARGET)

# -------------------------------- #

# Run Backend
run-be:
	cd $(BASE_DIR)/backend ; $(VENV)/bin/pserve $(BE_CONF) --reload

# -------------------------------- #

# Make Frontend
make-fe:
	cd $(BASE_DIR)/frontend; grunt

# -------------------------------- #

# Run Frontend
run-fe:
	cd $(BASE_DIR)/frontend ; grunt serve

# ================================ #

clean-be:
	cd $(BASE_DIR)/backend;  $(VENV)/bin/python setup.py clean
	#cd $(BASE_DIR)/backend;  $(SUDO) rm -rvf backend.egg-info
	cd $(BASE_DIR)/backend;  find . -name "*.pyc" -exec rm -vf '{}' \;

# -------------------------------- #

clean-fe:
	cd $(BASE_DIR)/frontend; grunt clean

# -------------------------------- #

clean: clean-be clean-fe

# ================================ #