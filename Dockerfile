ARG REQUIREMENT_TXT="keep"

FROM ubuntu:noble

RUN \
 apt update -y && \
 apt install python3 -y && \
 apt install python3.12-venv -y

COPY rss/import.rss.py rss/requirements.in rss/requirements.txt rss/venv.sh /build/rss/

COPY srt2md/srt2md.py /build/srt2md/

COPY tagger/requirements.in tagger/requirements.txt tagger/taglist.py tagger/tagmd.py tagger/venv.sh /build/tagger/

COPY wordpress/import.wp.py wordpress/requirements.in wordpress/requirements.txt wordpress/venv.sh /build/wordpress
COPY wordpress/wp-legacy/posts.mysql.schema wordpress/wp-legacy/posts.schema /build/wordpress/wp-legacy/

RUN test "$REQUIREMENT_TXT" = "refresh" ||\
 rm /build/rss/requirements.txt\
 /build/tagger/requirements.txt\
 /build/wordpress/requirements.txt

RUN cd /build/rss && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 import.rss.py -h

RUN cd /build/wordpress && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 import.wp.py -h

RUN python3 /build/srt2md/srt2md.py -h

RUN cd /build/tagger && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 tagmd.py -h && \
  .venv/bin/python3 taglist.py -h
