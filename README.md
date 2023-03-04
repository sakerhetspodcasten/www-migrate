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

Converts Wordpress MySQL to Hugo Yaml/Markdown and writes to:
* `../www-hugo/content/posts`
* `../www-hugo/content/pages`

An intermediary sqlite databse is used for ... reasons.

### Files:

* [import.wp.py](import.wp.py) - tool
* [wp-legacy/posts.mysql.schema](wp-legacy/posts.mysql.schema) - MySQL schema from an Wordpress export
* [wp-legacy/posts.schema](wp-legacy/posts.schema) - schema modified to be acceptable to sqlite3, our little utility helper database
* `wp-legacy/posts.sql` - the actual wordpress post insert SQL statements.
* `wp-legacy/sqllite.db` - our little helper database

### Usage

``` bash
python3 import.wp.py
```

## Miscellanous

* [.gitignore](.gitignore) - stuff we all just ignore
* [requirements.txt](requirements.txt) - stuff python3 depends upon

Install requirements:
``` bash
pip3 install -r requirements.txt
```

