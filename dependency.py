# coding=utf-8
# !/usr/bin/env python3
# coding=utf-8
import argparse
import os
import re
import sys
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.learner import write_json_in_file
from logic.decryptor import SubstitutionHacker
import logic.encryptor as e


def main():
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS] ALPHABET STAT FILE'.format(
            os.path.basename(
                sys.argv[0])),
        description='count the percentage of correctly guessed letters')

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
        '-d',
        '--debug',
        action='store_true',
        dest='debug',
        help='enable debug output')

    parser.add_argument(
        '-e',
        '--encoding',
        type=str,
        dest='encoding',
        default='utf-8',
        help='choose FILE (and output file, if key -o is chosen) encoding')

    parser.add_argument('-t', '--top', type=int, dest='top', default=15000,
                        help='choose, how many popular words will be stored')

    args = parser.parse_args()
    with open(args.fn.name) as file:
        original_text = file.read()
    coded_text = e.code(original_text,
                        e.generate_substitution(args.alph),
                        re.compile('[' + args.alph + ']'))

    result = {}
    for n in range(1, 101):
        sample = coded_text[:n * 25]
        original_sample = original_text[:n * 25]
        hacker = SubstitutionHacker(
            args.alph,
            args.stat,
            args.encoding,
            code_text=sample,
            top=args.top)
        hacker.hack()
        decoded_sample = hacker.decode_text(sample)
        diff = count_diff(decoded_sample, original_sample)
        res = ((len(sample) - diff) * 100) / len(sample)
        result[n * 25] = res
        if args.debug:
            print("Text\'s length {0}; Sample\'s length; {1} n is {2}; "
                  "Correctly guessed {3}%;"
                  .format(str(len(coded_text)), str(n * 25), str(n),
                          str(round(res, 2))))
        if len(coded_text) < n * 25:
            break

    if args.output:
        write_json_in_file(args.output, result, args.encoding)
    else:
        pprint(result)

    print("Last variant:\n", decoded_sample)


def count_diff(text_one, text_two):
    """

    :type text_one: str
    :type text_two: str
    :return:
    """
    i = 0
    count = 0
    for char in text_one:
        if char != text_two[i]:
            count += 1
        i += 1
    return count


if __name__ == '__main__':
    sys.exit(main())
