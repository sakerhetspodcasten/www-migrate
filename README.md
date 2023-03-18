# WWW Migration tools

This is very alpha stuff that are for personal project only.

Quick and dirty scripting.

Tools do not support malicious input =)

## Libsyn migration tool

Converts Libsyn RSS to Hugo Yaml/Markdown and writes to:
* `../www-hugo/content/posts`

### Files:

* [import.rss.py](import.rss.py) - tool
* `libsyn-legacy/rss` - file it depends on  

### Usage

``` bash
python3 import.rss.py
```  

## Wordpress migration tool

[wordpress/README.md](wordpress/README.md)

## Miscellaneous

* [.gitignore](.gitignore) - stuff we all just ignore
* [requirements.txt](requirements.txt) - stuff python3 depends upon
* [spellcheck.sh](spellcheck.sh) - spellcheck README.md

Install requirements:
``` bash
pip3 install -r requirements.txt
```

Spellcheck:
``` bash
./spellcheck.sh
```
