import argparse
import os
import sys

from .thumbnail import create_thumbnail

parser = argparse.ArgumentParser()
parser.add_argument('-r', type=int, dest='resize_to', help='Thumbnail to (square side length in px)')
parser.add_argument("input", help="Input filename")
parser.add_argument("output", help="Output filename or - for stdout")


def main():
    args = parser.parse_args()
    thumbnail_buffer = create_thumbnail(args.input, resize_to=args.resize_to)
    if not thumbnail_buffer:
        raise Exception('No suitable thumbnailer found.\n')

    if args.output == '-':
        os.write(sys.stdout.fileno(), thumbnail_buffer.read())
    else:
        file(args.output, 'wb').write(thumbnail_buffer.read())

if __name__ == "__main__":
    main()
