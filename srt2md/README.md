# SRT SubRip Text to Markdown converter

Converts SRT SubRip Text such as:

``` plain
101
00:55:10,200 --> 00:55:18,500
x
```

into Markdown such as:

``` md
### 101 00:55:10,200 --> 00:55:18,500
x
```

## Usage

Request usage help:

``` bash
python3 srt2md.py -h
```

Usage help output:

``` plain
usage: srt2md.py [-h] [-i FILENAME_IN] [-o FILENAME_OUT] [-O {a,w,x}] [-m MARKDOWN_HEADER]

srt to markdown converter

options:
  -h, --help            show this help message and exit
  -i FILENAME_IN, --in FILENAME_IN
                        File to read, default is <stdin>
  -o FILENAME_OUT, --out FILENAME_OUT
                        File to write, default is <stdout>
  -O {a,w,x}, --output-mode {a,w,x}
                        File output mode; a: append (default), w: truncating write, x: eXclusively create.
  -m MARKDOWN_HEADER, --markdown-header MARKDOWN_HEADER
                        markdown header preamble, default ###

Hope this help was helpful! :-)
```

Example:

``` bash
python3 srt2md.py -i 2025-02-19.srt
python3 srt2md.py -i 2025-02-19.srt -o 2025-02-19.md
python3 srt2md.py -i 2025-02-19.srt -o 2025-02-19.md -O x
python3 srt2md.py -i 2025-02-19.srt -o 2025-02-19.md -m '##'
```

Unix pipes:

``` bash
cat 2025-02-19.srt | python3 srt2md.py
cat 2025-02-19.srt | python3 srt2md.py > 2025-02-19.md
```
