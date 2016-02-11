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
import regex
import unicodedata
import itertools

def is_project_issue(text):
    """

    """

    return bool(re.match(r'\w+-\d+', re.UNICODE))

def is_issue(text):
    """
    Does this token look like an issue reference?
    https://help.github.com/articles/autolinked-references-and-urls/#issues-and-pull-requests

    >>> is_issue('26')
    False
    >>> is_issue('#26')
    True
    >>> is_issue('jlord#26')
    True
    >>> is_issue('jlord')
    False
    >>> is_issue('jlord/sheetsee.js')
    False
    >>> is_issue('jlord/sheetsee.js#26')
    True
    """
    return bool(re.match(r'''
        (?: (?:[\w.-]+/)?   # Owner
               [\w.-]+)?    # Repository
        [#]\d+$               # Issue number
    ''', text, re.VERBOSE | re.UNICODE))


def is_version_number(text):
    """
    Does this token look like a semantic versioning string?

    http://semver.org/

    It's ambiguous if this is a version number or just a number.
    >>> is_version_number('32')
    False

    This is more likely a version number.
    >>> is_version_number('2.2')
    True
    >>> is_version_number('0.2.1')
    True
    >>> is_version_number('1.2-alpha')
    True
    >>> is_version_number('1.2.3-rc1')
    True
    """
    return bool(re.match(r'''
        v?
        \d+              # Major number
        (?: [.] \d+)?    # Minor number
            [.] \d+      # Patch number
        (?: -(?:alpha|beta|rc[.]?\d+))?  # Tag
    ''', text, re.VERBOSE | re.IGNORECASE))


# I realize now that I'm only supposed to cover Java syntaxes...
# ...but I'm still tempted to match erlang:syntax/0
def is_method_name(text):
    """
    >>> is_method_name('hello')
    False
    >>> is_method_name('hello()')
    True
    >>> is_method_name('Foo::Bar')
    False
    >>> is_method_name('Foo::Bar#baz')
    True
    >>> is_method_name('Foo::Bar#baz()')
    True
    >>> is_method_name('user/repo#14')
    False
    """

    return bool(re.match(r'''
        (?:\w+(?:[.]|::))*  # Zero or more C++/Ruby namespaces
        \w+
        (?:
            [(][)]          # A standard function
         |
            [#]\w+(?:[(][)])? # A Ruby Method
        )
    ''', text, re.VERBOSE))


def is_file_pattern(text):
    """
    >>> is_file_pattern('file.java')
    True
    >>> is_file_pattern('.gitignore')
    True
    >>> is_file_pattern('file')
    False
    >>> is_file_pattern('java')
    False
    >>> is_file_pattern('*.java')
    True
    >>> is_file_pattern('docs/Makefile')
    True
    >>> is_file_pattern('**/*.jpg')
    True
    """
    return bool(re.match(r'''
        (?: [.]{0,2}[\-_*\w+]+ /)*  # Preceeding directories, if any
            [.]?[\-_*\w+]+          # The basename

        (?: [.][\-_*\w]+            # An extension
          | (?: file | ignore ))    # .gitignore, Makefile
    ''', text, re.VERBOSE | re.UNICODE))


def clean_token(token):
    """
    It cleans tokens:
    >>> clean_token('(foo,')
    'foo'
    >>> clean_token('readme.md.')
    'readme.md'
    >>> clean_token('*.lol)')
    '*.lol'

    It returns tokens made entirely of punctuation as is.
    >>> clean_token('[...]')
    '[...]'
    """

    # If it's entirely punctuation, return it as is
    if regex.match(r'^(?V1)[\p{Pi}\p{Ps}]+[\p{Pe}\p{Po}]+$', token):
        return token

    # Remove surrounding parens, and initial quotations.
    token = regex.sub(r'(?V1)[\p{Pe}\p{Po}--*#]+$', '', token)
    return regex.sub(r'^(?V1)[\p{Pi}\p{Ps}\p{Po}--*#]+', '', token)


def replace_special_token(dirty_token):
    # Do this one first...
    if is_method_name(dirty_token):
        return 'METHOD-NAME'

    token = clean_token(dirty_token)
    if is_issue(token):
        return 'ISSUE-NUMBER'
    elif is_version_number(token):
        return 'VERSION-NUMBER'
    elif is_file_pattern(token):
        return 'FILE-PATTERN'
    else:
        assert token.lower() == token
        # Remove trailing punctuation
        return token


def clean_tokens(tokens):
    """
    Generates only cleaned tokens. Tokens made of only punctuation are
    completely removed.
    """
    for token in tokens:
        cleaned = replace_special_token(token)
        if len(token) == 0:
            continue
        yield cleaned


def tokenize(string):
    """
    Tokenizes strings.

    It normalizes:
    >>> tokenize('Nai\u0308ve')
    ['na\u00efve']

    It can segment English text:
    >>> tokenize("I ain't havin' it, ya hear?")
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
    >>> tokenize("ignore **/*.png")
    ['ignore', 'FILE-PATTERN']

    It understands semantic versions.
    >>> tokenize("Release 2.1.0-rc.1")
    ['release', 'VERSION-NUMBER']
    """

    # Step 1: Normalize into NFC
    # Step 2: Lowercase
    ustring = unicodedata.normalize('NFC', string).lower()

    # Break on word boundaries
    segments = ustring.split()

    # Replace method names, issues, and filenames.
    return list(clean_tokens(segments))


if __name__ == '__main__':
    import doctest
    from blessings import Terminal
    failures, tests = doctest.testmod()

    term = Terminal()
    if failures > 0:
        print(term.red('{}/{} tests failed'.format(failures, tests)))
    else:
        print(term.green('{} tests passed!'.format(tests)))
