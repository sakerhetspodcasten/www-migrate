# v0.0.4

Files:
``` plain
A	.dockerignore
M	.gitignore
M	Dockerfile
M	README.md
M	build.sh
A	links2md/README.md
A	links2md/links2md.py
A	links2md/requirements.in
A	links2md/requirements.lock
A	links2md/requirements.txt
A	links2md/test.md
A	links2md/test.txt
A	links2md/venv.sh
A	lock.sh
M	release.sh
A	rss/requirements.lock
M	rss/venv.sh
M	spellcheck.sh
A	tagger/requirements.lock
M	tagger/venv.sh
A	wordpress/requirements.lock
M	wordpress/venv.sh
```

Commits:
``` plain
* bb293c1 0.0.4
* 4bd7ab8 requirements.lock build workflow
* d7705e4 Move global to function scoped variable
* 1c7b610 Sepeate authors by ", " instead of ","
* 89fc934 Deal with youtube etc. garabge parameters
* 6754483 Define globals in begining of module
* 5c9935f README.md
* de43763 links2md documentation
* 74a475b application/ld+json: support list of authors
* a40a2ca Hotfix for stupid 'the Guardian' site meta data...
* f352c14 application/ld+json: support list and non-list
* 9d5a1a5 Get author from application/ld+json scripts
* 6c90377 Remove pipe character site suffix
* c0aa6fa Reduce spamminess, sleep between requests
* 4d20f21 Identify as curl...
* 962c520 Output to stdout if no --output is provided
* 86452c5 Improved HTML/Meta/Link/JSON parsing...
* b32d3b1 Minor fixes
* 64d8239 Links to markdown
```

# v0.0.3

Files:
``` plain
M	Dockerfile
M	README.md
M	build.sh
M	release.sh
M	tagger/README.md
```

Commits:
``` plain
* 8c37383 Version 0.0.3
* f7e3eb9 Only update requirements.txt upon release
* 729c9d5 README.md updates
* 8bbe4f8 README.md various minor updates
```

# v0.0.2

Files:
``` plain
M	.gitignore
M	Dockerfile
M	build.sh
M	release.sh
M	rss/venv.sh
M	spellcheck.sh
A	tagger/README.md
A	tagger/requirements.in
A	tagger/requirements.txt
A	tagger/taglist.py
A	tagger/tagmd.py
A	tagger/venv.sh
M	wordpress/venv.sh
```

Commits:
``` plain
* d0977a6 Release 0.0.2
* 3555508 Dockerfile: small clarity improvements
* c00a674 venv.sh: make it nicer
* bfd9618 fix typo
* cbf2803 README update
* 0e20d63 Explain comma seperation
* 14e46e0 Make "taglist.py file.md" work
* 9f5bb84 Make taglist.py more stable
* ed79ad5 support adding multiple tags
* bb42b79 Search by count
* 9bf5927 search for blog posts containing a tag
* f3b72e5 remove extra line ending after yaml dump
* d53b191 Add tagger/requirements.txt to build
* 3a055b5 README.md
* a0b9de7 generalize spellchecker
* ba26d8c File prefix
* 99e002a tagmd.py
```

# v0.0.1

Files:
``` plain
A	.gitignore
A	Dockerfile
A	README.md
A	build.sh
D	import.old.py
A	release.sh
A	rss/README.md
A	rss/import.rss.py
A	rss/requirements.in
A	rss/requirements.txt
A	rss/venv.sh
A	spellcheck.sh
A	srt2md/README.md
A	srt2md/srt2md.py
A	wordpress/README.md
A	wordpress/import.wp.py
A	wordpress/requirements.in
A	wordpress/requirements.txt
A	wordpress/venv.sh
A	wordpress/wp-legacy/posts.mysql.schema
A	wordpress/wp-legacy/posts.schema
```

Commits:
``` plain
* 77bc291 release.sh
* 8cfbf9c Update build scripts
* daff2ff wordpress/requirements.txt
* dcdcfc2 Build scripts
* 26e105e Reorder file structure
* 6e331ee File output & mode selector
* 822ab87 Warn user if converting stdin TTY
* 8bda9cf README.md
* c6371a4 srt2md: code simplified
* 76ae16c README.md
* 86186d6 srt2md --markdown-header
* d31c414 srt to markdown
* e6e719f requirements.txt freeze and venv.sh for generation
* ed93d5f Remove garbage and turn <li> into list item.
* 644e406 Remove ref to legacy hard-coded file
* f435102 Remove reference to previously hard-coded dir
* 43487b2 --no-overwrite demo--no-overwrite demo
* 721b2be Move Libsyn/RSS tool to own dirMove Libsyn/RSS tool to own dir
* 210c355 README preamble update
* 7b1d7cc Coding practice: space before and after assignment
* 1f9a8ff Make dir a required variable, organize arguments
* da87f07 INFO log processing statistics/summary
* 482059b Set default log level to INFO
* 000ff3c Clean up code, messages
* ce1f168 Shorter lines in example
* 406857d README.md
* a66fd92 Specify URL from command line.
* 628e303 Specify if file overwrite is allowed or not
* 5a31225 Specify content post directory from command line
* 7a83eaa Debug log on skipping old posts
* 0d1b4e4 Set ancient_date from command line arguments
* cbfc9e2 Add logging and command line parsing
* 51084cb Handle ÅÄÖ
* 9cffbb1 spellcheck wordpress/README.md
* 4b106d5 Move wordpress into sub-dir
* 3c7a49f Replace </span> with "", not "\n"
* 9850884 Tab to space, don't linebreak link lines
* 25bf120 replace tab with space
* 1622d5b Remove iframe, h3
* 840526d remove uneccessary / impossible requirement
* 7f04124 Spellcheck
* cec0152 README.md - the file we all just love to read!
* 806d3a4 Ignore the RSS file
* b728935 python dependencies
* 3451a1a Emit Yaml/Markdown to file
* 51691fd Filename stub generator
* b01f175 We only want latest and greatest from libsyn
* 3c52259 More RSS to Markdown/yaml
* 85a0443 Libysn RSS to Hugo Yaml/Markdown very early
* 099e48a Even better HTML to Markdown :)
* afd7313 Fix handling of \r\n</a> HTML
* e8c30fe Remove dir="blah" snippets
* 6bdc355 Make headers h2 hash-hash to mittigate JS crash
* 533ebae Better markdown
* 99de96e Remove stray <strong>
* d57cda6 More stable a href to markdown regexp
* cde8da3 Remove anoying data-saferedirecturl
* 6840568 Replace even more junk HTML
* b4eef53 Hack HTML to markdown some more
* 2f3ade3 More amazing HTML special cases for fun!
* 74f0bc5 Don't remove line breaks!
* 3be2a5b Split long lines
* e5c0975 a href to markdown link regexp
* 41072bc yaml for real, proper T date, early content
* 1735d89 Put pages under /pages
* 99f9b54 export post to file initial commit
* 6db11f8 Export job poc
* 356ff95 Truncate table
* 7b77d20 Make schemas public
* 3055d25 .gitignore
* 01bb735 Rename command
```

# v0.0.0

Commits:
``` plain
* 3b91f39 Import wordpress.py
```
