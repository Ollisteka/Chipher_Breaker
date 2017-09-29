#!/usr/bin/env python3
# coding=utf-8
import json
import os
import re
import sys
import tempfile
from copy import deepcopy
from itertools import groupby

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.encryptor import code_stdin, code_text_from_file, make_alphabet, generate_substitution, code
from logic.learner import TextInfo

LETTERS = "letters"
WORDS = "words"
NGRAMMS = "ngramms"


def make_mask(word):
    """
    Match each letter of the word with a digit
    :type word: str
    :return:
    """
    next_num = 0
    letter_nums = {}
    word_mask = []
    for letter in word:
        if letter not in letter_nums:
            letter_nums[letter] = str(next_num)
            next_num += 1
        word_mask.append(letter_nums[letter])
    return ''.join(word_mask)


def make_words_masks(words):
    """
    Make masks for every word in a list
    :type words: list
    :return:a mask-word dictionary
    """
    all_masks = {}
    for word in words:
        mask = make_mask(word)
        if mask not in all_masks:
            all_masks[mask] = [word]
        else:
            all_masks[mask].append(word)
    return all_masks


def make_blank_substitution(alph):
    """
    Make a default blank substitution with a given alphabet
    :param alph: string: A-Za-z or А-Яа-яЁё
    :return:
    """
    return {letter: set() for letter in make_alphabet(alph)}


def expand_substitution(substitution, coded_word, word):
    """
    Find letters, which can be right for a given text
    :param substitution:
    :param coded_word:
    :param word:
    :return:
    """
    substitution = deepcopy(substitution)
    for i in range(len(coded_word)):
        substitution[coded_word[i]].add(word[i])
    return substitution


def intersect_substitutions(map_one, map_two, alphabet):
    """
    Find potential decryption letters using two different substitution
    :type map_one: dict
    :type map_two: dict
    :param alphabet: A-Za-z
    :return:
    """
    intersected_subst = make_blank_substitution(alphabet)
    for letter in intersected_subst.keys():
        suit_one = map_one[letter]
        suit_two = map_two[letter]
        if not suit_one or not suit_two:
            intersected_subst[letter] = suit_one | suit_two
        else:
            intersected_subst[letter] = suit_one & suit_two
    return intersected_subst


def remove_solved_letters(substitution):
    """
    Find letters, which will decrypt the code
    :param substitution:
    :return:
    """
    answer = deepcopy(substitution)
    loop_again = True
    while loop_again:
        loop_again = False
        solved_letters = []
        for coded_letter in substitution.keys():
            potential_keys = answer[coded_letter]
            if len(answer[coded_letter]) == 1:
                solved_letters.append(list(potential_keys)[0])

        for coded_letter in substitution.keys():
            potential_keys = answer[coded_letter]
            for right_letter in solved_letters:
                if len(potential_keys) != 1 and right_letter in potential_keys:
                    potential_keys.remove(right_letter)
                    if len(potential_keys) == 1:
                        loop_again = True
    return answer


def find_final_substitution(substitution, alphabet):
    """
    Replace unsolved letters with underscore
    :param substitution:
    :param alphabet:
    :return:
    """
    key = generate_substitution(alphabet)
    for coded_letter in substitution.keys():
        if len(substitution[coded_letter]) == 1:
            key[coded_letter] = list(substitution[coded_letter])[0]
        else:
            key[coded_letter] = '_'
    return key


def make_words_list(words, count=100):
    """
    Find COUNT most popular words of every length
    :param count:
    :param words:
    :return:
    """
    result = []
    sorted_groups = groupby(
        sorted(
            words.keys(),
            key=lambda x: (
                len(x),
                words[x]),
            reverse=True),
        lambda x: len(x))
    for _, group in sorted_groups:
        result.extend(list(group)[:count])
    return result


def process_statistic(filename, encoding):
    """
    Make masks for non encrypted words, stored in some file
    :param filename:
    :param encoding:
    :return:
    """
    # noinspection PyProtectedMember
    if isinstance(filename, tempfile._TemporaryFileWrapper):
        with filename as f:
            f.seek(0)
            text = f.read().decode(encoding)
            sample = json.loads(text)
    else:
        with open(filename, "r", encoding=encoding) as file:
            sample = json.loads(file.read())
    return make_words_masks(sample[WORDS].keys())


class SubstitutionHacker:
    """
    This class can hack and decode encrypted text or file
    """

    def __init__(
            self,
            alphabet,
            stat_fn,
            encoding,
            code_fn=None,
            code_text=None,
            top=15000):
        self.alphabet = alphabet
        self.word_patterns = process_statistic(
            stat_fn, encoding)  # original non encrypted words masks
        if code_fn:
            code_text_info = TextInfo(
                alphabet, encoding, input_filename=code_fn)
        elif code_text:
            code_text_info = TextInfo(alphabet, encoding, input_text=code_text)
        else:
            raise Exception("You must specify file name or the text itself")
        self.code_count_dict = code_text_info.find_info(top).make_count_dict()
        self.code_patterns = make_words_masks(
            make_words_list(
                self.code_count_dict[WORDS],
                top))  # encrypted words masks
        self.temp_subst = make_blank_substitution(alphabet)
        self.key = make_blank_substitution(alphabet)

    def hack(self):
        """
        Find right substitution for the decrypted text
        """
        for coded_word in self.code_count_dict[WORDS].keys():
            new_map = make_blank_substitution(self.alphabet)
            coded_mask = make_mask(coded_word)
            if coded_mask not in self.code_patterns:
                continue
            if coded_mask in self.word_patterns.keys():
                for candidate in self.word_patterns[coded_mask]:
                    new_map = expand_substitution(
                        new_map, coded_word, candidate)
            self.temp_subst = intersect_substitutions(
                self.temp_subst, new_map, self.alphabet)
        result = remove_solved_letters(self.temp_subst)
        self.key = find_final_substitution(result, self.alphabet)
        return self.key

    def decode_file(self, code_fn, encoding):
        """
        Decode text from file
        :param code_fn:
        :param encoding:
        :return:
        """
        return code_text_from_file(
            code_fn, encoding, self.key, regex(
                self.alphabet))

    def decode_stdin(self):
        """
        Decode text from stdin
        :return:
        """
        return code_stdin(self.key, regex(self.alphabet))

    def decode_text(self, text):
        """
        Decode given text
        :param text:
        :return:
        """
        return code(text, self.key, regex(self.alphabet))


def regex(alphabet):
    """
    Converts string of alphabet to regular expression of right form.
    :param alphabet:
    :return:
    """
    return re.compile('[' + alphabet + ']')
