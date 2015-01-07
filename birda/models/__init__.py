# -*- coding: utf-8 -*-

import os
import glob

import sqlalchemy.ext.declarative
import sqlalchemy.orm
import zope.sqlalchemy
import cryptacular.bcrypt


# Allow "import birda.models.*"
modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in modules]


DBSession = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(extension=zope.sqlalchemy.ZopeTransactionExtension()))

Base = sqlalchemy.ext.declarative.declarative_base()

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

def hash_password(password):
	return unicode(crypt.encode(password))

def initialize_sql(engine):
	DBSession.configure(bind=engine)
	Base.metadata.bind = engine
	Base.metadata.create_all(engine)