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
echo '              Frontend Setup'
echo '============================================'

# ...

echo
echo '============================================'
echo '              Frontend Serve'
echo '============================================'

# ...

echo