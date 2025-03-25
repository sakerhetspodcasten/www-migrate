#!/bin/bash

usage() {
	echo "usage: $0 <DIR>"
	echo ""
	echo "  <DIR>: directory to perform pip-compile in"
}

DIR="$1"


if [[ "$DIR" == "" ]]
then
	usage
	exit 1
fi

if [[ ! -d "$DIR" ]]
then
	usage
	echo "Error: $DIR is not a directory"
	exit 1
fi

set -x
set -e

#
# Generate requirements.lock
#
if which pip-compile
then
	pip-compile --generate-hashes -o "$DIR"/requirements.lock "$DIR"/requirements.txt
	exit
fi

if [[ ! -d .piptools ]]
then
	python3 -m venv .piptools
fi
source .piptools/bin/activate
python -m pip install pip-tools
pip-compile --generate-hashes -o "$DIR"/requirements.lock "$DIR"/requirements.txt
