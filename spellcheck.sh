#!/bin/bash

spellcheck() {
	local f="$1"
	echo "Spellcheck $f"
	aspell check --mode=markdown --lang=en_us -- "$f"
}

list_of_md_files() {
	#find . -name "*.md" -not -path "./rss/test/*" -not -path "./tagger/test/*"
	find . \
		-maxdepth 2 \
		-name "*.md" \
		-not -path "./links2md/test.md"
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
done 3< <( list_of_md_files )
