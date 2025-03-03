#!/bin/bash

spellcheck() {
	local f="$1"
	echo "Spellcheck $f"
	aspell check --mode=markdown --lang=en_us -- "$f"
}

which aspell >/dev/null
if [[ "$?" != "0" ]]
then
	echo "No aspell? Maybe:"
	echo "sudo apt install aspell aspell-en"
	exit 1
fi

while read -u3 mdfile
do
	spellcheck "$mdfile"
done 3< <( find . -name "*.md" -not -path "./rss/test/*" -not -path "./tagger/test/*" )
