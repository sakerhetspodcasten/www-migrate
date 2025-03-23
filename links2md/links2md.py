#!.venv/bin/python3

import argparse
from bs4 import BeautifulSoup
import json
import logging
import re
import requests
import time
import sys

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


def get_site_author(url, soup):
    site = None
    authors = [ ]

    metas = soup.head.find_all('meta')
    for meta in metas:
        #<meta property="og:site_name" content="Ars Technica" />
        if meta.has_attr('property') and meta.has_attr('content'):
            _property = meta['property']
            content = meta['content']
            if _property == 'og:site_name':
                site = content
        if meta.has_attr('name') and meta.has_attr('content'):
            name = meta['name']
            content = meta['content']
            if name == 'parsely-page':
                j = json.loads(content)
                if 'author' in j:
                    author = j['author']
                    if author not in authors:
                        authors.append(author)

    links = soup.head.find_all('link')
    for link in links:
        #youtube: <link content="Rick Astley" itemprop="name"/>
        if link.has_attr('itemprop') and link.has_attr('content'):
            itemprop = link['itemprop']
            content = link['content']
            if itemprop == 'name':
                if content not in authors:
                    authors.append(content)

    scripts = soup.head.find_all('script')
    for script in scripts:
        if script.has_attr('type'):
            _type = script['type']
            if _type == 'application/ld+json':
                script_text = script.string
                j = json.loads(script_text)
                if 'author' in j:
                    author = j['author']
                    if 'name' in author:
                        name = author['name']
                        if name not in authors:
                            authors.append(name)

    logger.debug(f'Authors: {authors} @ {url}')
    logger.debug(f'Site: {site} @ {url}')
    author = None
    if len(authors) == 0:
        pass
    else:
        author = ",".join(authors)
    return site, author


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

    # reduce chance of being considered spammy
    time.sleep(0.3)

    r = None
    try:
        headers = {
                'user-agent': 'curl/8.5.0',
                'accept': '*/*' }
        r = requests.get(url, headers=headers)
        #r = requests.get(url)
    except Exception as e:
        logger.debug(f'{url} {e}')
        ex = type(e).__name__
        return f'{default} `{ex}`'

    if r.status_code != 200:
        text = clean_whitespaces( r.text )
        logger.debug(f'{url} {r.status_code} {r.reason} {text}')
        return f'{default} `{r.status_code}` `{r.reason}`'

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
    site, author = get_site_author(url, soup)

    title_prefix = None
    if site is not None:
        if title.endswith(' - ' + site):
            title = title.replace(' - ' + site, '')
        elif title.endswith(' | ' + site):
            title = title.replace(' | ' + site, '')
        if site not in title:
            title_prefix = site
    if author is not None:
        if not author in title:
            if title_prefix is None:
                title_prefix = author
            else:
                title_prefix = title_prefix + '/ ' + author
    if title_prefix is not None:
        title = title.replace(': ', ' - ')
        title = title_prefix + ': ' + title

    tag = ''
    if url.startswith('https://www.youtube.com/watch'):
        tag = ' `video`'
    return f'* [{title}]({url}){tag}'


def process_lines(lines, out):
    for line in lines:
        processed = process( line )
        print(processed, file = out)


def main():
    parser = argparse.ArgumentParser(
            prog = 'links2md.py',
            description = 'convert links to markdown',
            epilog = 'Hope this help was helpful! :-)')
    parser.add_argument('--input', '-i',
            dest = "input_file",
            required = True,
            help = 'text file with urls to consume')
    parser.add_argument('--output', '-o',
            dest = "output_file",
            default = None,
            required = False,
            help = 'text file with urls to consume. Default is stdout.')
    parser.add_argument('--loglevel',
            dest = 'loglevel',
            default = 'INFO',
            choices = ['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    args = parser.parse_args()

    logging_setup(args.loglevel)

    lines = readfile( args.input_file )
    if args.output_file is None:
        process_lines( lines, sys.stdout )
    else:
        with open( args.output_file, 'a' ) as f:
            process_lines( lines, f )

if __name__ == "__main__":
    main()

