import argparse
import re
import sys

def srt2md(header, file_in):
    buf = []
    for line in file_in:
        buf.append(line.rstrip())
        if len(buf) == 2:
            t0 = buf[0]
            t1 = buf[1]
            m0 = re.search("^[0-9]+$", t0)
            m1 = re.search("^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+ --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+$", t1)
            if m0 and m1:
                print(f"{header} {t0} {t1}")
                buf.clear()
            else:
                print(t0)
                del buf[0]

    for line in buf:
        print(line)

def main():
    parser = argparse.ArgumentParser(
            prog = 'srt2md.py',
            description = 'srt to markdown converter',
            epilog = 'Hope this help was helpful! :-)')

    parser.add_argument('-i', '--in',
            dest = 'filename_in',
            default = None,
            help = f'which file to read')

    parser.add_argument('-m', '--markdown-header',
            dest = 'markdown_header',
            default = "###",
            help = f'markdown header preamble, default ###')

    args = parser.parse_args()

    file_in = sys.stdin
    if args.filename_in is not None:
        file_in = open(args.filename_in)

    srt2md(args.markdown_header, file_in)

    if args.filename_in is not None:
        file_in.close()

if __name__ == "__main__":
    main()
