# -*- coding: utf-8 -*-

"""
Script that initializes sqlite db with default users
"""
# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import sys
import os

import sqlalchemy
import transaction
import pyramid.paster
import birda
from birda.models import *

# ============================================================================ #

def usage(argv):
	cmd = os.path.basename(argv[0])
	print('usage: %s <config_uri>\n'
		  '(example: "%s development.ini")' % (cmd, cmd))
	sys.exit(1)

# ---------------------------------------------------------------------------- #

def main(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	pyramid.paster.setup_logging(config_uri)
	settings = pyramid.paster.get_appsettings(config_uri)
	engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
	birda.models.DBSession.configure(bind=engine)

	# Create tables
	birda.models.Base.metadata.create_all(engine, checkfirst=True)

	# Add initial (dummy) data to tables
	with transaction.manager:
		if not birda.models.users.User.get_by_username(u'editor'):
			editor = birda.models.users.User(u'editor', u'editor', u'Editor', u'dummy@mail.com')
			birda.models.DBSession.add(editor)

# ============================================================================ #

if __name__ == '__main__':
	main()
