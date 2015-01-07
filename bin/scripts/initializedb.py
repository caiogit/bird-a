import os
import sys

import sqlalchemy
import pyramid.paster
import bin.models.base


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
    bin.models.base.DBSession.configure(bind=engine)
    bin.models.base.Base.metadata.create_all(engine)

