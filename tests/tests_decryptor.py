#!/usr/bin/env python3
import unittest
import re
import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))

import logic.decryptor as d

ENCODING = "utf-8"


class MyTestCase(unittest.TestCase):
    def test_make_mask(self):
        word_one = "hello"
        mask_one = "01223"
        word_two = "puppy"
        mask_two = "01002"
        self.assertEqual(mask_one, d.make_mask(word_one))
        self.assertEqual(mask_two, d.make_mask(word_two))

    def test_make_words_masks(self):
        self.assertEqual(d.make_words_masks(["lazy", 'summer', "abcdef", "qwerty"]),
                         {"0123": ["lazy"],
                          "012234": ["summer"],
                          "012345": ["abcdef", "qwerty"]})

    def test_get_blank_letter_mapping(self):
        self.assertDictEqual(d.make_blank_substitution("A-Za-z"),
                             {'a': set(),
                              'b': set(),
                              'c': set(),
                              'd': set(),
                              'e': set(),
                              'f': set(),
                              'g': set(),
                              'h': set(),
                              'i': set(),
                              'j': set(),
                              'k': set(),
                              'l': set(),
                              'm': set(),
                              'n': set(),
                              'o': set(),
                              'p': set(),
                              'q': set(),
                              'r': set(),
                              's': set(),
                              't': set(),
                              'u': set(),
                              'v': set(),
                              'w': set(),
                              'x': set(),
                              'y': set(),
                              'z': set()})

    def test_intersect(self):
        subst_one = {'a': {'b', 'c'},
                     'b': {'a'},
                     'c': set(),
                     'd': {'x'},
                     'e': set(),
                     'f': set(),
                     'g': set(),
                     'h': set(),
                     'i': set(),
                     'j': set(),
                     'k': set(),
                     'l': set(),
                     'm': set(),
                     'n': set(),
                     'o': set(),
                     'p': set(),
                     'q': set(),
                     'r': set(),
                     's': set(),
                     't': set(),
                     'u': set(),
                     'v': set(),
                     'w': set(),
                     'x': set(),
                     'y': set(),
                     'z': set()}
        subst_two = {'a': {'c', 'd'},
                     'b': {'e'},
                     'c': {'z'},
                     'd': set(),
                     'e': set(),
                     'f': set(),
                     'g': set(),
                     'h': set(),
                     'i': set(),
                     'j': set(),
                     'k': set(),
                     'l': set(),
                     'm': set(),
                     'n': set(),
                     'o': set(),
                     'p': set(),
                     'q': set(),
                     'r': set(),
                     's': set(),
                     't': set(),
                     'u': set(),
                     'v': set(),
                     'w': set(),
                     'x': set(),
                     'y': set(),
                     'z': set()}
        expected_result = {'a': {'c'},
                           'b': set(),
                           'c': {'z'},
                           'd': {'x'},
                           'e': set(),
                           'f': set(),
                           'g': set(),
                           'h': set(),
                           'i': set(),
                           'j': set(),
                           'k': set(),
                           'l': set(),
                           'm': set(),
                           'n': set(),
                           'o': set(),
                           'p': set(),
                           'q': set(),
                           'r': set(),
                           's': set(),
                           't': set(),
                           'u': set(),
                           'v': set(),
                           'w': set(),
                           'x': set(),
                           'y': set(),
                           'z': set()}
        self.assertDictEqual(
            expected_result,
            d.intersect_substitutions(
                subst_one,
                subst_two,
                "A-Za-z"))

    def test_remove_solved_letters(self):
        subst_one = {'a': {'a', 'b'},
                     'b': {'a'},
                     'c': set(),
                     'd': {'x'},
                     'e': set(),
                     'f': set(),
                     'g': set(),
                     'h': set(),
                     'i': set(),
                     'j': set(),
                     'k': set(),
                     'l': set(),
                     'm': set(),
                     'n': set(),
                     'o': set(),
                     'p': set(),
                     'q': set(),
                     'r': set(),
                     's': set(),
                     't': set(),
                     'u': set(),
                     'v': set(),
                     'w': set(),
                     'x': set(),
                     'y': set(),
                     'z': set()}
        expected_result = {'a': {'b'},
                           'b': {'a'},
                           'c': set(),
                           'd': {'x'},
                           'e': set(),
                           'f': set(),
                           'g': set(),
                           'h': set(),
                           'i': set(),
                           'j': set(),
                           'k': set(),
                           'l': set(),
                           'm': set(),
                           'n': set(),
                           'o': set(),
                           'p': set(),
                           'q': set(),
                           'r': set(),
                           's': set(),
                           't': set(),
                           'u': set(),
                           'v': set(),
                           'w': set(),
                           'x': set(),
                           'y': set(),
                           'z': set()}
        self.assertDictEqual(
            expected_result,
            d.remove_solved_letters(subst_one))

    def test_find_final(self):
        subst = {'a': {'c', 'd'},
                 'b': {'e'},
                 'c': {'z'},
                 'd': set(),
                 'e': set(),
                 'f': set(),
                 'g': set(),
                 'h': set(),
                 'i': set(),
                 'j': set(),
                 'k': set(),
                 'l': set(),
                 'm': set(),
                 'n': set(),
                 'o': set(),
                 'p': set(),
                 'q': set(),
                 'r': set(),
                 's': set(),
                 't': set(),
                 'u': set(),
                 'v': set(),
                 'w': set(),
                 'x': set(),
                 'y': set(),
                 'z': set()}
        expected_result = {'a': '_',
                           'b': 'e',
                           'c': 'z',
                           'd': '_',
                           'e': '_',
                           'f': '_',
                           'g': '_',
                           'h': '_',
                           'i': '_',
                           'j': '_',
                           'k': '_',
                           'l': '_',
                           'm': '_',
                           'n': '_',
                           'o': '_',
                           'p': '_',
                           'q': '_',
                           'r': '_',
                           's': '_',
                           't': '_',
                           'u': '_',
                           'v': '_',
                           'w': '_',
                           'x': '_',
                           'y': '_',
                           'z': '_'}
        self.assertDictEqual(
            expected_result,
            d.find_final_substitution(
                subst,
                "A-Za-z"))

    def test_make_words_list(self):
        words = {
            "the": 900,
            "and": 2,
            "to": 45,
            "he": 12,
            "a": 9,
            "harry": 1327,
            "of": 9000000,
            "it": 900,
            "was": 4567,
            "you": 1037,
            "s": 1019,
        }
        expected_result = ["harry", "was", "of", "s"]
        self.assertEqual(expected_result, d.make_words_list(words, 1))

    def test_expand_substitution(self):
        word = "abc"
        coded = "xyz"
        subst = {'a': set(),
                 'b': set(),
                 'c': set(),
                 'd': set(),
                 'e': set(),
                 'f': set(),
                 'g': set(),
                 'h': set(),
                 'i': set(),
                 'j': set(),
                 'k': set(),
                 'l': set(),
                 'm': set(),
                 'n': set(),
                 'o': set(),
                 'p': set(),
                 'q': set(),
                 'r': set(),
                 's': set(),
                 't': set(),
                 'u': set(),
                 'v': set(),
                 'w': set(),
                 'x': {'a'},
                 'y': {'b'},
                 'z': {'c'}}
        self.assertDictEqual(subst, d.expand_substitution(d.make_blank_substitution("A-Za-z"), coded, word))


    def test_regex(self):
        regex = re.compile('[A-Za-z]')
        self.assertEqual(d.regex("A-Za-z"), regex)


if __name__ == '__main__':
    unittest.main()
