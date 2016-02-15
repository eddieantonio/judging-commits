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

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


def is_sha(text):
    """
    >>> is_sha('afa67f75a65f6a7f87af54a0')
    False
    >>> is_sha('d670460b4b4aece5915caf5c68d12f560a9fe3e4')
    True
    >>> is_sha('ad670460b4b4aece5915caf5c68d12f560a9fe3e4')
    False
    >>> is_sha('670460b4b4aece5915caf5c68d12f560a9fe3e4')
    False
    """

    return bool(re.match(r'''^[a-f0-9]{40}$''', text))


def is_bracketed_email(text):
    """
    >>> is_bracketed_email('<html>')
    False
    >>> is_bracketed_email('<alexander.laamanen@valotrading.fi>')
    True
    >>> is_bracketed_email('<@new-js.bundle@/>')
    False
    >>> is_bracketed_email('<bob@ci.prod.valotrading.com>')
    True
    >>> is_bracketed_email('<ankit1991laddha@gmail.com>')
    True
    >>> is_bracketed_email('<http://www.nodeclipse.org/#support>')
    False
    """

    return bool(re.match(r'''
        <
            [.\w]+          # User
            @
            (?:[\w]+[.])+   #
            \w+             # TLD
        >
    ''', text, re.VERBOSE))


def is_project_issue(text):
    """
    Issues/pull requests from Apache projects in  Jira.

    See: https://issues.apache.org/jira/secure/BrowseProjects.jspa#all

    >>> is_project_issue('thrift-3615')
    True
    >>> is_project_issue('sling-5511')
    True
    >>> is_project_issue('sling')
    False

    >>> is_project_issue('project-8.1')
    False

    Special cases:
    >>> is_project_issue('utf-8')
    False
    >>> is_project_issue('latin-1')
    False
    >>> is_project_issue('iso-8858')
    False
    """

    return bool(re.match(r'''
        (?!utf-)    # Some special cases...
        (?!latin-)
        (?!iso-)

        \w+-\d+$
    ''', text, re.VERBOSE | re.UNICODE))


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
    >>> is_version_number('1.3.1.Final')
    True
    >>> is_version_number('1.11.0.RELEASE')
    True
    >>> is_version_number('0.1-SNAPSHOT')
    True
    """
    return bool(re.match(r'''
        v?
        \d+              # Major number
        (?: [.] \d+)?    # Minor number
            [.] \d+      # Patch number
        (?: [\-.](?:\w+|rc[.]?\d+))*  # Tag
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


def is_build_version(text):
    """
    >>> is_build_version('1134-31')
    True
    >>> is_build_version('a-42')
    False
    """

    return bool(re.match(r'''
        \d+-\d+
    ''', text, re.VERBOSE))



def is_release_identifier(text):
    """
    >>> is_release_identifier('utf-8')
    False
    >>> is_release_identifier('killbill-0.1.66')
    True
    >>> is_release_identifier('jargo-parent-0.1.1')
    True
    """

    return bool(re.match(r'''
        [\w\-_]+
        # Copy-pasted is_version_number() regex
        \d+              # Major number
        (?: [.] \d+)?    # Minor number
            [.] \d+      # Patch number
        (?: [\-.](?:\w+|rc[.]?\d+))*  # Tag
    ''', text, re.VERBOSE))


def is_url(text):
    """
    URL restricted to http://, or https://, svn://,

    >>> is_url('example.org')
    False
    >>> is_url('http://example.org')
    True
    >>> is_url('http://example.org/')
    True
    >>> is_url('mailto:ed@example.org')
    False
    >>> is_url('http://x-name.donuts/')
    True
    >>> is_url('http://x-name.donuts/herp?q=herp#derp')
    True
    >>> is_url('x-name.donuts/herp?q=herp#derp')
    False
    >>> is_url('svn://pc-lab14/SVN/xap/trunk/openspaces@160822')
    True
    """

    pieces = urlparse(text)
    if pieces.scheme not in ('http', 'https', 'svn'):
        return False
    if not pieces.netloc:
        return False

    return True


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
    >>> is_file_pattern('.rubocop.yml')
    True
    >>> is_file_pattern('Class.{h,cpp}')
    True
    """
    return bool(re.match(r'''
        (?: [.]{0,2}[\-_*\w+]+ /)*  # Preceeding directories, if any
            [.]?[\-_*\w+]+          # The basename

        (?: [.][\-_*\w]+            # An extension
          | [.][{][^}*,]+,[^}*]+[}] # An alternation
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
    token = regex.sub(r'^(?V1)[`\p{Pi}\p{Ps}\p{Po}--*#]+', '', token)
    return regex.sub(r'(?V1)[`\p{Pe}\p{Po}--*#]+$', '', token)


def replace_special_token(dirty_token):
    # Do these two first...
    if is_method_name(dirty_token):
        return 'METHOD-NAME'

    token = clean_token(dirty_token)
    if is_issue(token):
        return 'ISSUE-NUMBER'
    elif is_build_version(token):
        return 'BUILD-VERSION'
    elif is_project_issue(token):
        return 'PROJECT-ISSUE'
    elif is_sha(token):
        return 'GIT-SHA'
    elif is_bracketed_email(token):
        return 'EMAIL'
    elif is_release_identifier(token):
        return 'RELEASE-IDENTIFIER'
    elif is_version_number(token):
        return 'VERSION-NUMBER'
    elif is_url(token):
        return 'URL'
    # Do this one last...
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


def clean_front(text):
    """
    Removes various method prefixes.

    >>> clean_front(' - herp')
    'herp'
    >>> clean_front('#34')
    '#34'
    >>> clean_front('* Makefile comment')
    'Makefile comment'
    >>> clean_front('*)use libcurl to handle fetion request')
    'use libcurl to handle fetion request'
    >>> clean_front('** added branch whitelist for travis')
    'added branch whitelist for travis'
    >>> clean_front('+ config changes')
    'config changes'
    >>> clean_front('+)add action type all')
    'add action type all'
    """

    return re.sub(r'''
        ^\s*
            (?: [#](?!\d)
              | [*+\-]+[)]?)
        \s*
    ''', '', text, flags=re.VERBOSE)


def tokenize(string):
    """
    Tokenizes strings.

    It normalizes:
    >>> tokenize('Nai\u0308ve')
    ['na\u00efve']

    It can segment English text:
    >>> tokenize("I ain't havin' it, ya hear?")
    ['i', "ain't", 'havin', 'it', 'ya', 'hear']

    It can replace issue numbers and filenames:
    >>> tokenize("Fixed #22 in filename.py ")
    ['fixed', 'ISSUE-NUMBER', 'in', 'FILE-PATTERN']

    It tokenizes simple function names:
    >>> tokenize("Implement foobar()")
    ['implement', 'METHOD-NAME']

    It understands C++/Ruby namespaces:
    >>> tokenize("Fixed #31 in std::whoopsie_handler() ")
    ['fixed', 'ISSUE-NUMBER', 'in', 'METHOD-NAME']

    It understands Ruby method notation:
    >>> tokenize("Fixed #31 in Herp#derp")
    ['fixed', 'ISSUE-NUMBER', 'in', 'METHOD-NAME']

    It understands globs:
    >>> tokenize("ignore *.aux")
    ['ignore', 'FILE-PATTERN']
    >>> tokenize("ignore paper.*")
    ['ignore', 'FILE-PATTERN']
    >>> tokenize("ignore **/*.png")
    ['ignore', 'FILE-PATTERN']

    It understands semantic versions:
    >>> tokenize("Release 2.1.0-rc.1")
    ['release', 'VERSION-NUMBER']

    It understands Jira project issues:
    >>> tokenize('THRIFT-2183 gem install fails on zsh')
    ['PROJECT-ISSUE', 'gem', 'install', 'fails', 'on', 'zsh']

    It can separate on semi-colons:
    >>> tokenize('#345;fixed critical bug')
    ['ISSUE-NUMBER', 'fixed', 'critical', 'bug']

    It understands surrounding backticks:
    >>> tokenize('Create `.rubocop.yml`')
    ['create', 'FILE-PATTERN']

    It can handle a bracketed initial token:
    >>> tokenize('[#41229165] Improve login box layout')
    ['ISSUE-NUMBER', 'improve', 'login', 'box', 'layout']

    It can parse git SHAs:
    >>> tokenize('Squashed commit 95c3adb49ea2a9831dbbe85d33a2b13c6781e860')
    ['squashed', 'commit', 'GIT-SHA']

    It understands email notation:
    >>> tokenize('Bump version 3.2.0 signed off by <foo@example.org>')
    ['bump', 'version', 'VERSION-NUMBER', 'signed', 'off', 'by', 'EMAIL']

    It understands release identifiers:
    >>> tokenize('[maven-release-plugin] prepare release killbill-0.1.66')
    ['maven-release-plugin', 'prepare', 'release', 'RELEASE-IDENTIFIER']

    It understands URLs:
    >>> tokenize('GS-803 git-svn-id: svn://pc-lab14/SVN/xap/trunk/openspaces@160822')
    ['PROJECT-ISSUE', 'git-svn-id', 'URL']

    It understand numbers:
    >>> tokenize('GS-803 Build version advanced to 10491-7')
    ['PROJECT-ISSUE', 'build', 'version', 'advanced', 'to', 'BUILD-VERSION']
    """

    # Step 1: Normalize into NFC
    # Step 2: Lowercase
    ustring = unicodedata.normalize('NFC', string).lower()

    # Remove leading '-', '*', '#'
    cleaned = clean_front(ustring)

    # Break on whitespace and semi-colons.
    segments = re.split(r'[\s;]+', cleaned, flags=re.UNICODE)

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
