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

import os
import subprocess
import tempfile


class ModelError(Exception):
    pass


class ModelTrainingError(ModelError):
    pass


class ModelEvaluationError(ModelError):
    pass


class MITLanguageModel(object):
    def __init__(self, commits=None, order=3):
        self.name = None
        self.order = order
        if commits is not None:
            self.train(commits)

    def train(self, commits):
        assert self.name is None

        self.name = tempfile.mktemp()
        with tempfile.NamedTemporaryFile('wb') as text_file:
            print_commits(commits, text_file)
            try:
                train_model(text_file.name, self.name,
                            order=self.order)
            except subprocess.CalledProcessError:
                raise ModelTrainingError()

        return self

    def evaluate_perlexity(self, commits, order=None):
        if order is None:
            order = self.order

        with tempfile.NamedTemporaryFile('wb') as text_file:
            print_commits(commits, text_file)
            try:
                return evaluate_ngram(self.name, text_file.name, order=order)
            except subprocess.CalledProcessError:
                raise ModelEvaluationError()

    def __enter__(self):
        return self

    def __exit__(self, cls, exception, traceback):
        if self.name:
            os.remove(self.name)
            self.name = None


def print_commits(maybe_commits, file_obj):
    try:
        tokens = maybe_commits.tokens_as_string
    except AttributeError:
        for commit in maybe_commits:
            tokens = commit.tokens_as_string
            print_tokens(tokens, file_obj, flush=False)
        file_obj.flush()
    else:
        print_tokens(tokens, text_file)


def print_tokens(line, file_obj, flush=True):
    assert '\n' not in line
    file_obj.write(line.encode('UTF-8'))
    file_obj.write('\n'.encode('UTF-8'))
    if flush:
        file_obj.flush()


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
    subprocess.check_call(args,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
