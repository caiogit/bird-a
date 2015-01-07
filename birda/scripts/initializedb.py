import os
import sys

import sqlalchemy
import transaction
import pyramid.paster
import birda
from birda.models import *

def usage(argv):
	cmd = os.path.basename(argv[0])
	print('usage: %s <config_uri>\n'
		  '(example: "%s development.ini")' % (cmd, cmd))
	sys.exit(1)

def main(argv=sys.argv):
	if len(argv) != 2:
		usage(argv)
	config_uri = argv[1]
	pyramid.paster.setup_logging(config_uri)
	settings = pyramid.paster.get_appsettings(config_uri)
	engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
	birda.models.base.DBSession.configure(bind=engine)

	# Create tables
	birda.models.base.Base.metadata.create_all(engine, checkfirst=True)

	# Add initial (dummy) data to tables
	with transaction.manager:
		editor = birda.models.users.User('editor','editor', 'Editor', 'dummy@mail.com')
		birda.models.base.DBSession.add(editor)


