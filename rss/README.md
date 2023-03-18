# Libsyn migration tool

Converts Libsyn RSS to Hugo Yaml/Markdown content/posts.

## Files:

* [import.rss.py](import.rss.py) - tool

## Usage

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

Usage showing `--no-overwrite` effect:
``` bash
# First run
python3 import.rss.py --no-overwrite --dir test --url https://sakerhetspodcasten.libsyn.com/rss
# 2023-03-18 21:53:06,568 INFO Request feed from https://sakerhetspodcasten.libsyn.com/rss
# 2023-03-18 21:53:18,196 INFO Update: test/sakerhetspodcasten_235_ostrukturerat_v_9.md
# 2023-03-18 21:53:18,197 INFO Update: test/sakerhetspodcasten_234_nyar_2022.md
# 2023-03-18 21:53:18,207 INFO Update: test/sakerhetspodcasten_233_ostrukturerat_v_3.md
# 2023-03-18 21:53:18,209 INFO Update: test/sakerhetspodcasten_232_jul_2022.md
# 2023-03-18 21:53:18,210 INFO Update: test/sakerhetspodcasten_231_ostrukturerat_v_51.md
# 2023-03-18 21:53:18,211 INFO Update: test/sakerhetspodcasten_230_testa_nya_saker.md
# 2023-03-18 21:53:18,212 INFO Update: test/sakerhetspodcasten_229_ostrukturerat_v_46.md
# 2023-03-18 21:53:18,213 INFO Update: test/sakerhetspodcasten_228_sec_t_community_night_2022.md
# 2023-03-18 21:53:18,214 INFO Update: test/sakerhetspodcasten_227_ostrukturerat_v_42.md
# 2023-03-18 21:53:18,215 INFO Update: test/sakerhetspodcasten_226_riskanalys.md
# 2023-03-18 21:53:18,215 INFO Update: test/sakerhetspodcasten_225_ostrukturerat_v_25.md
# 2023-03-18 21:53:18,216 INFO Update: test/sakerhetspodcasten_224_tjugofem_tips_for_ett_sakrare_liv.md
# 2023-03-18 21:53:18,217 INFO Update: test/sakerhetspodcasten_223_ostrukturerat_v_20.md
# 2023-03-18 21:53:18,218 INFO Update: test/sakerhetspodcasten_222_ostrukturerat_v_15.md
# 2023-03-18 21:53:18,219 INFO Update: test/sakerhetspodcasten_221_cyber_krig.md
# 2023-03-18 21:53:18,220 INFO Update: test/sakerhetspodcasten_220_ostrukturerat_v_11.md
# 2023-03-18 21:53:18,221 INFO Update: test/sakerhetspodcasten_219_nyarsspecial.md
# 2023-03-18 21:53:18,222 INFO Update: test/sakerhetspodcasten_218_sec_t_2021_del_2.md
# 2023-03-18 21:53:18,233 INFO Update: test/sakerhetspodcasten_217_ostrukturerat_v_3.md
# 2023-03-18 21:53:18,246 INFO Update: test/sakerhetspodcasten_216_ransomware.md
# 2023-03-18 21:53:18,247 INFO Update: test/sakerhetspodcasten_215_log4shell.md
# 2023-03-18 21:53:18,248 INFO Entries processed: 252
# 2023-03-18 21:53:18,248 INFO Entries skipped due to ancient date: 231
# 2023-03-18 21:53:18,249 INFO Entries skipped due to file exists/no-overwrite: 0
# 2023-03-18 21:53:18,250 INFO Files updated: 21

# Second run
python3 import.rss.py --no-overwrite --dir test --url https://sakerhetspodcasten.libsyn.com/rss
# 2023-03-18 21:53:30,349 INFO Request feed from https://sakerhetspodcasten.libsyn.com/rss
# 2023-03-18 21:53:41,567 INFO Entries processed: 252
# 2023-03-18 21:53:41,568 INFO Entries skipped due to ancient date: 231
# 2023-03-18 21:53:41,568 INFO Entries skipped due to file exists/no-overwrite: 21
# 2023-03-18 21:53:41,568 INFO Files updated: 0
```
