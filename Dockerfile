FROM ubuntu:noble

RUN apt update -y
RUN apt install python3 -y
RUN apt install python3.12-venv -y

COPY  rss/import.rss.py rss/requirements.in rss/venv.sh /build/rss/

RUN cd /build/rss && \
  bash -c "source venv.sh" && \
  .venv/bin/python3 import.rss.py -h
