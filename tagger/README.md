# Scripts for tag manipulation in Markdown / GLFM / etc.

Scripts deals with `tags` list in `yaml`/`Markdown` files, e.g.:

``` plain
---
date: '2017-12-04T16:32:28'
lastmod: '2018-09-26T08:21:26'
tags:
- foo
title: "alice.md"

---
## Markdown

Content....
```

Tools:
* [tagmd](#tagmd) _command for adding tags to Markdown files_
* [taglist](#taglist) _command for finding files matching tags etc_

## tagmd

Add new tags using e.g.:
* `python3 tagmd.py -t foo alice.md` 
* `python3 tagmd.py -t bar alice.md`
* `python3 tagmd.py -t foo,bar,baz alice.md` - add three tags in one go!

Request usage help:

``` bash
python3 tagmd.py -h
```

Usage help:

``` plain
usage: tagmd.py [-h] --tag TAG [--dir DIR] [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}] file [file ...]

add tags to yaml/md contant files

positional arguments:
  file                  files to process

options:
  -h, --help            show this help message and exit
  --tag TAG, -t TAG     tag to add to markdown files. Sperate multiple tags with comma.
  --dir DIR, -d DIR     directory prefix to append to file names
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}

Hope this help was helpful! :-)
```
 
**Basic example:**

Add tag `foo` to `alice.md` and `bob.md`, and non-existent file `charlie.md`:
 
``` bash
python3 tagmd.py -t foo alice.md bob.md charlie.md
2025-03-03 21:25:45,476 INFO Process alice.md
2025-03-03 21:25:45,477 INFO Process bob.md
2025-03-03 21:25:45,477 WARNING File does not exists: charlie.md
```

Note:
* Non-existent files will be ignored.
* Markdown files without `yaml` header will be ignored.
* If no `tags:` entry exists within `yaml`, a new `tags:` list will be added.
* If a `tags:` entry exists, 
  and the tag is not already in the list,
  the tag will be appended.

**Advanced examples:**

Add tag `foo` to articles in directory `../foo` from list in file `cat foo-list.txt`:

``` bash
cat foo-list.txt | xargs python3 tagmd.py -t foo --dir ../foo
```

## taglist

Request usage help:

``` bash
python3 taglist.py -h
```

``` plain
usage: taglist.py [-h] [--tag TAG] [--tagcount TAGCOUNT] [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}] file [file ...]

list files with tags

positional arguments:
  file                  files or directories to process

options:
  -h, --help            show this help message and exit
  --tag TAG, -t TAG     file files with tag
  --tagcount TAGCOUNT, -c TAGCOUNT
                        file files with tag
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}

Hope this help was helpful! :-)
```

Examples:
* `python3 taglist.py file.md`
* `python3 taglist.py directory`
* `python3 taglist.py -t foo directory` lists only markdown files tagged with `foo`.
* `python3 taglist.py -c 2 directory` lists only markdown files with exactly `2` tags.
* `python3 taglist.py -t foo -c 2 directory` require both tag and tag count to match.
* `python3 taglist.py -c '<2' directory` _less than..._
* `python3 taglist.py -c '<=2' directory` _less or equal to..._
* `python3 taglist.py -c '>2' directory` _more than..._
* `python3 taglist.py -c '>=2' directory` _more than or euql to..._
