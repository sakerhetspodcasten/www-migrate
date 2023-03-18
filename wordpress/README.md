# Wordpress migration tool

Converts Wordpress MySQL to Hugo Yaml/Markdown and writes to:
* `../../www-hugo/content/posts`
* `../../www-hugo/content/pages`

An intermediary `SQLite` database is used for ... reasons.

## Usage

``` bash
python3 import.wp.py
```

## Files:

* [import.wp.py](import.wp.py) - tool
* [wp-legacy/posts.mysql.schema](wp-legacy/posts.mysql.schema) - MySQL schema from an Wordpress export
* [wp-legacy/posts.schema](wp-legacy/posts.schema) - schema modified to be acceptable to SQLite3, our little utility helper database
* `wp-legacy/posts.sql` - the actual Wordpress post insert SQL statements.
* `wp-legacy/sqllite.db` - our little helper database
