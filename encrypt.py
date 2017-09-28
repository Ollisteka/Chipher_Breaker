#!/usr/bin/env python3
import re
import sys
import argparse
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.learner import write_json_in_file
from logic.encryptor import read_json_file, reverse_substitution, \
    generate_substitution, code_stdin, code_text_from_file


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS] ALPHABET FILE'.format(
            os.path.basename(
                sys.argv[0])),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Encode text using substitution cipher',
        epilog="Made by Zhukova Olga, FT-202")

    subst_group = parser.add_mutually_exclusive_group(required=True)

    subst_group.add_argument(
        '-s',
        '--substitution',
        type=str,
        dest='substitution',
        metavar="FILENAME",
        help='file with the substitution in json format')
    subst_group.add_argument(
        '-r',
        '--reverse',
        type=str,
        dest='reverse',
        metavar="FILENAME",
        help='reverse substitution from file, and use it to encode text')
    subst_group.add_argument(
        '-g',
        '--generate',
        type=str,
        dest='generate',
        metavar="FILENAME",
        default="subst.txt",
        help='generate substitution and choose where to store it')

    parser.add_argument(
        'alph',
        metavar='alphabet',
        help='language, in which text is written (for example: A-Za-z)')
    parser.add_argument(
        'fn',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('r'),
        default=None,
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

    args = parser.parse_args()
    if not args.alph:
        sys.exit("Error: alphabet must be specified")

    if args.substitution:
        subst = read_json_file(args.substitution, args.encoding)
    elif args.reverse:
        subst = reverse_substitution(
            read_json_file(
                args.reverse,
                args.encoding))
    elif args.generate:
        subst = generate_substitution(args.alph)

    alph = re.compile('[' + args.alph + ']')
    if not args.fn:
        result = code_stdin(subst, alph)
    else:
        result = code_text_from_file(args.fn.name, args.encoding, subst, alph)

    # print("Saving substitution to '{}{}'...".format(os.path.sep, SUBST_FILE))
    write_json_in_file(args.generate, subst, args.encoding)
    # print("DONE")

    if args.output:
        with open(args.output, 'w', encoding=args.encoding) as file:
            file.write(result)
    else:
        sys.stdout.write(result)

if __name__ == '__main__':
    sys.exit(main())