#!/usr/bin/env python3
# -*- encoding: UTF-8 -*-

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

import csv
import pickle
from collections import namedtuple, Counter

import persist


class Bin(object):
    __slots__ = ('_lower', '_upper', '_commits')

    def __init__(self, lower, upper):
        assert lower < upper
        self._lower = lower
        self._upper = upper
        self._commits = []

    @property
    def range(self):
        return (self.lower, self.upper)

    @property
    def lower(self):
        return self._lower

    @property
    def upper(self):
        return self._upper

    @property
    def commits(self):
        return list(self._commits)

    @property
    def size(self):
        return len(self._commits)

    @property
    def proportion_failed(self):
        failed = sum(1 for c in self
                     if c.status == 'failed')
        return failed / self.size

    @property
    def midpoint(self):
        lower, upper = self.range
        return lower + (upper - lower) / 2

    @property
    def proportion_errored(self):
        errored = sum(1 for c in self
                      if c.status == 'errored')
        return errored / self.size

    @property
    def proportion_broken(self):
        broken = sum(1 for c in self
                     if c.status in ('failed', 'errored'))
        return broken / self.size

    @property
    def proportion_passed(self):
        passed = sum(1 for c in self
                     if c.status == 'passed')
        return passed / self.size

    def append(self, commit):
        lower, upper = self.range
        assert lower <= commit.cross_entropy < upper,\
            "{} not in [{}, {})".format(commit.cross_entropy, lower, upper)

        self._commits.append(commit)

    def count_commits(self):
        return Counter(c.tokens_as_string for c in self)

    def __getitem__(self, index):
        '''
        Use a bin like a list of commits.
        '''
        return self._commits[index]

    def __iter__(self):
        return iter(self._commits)

    def __repr__(self):
        return '''
            <{clsname!s} range={self.range!r}, size={self.size!r}>
        '''.format(self=self, clsname=self.__class__.__name__).strip()

    @classmethod
    def create(cls, start, width):
        assert start > 0
        assert width > 0
        return cls(start, start + width)


def load_bins():
    filename = 'bins.pickle'
    try:
        with open(filename, 'rb') as bin_file:
            return pickle.load(bin_file)
    except IOError:
        bins = create_bins()
        with open(filename, 'wb') as bin_file:
            pickle.dump(bins, bin_file)
        return bins


def next_smallest_bounds(starting, width, to_fit):
    assert width > 0
    assert to_fit >= starting
    lower = starting
    upper = lower + width
    while to_fit > upper:
        lower = upper
        upper += width

    return lower, upper


def identity(x):
    return x


def iqr(seq, key=identity):
    n = len(seq)

    lower = seq[n // 4]
    upper = seq[3 * n // 4]

    lower_val = key(lower)
    upper_val = key(upper)

    if not (lower_val <= upper_val):
        raise ValueError('Must be sorted range')

    return upper_val - lower_val


def freedman_diaconis_rule(seq, key=identity):
    return 2 * iqr(seq, key=key) * len(seq) ** (-1.0 / 3.0)


def create_bins(autogen=False):

    commits = list(persist.fetch_commits(autogen))
    assert len(commits) >= 2

    def by_xentropy(commit):
        return commit.cross_entropy

    commits.sort(key=by_xentropy)

    bin_width = freedman_diaconis_rule(commits, key=by_xentropy)
    assert bin_width > 0.0
    min_value = commits[0].cross_entropy

    bins = []
    next_cuttoff = min_value
    for commit in commits:
        if commit.cross_entropy >= next_cuttoff:
            lower, upper = next_smallest_bounds(next_cuttoff, bin_width,
                                                commit.cross_entropy)
            bins.append(Bin.create(lower, bin_width))
            current_bin = bins[-1]
            next_cuttoff = upper

        current_bin.append(commit)

    return bins


def export_csv(filename, values):
    with open(filename, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(('mid.xentropy', 'proportion'))
        for row in values:
            writer.writerow(row)


if __name__ in ('__main__', '__console__'):
    bins = load_bins()

    # Sort bins by size.
    by_size = sorted(bins, key=lambda b: b.size, reverse=True)
    # Get the obvious outlier bins
    outliers = [bin for bin in by_size if bin.midpoint < 2]

    failed = ((b.midpoint, b.proportion_failed) for b in bins)
    export_csv('failed.csv', failed)
