#!/usr/bin/env bash

VENV=$1
BE_CONF=$2
METHOD=$3
SRV_FULL_URI="$4"

TMP_FILE=/tmp/$(basename $0).$$.tmp

# Functions definition
function search_for_error {
	output_file=$1
	error_str=$2
	
	found=$(cat ${output_file} | grep "${error_str}")
	
	if [[ "${found}" != "" ]]
	then
		echo "An Error occurred:"
		echo
		echo "    \"${error_str}\""
		echo
		exit 1
	fi
}

# Simulating request
echo
${VENV}/bin/prequest -m${METHOD} -d ${BE_CONF} "${SRV_FULL_URI}" | tee ${TMP_FILE}
echo

# Look for errors
search_for_error ${TMP_FILE} "500 Internal Server Error"

# Remove temporary file
rm -f ${TMP_FILE}