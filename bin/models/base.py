# -*- coding: utf-8 -*-

import sqlalchemy.ext.declarative
import sqlalchemy.orm
import zope.sqlalchemy
import cryptacular

DBSession = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(extension=zope.sqlalchemy.ZopeTransactionExtension()))

Base = sqlalchemy.ext.declarative.declarative_base()

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

def hash_password(password):
    return unicode(crypt.encode(password))
