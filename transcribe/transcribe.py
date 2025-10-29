#!.venv/bin/python3

import argparse
import hashlib
import os.path
import re
import requests
import tempfile
import subprocess
import sys

def download(url, download_dir):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with tempfile.TemporaryFile(dir=download_dir) as f:
            m = hashlib.sha256()
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                m.update(chunk)

            identifier = m.hexdigest()
            filename = os.path.join(download_dir, identifier)

            if os.path.exists(filename):
                print(f'Warning, allready exists {filename}', file=sys.stderr)
                return identifier

            f.seek(0)
            with open(filename, 'wb') as f2:
                while True:
                    chunk = f.read(8192)
                    if len(chunk) == 0:
                        break
                    f2.write(chunk)

            return identifier

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

def srt2md(file_in, file_out):
    buf = []
    for line in file_in:
        buf.append(line.rstrip())
        if len(buf) == 2:
            t0 = buf[0]
            t1 = buf[1]
            m0 = re.search('^[0-9]+$', t0)
            m1 = re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+(\\.[0-9]+)? --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+(\\.[0-9]+)?$', t1)
            if m0 and m1:
                print(f"`{t0} {t1}`", file=file_out)
                buf.clear()
            else:
                md = cleanup_markdown(t0)
                print(md, file=file_out)
                print("", file=file_out)
                del buf[0]

    for line in buf:
        print(line, file=file_out)

def cleanup_markdown(transcription):
    out = ""
    special_long  = "\\`*_{}[]<>()#+-.!|"
    special_short = "\\`*_{}[]<>()#+!|"
    special = special_long
    for c in transcription:
        if c in special:
            out += "\\"
        out += c
        if c != " ":
            # '-' no longer means start of list...
            # - and . looks annoying when replaced in general text.
            special = special_short
    return out

def main():
    parser = argparse.ArgumentParser(
            prog = 'transcribe.py',
            description = 'transcription tool', #TODO write a description
            epilog = 'Hope this help was helpful! :-)')
    parser.add_argument('--dir-mp3',
            dest = 'dir_mp3',
            required = True,
            help = 'directory to download mp3s to')
    parser.add_argument('--dir-trans',
            dest = 'dir_trans',
            required = True,
            help = 'directory to store transcriptions to')
    parser.add_argument('--transcribe-header',
            dest = 'transcribe_header',
            default = 'AI transkribering',
            help = 'directory prefix to append to file names')
    parser.add_argument('--transcribe-description',
            dest = 'transcribe_description',
            default = 'AI försöker förstå oss... Ha överseende med galna feltranskriberingar.',
            help = 'A short comment about the transcription')
    parser.add_argument('--whisper-bin',
                        dest = 'whisper_bin',
                        default = '.venv/bin/whisper',
                        help = 'whisper executable')
    parser.add_argument('file',
            nargs='+',
            help = 'files to process')
    args=parser.parse_args()

    if not os.path.isdir(args.dir_mp3):
        print(f'Error: not a dir {args.dir_mp3}', file=sys.stderr)
        return SystemExit, 1

    if not os.path.isdir(args.dir_trans):
        print(f'Error: not a dir {args.dir_trans}', file=sys.stderr)
        return SystemExit, 1

    for file in args.file:
        parsed = parse_md(file, args.transcribe_header)
        if parsed is None:
            continue
        (mp3, transcribed) = parsed
        if transcribed:
            continue
        print(f"{file}")
        print(f' * mp3: {mp3}')
        identifier = download(mp3, args.dir_mp3)
        mp3_filename = os.path.join(args.dir_mp3, identifier)
        srt = os.path.join(args.dir_trans, identifier + ".srt")

        if not os.path.exists(srt):
            subprocess.run([args.whisper_bin, "--model", "large", "--language", "Swedish", "--task", "transcribe", "--output_format", "all", "--output_dir", args.dir_trans, mp3_filename])

        with open(srt) as file_in:
            with open(file, "a") as file_out:
                print("", file=file_out)
                print(f"## {args.transcribe_header}", file=file_out)
                print("", file=file_out)
                print(f"_{args.transcribe_description}_", file=file_out)
                print("", file=file_out)
                srt2md(file_in, file_out)

if __name__ == "__main__":
    main()
