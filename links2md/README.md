# links2md

Create Markdown documents from list of links/URLs.

Features:
* title from `head.title` metadata
* Publisher/site from metadata
* Authors from metadata

## Metadata support

Various metadata supported:

* `head.meta`
  * `og:site_name`
  * `parsely-page` JSON
* `head.script`
   * `application/ld+json` JSON, multiple variants...
* `head.link` `itemprop="name"` (YouTube)

Poke source code for more details...

## Usage

Example usage:

* `./links2md.py -h`
* `./links2md.py -i test.txt`
* `./links2md.py -i test.txt -o test.md`
  _Example files:_ [test.txt](test.txt), [test.md](test.md)

``` plain
usage: links2md.py [-h] --input INPUT_FILE [--output OUTPUT_FILE]
                   [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

convert links to markdown

options:
  -h, --help            show this help message and exit
  --input INPUT_FILE, -i INPUT_FILE
                        text file with urls to consume
  --output OUTPUT_FILE, -o OUTPUT_FILE
                        text file with urls to consume. Default is stdout.
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}

Hope this help was helpful! :-)
```

Creates markdown links like this:

``` markdown
* [Säkerhetspodcasten · GitHub](https://github.com/sakerhetspodcasten/)
* [Example Domain](https://example.com/)
* [YouTube: Rick Astley - Never Gonna Give You Up (Official Music Video)](https://www.youtube.com/watch?v=dQw4w9WgXcQ) `video`
```
