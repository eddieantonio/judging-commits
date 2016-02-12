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
            for commit in commits:
                print_commit(commit, text_file)
            input(text_file.name)
            train_model(text_file.name, self.name,
                        order=self.order)
        return self

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
            os.remove(self.name)
            self.name = None


def print_commit(commit, file_obj):
    line = commit.message_as_ngrams
    assert '\n' not in line
    file_obj.write(line.encode('UTF-8'))
    file_obj.write('\n'.encode('UTF-8'))
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
    subprocess.check_call(args)
