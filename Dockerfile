FROM ubuntu:noble

RUN apt update -y
RUN apt install python3 -y
RUN apt install python3.12-venv -y

COPY rss/import.rss.py rss/requirements.in rss/venv.sh /build/rss/

RUN cd /build/rss && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 import.rss.py -h

COPY wordpress/import.wp.py wordpress/requirements.in wordpress/venv.sh /build/wordpress
COPY wordpress/wp-legacy/posts.mysql.schema wordpress/wp-legacy/posts.schema /build/wordpress/wp-legacy/

RUN cd /build/wordpress && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 import.wp.py -h

COPY srt2md/srt2md.py /build/srt2md/

RUN python3 /build/srt2md/srt2md.py -h

COPY tagger/requirements.in tagger/tagmd.py tagger/venv.sh /build/tagger/

RUN cd /build/tagger && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 tagmd.py -h
