## Tag script for Markdown / GLFM / etc.

`tagmd.py` adds `yaml` tags to Markdown files, e.g.:

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

Add new tags using e.g.:
* `python3 tagmd.py -t foo alice.md` 
* `python3 tagmd.py -t bar alice.md`


## Usage

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
  --tag TAG, -t TAG     tag to add to markdown files
  --dir DIR, -d DIR     directory prefix to append to file names
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
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
