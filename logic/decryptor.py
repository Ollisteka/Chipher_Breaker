#!/usr/bin/env python3
# coding=utf-8
import json
import os
import sys
import random
import tempfile
from copy import copy
from itertools import groupby
from collections import OrderedDict

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

from logic.encryptor import code_stdin, code_text_from_file, \
    make_alphabet, generate_substitution, code
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
    substitution = copy(substitution)
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
    answer = copy(substitution)
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

    free_keys = [letter for letter in key.keys()
                 if key[letter] == "_"]
    unused_letters = [letter for letter in key.keys()
                      if letter not in key.values()]

    if len(free_keys) == 1:
        key[free_keys[0]] = unused_letters[0]
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


def load_statistic(filename, encoding):
    """
    Load json statistics
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
    return sample


class SubstitutionHacker:
    """
    This class can hack and decode encrypted text or file
    """
    possible_keys = []

    def __init__(
            self,
            alphabet,
            stat_fn,
            encoding,
            code_fn=None,
            code_text=None,
            top=15000):
        self.alphabet = alphabet
        self.original_count_dict = load_statistic(stat_fn, encoding)
        self.word_patterns = make_words_masks(
            self.original_count_dict[WORDS].keys())
        # original non encrypted words masks
        if code_fn:
            self.__code_filename = code_fn
            self.__code_text = None
            self.encoding = encoding
            code_text_info = TextInfo(
                alphabet, encoding, input_filename=code_fn)
        elif code_text:
            self.__code_filename = None
            self.__code_text = code_text
            code_text_info = TextInfo(alphabet, encoding, input_text=code_text)
        else:
            raise Exception("You must specify file name or the text itself")
        self.code_count_dict = code_text_info.find_info(top).make_count_dict()
        self.code_patterns = make_words_masks(
            make_words_list(
                self.code_count_dict[WORDS],
                top))  # encrypted words masks
        self.__temp_subst = make_blank_substitution(alphabet)
        self.key = make_blank_substitution(alphabet)
        self.__example_quadgrams = self.__count_standard_quadgrams()

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
            self.__temp_subst = intersect_substitutions(
                self.__temp_subst, new_map, self.alphabet)
        result = remove_solved_letters(self.__temp_subst)
        self.key = find_final_substitution(result, self.alphabet)
        return self.key

    def find_possible_substitution(self):
        """
        Returns an ordered dict of possible substitutions, from best to worst
        :return:
        """
        from math import factorial
        free_keys = [letter for letter in self.key.keys() if self.key[
            letter] == "_"]
        used_substs = []
        result = {}
        max_score = -9999999999
        i = 0
        while i < 20:
            i += 1
            parent = self.__generate_key()
            decode = self.__decode(parent)
            parent_score = self.__count_score(decode)
            count = 0
            while count < 500:
                if len(used_substs) == factorial(len(free_keys)):
                    break
                child = copy(parent)
                while child in used_substs or count == 0:
                    a = random.choice(free_keys)
                    b = random.choice(free_keys)
                    while a == b:
                        b = random.choice(free_keys)
                    count += 1
                used_substs.append(child)
                child[a], child[b] = child[b], child[a]
                decode = self.__decode(parent)
                child_score = self.__count_score(decode)
                count += 1
                if child_score > parent_score:
                    parent_score = child_score
                    parent = copy(child)
                    count = 0
            if parent_score > max_score:
                max_score = parent_score
                result[max_score] = copy(parent)
        return OrderedDict(sorted(result.items(), reverse=True))

    def __count_standard_quadgrams(self):
        """
        Count the probability of quadgram appearance in a real non coded text
        :return:
        """
        from math import log10
        quadgrams = copy(self.original_count_dict[NGRAMMS]['4'])
        self.__N = sum(quadgrams.values())
        for key in quadgrams.keys():
            quadgrams[key] = log10(float(quadgrams[key]) / self.__N)
        self.__floor = log10(0.01 / self.__N)
        return quadgrams

    def __count_score(self, coded_text):
        score = 0
        coded_quadgrams = TextInfo(self.alphabet, self.encoding,
                                   input_text=coded_text).find_info(
            15000).make_ngramms_dict()['4']
        for quadgram in coded_quadgrams:
            if quadgram in self.__example_quadgrams.keys():
                score += self.__example_quadgrams[quadgram]
            else:
                score += self.__floor
        return score

    def __decode(self, key):
        """
        Returns text, decoded with given key
        :param key:
        :return:
        """
        if self.__code_filename:
            decode = self.decode_file(self.__code_filename, self.encoding, key)
        else:
            decode = self.decode_text(self.__code_text, key)
        return decode

    def __generate_key(self):
        """
        Find a random possible substitution, based on the unused letters
        :return:
        """
        unused_letters = [letter for letter in self.key.keys() if letter not
                          in self.key.values()]
        free_keys = [letter for letter in self.key.keys() if self.key[
            letter] == "_"]
        temp = copy(self.key)
        for key in free_keys:
            element = random.choice(unused_letters)
            temp[key] = element
            unused_letters.remove(element)
        return temp

    def decode_file(self, code_fn, encoding='utf-8', key=None):
        """
        Decode text from file
        :param key:
        :param code_fn:
        :param encoding:
        :return:
        """
        if not key:
            key = self.key
        return code_text_from_file(code_fn, encoding, key)

    def decode_stdin(self):
        """
        Decode text from stdin
        :return:
        """
        return code_stdin(self.key)

    def decode_text(self, text, key=None):
        """
        Decode given text
        :param text:
        :param key:
        :return:
        """
        if not key:
            key = self.key
        return code(text, key)
