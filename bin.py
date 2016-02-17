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

import pickle
from collections import namedtuple


class Bin(namedtuple('Bin', 'range commits')):
    __slots__ = ()
    @property
    def size(self):
        return len(self.commits)

    @property
    def proportion_failed(self):
        failed = sum(1 for c in self.commits
                     if c.status == 'failed')
        return failed / self.size

    @property
    def midpoint(self):
        lower, upper = self.range
        return lower + (upper - lower) / 2

    @property
    def proportion_errored(self):
        errored = sum(1 for c in self.commits
                      if c.status == 'errored')
        return errored / self.size

    @property
    def proportion_broken(self):
        broken = sum(1 for c in self.commits
                     if c.status in ('failed', 'errored'))
        return broken / self.size

    @property
    def proportion_passed(self):
        passed = sum(1 for c in self.commits
                     if c.status == 'passed')
        return passed / self.size

    # TODO: Failure rate
    # TODO: Fail'd rate
    # TODO: Error'd rate

    # https://docs.travis-ci.com/user/customizing-the-build#Breaking-the-Build

    def append(self, commit):
        lower, upper = self.range
        assert lower <= commit.cross_entropy < upper,\
            "{} not in [{}, {})".format(commit.cross_entropy, lower, upper)

        self.commits.append(commit)

    @classmethod
    def create(cls, start, width):
        assert start > 0
        assert width > 0
        return cls((start, start + width), [])


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

def create_bins():
    import persist
    commits = list(persist.fetch_commits())
    commits.sort(key=lambda commit: commit.cross_entropy)

    # Calculated in R:
    # 2 * IQR(cross_entropy) * len(commits) ** (-1.0/3.0)
    bin_width = 0.146244666423261

    assert len(commits) >= 2
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
    import csv
    with open(filename, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(('est.xentropy', 'proportion'))
        for row in values:
            writer.writerow(row)

if __name__ in ('__main__', '__console__'):
    bins = load_bins()
    from collections import Counter

    # Sort commits by size.
    suitable_bins = (b for b in bins if b.range[0] < 5.5)
    by_size = sorted(suitable_bins, key=lambda b: b.size, reverse=True)
    counts = [Counter(c.tokens_as_string for c in bin.commits)
              for bin in by_size]

    # Figure out the most common commits.
    #commit_counter = Counter(c.tokens_as_string for c in persist.fetch_commits())

    #passed = [(b.midpoint, b.proportion_passed) for b in bins]
    #failed = [(b.midpoint, b.proportion_failed) for b in bins]
    #errored = [(b.midpoint, b.proportion_errored) for b in bins]
    #broken = [(b.midpoint, b.proportion_broken) for b in bins]
    #export_csv('passed.csv', passed)
    #export_csv('failed.csv', failed)
    #export_csv('errored.csv', errored)
