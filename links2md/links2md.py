#!.venv/bin/python3

import argparse
from bs4 import BeautifulSoup
import logging
import re
import requests

def logging_setup(level):
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    FORMAT = '%(asctime)s %(levelname)-s %(message)s'
    logging.basicConfig(format = FORMAT)

def readfile(filename):
    lines = []
    with open(filename) as file:
        while line := file.readline():
            lines.append( line.rstrip() )
    return lines


def unshorten(url):
    if url.startswith('http://youtu.be/'):
        url = url.replace('http://youtu.be/', 'http://www.youtube.com/watch?v=')
    return url


def get_author(url, soup):
    links = soup.head.find_all('link')
    for link in links:
        logger.debug(f'{url} link: {link}')
        #youtube: <link content="Rick Astley" itemprop="name"/>
        if link.has_attr('itemprop') and link.has_attr('content'):
            itemprop = link.itemprop
            content = link.content
            if itemprop == 'name':
                return content
    return None


def clean_whitespaces(text):
    text = text.strip()
    return ' '.join( text.split() )


do_not_visit_suffixes = [ '.mp3', '.pdf' ]

def process(url):
    if not url.startswith('https://'):
        return url
    url = unshorten(url)

    default = f'* {url}'
    for suffix in do_not_visit_suffixes:
        if url.endswith(suffix):
            return default

    r = None
    try:
        r = requests.get(url)
    except Exception as e:
        logger.debug(f'{url} {e}')
        ex = type(e).__name__
        return f'{default} `{ex}`'

    if r.status_code != 200:
       return f'{default} `{r.status_code}`'

    content_type = None
    if 'content-type' in r.headers:
        content_type = r.headers['content-type']
    elif 'Content-Type' in r.headers:
        content_type = r.headers['Content-Type']
    else:
        logger.debug(f'No content type: {url}')
        return default

    if content_type == 'text/html':
        pass
    elif content_type.startswith('text/html;'):
        pass
    else:
        logger.debug(f'Unsupported content-type: {content_type} @ {url}')
        return default

    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title
    if title is None:
        logger.warning(f'Error inspecting page without title: {url}')
        return url
    title = clean_whitespaces( title.text )
    author = get_author(url, soup)

    if title.endswith(' - YouTube'):
        title = title.replace(' - YouTube', '')
    if author is not None:
        if not author in title:
            title = author + ': ' + title

    tag = ''
    if url.startswith('https://www.youtube.com/watch'):
        tag = ' `video`'
    return f'* [{title}]({url}){tag}'


def main():
    parser = argparse.ArgumentParser(
            prog = 'links2md.py',
            description = 'convert links to markdown',
            epilog = 'Hope this help was helpful! :-)')
    parser.add_argument('--input', '-i',
            dest = "input_file",
            required = True,
            help = 'text file with urls to consume')
    parser.add_argument('--loglevel',
            dest = 'loglevel',
            default = 'INFO',
            choices = ['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    args = parser.parse_args()

    logging_setup(args.loglevel)

    lines = readfile( args.input_file )
    for line in lines:
        out = process( line )
        print(out)

if __name__ == "__main__":
    main()

