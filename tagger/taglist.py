import argparse
import logging
import os
import yaml

# Global variables
logger = None
search_tag = None
search_tagcount = None

def logging_setup(level):
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    FORMAT = '%(asctime)s %(levelname)-s %(message)s'
    logging.basicConfig(format = FORMAT)

def parse(file):
    header=[]
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
                            break
                case 'READ_YAML':
                    match line:
                        case '---':
                            break
                        case _:
                            header.append(line)
    strheader="\n".join(str(h) for h in header)
    yheader=yaml.safe_load(strheader)
    return yheader

def good_count(count):
    sc = search_tagcount

    if sc is None:
        return True
    if sc.isdigit():
        return int(sc) == count
    if sc.startswith('<='):
        sc = int(sc[2:])
        return count <= int(sc)
    if sc.startswith('<'):
        sc = int(sc[1:])
        return count < int(sc)
    if sc.startswith('>='):
        sc = int(sc[2:])
        return count >= int(sc)
    if sc.startswith('>'):
        sc = int(sc[1:])
        return count > int(sc)
    raise Exception(f'Bad argument: {sc}')

def process_file(file):
    logger.debug(f"Process {file}")

    header=None
    try:
        header=parse(file)
    except yaml.parser.ParserError:
        logger.error(f'Error safe yaml parser failed on: {file}')
        return

    if header is None:
        return
    if len(header) == 0:
        logger.warning(f'Skip {file} due to empty header')
        return
    tags = []
    if 'tags' in header:
        tags = header["tags"]

    if search_tag is not None:
        found = False
        for tag in tags:
            if tag == search_tag:
                found = True
                break
        if not found:
            return

    if not good_count(len(tags)):
        return

    print(f"{file}: {tags}")

def good_filename(filename):
    valid_suffixes = [".md", ".markdown", ".yaml", ".yml"]
    good_suffix = False
    for valid_suffix in valid_suffixes:
        if filename.endswith(valid_suffix):
            good_suffix = True
            break
    if not good_suffix:
        return False
    invalid_prefixes = ["."]
    good_prefix = True
    for invalid_suffix in invalid_prefixes:
        if filename.startswith(invalid_suffix):
            good_prefix = False
            break
    if not good_prefix:
        return False
    return True

def process(file):
    if not os.path.exists(file):
        logger.warning(f'File does not exists: {file}')
        return

    if os.path.isfile(file):
        process_file(file)
        return

    for (dirpath, dirnames, filenames) in os.walk(file):
        for filename in filenames:
            if not good_filename(filename):
                continue
            full_filename = os.path.join(dirpath,filename)
            if os.path.isfile(full_filename):
                process_file(full_filename)

def main():
    global search_tag
    global search_tagcount
    parser = argparse.ArgumentParser(
            prog = 'taglist.py',
            description = 'list files with tags',
            epilog = 'Hope this help was helpful! :-)')
    parser.add_argument('--tag', '-t',
            dest = 'tag',
            help = 'file files with tag')
    parser.add_argument('--tagcount', '-c',
            dest = 'tagcount',
            help = 'file files with tag')
    parser.add_argument('file',
            nargs='+',
            help = 'files or directories to process')
    parser.add_argument('--loglevel',
            dest = 'loglevel',
            default = 'INFO',
            choices = ['DEBUG','INFO','WARNING','ERROR','CRITICAL'])
    args=parser.parse_args()

    logging_setup(args.loglevel)

    search_tag = args.tag
    search_tagcount = args.tagcount
    for file in args.file:
        process(file)

if __name__ == "__main__":
    main()
