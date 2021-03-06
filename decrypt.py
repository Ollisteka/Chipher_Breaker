#!/usr/bin/env python3
# coding=utf-8
import argparse
import os
import sys
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

    parser.add_argument('-t', '--top', type=int, dest='top', default=15000,
                        help='choose, how many popular words will be stored')

    parser.add_argument('-p', '--possible', nargs='?', const=10,
                        dest='num', type=int,
                        help='if the usual decryption process has left some '
                             'letters empty - try to guess them, '
                             'using another method, and then choose the best'
                             ' one')

    args = parser.parse_args()
    if not args.alph:
        sys.exit("Error: alphabet must be specified")

    if not isinstance(args.fn, str):
        text = stdin_to_text()
        hacker = SubstitutionHacker(
            args.alph,
            args.stat,
            args.encoding,
            code_text=text,
            top=args.top)
        key = hacker.hack()
        if "_" in key.values() and args.num:
            key = choose_best_key(hacker, args)
        decoded_text = hacker.decode_text(text, key)
    else:
        hacker = SubstitutionHacker(
            args.alph,
            args.stat,
            args.encoding,
            code_fn=args.fn,
            top=args.top)
        key = hacker.hack()
        if "_" in key.values() and args.num:
            key = choose_best_key(hacker, args)
        decoded_text = hacker.decode_file(args.fn, args.encoding, key)

    if args.output:
        with open(args.output, 'w', encoding=args.encoding) as file:
            file.write(decoded_text)
    else:
        print(decoded_text)

    if args.substitution:
        write_json_in_file(args.substitution, key, args.encoding)


def choose_best_key(hacker, args):
    """
    Try to guess empty letters, let the user decide, which one fits best
    :param hacker:
    :param args:
    :return:
    """
    possibilities = ordered_dict_to_list(
        hacker.find_possible_substitution(), args.num)
    count = 0
    for subst in possibilities:
        print("Variant " + str(count) + ":")
        print(hacker.decode_file(args.fn, args.encoding, subst)[:300])
        print("========")
        count += 1
    return possibilities[int(input("Please, choose best variant:\n"))]


def ordered_dict_to_list(ord_dict, count):
    """
    Convert ordered dictionary to list
    :param ord_dict:
    :param count:
    :return:
    """
    i = 0
    result = []
    for key in ord_dict:
        if i == count:
            return result
        result.append(ord_dict[key])
        i += 1
    return result


def stdin_to_text():
    """
    Covert stdin text to a normal string, so it could be used many times.
    :return:
    """
    return str.join("", sys.stdin)


if __name__ == '__main__':
    sys.exit(main())
