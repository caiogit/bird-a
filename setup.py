import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'setuptools',
    'pyramid>=1.3',
    'SQLAlchemy',
    'transaction',
#    'pyramid_chameleon',
	'pyramid_jinja2',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_exclog',
    'zope.sqlalchemy',
    'pyramid_simpleform',
    'cryptacular',
    'waitress',
    'pycrypto',
    'webtest',
    ]

if sys.version_info[:3] < (2,5,0):
    raise RuntimeError('This application requires Python 2.6+')

setup(name='bird-a',
      version='0.0.1',
      description='Builder of Interfaces for RDF Data Authoring (BIRD-A)',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Framework :: Pylons",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author="Silvio Peroni, Francesco Caliumi",
      author_email="silvio.peroni@unibo.it, francesco.caliumi@gmail.com",
      url='...',
      license="...",
      keywords='birda rdf ontology',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='birda.tests',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = birda:main
      [console_scripts]
      initialize_birda_db = birda.scripts.initializedb:main
      """,
      )
