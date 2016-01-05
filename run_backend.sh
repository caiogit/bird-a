#!/bin/bash

PROD=
DEVEL=

echo
echo -n 'Production or Development? (p/D) '
read answer

case $answer in
  [pP])
     echo "Production environment..."
     PROD=true
     ;;

  [dD]|"")
     echo "Development environment..."
     DEVEL=true
     ;;

  *)
     echo "Bad answer. Aborting..."
     echo
     exit 1
     ;;
esac

if [[ ! $VENV ]]; then
	VENV=/usr
fi

BASE_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


echo
echo '============================================'
echo '              Backend Setup'
echo '============================================'

echo cd $BASE_PATH/backend
cd $BASE_PATH/backend

if [[ $PROD ]]
then
	echo $VENV/bin/python setup.py install
	$VENV/bin/python setup.py install
else
	echo $VENV/bin/python setup.py develop
	$VENV/bin/python setup.py develop
fi

if [[ $? -ne 0 ]] ; then
	echo -e "\n\e[1;31mError!\e[0m Setup did not end correctly. Read the README file for troubleshooting.\n"
	#exit 1
fi

echo cd $BASE_PATH
cd $BASE_PATH

echo
echo '============================================'
echo '              Backend Serve'
echo '============================================'

if [[ $PROD ]]
then
	echo $VENV/bin/pserve config/production.ini
	$VENV/bin/pserve config/production.ini
else
	echo $VENV/bin/pserve config/development.ini --reload
	$VENV/bin/pserve config/development.ini --reload
fi

echo
