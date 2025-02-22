import argparse
import re
import sys


def main():
    parser = argparse.ArgumentParser(
            prog = 'srt2md.py',
            description = 'srt to markdown converter',
            epilog = 'Hope this help was helpful! :-)')

    parser.add_argument('-i', '--in',
            dest = 'filename_in',
            default = None,
            help = f'which file to read')

    args = parser.parse_args()

    file_in = sys.stdin
    if args.filename_in is not None:
        file_in = open(args.filename_in)

    buf = []
    for line in file_in:
        buf.append(line)
        if len(buf) == 2:
            t1 = buf[0].rstrip()
            t2 = buf[1].rstrip()
            m1 = re.search("^[0-9]+$", t1)
            m2 = re.search("^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+ --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+$", t2)
            #print(f"t1:{t1} t2:{t2}")
            #print(f"m1:{m1} m2:{m2}")
            if m1 and m2:
                print(f"### {t1} {t2}")
                buf.clear()
            else:
                t = buf.pop(0)
                print(t)

    for line in buf:
        print(line.rstrip())

    if args.filename_in is not None:
        file_in.close()

if __name__ == "__main__":
    main()
