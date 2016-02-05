#!/usr/bin/env python3

# Copyright 2016 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Tokenize files
"""

import re
import unicodedata
import itertools

def pairs(sequence):
    first, second = itertools.tee(sequence, 2)
    return itertools.zip_longest(first, itertools.islice(sequence, 1, None))

def looks_like_issue(first, second):
    if first == '#' and re.match(r'^\d+$', second):
        return True
    return False

def looks_like_method_name(first, second):
    if second == '()':
        return True

def is_integer(number):
    try:
        int(number)
    except ValueError:
        return False
    else:
        return True

def is_file_pattern(text):
    return re.match(r'[*\w]+\.[*\w]+', text)

def replace_special_tokens(sequence):
    sequence = list(sequence)
    index = 0
    last = len(sequence)

    # "Safe" peek at next word
    def next_token(n=1):
        start, end = index + n, index + n + 1
        peek = sequence[start:end]
        return peek[0] if len(peek) else ''

    def segment():
        nonlocal index
        while index < last:
            current = sequence[index]
            if current.startswith('*') and next_token().startswith('.'):
                yield 'FILE-PATTERN'
                index += 2
            if is_file_pattern(current):
                yield 'FILE-PATTERN'
                index += 1
            elif is_word(current) and next_token() == '(' and next_token(2) == ')':
                yield 'METHOD-NAME'
                index += 3
            elif is_word(current):
                yield current
                index += 1
            elif current == '#' and is_integer(next_token()):
                # Yield the issue number.
                yield 'ISSUE-NUMBER'
                index += 2
            else:
                index += 1

    return list(segment())

def tokenize(string):
    """
    Tokenizes strings.

    It normalizes:
    >>> tokenize('Nai\u0308ve')
    ['na\u00efve']

    It can segment English text:
    >>> tokenize("I ain't havin' it: ya hear?")
    ['i', "ain't", 'havin', 'it', 'ya', 'hear']

    It can replace issue numbers and filenames.
    >>> tokenize("Fixed #22 in filename.py ")
    ['fixed', 'ISSUE-NUMBER', 'in', 'FILE-PATTERN']

    It tokenizes simple function names
    >>> tokenize("Implement foobar()")
    ['implement', 'METHOD-NAME']

    It understands C++/Ruby namespaces
    >>> tokenize("Fixed #31 in std::whoopsie_handler() ")
    ['fixed', 'ISSUE-NUMBER', 'in', 'METHOD-NAME']

    It understands Ruby method notation
    >>> tokenize("Fixed #31 in Herp#derp")
    ['fixed', 'ISSUE-NUMBER', 'in', 'METHOD-NAME']

    It understands globs.
    >>> tokenize("ignore *.aux")
    ['ignore', 'FILE-PATTERN']

    >>> tokenize("ignore paper.*")
    ['ignore', 'FILE-PATTERN']
    """

    # Step 1: Normalize into NFC
    # Step 2: Lowercase
    ustring = unicodedata.normalize('NFC', string).lower()

    # Break on word boundaries
    segments = (text for text in uniseg.wordbreak.words(ustring))

    # Replace method names.
    return replace_special_tokens(segments)

def is_word(text):
    # Text starts with a WORD character.
    return re.match(r'\w', text, re.UNICODE)
