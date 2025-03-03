import argparse
import logging
import os
import yaml

# Global variables, arguments
logger = None

def add_tag(y, tag):
    tags=[]
    if "tags" in y:
        tags=y["tags"]
    if tag in tags:
        return
    tags.append(tag)
    y["tags"]=tags

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
        logger.debug(f'File: {file} H: {h}')
    for c in content:
        logger.debug(f'File: {file} C: {c}')

    strheader="\n".join(str(h) for h in header)
    yheader=yaml.safe_load(strheader)
    return yheader, content

def emit(file, header, content):
    with open(file, 'w') as f:
        f.write('---\n')
        f.write( yaml.dump(header) )
        f.write('\n---\n')
        for line in content:
            f.write( line )
            f.write( '\n' )

def process(file, tag):
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

    logger.debug(f"before: {header}")
    add_tag(header, tag)
    logger.debug(f"after: {header}")

    emit(file, header, content)

def main():
    parser = argparse.ArgumentParser(
            prog = 'tagmd.py',
            description = 'add tags to yaml/md contant files',
            epilog = 'Hope this help was helpful! :-)')
    parser.add_argument('--tag', '-t',
            dest = 'tag',
            required = True,
            help = 'tag to add to markdown files')
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
        process(file, args.tag)

if __name__ == "__main__":
    main()
