#!/usr/bin/env python3
import sys
import argparse
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.learner import write_json_in_file
from logic.decryptor import SubstitutionHacker

LETTERS = "letters"
WORDS = "words"
NGRAMMS = "ngramms"


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS] ALPHABET STAT FILE'.format(
            os.path.basename(
                sys.argv[0])),
        description='Decode text, encrypted in substitution cipher')

    parser.add_argument(
        'alph',
        metavar='alphabet',
        help='language, in which text is written (for example: A-Za-z)')

    parser.add_argument(
        'stat',
        metavar='stat',
        help='statistics of the language')

    parser.add_argument(
        'fn',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='name of the file with text')
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        dest='output',
        metavar="FILENAME",
        help='choose, where to store output')
    parser.add_argument(
        '-e',
        '--encoding',
        type=str,
        dest='encoding',
        default='utf-8',
        help='choose FILE (and output file, if key -o is chosen) encoding')
    parser.add_argument(
        '-s',
        '--substitution',
        type=str,
        dest='substitution',
        metavar="FILENAME",
        help='file where to store right substitution')

    parser.add_argument('-t', '--top', type=int, dest='top',
                        help='choose, how many popular words will be stored')

    args = parser.parse_args()
    if not args.alph:
        sys.exit("Error: alphabet must be specified")

    hacker = SubstitutionHacker(
        args.alph,
        args.stat,
        args.encoding,
        args.fn,
        args.top)
    key = hacker.hack()
    if args.fn.name == '<stdin>':
        decoded_text = hacker.decode_stdin()
    else:
        decoded_text = hacker.decode_file(args.fn.name, args.encoding)

    if args.output:
        with open(args.output, 'w', encoding=args.encoding) as file:
            file.write(decoded_text)
    else:
        sys.stdout.write(decoded_text)

    if args.substitution:
        write_json_in_file(args.substitution, key, args.encoding)


if __name__ == '__main__':
    sys.exit(main())