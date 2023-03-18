import argparse
import datetime
import feedparser
import logging
import os
import re
import time
import yaml

ancient_date=None
logger=None

def load_rss():
    d = feedparser.parse('./libsyn-legacy/rss')
    return d

def timestruct_to_isoformat(ts):
    t = time.mktime(ts)
    dt = datetime.datetime.fromtimestamp(t)
    iso = dt.isoformat()
    return iso

def gimme_mp3(links):
    yolo=None
    for link in links:
        href = link['href']
        if href.endswith('.mp3'):
            return href
        else:
            yolo = href
    return yolo

def line_break_text(text):
    out=""
    lines = text.split("\n")
    for line in lines:
        if " " not in line:
            out = out + line + "\n"
            continue
        if len(line) < 100:
            out = out + line + "\n"
            continue
        try:
            index = line.index(" ", 80)
        except ValueError as ve:
            out = out + line + "\n"
            continue
        a = line[:index].strip(' ')
        b = line[index:].strip(' ')
        out = out + a + "\n"
        out = out + line_break_text(b)
    return out

def libsyn_to_markdown(text):
    text = re.sub("<[/]*p>", "", text)
    text = re.sub('<a href="([^"]+)">([^<]+)</a>', r"[\2](\1)", text)
    text = line_break_text( text )
    return text

def ancient_setup(ad):
    global ancient_date
    if ad is None:
        # Extremly specific for our puproses.
        # Older than November 2021, we don't care
        ancient_date = 202111
        return
    if ad == 'None' or ad == 'none':
        ancient_date = None
        return
    if len( ad ) == 6:
        ancient_date = int( ad )
        return
    raise Exception(f"Incomprehensible ancient date: {ad}")

def ancient(st):
    if ancient_date is None:
        return False
    value = st.tm_year * 100 + st.tm_mon
    if value <= ancient_date:
        return True
    return False

def generate_filename(title):
    fn = title
    fn = fn.lower()
    fn = fn.replace('å','a')
    fn = fn.replace('ä','a')
    fn = fn.replace('ö','o')
    fn = fn.replace('Å','A')
    fn = fn.replace('Ä','A')
    fn = fn.replace('Ö','O')
    fn = re.sub('[^a-zA-Z0-9]+', '_', fn)
    fn = fn.strip('_')
    fn = fn + ".md"
    return fn

def mkdir(p):
    if not os.path.exists(p):
        os.makedirs(p)

def process_entry(e):
    published    = e['published']
    published_p  = e['published_parsed']
    if ancient(published_p):
        logger.debug(f"Ignore old: {published}")
        return
    title        = e['title']
    summary      = e['summary']
    duration     = e['itunes_duration']
    links        = e['links']
    published_pp  = timestruct_to_isoformat( published_p )
    mp3 = gimme_mp3(links)

    fdir = "../www-hugo/content/posts"
    mkdir(fdir)

    fname = generate_filename(title)
    logger.info(f"Filename: {fname} ({title})")
    with open(fdir + "/" + fname, "w") as f:
        header = {}
        header['title'] = title
        header['date'] = published_pp
        header_yaml = yaml.dump(header)
        md_content = libsyn_to_markdown(summary)
        f.write("---\n")
        f.write(header_yaml)
        f.write("---\n")
        f.write("## Lyssna\n")
        f.write(f"* [mp3]({mp3}), längd: {duration}\n\n")
        f.write("## Innehåll\n")
        f.write(md_content)

def logging_setup(level):
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    FORMAT = '%(asctime)s %(levelname)-s %(message)s'
    logging.basicConfig(format=FORMAT)

def main():
    parser = argparse.ArgumentParser(
            prog='import.rss.py',
            description='Libsyn RSS to Hugo converter (Alpha quality only!)',
            epilog='Hope this help was helpful! :-)')
    parser.add_argument('--ancient_date',
            dest='ancient_date',
            default=None,
            help='Date in YYYYMM format that is a post too old to migrate. Set to either of [None,none] to migrate all.')
    parser.add_argument('--loglevel',
            dest='loglevel',
            default='WARNING',
            choices=['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    args = parser.parse_args()
    logging_setup(args.loglevel)
    ancient_setup(args.ancient_date)
    rss = load_rss()
    entries = rss['entries'];
    for entry in entries:
        process_entry(entry)

if __name__ == "__main__":
    main()
