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


# I could have used nltk.model.ngrams, but it only works in Python 2 :C

import pickle

from tqdm import tqdm

from commit import Commit
from mit_language_model import MITLanguageModel, ModelError


def load_commits_by_repo():
    with open('./commits.pickle', 'rb') as fp:
        return pickle.load(fp)


def evaluate_repo(name, repositories):
    # Get all commits NOT from this repository
    other_commits = (c for repo_name, commits in repositories.items()
                     for c in commits
                     if repo_name != name)
    model = None

    def perplexities():
        assert model is not None
        for commit in repositories[name]:
            perplexity = model.evaluate_perlexity(commit)
            yield commit.repo, commit.sha, perplexity

    with MITLanguageModel(other_commits) as model:
        return tuple(perplexities())


def main():
    repositories = load_commits_by_repo()
    repo_names = tuple(repositories.keys())

    with open('errors.csv', 'w') as errors, open('perps-leave1.csv', 'w') as perps:
        for name in tqdm(repo_names, desc="Repositories"):
            try:
                lines = evaluate_repo(name, repositories)
                for repo, sha, line in tqdm(lines, desc="Commits"):
                    print(repo, sha, line, sep=',', file=perps)
                perps.flush()
            except ModelError:
                print(name, file=errors)
                errors.flush()

if __name__ == '__main__':
    main()
