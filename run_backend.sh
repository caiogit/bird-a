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

echo
echo '============================================'
echo '              Backend Setup'
echo '============================================'

if [[ $PROD ]]
then
	echo python backend/setup.py install
else
	echo python backend/setup.py develop
fi

# ...

echo
echo '============================================'
echo '              Backend Serve'
echo '============================================'

# ...

echo
