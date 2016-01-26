# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import os
import glob

import sqlalchemy.ext.declarative
import sqlalchemy.orm
import zope.sqlalchemy
import cryptacular.bcrypt

# ============================================================================ #

# Allow "import birda.models.*"
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in modules]

# Patch for unicode strings (to be removed in Python3)
__all__ = [n.encode('ascii') for n in __all__]

# ---------------------------------------------------------------------------- #

DBSession = sqlalchemy.orm.scoped_session(
				sqlalchemy.orm.sessionmaker(
					extension=zope.sqlalchemy.ZopeTransactionExtension()))

Base = sqlalchemy.ext.declarative.declarative_base()

def initialize_sql(engine):
	DBSession.configure(bind=engine)
	Base.metadata.bind = engine
	Base.metadata.create_all(engine)

# ---------------------------------------------------------------------------- #

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

def hash_password(password):
	return unicode(crypt.encode(password))

# ---------------------------------------------------------------------------- #
