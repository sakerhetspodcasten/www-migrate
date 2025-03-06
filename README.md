# Web migration tools for Markdown

Migrate input files to Markdown web formats appropriate for Hugo,
Jekyll or other web/blog hosting platforms based on Markdown
plaintext!

Releases your information held captive in RSS, SRT or Wordpress
to live free as Markdown `.md` files!

Tools:
* [Libsyn/RSS migration tool](#libsynrss-migration-tool) - import libsyn episodes.
* [SRT to Markdown tool](#srt-to-markdown-tool) - import Sub Rip Text transcribe files.
* [Tagging](#tagging) - tools for searching or adding tags.
* [Wordpress migration tool](#wordpress-migration-tool) (_note: abandoned_).

Deals with Markdown/GLFM, i.e.:

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

**LIMITATIONS**:

> This is very alpha stuff that are for personal project only.
> **Quick and dirty** scripting.
> Tools do not support malicious input =)

## Tools

### Libsyn/RSS migration tool

RSS to Markdown/Yaml/GLFM converter.

* [rss/README.md](rss/README.md)
* Pretty usable for our specific needs.
* Emits MP3 link, duration etc. into Markdown.

### SRT to Markdown tool

Google SRT (SubRip Text) transcribe files to Markdown converter.

* [srt2md/README.md](srt2md/README.md)

### Tagging

Tools to manipulate `tags:` Yaml list.
* [tagger/README.md](tagger/README.md)
* `tagmd.py` for adding one or more tags to one or more Markdown files.
* `taglist.py` for listing markdown files that meets one or more search conditions.
   Search for specific tag.
   Search for tag count; supporting exact match, or more than / less than.

## Abandoned tools

No longer used or maintained; the move from Wordpress is done...

### Wordpress migration tool

Wordpress database to Markdown converter.

* [wordpress/README.md](wordpress/README.md)
* **WARNING**
  * Extremely alpha quality.
  * Not used by us any more, will never improve, abandon-ware.

## Build and update

* [Dockerfile](Dockerfile) - a reproducible build for regenerating virtual environments.
* [build.sh](build.sh) - runs `podman build` to regenerate `requirements.txt` files using `podman`.
* [release.sh](release.sh) - tags a release if:
  - `build.sh` succeeds
  - `git procelain` reports that directory is clean.
  - `tag` does not already exist.

## Miscellaneous

* [.gitignore](.gitignore) - stuff we all just ignore
* [spellcheck.sh](spellcheck.sh) - spellcheck README.md

Spellcheck:
``` bash
./spellcheck.sh
```
