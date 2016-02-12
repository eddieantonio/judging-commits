#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

# I could have used nltk.model.ngrams, but it only works in Python 2 :C

import os
import pickle
import subprocess
import tempfile

from math import exp

from commit import Commit


class MITLanguageModel(object):
    def __init__(self, utterences, order=3):
        self.name = None
        self.order = order
        self.train(utterences)

    def train(self, utterences):
        assert self.name is None

        self.name = tempfile.mktemp()
        with tempfile.NamedTemporaryFile('wb') as text_file:
            print_commits(utterences, text_file)
            train_model(text_file.name, self.name,
                        order=self.order)

    def evaluate_perlexity(self, commit, order=None):
        if order is None:
            order = self.order

        with tempfile.NamedTemporaryFile('wb') as text_file:
            print_commit(commit, text_file)
            return evaluate_ngram(self.name, text_file.name, order=order)

    def __enter__(self):
        return self

    def __exit__(self, cls, exception, traceback):
        if self.name:
            os.unlink(self.name)
            self.name = None


def load_commits_by_repo():
    with open('./commits.pickle', 'rb') as fp:
        return pickle.load(fp)


def perplexity_of_each(commits):
    write_repositories(repositories)
    train_model('train.txt', 'train.lm', order=3)

    for commit in commits:
        with open('test.txt', 'w', encoding='UTF-8') as test_file:
            print_commit(commit, test_file)
        perp = evaluate_ngram('train.lm', 'test.txt', order=3)
        print("{:g}: ``{:s}''".format(log2(perp), commit.message_as_ngrams))


def evaluate_ngram(model, test, order=3):
    args = ['evaluate-ngram',
            '-lm', model,
            '-order', str(order),
            '-eval-perp', test]
    output = subprocess.check_output(args)
    last_line = output.decode('UTF-8').splitlines()[-1]
    _, _, perp = last_line.split()
    return float(perp)


def train_model(corpus, output_name, order=3):
    args = ['estimate-ngram',
            '-text', corpus,
            '-order', str(order),
            '-write-lm', output_name]
    subprocess.check_call(args)


def print_commit(commit, file_obj):
    line = commit.message_as_ngrams
    assert '\n' not in line
    file_obj.write(line.encode('UTF-8'))
    file_obj.flush()


def print_commits(commits, file_obj):
    for commit in commits:
        print_commit(commit, file_obj)


def main():
    repositories = load_commits_by_repo()
    project, commits = repositories.popitem()
    other_commits = (c for c in commits for commits in repositories.values())
    with MITLanguageModel(other_commits) as model:
        for commit in commits:
            perp = model.evaluate_perlexity(commit)
            print("{:g}: ``{:s}''".format(perp,
                                          commit.message_as_ngrams))

if __name__ == '__main__':
    main()
