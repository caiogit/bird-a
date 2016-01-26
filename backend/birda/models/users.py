# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

from sqlalchemy import (
	Table,
	Column,
	ForeignKey,
)

from sqlalchemy.types import (
	Integer,
	Unicode,
	UnicodeText,
)

import sqlalchemy.orm

import birda.models

# ================================================================================================ #

class User(birda.models.Base):
	"""
	Application's user model.
	"""

	# ----------------------------------- #
	__tablename__ = 'users'
	user_id = Column(Integer, primary_key=True)
	username = Column(Unicode(20), unique=True)
	name = Column(Unicode(50))
	email = Column(Unicode(50))
	# ----------------------------------- #

	# ----------------------------------- #
	_password = Column('password', Unicode(60))

	def _get_password(self):
		return self._password

	def _set_password(self, password):
		self._password = birda.models.hash_password(password)

	password = property(_get_password, _set_password)
	password = sqlalchemy.orm.synonym('_password', descriptor=password)
	# ----------------------------------- #

	# ----------------------------------------------------------------------- #

	def __init__(self, username, password, name, email):
		self.username = username
		self.name = name
		self.email = email
		self.password = password

	# ----------------------------------------------------------------------- #

	@classmethod
	def get_by_username(cls, username):
		return birda.models.DBSession.query(cls).filter(cls.username == username).first()


	# ----------------------------------------------------------------------- #

	@classmethod
	def check_password(cls, username, password):
		user = cls.get_by_username(username)
		if not user:
			return False
		return birda.models.crypt.check(user.password, password)