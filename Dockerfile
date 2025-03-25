ARG REQUIREMENT_TXT="keep"

FROM ubuntu:noble

RUN \
 apt update -y && \
 apt install python3 -y && \
 apt install python3.12-venv -y

COPY lock.sh /build/

COPY \
 links2md/links2md.py \
 links2md/requirements.in \
 links2md/requirements.lock \
 links2md/requirements.txt \
 links2md/venv.sh \
 /build/links2md/

COPY \
 rss/import.rss.py\
 rss/requirements.in\
 rss/requirements.lock\
 rss/requirements.txt\
 rss/venv.sh\
 /build/rss/

COPY srt2md/srt2md.py /build/srt2md/

COPY \
 tagger/requirements.in\
 tagger/requirements.lock\
 tagger/requirements.txt\
 tagger/taglist.py\
 tagger/tagmd.py\
 tagger/venv.sh\
 /build/tagger/

COPY \
 wordpress/import.wp.py\
 wordpress/requirements.in\
 wordpress/requirements.lock\
 wordpress/requirements.txt\
 wordpress/venv.sh\
 /build/wordpress
COPY \
 wordpress/wp-legacy/posts.mysql.schema\
 wordpress/wp-legacy/posts.schema\
 /build/wordpress/wp-legacy/

RUN test "$REQUIREMENT_TXT" = "refresh" ||\
 rm \
 /build/links2md/requirements.txt\
 /build/links2md/requirements.lock\
 /build/rss/requirements.txt\
 /build/rss/requirements.lock\
 /build/tagger/requirements.txt\
 /build/tagger/requirements.lock\
 /build/wordpress/requirements.txt\
 /build/wordpress/requirements.lock

RUN cd /build/links2md && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 links2md.py -h
RUN cd /build/ && ./lock.sh links2md

RUN cd /build/rss && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 import.rss.py -h
RUN cd /build/ && ./lock.sh rss

RUN cd /build/tagger && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 tagmd.py -h && \
  .venv/bin/python3 taglist.py -h
RUN cd /build/ && ./lock.sh tagger

RUN python3 /build/srt2md/srt2md.py -h

RUN cd /build/wordpress && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 import.wp.py -h
RUN cd /build/ && ./lock.sh wordpress

