#!/usr/bin/env python3
# coding=utf-8
import argparse
import os
import sys
from pprint import pprint

LETTERS = "letters"
WORDS = "words"
NGRAMMS = "ngramms"

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.learner import TextInfo, write_json_in_file


def main():
    parser = argparse.ArgumentParser(usage='{} [OPTIONS] ALPHABET FILE'.format(
        os.path.basename(sys.argv[0])), description='Learn letter frequency')
    parser.add_argument(
        'alph',
        metavar='alphabet',
        help='language, in which text is written (for example: A-Za-z)')
    parser.add_argument(
        'fn',
        metavar='FILE',
        nargs='*',
        default=sys.stdin,
        help='name of the file with text or a full path to a folder')
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        dest='output',
        metavar="FILENAME",
        help='choose, where to store output')
    parser.add_argument(
        '-u',
        '--update',
        type=str,
        dest='update_fn',
        metavar="FILENAME",
        help='choose, which file is to be updated')
    parser.add_argument(
        '-e',
        '--encoding',
        type=str,
        dest='encoding',
        default='utf-8',
        help='choose FILE (and output file, if key -o is chosen) encoding')

    parser.add_argument('-t', '--top', type=int, dest='top',
                        help='choose, how many popular words will be stored')

    args = parser.parse_args()
    if not isinstance(args.fn, list) and args.fn.name == '<stdin>':
        handle_one_object(args, text=sys.stdin)
    elif len(args.fn) == 1:
        if os.path.isdir(args.fn[0]):
            origin_path = os.path.join(os.getcwd(), args.output)
            os.chdir(args.fn[0])
            handle_many_files(args, os.listdir(args.fn[0]))
            os.replace(os.path.join(os.getcwd(), args.output), origin_path)
        else:
            handle_one_object(args, file_name=args.fn[0])
    elif not args.output:
        print("Error: an output file must be specified, to let numerous "
              "files to be handled")
        sys.exit(2)
    else:
        handle_many_files(args, args.fn)


def handle_many_files(args, files):
    """
    Process a list of files
    :param args:
    :param files: a list of files' names
    """
    handle_one_object(args, files[0])
    for i in range(1, len(files)):
        text_info = TextInfo(args.alph, args.encoding, input_filename=files[i])
        count_info = text_info.find_info(args.top)
        count_info.update_count_info(
            args.output,
            text_info.alph,
            args.top,
            args.encoding)
        updated_dict = count_info.make_count_dict()
        write_json_in_file(args.output, updated_dict, args.encoding)


def handle_one_object(args, file_name=None, text=None):
    """
    Process one file at a time, or a given piece of text
    :param args:
    :param file_name:
    :param text:
    """
    if file_name:
        text_info = TextInfo(
            args.alph,
            args.encoding,
            input_filename=file_name)
    elif text:
        text_info = TextInfo(args.alph, args.encoding, input_text=text)
    count_info = text_info.find_info(args.top)
    if args.update_fn:
        count_info.update_count_info(
            args.update_fn,
            text_info.alph,
            args.top,
            args.encoding)
        updated_dict = count_info.make_count_dict()
    else:
        updated_dict = count_info.make_count_dict()
    if args.output:
        write_json_in_file(args.output, updated_dict, args.encoding)
    else:
        pprint(updated_dict)


if __name__ == '__main__':
    sys.exit(main())
