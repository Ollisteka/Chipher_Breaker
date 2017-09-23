#!/usr/bin/env python3
import sys
import re
import json
import tempfile
import string
from collections import Counter, defaultdict

LETTERS = "letters"
WORDS = "words"
NGRAMMS = "ngramms"


class CountInfo:
    """
    This class is to be updated and then written into file.
    """

    def __init__(self, letters, words, ngramms):
        """

        :type letters: Counter
        :type words: Counter
        """
        self.letters = letters
        self.words = words
        self.ngramms = ngramms

    def make_ngramms_dict(self):
        """
        Make dictionary with information about ngramms
        :return:
        """
        return {str(n): dict(self.ngramms[str(n)]) for n in self.ngramms}

    def make_count_dict(self):
        """
        Make dictionary with information about how many letters appeared in the text
        and most popular words

        :return:
        """
        return {LETTERS: dict(self.letters),
                WORDS: dict(self.words),
                NGRAMMS: self.make_ngramms_dict()}

    def make_frequency_dict(self):
        """
        Make dictionary with information about frequency of the letters
        and most popular words

        :return:
        """
        return {LETTERS: count_frequencies(dict(self.letters)),
                WORDS: count_frequencies(dict(self.words))}

    def update_count_info(self, filename, alphabet, top_words, encoding):
        """
        Try update information in current CountInfo, using information from file
        :type encoding: str
        :type top_words: int
        :type filename: str
        :type alphabet: __Regex
        :return:
        """
        if top_words is None:
            top_words = 100

        try:
            with open(filename, "r", encoding=encoding) as f:
                prev_data = json.loads(f.read())
            # файл, используя который хотим обновить данные, на другом языке
            # Стоит ли сделать свой эксэпшн, чтобы кидать в таком случае?
            if alphabet.match(list(prev_data[LETTERS].keys())[0]) is None:
                return
            else:
                self.letters += Counter(prev_data[LETTERS])
                self.words += Counter(prev_data[WORDS])
                old_ngramms = {}
                for n in prev_data[NGRAMMS]:
                    old_ngramms[n] = Counter(prev_data[NGRAMMS][n])
                # old_ngramms = {n: Counter(v) for (n, v) in prev_data[NGRAMMS]}
                for n in old_ngramms:
                    self.ngramms[n] += old_ngramms[n]

            if len(self.words) > top_words:
                self.words = Counter(dict(self.words.most_common(top_words)))
            return
        except FileNotFoundError:
            return


class TextInfo:
    """
    This class stores information about current text
    """

    def __init__(self, alphabet, encoding, input_filename=None, input_text=None):
        try:
            if isinstance(input_filename, tempfile._TemporaryFileWrapper):
                self.is_tmpfile = True
                raise AttributeError
            self.is_tmpfile = False
            self.input = input_filename.name
        except AttributeError:
            self.input = input_filename
        self.alph = re.compile('[' + alphabet + ']')
        self.letters = Counter()
        self.words = Counter()
        self.ngramms = defaultdict(Counter)
        self.encoding = encoding
        self.text = input_text

    def find_info(self, top_words):
        """
        Functions counts letters in the file and words in the text.
        Returns CountInfo
        :type top_words: int
        :return:
        """
        if top_words is None:
            top_words = 100

        if self.text is not None:
            leftover = self.__count(self.text)
        elif self.input == '<stdin>':
            leftover = self.__count(sys.stdin)
        elif self.is_tmpfile:
            with self.input as f:
                f.seek(0)
                leftover = self.__count(f.read().decode(self.encoding))
        else:
            with open(self.input, "r", encoding=self.encoding) as f:
                leftover = self.__count(f)

        if leftover != '':
            self.words[leftover] += 1
            self.make_ngramms(leftover)

        if len(self.words) > top_words:
            self.words = Counter(dict(self.words.most_common(top_words)))

        return CountInfo(self.letters, self.words, self.ngramms)

    def make_ngramms(self, word):
        """
        Function finds all the ngramms from the word and updates information about them in self.
        :type word: str
        :return:
        """
        for n in range(2, len(word)+1):
            ngramms = word_to_ngramms(word, n)
            for ngramm in ngramms:
                self.ngramms[str(n)][ngramm] += 1

    def __count(self, text):
        """
        Functions counts letters in the file and words in the text.
        Returns a word left after the counting.
        :param text:
        :return:
        """
        word = ''
        for line in text:
            for char in line:
                if self.alph.match(char) is not None:
                    word += char.lower()
                    self.letters[char.lower()] += 1
                if char in string.whitespace or char in string.punctuation or char == '—':
                    if word != '':
                        self.words[word] += 1
                        self.make_ngramms(word)
                    word = ''
        return word


def word_to_ngramms(text, n):
    """ Convert text into character ngramms. """
    return [text[i:i + n] for i in range(len(text) - n + 1)]


def count_frequencies(dictionary):
    """
    Function sums up dictionary's values, and based on that counts the frequency for each key.
    :param dictionary:
    :return:
    """
    divider = sum(dictionary.values())
    return {k: v / divider for k, v in dictionary.items()}


def write_json_in_file(filename, data, encoding):
    """
    Write dict into file, using json
    :param encoding:
    :type filename: str
    :type data: dict
    :return:
    """
    with open(filename, "w", encoding=encoding) as f:
        f.write(json.dumps(data))
