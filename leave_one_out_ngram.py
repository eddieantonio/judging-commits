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

from commit import Commit
from mit_language_model import MITLanguageModel


def load_commits_by_repo():
    with open('./commits.pickle', 'rb') as fp:
        return pickle.load(fp)


def main():
    repositories = load_commits_by_repo()
    project, commits = repositories.popitem()
    other_commits = (c for commits in repositories.values()
                    for c in commits)
    with MITLanguageModel(other_commits) as model:
        for commit in commits:
            perp = model.evaluate_perlexity(commit)
            print("{:g}: ``{:s}''".format(perp,
                                          commit.message_as_ngrams))

if __name__ == '__main__':
    main()
