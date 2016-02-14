#!/usr/bin/env python
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


import pickle
from random import shuffle

from tqdm import trange

from commit import Commit
from mit_language_model import MITLanguageModel, ModelError


def load_commits_by_repo():
    with open('./commits.pickle', 'rb') as fp:
        return pickle.load(fp)


def create_folds(repositories, k=10):
    repos_by_size = sorted(repositories.keys(),
                           key=lambda repo: len(repositories[repo]),
                           reverse=True)
    total_repos = len(repos_by_size)
    size_of_each = total_repos // 10

    # Create the bins and shuffle them
    bins = []
    for num, start in enumerate(range(0, total_repos, size_of_each)):
        bins.append(list(repos_by_size[start:size_of_each]))
        shuffle(bins[num])

    # Initialize the folds.
    folds = [[] for _ in range(k)]

    # Fill the folds
    for i in range(len(bins)):
        bin = bins[i]
        for j in range(len(bin)):
            fold = folds[j % len(folds)]
            repo = bin.pop()
            fold.extend(commit for commit in repositories[repo])

    return folds


def evaluate_fold(i, folds):
    # Get all commits NOT from this repository
    model = None

    other_commits = (commit
                     for j in range(len(folds))
                     for commit in folds[j]
                     if j != i)

    with MITLanguageModel(other_commits) as model:
        for commit in folds[i]:
            perplexity = model.evaluate_perlexity(commit)
            yield commit.repo, commit.sha, perplexity


def main():
    repositories = load_commits_by_repo()
    folds = create_folds(repositories, k=10)

    with open('errors.csv', 'w') as errors, open('perps.csv', 'w') as perps:
        for i in trange(len(folds)):
            try:
                lines = evaluate_fold(i, folds)
                for repo, sha, line in lines:
                    print(repo, sha, line, sep=',', file=perps)
            except ModelError:
                print(name, file=errors)


if __name__ == '__main__':
    main()
