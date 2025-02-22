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

``` plain
usage: srt2md.py [-h] [-i FILENAME_IN] [-m MARKDOWN_HEADER]

srt to markdown converter

options:
  -h, --help            show this help message and exit
  -i FILENAME_IN, --in FILENAME_IN
                        which file to read
  -m MARKDOWN_HEADER, --markdown-header MARKDOWN_HEADER
                        markdown header preamble, default ###
```

Example:

``` bash
python3 srt2md.py -i 2025-02-19.srt
```

Unix pipes:

``` bash
cat 2025-02-19.srt | python3 srt2md.py
```
