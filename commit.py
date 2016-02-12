#!/usr/bin/env python

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

from __future__ import division

import regex
from collections import namedtuple

class Commit(namedtuple(..., 'repo sha time message tokens status')):
    """
    All of the relevant state of a particular commit.
    """
    __slots__ = ()

    @property
    def is_merge(self):
        return (self.message.startswith('Merge branch') or
                self.message.startswith('Merge pull request') or
                self.message.startswith('Merge remote-tracking'))

    @property
    def build_was_cancelled(self):
        return self.status == 'canceled'

    @property
    def is_valid(self):
        return (not self.build_was_cancelled and
                not self.is_merge and
                not self.is_empty and
                self.is_plausibly_english)

    @property
    def message_as_ngrams(self):
        return ' '.join(self.tokens)

    @property
    def is_empty(self):
        return len(self.message_as_ngrams.strip()) == 0

    @property
    def is_plausibly_english(self):
        if len(self.message) == 0:
            return False

        pattern = r'[\p{Script=Common}\p{Script=Latin}]+'
        # langdetect performs very poorly, so a hand made heurisitic follows:
        latin_or_common_chars = sum(len(match) for match in
                                    regex.findall(pattern, self.message))
        return (latin_or_common_chars / len(self.message)) > 0.5
