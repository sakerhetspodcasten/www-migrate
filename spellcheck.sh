#!/bin/bash

which aspell >/dev/null
if [[ "$?" != "0" ]]
then
	echo "No aspell? Maybe:"
	echo "sudo apt install aspell aspell-en"
else
	set -x
	aspell check --mode=markdown --lang=en_us README.md
fi
