import argparse
import logging
import os
import yaml

# Global variables, arguments
logger = None

def logging_setup(level):
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    FORMAT = '%(asctime)s %(levelname)-s %(message)s'
    logging.basicConfig(format = FORMAT)

def parse(file):
    header=[]
    content=[]
    mode='FIND_YAML'
    with open(file, 'r') as file:
        for line in file:
            line = line.rstrip()
            match mode:
                case 'FIND_YAML':
                    match line:
                        case '---':
                            mode='READ_YAML'
                        case _:
                            content.append(line)
                            mode='READ_CONTENT'
                case 'READ_YAML':
                    match line:
                        case '---':
                            mode='READ_CONTENT'
                        case _:
                            header.append(line)
                case 'READ_CONTENT':
                    content.append(line)
    for h in header:
        logger.debug(f'H: {h}')
    #for c in content:
    #    logger.debug(f'File: {file} C: {c}')

    strheader="\n".join(str(h) for h in header)
    yheader=yaml.safe_load(strheader)
    return yheader, content

def emit(file, header, content):
    seperator = '---\n'.encode('utf-8')
    linefeed = '\n'.encode('utf-8')
    encoded_header = yaml.dump(header, encoding="utf8", allow_unicode=True)
    with open(file, 'wb') as f:
        f.write(seperator)
        f.write(encoded_header)
        f.write(seperator)
        for line in content:
            f.write(line.encode('utf-8'))
            f.write(linefeed)

def process(file, before, after):
    if not os.path.isfile(file):
        logger.warning(f'File does not exists: {file}')
        return
    logger.info(f"Process {file}")

    header, content = parse(file)
    

    if len(header) == 0:
        logger.warning(f'Skip {file} due to empty header')
        return
    if len(content) == 0:
        logger.warning(f'Skip {file} due to empty content')
        return
    if 'title' not in header:
        logger.warning(f'Skip {file} due to no title')
        return
    title = header['title']
    if type(title) != str:
        logger.warning(f'Skip {file} due to title type error')
        return

    logger.debug(f"before: {header}")
    title = title.replace(before, after)
    header['title'] = title
    logger.debug(f"after: {header}")

    emit(file, header, content)

def main():
    parser = argparse.ArgumentParser(
            prog = 'title-fixer.py',
            description = 'add tags to yaml/md contant files',
            epilog = 'Hope this help was helpful! :-)')
    parser.add_argument('--old-term',
            dest = 'old',
            required = True,
            help = 'thing to search for.')
    parser.add_argument('--new-term',
            dest = 'new',
            required = True,
            help = 'thing to replace with.')
    parser.add_argument('file',
            nargs='+',
            help = 'files to process')
    parser.add_argument('--loglevel',
            dest = 'loglevel',
            default = 'INFO',
            choices = ['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    args=parser.parse_args()

    logging_setup(args.loglevel)

    for file in args.file:
        process(file, args.old, args.new)

if __name__ == "__main__":
    main()
