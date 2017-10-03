#!/usr/bin/env python3
# coding=utf-8
import json
import sys
import tempfile
from copy import copy
from random import shuffle


def read_json_file(filename, encoding):
    """
    Read data, written in a json format from a file, and return it
    :param encoding:
    :param filename:
    :return:
    """
    with open(filename, "r", encoding=encoding) as file:
        return json.loads(file.read())


def generate_alphabet_list(start, end):
    """
    Function makes a list, containing all the letters from start
    to end included.
    :type end: str
    :type start: str
    :return:
    """
    return [x for x in map(chr, range(ord(start), ord(end) + 1))]


def make_alphabet(string):
    """
    Function makes a list, containing all the letters from the range.
    :param string: A-Za-z or А-Яа-яЁё
    :return:
    """
    letter_range = "".join(
        x for x in string if x.islower() or x == '-').strip('-')
    if len(letter_range) == 3:
        return generate_alphabet_list(letter_range[0], letter_range[2])
    defis = letter_range.find('-')
    alphabet = generate_alphabet_list(
        letter_range[defis - 1], letter_range[defis + 1])
    for letter in letter_range:
        if letter_range.find(letter) not in range(defis - 1, defis + 2):
            alphabet.append(letter)
    return alphabet


def generate_substitution(string):
    """
    Generate new substitution, based on the given letter's range.
    :param string: A-Za-z or А-Яа-яЁё
    :return:
    """
    alphabet = make_alphabet(string)
    shuffled = copy(alphabet)
    shuffle(shuffled)
    return dict(zip(alphabet, shuffled))


def reverse_substitution(substitution):
    """
    Exchange keys with values.
    :type substitution: dict
    :return:
    """
    return {v: k for k, v in substitution.items()}


def code_text_from_file(filename, encoding, substitution):
    """
    Code text from file
    :param filename:
    :param encoding:
    :param substitution:
    :return:
    """
    # noinspection PyProtectedMember
    if isinstance(filename, tempfile._TemporaryFileWrapper):
        with filename as f:
            f.seek(0)
            text = f.read().decode(encoding)
            return code(text, substitution)
    with open(filename, 'r', encoding=encoding) as file:
        return code(file, substitution)


def code_stdin(substitution):
    """
    Code text from stdin
    :param substitution:
    :return:
    """
    return code(sys.stdin, substitution)


def code(text, substitution):
    """
    The function encrypts the text, assigning each letter
    a new one from the substitution
    :type text: str or Text.IOWrapper[str]
    :type substitution: dict of (str, str)
    :return:
    """
    result = text[:]
    for (coded_letter, decoded_letter) in substitution.items():
        text.replace(coded_letter, decoded_letter)
        text.replace(coded_letter.upper(), decoded_letter.upper())
    return result
