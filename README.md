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

Example:
``` bash
mkdir test
python3 import.rss.py --loglevel INFO --dir test --overwrite --url https://sakerhetspodcasten.libsyn.com/rss
```  

Help
``` bash
python3 import.rss.py --help
usage: import.rss.py [-h] [--ancient_date ANCIENT_DATE] [--dir DIR] [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--overwrite | --no-overwrite] --url URL

Libsyn RSS to Hugo converter (Alpha quality only!)

options:
  -h, --help            show this help message and exit
  --ancient_date ANCIENT_DATE
                        Date in YYYYMM format that is a post too old to migrate. Set to either of [None,none] to migrate all.
  --dir DIR             Hugo posts directory (where to write files to). Default: ../www-hugo/content/posts
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
  --overwrite, --no-overwrite
                        Overwrite existing files, or not. (default: False)
  --url URL             URL to lib-syn RSS feed, e.g. https://sakerhetspodcasten.libsyn.com/rss

Hope this help was helpful! :-)
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
