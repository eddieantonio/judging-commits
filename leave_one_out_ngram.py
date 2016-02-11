#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

# I could have used nltk.model.ngrams, but it only works in Python 2 :C

import subprocess
import pickle

from commit import Commit


def load_commits_by_repo():
    with open('./commits.pickle', 'rb') as fp:
        return pickle.load(fp)

repositories = load_commits_by_repo()
_, commits = repositories.popitem()


def print_commit(commit, file_obj):
    line = commit.message_as_ngrams
    assert '\n' not in line
    print(line, file=file_obj)


def evaluate_ngram(model, test, order=3):
    args = ['evaluate-ngram',
            '-lm', model,
            '-order', str(order),
            '-eval-perp', test]
    output = subprocess.check_output(' '.join(args), shell=True)
    last_line = output.decode('UTF-8').splitlines()[-1]
    _, _, perp = last_line.split()
    return float(perp)


def print_commits(repos, file_obj):
    for commits in repos.values():
        for commit in commits:
            print_commit(commit, file_obj)


def write_repositories(repos):
    with open('train.txt', 'w', encoding='UTF-8') as train_file:
        print_commits(repos, train_file)


def train_model(corpus, output_name, order=3):
    args = ['estimate-ngram',
            '-text', corpus,
            '-order', str(order),
            '-write-lm', output_name]
    subprocess.run(' '.join(args), shell=True, check=True)


def perplexity_of_each(commits):
    write_repositories(repositories)
    train_model('train.txt', 'train.lm')

    for commit in commits:
        with open('test.txt', 'w', encoding='UTF-8') as test_file:
            print_commit(commit, test_file)
            perp = evaluate_ngram('train.lm', 'test.txt')
            print(perp, commit.message_as_ngrams)


perplexity_of_each(commits)
