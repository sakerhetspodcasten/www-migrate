#!.venv/bin/python3

import argparse
from bs4 import BeautifulSoup
import json
import logging
import re
import requests
import time
import sys


logger = None


def logging_setup(level):
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    FORMAT = '%(asctime)s %(levelname)-s %(message)s'
    logging.basicConfig(format = FORMAT)


def readfile(file):
    lines = []
    while line := file.readline():
        lines.append( line.rstrip() )
    return lines


def unshorten(url):
    if url.startswith('https://youtu.be/'):
        url = url.replace('?', '&')
        url = url.replace('https://youtu.be/', 'https://www.youtube.com/watch?v=')
    return url


def append_params_to_url(url, param):
    if url is None:
        return param
    elif '?' in url:
        return url + '&' + param
    else:
        return url + '?' + param


def remove_garbage_params(url):
    us = re.split('\\?|\\&', url)

    if url.startswith('https://www.youtube.com/'):
        url = None
        for split in us:
            if split.startswith("si="):
                continue
            url = append_params_to_url(url, split)
        return url

    if len(us) == 2:
        if us[1] == 'm=1':
            # remove anying is mobile marker
            return us[0]

    return url


def parse_application_ld_json(script):
    site = None
    authors = []

    script_text = script.string
    try:
        jj = json.loads(script_text)
    except:
        logger.warning('Invalid <script type="application/ld+json">... did not parse')
        logger.debug(f'json: {script_text}')
        return site, authors


    # Some websites return object, some return list of object...
    # Canonicalize
    if not isinstance(jj, list):
        jj = [ jj ]

    for j in jj:
        if 'publisher' in j:
            publisher = j['publisher']
            if 'name' in publisher:
                name = publisher['name']
                site = site or name
        if 'author' in j:
            _author = j['author']
            # Some websites return object, some return list of object...
            # Canonicalize
            if not isinstance(_author, list):
                _author = [ _author ]
            for author in _author:
                if 'name' in author:
                    name = author['name']
                    if name not in authors:
                        authors.append(name)
    return site, authors

def get_site_author_description(url, soup):
    head = soup.head
    if head is None:
        return None, None, None

    site = None
    authors = [ ]
    description = None

    metas = soup.head.find_all('meta')
    if metas is not None:
        for meta in metas:
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
                elif name == 'description':
                    description = content

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
                _s, _a = parse_application_ld_json( script )
                site = site or _s
                for name in _a:
                    if name not in authors:
                        authors.append(name)

    logger.debug(f'Authors: {authors} @ {url}')
    logger.debug(f'Site: {site} @ {url}')
    author = None
    if len(authors) == 0:
        pass
    else:
        author = ", ".join(authors)
    return site, author, description


def clean_whitespaces(text):
    text = text.strip()
    return ' '.join( text.split() )


def process(url):
    if not url.startswith('https://'):
        return url
    url = unshorten(url)
    url = remove_garbage_params(url)

    default = f'* {url}'

    do_not_visit_suffixes = [ '.mp3', '.pdf' ]
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
        r = requests.get(url, headers=headers, timeout=10)
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
    site, author, description = get_site_author_description(url, soup)

    title_prefix = None
    if site is not None:
        if site == 'the Guardian':
            site = 'The Guardian'

        if title.endswith(' - ' + site):
            title = title.replace(' - ' + site, '')
        elif title.endswith(' | ' + site):
            title = title.replace(' | ' + site, '')
        if site not in title:
            title_prefix = site
    if author is not None:
        if title is None:
            title = author
        else:
            if not author in title:
                if title_prefix is None:
                    title_prefix = author
                else:
                    title_prefix = title_prefix + '/ ' + author
    if title_prefix is not None:
        title = title.replace(': ', ' - ')
        title = title_prefix + ': ' + title

    skip_description = False
    if description is None:
        skip_description = True
    if len(title) < 80:
        skip_description = True
    # blacklist of sites that tend to have unhelpful descriptions
    skip_description_prefix_list = [ 'https://www.youtube.com/' ]
    for prefix in skip_description_prefix_list:
        if url.startswith(prefix):
            skip_description = True
            break
    if not skip_description:
        description = clean_whitespaces( description )
        title = title + ' - ' + description

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
            help = 'text file with urls to consume. - for stdin.')
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

    lines = None
    if args.input_file == "-":
        lines = readfile(sys.stdin)
    else:
        with open(args.input_file) as file:
            lines = readfile(file)

    if args.output_file is None:
        process_lines( lines, sys.stdout )
    else:
        with open( args.output_file, 'a' ) as f:
            process_lines( lines, f )

if __name__ == "__main__":
    main()

