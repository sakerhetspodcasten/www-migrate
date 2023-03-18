# Web migration tools

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
# Print help
python3 import.rss.py --help

# Running the tool:
mkdir testdir
python3 import.rss.py --dir testdir --url https://sakerhetspodcasten.libsyn.com/rss
```  

Full usage:
```
usage: import.rss.py [-h] --dir DIR --url URL
                     [--ancient_date ANCIENT_DATE]
                     [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                     [--overwrite | --no-overwrite]

Libsyn RSS to Hugo converter (Alpha quality only!)

options:
  -h, --help            show this help message and exit
  --dir DIR             Hugo posts directory (where to write files to).
  --url URL             URL to lib-syn RSS feed, e.g. https://sakerhetspodcasten.libsyn.com/rss
  --ancient_date ANCIENT_DATE
                        Date in YYYYMM format that is a post too old to migrate. Set to either of [None,none] to migrate all.
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
  --overwrite, --no-overwrite
                        Overwrite existing files, or not. (default: False)

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
