import argparse
import re
import sys

def srt2md(header, file_in, file_out):
    buf = []
    for line in file_in:
        buf.append(line.rstrip())
        if len(buf) == 2:
            t0 = buf[0]
            t1 = buf[1]
            m0 = re.search("^[0-9]+$", t0)
            m1 = re.search("^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+(\.[0-9]+)? --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]+(\.[0-9]+)?$", t1)
            if m0 and m1:
                print(f"{header} {t0} {t1}", file=file_out)
                buf.clear()
            else:
                print(t0, file=file_out)
                del buf[0]

    for line in buf:
        print(line, file=file_out)

def main():
    parser = argparse.ArgumentParser(
            prog = 'srt2md.py',
            description = 'srt to markdown converter',
            epilog = 'Hope this help was helpful! :-)')

    parser.add_argument('-i', '--in',
            dest = 'filename_in',
            default = None,
            help = f'File to read, default is <stdin>')

    parser.add_argument('-o', '--out',
            dest = 'filename_out',
            default = None,
            help = f'File to write, default is <stdout>')

    parser.add_argument('-O', '--output-mode',
            dest = 'output_mode',
            default = 'a',
            choices=['a', 'w', 'x'],
            help = f'File output mode; a: append (default), w: truncating write, x: eXclusively create.')

    parser.add_argument('-m', '--markdown-header',
            dest = 'markdown_header',
            default = "###",
            help = f'markdown header preamble, default ###')

    args = parser.parse_args()

    file_in = None
    if args.filename_in is not None:
        file_in = open(args.filename_in)
    else:
        file_in = sys.stdin
        if sys.stdin.isatty():
            print("Warning: converting <stdin> TTY to Markdown", file=sys.stderr)

    file_out = None
    if args.filename_out is not None:
        file_out = open(args.filename_out, args.output_mode)
    else:
        file_out = sys.stdout

    #
    # Call the actual useful logic
    #
    srt2md(args.markdown_header, file_in, file_out)

    if args.filename_out is not None:
        file_out.close()

    if args.filename_in is not None:
        file_in.close()

if __name__ == "__main__":
    main()
