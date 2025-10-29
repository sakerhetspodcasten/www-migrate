import argparse
import os.path
import re
import sys

def download(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def parse_md(fname, transcribe_header):
    if not os.path.isfile(fname):
        print(f'Error: not a file {fname}', file=sys.stderr)
        return None
    mp3 = None
    transcribed = False
    with open(fname, 'r') as file:
        needle = transcribe_header.lower()
        for line in file:
            if line.startswith("#"):
                if needle in line.lower():
                    transcribed = True
            if mp3 is None:
                pattern = r'\[mp3\]\((.*?)\)'
                match = re.search(pattern, line)
                if match:
                   mp3 = match.group(1)
    return (mp3, transcribed)

def main():
    parser = argparse.ArgumentParser(
            prog = 'transcribe.py',
            description = 'transcription tool', #TODO write a description
            epilog = 'Hope this help was helpful! :-)')
    #parser.add_argument('--dir-mp3',
    #        dest = 'dir_mp3',
    #        required = True,
    #        help = 'directory to download mp3s to')
    #parser.add_argument('--dir-trans',
    #        dest = 'dir_trans',
    #        required = True,
    #        help = 'directory to download mp3s to')
    parser.add_argument('--transcribe-header',
            dest = 'transcribe_header',
            default = 'AI transkribering',
            help = 'directory prefix to append to file names')
    parser.add_argument('--transcribe-description',
            dest = 'transcribe_description',
            default = 'AI försöker förstå oss... Ha överseende med galna feltranskriberingar.',
            help = 'A short comment about the transcription')
    parser.add_argument('--whisper-bin',
                        dest = 'whisper-bin',
                        default = '.venv/bin/whisper',
                        help = 'whisper executable')
    parser.add_argument('file',
            nargs='+',
            help = 'files to process')
    args=parser.parse_args()

    for file in args.file:
        parsed = parse_md(file, args.transcribe_header)
        if parsed is None:
            continue
        (mp3, transcribed) = parsed
        if transcribed:
            continue
        print(f"{file}")
        print(f' * mp3: {mp3}')
        #print(f' * transcribed: {transcribed}')

if __name__ == "__main__":
    main()
